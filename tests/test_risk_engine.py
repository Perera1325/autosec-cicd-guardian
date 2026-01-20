from src.risk_engine import calculate_final_risk

def test_risk_engine_output():
    workflow_report = {"total_findings": 2, "files": []}
    gitleaks_report = []
    pipaudit_report = {"dependencies": []}

    result = calculate_final_risk(workflow_report, gitleaks_report, pipaudit_report)

    assert "final_risk_score" in result
    assert "severity" in result
    assert 0 <= result["final_risk_score"] <= 100
