import json
import os
from typing import Dict, Any


def read_json(path: str) -> Dict[str, Any]:
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def risk_level(score: int) -> str:
    if score >= 70:
        return "HIGH"
    if score >= 40:
        return "MEDIUM"
    return "LOW"


def calculate_final_risk(workflow_report: Dict[str, Any],
                         gitleaks_report: Dict[str, Any],
                         pipaudit_report: Dict[str, Any]) -> Dict[str, Any]:
    """
    Combines multiple security scan outputs into a single risk score.
    This is Day-4 'AI-like' scoring (heuristic model).
    Later we can upgrade into ML model.
    """

    score = 0
    reasons = []

    # -----------------------------
    # 1) Workflow Analyzer Risk
    # -----------------------------
    workflow_files = workflow_report.get("files", [])
    workflow_total_findings = workflow_report.get("total_findings", 0)

    if workflow_total_findings > 0:
        # Add base score
        score += min(50, workflow_total_findings * 15)
        reasons.append(f"Workflow risk findings: {workflow_total_findings}")

    # -----------------------------
    # 2) Gitleaks Risk (Secrets leak)
    # -----------------------------
    # gitleaks json format may vary. We'll handle common patterns.
    secrets_found = 0
    if isinstance(gitleaks_report, list):
        secrets_found = len(gitleaks_report)
    elif isinstance(gitleaks_report, dict):
        # Sometimes "leaks" field exists
        leaks = gitleaks_report.get("leaks", [])
        if isinstance(leaks, list):
            secrets_found = len(leaks)

    if secrets_found > 0:
        score += min(60, secrets_found * 30)
        reasons.append(f"Secrets found by gitleaks: {secrets_found}")

    # -----------------------------
    # 3) pip-audit Risk (Dependencies)
    # -----------------------------
    vuln_count = 0
    if isinstance(pipaudit_report, dict):
        deps = pipaudit_report.get("dependencies", [])
        for d in deps:
            vulns = d.get("vulns", [])
            vuln_count += len(vulns)

    if vuln_count > 0:
        score += min(40, vuln_count * 10)
        reasons.append(f"Dependency vulnerabilities found: {vuln_count}")

    # clamp score
    score = max(0, min(100, score))
    level = risk_level(score)

    recommended_action = "ALLOW"
    if level == "MEDIUM":
        recommended_action = "REVIEW"
    elif level == "HIGH":
        recommended_action = "BLOCK"

    return {
        "final_risk_score": score,
        "severity": level,
        "recommended_action": recommended_action,
        "details": {
            "workflow_findings": workflow_total_findings,
            "workflow_files": workflow_files,
            "secrets_found": secrets_found,
            "dependency_vulns": vuln_count
        },
        "reasons": reasons
    }


def save_report(report: Dict[str, Any], output_path: str) -> None:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)


if __name__ == "__main__":
    workflow = read_json("reports/workflow-risk-report.json")
    gitleaks = read_json("reports/gitleaks-report.json")
    pipaudit = read_json("reports/pip-audit-report.json")

    final = calculate_final_risk(workflow, gitleaks, pipaudit)
    save_report(final, "reports/final-risk-report.json")

    print("✅ Final Risk Report Generated")
    print(json.dumps(final, indent=2))
