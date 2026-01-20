import json
import os
import sys
import subprocess
from typing import Dict, Any


FINAL_REPORT_PATH = "reports/final-risk-report.json"


def load_final_report() -> Dict[str, Any]:
    if not os.path.exists(FINAL_REPORT_PATH):
        print("❌ Final risk report not found. Run risk_engine.py first.")
        return {}
    with open(FINAL_REPORT_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def create_github_issue(title: str, body: str) -> None:
    """
    Uses GitHub CLI (gh) to create an issue.
    Requires GH_TOKEN in Actions.
    """
    try:
        subprocess.run(
            ["gh", "issue", "create", "--title", title, "--body", body],
            check=True
        )
        print("✅ GitHub issue created.")
    except Exception as e:
        print(f"⚠️ Failed to create issue: {e}")


def comment_on_pr(pr_number: str, comment: str) -> None:
    """
    Comment on PR using GitHub CLI.
    """
    try:
        subprocess.run(
            ["gh", "pr", "comment", pr_number, "--body", comment],
            check=True
        )
        print("✅ Comment added to PR.")
    except Exception as e:
        print(f"⚠️ Failed to comment on PR: {e}")


def main():
    report = load_final_report()
    if not report:
        sys.exit(0)

    score = report.get("final_risk_score", 0)
    severity = report.get("severity", "LOW")
    action = report.get("recommended_action", "ALLOW")
    reasons = report.get("reasons", [])
    details = report.get("details", {})

    print("✅ Response Engine Running...")
    print(f"Final Score: {score} | Severity: {severity} | Action: {action}")

    # Environment details (GitHub Actions)
    event_name = os.getenv("GITHUB_EVENT_NAME", "")
    repo = os.getenv("GITHUB_REPOSITORY", "")
    run_id = os.getenv("GITHUB_RUN_ID", "")
    pr_number = os.getenv("PR_NUMBER", "")

    # Build incident text
    issue_title = f"🚨 AutoSec Incident: {severity} risk detected (score={score})"
    issue_body = f"""
## AutoSec CI/CD Guardian Incident Report

**Repository:** {repo}  
**Run ID:** {run_id}  
**Severity:** {severity}  
**Final Score:** {score}  
**Recommended Action:** {action}  

### Reasons
{chr(10).join(['- ' + r for r in reasons])}

### Details
- Workflow findings: {details.get('workflow_findings', 0)}
- Secrets found: {details.get('secrets_found', 0)}
- Dependency vulns: {details.get('dependency_vulns', 0)}

✅ Report file: `{FINAL_REPORT_PATH}`
"""

    pr_comment = f"""
🚨 **AutoSec CI/CD Guardian Alert**

**Final Risk Score:** `{score}`  
**Severity:** `{severity}`  
**Recommended Action:** `{action}`  

### Reasons:
{chr(10).join(['- ' + r for r in reasons])}

Please review the security reports in CI artifacts.
"""

    # MEDIUM/HIGH -> create issue
    if severity in ["MEDIUM", "HIGH"]:
        create_github_issue(issue_title, issue_body)

    # If PR, comment on PR
    if event_name == "pull_request" and pr_number:
        comment_on_pr(pr_number, pr_comment)

    # HIGH -> block pipeline
    if severity == "HIGH":
        print("❌ HIGH risk detected -> failing pipeline (blocking merge).")
        sys.exit(1)

    print("✅ Pipeline allowed (no block).")
    sys.exit(0)


if __name__ == "__main__":
    main()
