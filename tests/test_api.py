"""FastAPI smoke tests for static UI and numerical TDI endpoint."""
import math
from fastapi.testclient import TestClient
from agents.api import app

client = TestClient(app)


def test_browser_page_and_assets():
    response = client.get("/")
    assert response.status_code == 200
    assert "CYP time-dependent inactivation" in response.text
    assert client.get("/app.mjs").status_code == 200
    assert client.get("/kinetics.mjs").status_code == 200


def test_tdi_endpoint():
    response = client.post("/api/kinetics", json={
        "kinact_per_min": 0.2, "ki_um": 5, "inhibitor_um": 5, "time_min": 10
    })
    assert response.status_code == 200
    data = response.json()
    assert abs(data["kobs_per_min"] - 0.1) < 1e-10
    assert abs(data["remaining_activity_pct"] - 100 * math.exp(-1)) < 1e-10


def test_tdi_endpoint_rejects_invalid():
    response = client.post("/api/kinetics", json={
        "kinact_per_min": 0.2, "ki_um": 0, "inhibitor_um": 5, "time_min": 10
    })
    assert response.status_code == 422


def test_health_still_available():
    assert client.get("/health").status_code == 200
