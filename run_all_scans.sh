#!/usr/bin/env bash
set -e

echo "======================================="
echo " AutoSec CI/CD Guardian - Full Scan Run "
echo "======================================="

# 1) Ensure reports folder exists
mkdir -p reports

echo ""
echo "[1/5] Workflow Risk Analyzer..."
python src/workflow_analyzer.py

echo ""
echo "[2/5] Dependency Vulnerability Scan (pip-audit)..."
python -m pip install -r requirements.txt >/dev/null
pip-audit -r requirements.txt -f json -o reports/pip-audit-report.json || true

echo ""
echo "[3/5] Secret Scan (gitleaks)..."

# If gitleaks not installed, install it (windows-friendly)
if ! command -v gitleaks >/dev/null 2>&1; then
  echo "Gitleaks not found. Installing..."
  curl -sSL https://github.com/gitleaks/gitleaks/releases/latest/download/gitleaks_windows_x64.zip -o gitleaks.zip
  unzip -o gitleaks.zip -d gitleaks-bin
  mv gitleaks-bin/gitleaks.exe ./gitleaks.exe
  rm -rf gitleaks-bin gitleaks.zip
fi

# Run gitleaks scan
./gitleaks.exe detect --source . --report-format json --report-path reports/gitleaks-report.json || true

echo ""
echo "[4/5] Final Risk Engine..."
python src/risk_engine.py

echo ""
echo "[5/5] Done ✅ Reports generated in /reports"
echo " - reports/workflow-risk-report.json"
echo " - reports/pip-audit-report.json"
echo " - reports/gitleaks-report.json"
echo " - reports/final-risk-report.json"
