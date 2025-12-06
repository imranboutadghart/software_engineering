from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
import logging

from app.services.git_analysis import GitAnalysisService
from app.services.complexity import ComplexityService
from app.services.risk import RiskScorer
from app.models.analysis_model import FileAnalysis, ProjectAnalysis

app = FastAPI(title="Bug Predictor")

# Mount templates
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze", response_class=HTMLResponse)
async def analyze_project(request: Request, path: str = Form(...)):
    if not os.path.isdir(path):
        return templates.TemplateResponse("index.html", {
            "request": request, 
            "error": "Invalid directory path provided."
        })

    # 1. Get Churn Data
    git_service = GitAnalysisService(path)
    churn_data = git_service.get_churn_metrics()
    
    analyzed_files = []
    
    # 2. Walk directory
    for root, dirs, files in os.walk(path):
        # Exclude common ignore dirs
        dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'venv', 'node_modules', '.idea', '.vscode']]
        
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, path)
            
            # Normalize path for matching with git data (which uses / usually)
            # GitPython stats usually return paths relative to repo root
            # We need to handle path separators carefully
            
            # Simple normalization check
            # churn_data keys might be 'app/main.py'
            # rel_path might be 'app\main.py' on windows
            
            lookup_keys = [rel_path, rel_path.replace(os.sep, '/')]
            churn_count = 0
            for key in lookup_keys:
                if key in churn_data:
                    churn_count = churn_data[key]
                    break
            
            # Calculate Complexity
            complexity = ComplexityService.get_complexity(full_path)
            
            # Calculate Risk
            risk = RiskScorer.calculate_risk(churn_count, complexity)
            
            if risk > 0 or churn_count > 0 or complexity > 0:
                analyzed_files.append(FileAnalysis(
                    filename=rel_path,
                    churn_count=churn_count,
                    complexity_score=complexity,
                    risk_score=risk
                ))
    
    # Sort by risk descending
    analyzed_files.sort(key=lambda x: x.risk_score, reverse=True)
    
    proj_analysis = ProjectAnalysis(
        project_path=path,
        total_files=len(analyzed_files),
        files=analyzed_files
    )

    return templates.TemplateResponse("index.html", {
        "request": request,
        "analysis": proj_analysis,
        "path": path
    })
