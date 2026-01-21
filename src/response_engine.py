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
    Create issue only if a similar one is not already open (dedup).
    """
    try:
        # Check if similar issue already exists (open)
        result = subprocess.run(
            ["gh", "issue", "list", "--state", "open", "--search", title, "--json", "title"],
            capture_output=True,
            text=True,
            check=True
        )

        existing = json.loads(result.stdout)
        if existing and len(existing) > 0:
            print("✅ Similar incident already exists. Skipping duplicate issue.")
            return

        subprocess.run(
            ["gh", "issue", "create", "--title", title, "--body", body],
            check=True
        )
        print("✅ GitHub incident issue created.")

    except Exception as e:
        print(f"⚠️ Failed to create issue: {e}")
