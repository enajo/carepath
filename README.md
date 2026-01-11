# CarePath — Rule-based Symptom Triage Wizard (Not Diagnosis)

CarePath is a small healthcare demo app that asks a short questionnaire and returns a conservative triage category:
- Emergency now
- Urgent today
- See a clinician soon (24–72h)
- Self-care / monitor

⚠️ DISCLAIMER: This tool is NOT medical advice and does NOT provide diagnosis. If symptoms are severe, rapidly worsening, or you feel unsafe, seek urgent care or call local emergency services.

## Tech
- FastAPI (API + serves the UI)
- Single-page wizard UI (HTML + JS)
- Docker + Docker Compose
- GitHub Actions CI (lint + tests) and CD (build/push + deploy to server + health check)

---

## Run locally (no Docker)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt

uvicorn app.main:app --reload --port 8000
