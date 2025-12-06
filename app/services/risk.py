class RiskScorer:
    @staticmethod
    def calculate_risk(churn: int, complexity: float) -> float:
        # Heuristic Formula
        # Churn is highly indicative of instability.
        # Complexity makes it harder to fix properly.
        
        w_churn = 10.0     # Each recent bug fix adds 10 points
        w_complexity = 0.5 # A file with CC 20 adds 10 points
        
        return (churn * w_churn) + (complexity * w_complexity)
