# Bug Predictor

## Mini-Project: Bug Prediction Tool

**Objective**: Automatically predict at-risk files in a software project.

### Features
- **Git History Analysis**: Identifies files frequently involved in bug fixes.
- **Complexity Analysis**: Calculates Cyclomatic Complexity using Radon.
- **Risk Scoring**: Combines history and complexity to generate a risk score.
- **Dashboard**: Web interface to view analysis results.

### Technologies
- Python 3.x
- FastAPI
- GitPython
- Radon
- HTML/TailwindCSS

### Setup
1. `pip install -r requirements.txt`
2. `uvicorn app.main:app --reload`
3. Open `http://localhost:8000`
