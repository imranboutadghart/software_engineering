import os
from git import Repo
from collections import defaultdict
import logging

class GitAnalysisService:
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.valid = False
        try:
            # Check if it is a valid git repo
            if os.path.isdir(os.path.join(repo_path, '.git')):
                self.repo = Repo(repo_path)
                self.valid = True
        except Exception as e:
            logging.error(f"Failed to initialize Git repo at {repo_path}: {e}")

    def get_churn_metrics(self, limit: int = 100):
        churn_counts = defaultdict(int)
        if not self.valid:
            print(f"Warning: {self.repo_path} is not a valid git repo.")
            return churn_counts
        
        # Keywords that suggest a bug fix
        fix_keywords = ['fix', 'bug', 'issue', 'resolve', 'patch', 'hotfix']
        
        try:
            commits = list(self.repo.iter_commits('HEAD', max_count=limit))
            for commit in commits:
                msg = commit.message.lower()
                if any(kw in msg for kw in fix_keywords):
                    # This is a fix commit, count the files changed
                    for file_path in commit.stats.files:
                        # Normalize path separators
                        norm_path = file_path.replace('/', os.sep)
                        churn_counts[norm_path] += 1
        except Exception as e:
            logging.error(f"Error analyzing git history: {e}")
            
        return churn_counts
