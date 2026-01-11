from fastapi.testclient import TestClient

from app.main import app


def test_triage_endpoint_returns_category():
    client = TestClient(app)
    payload = {
        "age_group": "13_to_64",
        "main_symptom": "fever",
        "severity": "moderate",
        "red_flags": [],
        "fever_temp": "39_5_or_more",
        "duration": "less_24h",
        "risk_factors": ["none"],
    }
    r = client.post("/triage", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "category" in data
    assert "reasons" in data
    assert "timestamp" in data
