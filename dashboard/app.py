from flask import Flask, render_template
import json
import os

app = Flask(__name__)

REPORTS = {
    "final": "reports/final-risk-report.json",
    "workflow": "reports/workflow-risk-report.json",
    "gitleaks": "reports/gitleaks-report.json",
    "pipaudit": "reports/pip-audit-report.json",
}


def load_json(path: str):
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


@app.route("/")
def index():
    final_report = load_json(REPORTS["final"])
    workflow_report = load_json(REPORTS["workflow"])
    gitleaks_report = load_json(REPORTS["gitleaks"])
    pipaudit_report = load_json(REPORTS["pipaudit"])

    # For gitleaks list style
    secrets_found = 0
    if isinstance(gitleaks_report, list):
        secrets_found = len(gitleaks_report)

    # For pip-audit
    vuln_count = 0
    if isinstance(pipaudit_report, dict):
        deps = pipaudit_report.get("dependencies", [])
        for d in deps:
            vuln_count += len(d.get("vulns", []))

    return render_template(
        "index.html",
        final=final_report,
        workflow=workflow_report,
        gitleaks=gitleaks_report,
        pipaudit=pipaudit_report,
        secrets_found=secrets_found,
        vuln_count=vuln_count
    )


if __name__ == "__main__":
    app.run(debug=True)
