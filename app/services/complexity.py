import radon.complexity as radon_cc
import logging
import os

class ComplexityService:
    @staticmethod
    def get_complexity(file_path: str) -> float:
        if not os.path.exists(file_path):
            return 0.0
            
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                code = f.read()
            
            # Radon only works on Python files effectively for CC
            if not file_path.endswith('.py'):
                return 0.0

            blocks = radon_cc.cc_visit(code)
            if not blocks:
                return 0.0
            
            # Return Total Complexity of the file
            total_cc = sum(block.complexity for block in blocks)
            return float(total_cc)
        except Exception as e:
            # Only log valid errors, ignore syntax errors in non-python files if they somehow get here
            # logging.error(f"Error calculating complexity for {file_path}: {e}")
            return 0.0
