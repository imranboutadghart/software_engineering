# Test Plan: Bug Predictor

## 1. Introduction
This document outlines the testing strategy for the Bug Predictor mini-project.

## 2. Scope
- **Unit Testing**: Services (Git, Complexity, Risk).
- **Integration Testing**: API Endpoints.
- **System Testing**: End-to-end flow via Dashboard.

## 3. Test Cases

### 3.1 Unit Tests
| ID | Module | Test Case | Expected Result |
|----|--------|-----------|-----------------|
| UT-01 | GitService | Analyze a known repo with fixes | Should return correct count of fix commits |
| UT-02 | Complexity | Analyze a simple python file | Should return correct CC score |
| UT-03 | RiskScorer | Score with high complexity/high churn | Should return high risk score |

### 3.2 System Tests
| ID | Scenario | Steps | Expected Result |
|----|----------|-------|-----------------|
| ST-01 | Analyze Self | Input current project path | Dashboard displays list of files |
| ST-02 | Navigation | Click on a file detail (if impl) | Show detailed metrics |
