![AutoSec CI](https://github.com/Perera1325/autosec-cicd-guardian/actions/workflows/ci.yml/badge.svg)
![Security Scan](https://img.shields.io/badge/DevSecOps-Automation-blue)
![SOAR](https://img.shields.io/badge/SOAR-Auto%20Response-red)
![Dashboard](https://img.shields.io/badge/SOC-Dashboard-purple)

# 🚨 AutoSec CI/CD Guardian — DevSecOps + SOAR Automation
A **production-ready DevSecOps automation system** that secures CI/CD pipelines against:
- **workflow supply chain risks**
- **secret leaks**
- **vulnerable dependencies**

It automatically calculates a **final risk score (0–100)**, triggers **SOAR response actions** (issue creation + PR comment + block pipeline), and provides a **SOC dashboard** for visibility.

> 🔥 Built as a hire-level project to demonstrate real-world CI/CD security, automation engineering, and SOC/SOAR concepts.

---

## 🌍 Real-World Problem
Modern organizations rely on CI/CD pipelines (GitHub Actions, Jenkins, GitLab CI).  
Attackers increasingly target CI pipelines using:

- Untrusted third-party GitHub Actions (supply-chain attacks)
- Excessive workflow permissions (`write-all`)
- Secrets exposure (`GITHUB_TOKEN`, API keys)
- Dependency vulnerabilities (CVE exploitation)
- Malicious script patterns (`curl | bash`)

Most of these attacks go undetected until damage happens.

✅ **AutoSec CI/CD Guardian solves this by continuously scanning pipelines and automatically responding like a SOC.**

---

## ✅ Key Features

### 🔎 Detection (Automated Security Scanning)
- **Gitleaks** secret scanning
- **pip-audit** dependency vulnerability scan
- **Workflow Risk Analyzer**
  - detects unpinned actions
  - detects dangerous permissions
  - detects supply-chain risky workflow triggers
  - detects unsafe patterns like `curl | bash`

### 🧠 Risk Intelligence
- Combines all scan results → generates:
  - **final risk score (0–100)**
  - severity: **LOW / MEDIUM / HIGH**
  - recommended action: **ALLOW / REVIEW / BLOCK**

### 🚨 SOAR Auto Response (Security Automation)
If risk is MEDIUM/HIGH:
- ✅ Auto creates GitHub **incident issue**
- ✅ (PR only) Auto comments with alert

If risk is HIGH:
- ❌ **Blocks pipeline** (fails build and prevents merge)

### 🛰 SOC Dashboard
- Risk ring with severity animations
- Findings summary & workflow findings table
- Expandable raw JSON reports as evidence

### 🐳 Production Ready
- Fully **Dockerized**
- Runs with **Gunicorn production server**
- Deployable on any cloud/server

---

## 🏗 Architecture

```text
┌───────────────────────────────┐
│       Developer Push / PR      │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│       GitHub Actions (CI)      │
│   Triggered on push / PR       │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────────────────────────┐
│                 Security Scanning                  │
│                                                   │
│  1) Secret Scan        → Gitleaks                  │
│  2) Dependency Scan    → pip-audit                 │
│  3) Workflow Risk Scan → workflow_analyzer.py      │
└───────────────┬───────────────────────────────────┘
                │
                ▼
┌───────────────────────────────────────────────────┐
│                 Final Risk Engine                  │
│        risk_engine.py (Score: 0–100)               │
│        Severity: LOW / MEDIUM / HIGH               │
│        Action: ALLOW / REVIEW / BLOCK              │
└───────────────┬───────────────────────────────────┘
                │
                ▼
┌───────────────────────────────────────────────────┐
│                SOAR Response Engine                │
│                  response_engine.py                │
│                                                   │
│  ✅ Create incident issue (GitHub Issue)           │
│  ✅ Comment on PR                                  │
│  ⛔ Block pipeline if HIGH risk                     │
└───────────────┬───────────────────────────────────┘
                │
                ▼
┌───────────────────────────────────────────────────┐
│                 SOC Dashboard (UI)                 │
│                Flask dashboard app                 │
│       Shows score + findings + raw JSON reports    │
└───────────────────────────────────────────────────┘





---

# 🔥 Demo Tour (Perfect for recruiters / GitHub users)

## ✅ Demo Tour in 3 Minutes

### 1) GitHub Actions Automation
Go to:
✅ **Actions tab**
- Every push/PR runs automatic scans:
  - gitleaks
  - pip-audit
  - workflow analyzer
  - risk engine
  - response engine

### 2) Download Evidence Reports
Open any workflow run → download artifacts:

✅ `security-reports.zip`

Contains:
- `workflow-risk-report.json`
- `pip-audit-report.json`
- `gitleaks-report.json`
- `final-risk-report.json`

### 3) SOAR Incident Automation
Go to:
✅ **Issues tab**
- You will see auto-generated incidents like:
  - `🚨 AutoSec Incident: HIGH risk detected`

### 4) SOC Dashboard Visualization
Run dashboard (local or Docker) to view:
- risk score
- severity
- findings table
- raw JSON evidence

---

## 🧨 Attack Simulation Demo (WOW moment)
You can simulate a CI/CD attack to prove AutoSec blocks unsafe workflows.

### ✅ Step 1: Create a demo branch
```bash
git checkout -b demo-incident



✅ Step 2: Make workflow risky

Edit .github/workflows/ci.yml and add:

permissions: write-all

✅ Step 3: Push branch
git add .
git commit -m "Demo: risky workflow permissions"
git push -u origin demo-incident

✅ Step 4: Create PR on GitHub

Expected result:

analyzer detects risk

risk score becomes HIGH/MEDIUM

response engine creates incident issue

PR gets comment

if HIGH → pipeline fails (blocks merge)

🚀 Running the Project
✅ Local Run (SOC Dashboard)
pip install -r requirements.txt
python dashboard/app.py


Open:
👉 http://127.0.0.1:5000

✅ One Command Full Scan (Generate Reports)
./run_all_scans.sh


Generates:

reports/workflow-risk-report.json

reports/pip-audit-report.json

reports/gitleaks-report.json

reports/final-risk-report.json

✅ Docker Run (Production)
docker compose up --build


Open:
👉 http://localhost:5000



📁 Output Reports

All evidence reports are stored in:

📌 reports/


🛠 Tech Stack

Python 3.12

Flask (SOC Dashboard)

GitHub Actions (DevSecOps automation)

Gitleaks (Secret scanning)

pip-audit (Dependency scanning)

GitHub CLI (SOAR issue + PR comment automation)

Docker + Gunicorn (Production deployment)


✅ Demo PR created to showcase SOAR PR commenting feature.


