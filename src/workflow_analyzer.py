import os
import re
import json
from typing import Dict, Any, List

WORKFLOW_DIR = ".github/workflows"


def scan_workflow_file(filepath: str) -> Dict[str, Any]:
    """
    Analyze a GitHub Actions workflow YAML file for risky patterns.
    Returns findings + risk score.
    """
    findings: List[Dict[str, str]] = []
    risk_score = 0

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1) Actions not pinned to commit SHA
    # Example risky: uses: actions/checkout@v4
    # Better: uses: actions/checkout@<40-char-sha>
    uses_lines = re.findall(r"uses:\s*([^\s]+)", content)
    for action in uses_lines:
        # Ignore local actions like: uses: ./.github/actions/something
        if action.startswith("./"):
            continue

        # If not pinned to SHA, add finding
        if not re.search(r"@[0-9a-fA-F]{40}$", action):
            findings.append({
                "type": "UNPINNED_ACTION",
                "severity": "MEDIUM",
                "message": f"Action not pinned to commit SHA: {action}"
            })
            risk_score += 15

    # 2) Dangerous global permissions
    if re.search(r"permissions:\s*write-all", content):
        findings.append({
            "type": "DANGEROUS_PERMISSIONS",
            "severity": "HIGH",
            "message": "Workflow uses permissions: write-all (too powerful)"
        })
        risk_score += 30

    # 3) pull_request_target trigger (common supply chain attack vector)
    if "pull_request_target" in content:
        findings.append({
            "type": "PULL_REQUEST_TARGET",
            "severity": "HIGH",
            "message": "Workflow triggered by pull_request_target (dangerous if misused)"
        })
        risk_score += 35

    # 4) curl|bash pattern (download and execute)
    if re.search(r"curl.+\|\s*bash", content) or re.search(r"wget.+\|\s*bash", content):
        findings.append({
            "type": "CURL_PIPE_BASH",
            "severity": "HIGH",
            "message": "Workflow contains curl|bash or wget|bash pattern (high risk)"
        })
        risk_score += 40

    # 5) persist-credentials true (token leakage risk)
    if re.search(r"persist-credentials:\s*true", content):
        findings.append({
            "type": "PERSIST_CREDENTIALS",
            "severity": "MEDIUM",
            "message": "checkout persist-credentials:true may increase token leakage risk"
        })
        risk_score += 15

    # Clamp score 0..100
    risk_score = max(0, min(100, risk_score))

    return {
        "workflow_file": filepath,
        "risk_score": risk_score,
        "findings": findings
    }


def scan_all_workflows() -> Dict[str, Any]:
    """
    Scan all workflows in .github/workflows and create summary report.
    """
    report: Dict[str, Any] = {
        "total_files_scanned": 0,
        "total_findings": 0,
        "files": []
    }

    if not os.path.exists(WORKFLOW_DIR):
        return report

    for filename in os.listdir(WORKFLOW_DIR):
        if filename.endswith(".yml") or filename.endswith(".yaml"):
            filepath = os.path.join(WORKFLOW_DIR, filename)
            file_report = scan_workflow_file(filepath)

            report["total_files_scanned"] += 1
            report["total_findings"] += len(file_report["findings"])
            report["files"].append(file_report)

    return report


def save_report(report: Dict[str, Any], output_path: str = "reports/workflow-risk-report.json") -> None:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)


if __name__ == "__main__":
    report_data = scan_all_workflows()
    save_report(report_data)

    print("Workflow risk analysis completed ✅")
    print(json.dumps(report_data, indent=2))
