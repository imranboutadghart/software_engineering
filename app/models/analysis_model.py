from pydantic import BaseModel
from typing import List, Optional

class FileAnalysis(BaseModel):
    filename: str
    churn_count: int = 0
    complexity_score: float = 0.0
    risk_score: float = 0.0
    details: Optional[str] = None

class ProjectAnalysis(BaseModel):
    project_path: str
    total_files: int
    files: List[FileAnalysis]
