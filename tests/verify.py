import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.git_analysis import GitAnalysisService
from app.services.complexity import ComplexityService
from app.services.risk import RiskScorer

def verify():
    print("Starting verification...")
    
    # Use current directory
    target_path = os.path.abspath(os.getcwd())
    print(f"Analyzing: {target_path}")

    # 1. Test Git Service
    try:
        git_service = GitAnalysisService(target_path)
        if git_service.valid:
            print("Git Repo detected.")
            churn = git_service.get_churn_metrics(limit=10)
            print(f"Churn metrics obtained: {len(churn)} files found in last 10 commits.")
        else:
            print("Git Repo NOT detected (Expected if this is a fresh folder without commits).")
    except Exception as e:
        print(f"Git Service Failed: {e}")

    # 2. Test Complexity Service
    # Let's test on app/main.py
    test_file = os.path.join(target_path, 'app', 'main.py')
    if os.path.exists(test_file):
        cc = ComplexityService.get_complexity(test_file)
        print(f"Complexity of main.py: {cc}")
        if cc > 0:
            print("Complexity Service verified.")
        else:
            print("Complexity Service returned 0 (Check if radon works).")
    else:
        print(f"Test file not found: {test_file}")

    # 3. Test Risk Scorer
    risk = RiskScorer.calculate_risk(5, 10.0)
    print(f"Risk Score (5 churn, 10 cc): {risk}")
    assert risk == 55.0, "Risk calculation mismatch"
    print("Risk Scorer verified.")
    
    print("Verification complete.")

if __name__ == "__main__":
    verify()
