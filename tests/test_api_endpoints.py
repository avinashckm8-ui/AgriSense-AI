"""
Integration tests for FastAPI endpoints using Starlette/HTTPX TestClient.
"""

from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Verify that root system endpoint returns service info."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["project"] == "AgriSense AI"
    assert "documentation" in data


def test_system_health_endpoint():
    """Verify system health endpoint reports module availability."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "fertilizer_recommendation" in data["modules"]


def test_fertilizer_health_endpoint():
    """Verify fertilizer module health reporting."""
    response = client.get("/api/predict/fertilizer/health")
    assert response.status_code == 200
    data = response.json()
    assert data["module"] == "fertilizer_recommendation"
    assert "model_loaded" in data


def test_fertilizer_prediction_missing_body():
    """Verify that sending empty/malformed body returns 422 Unprocessable Entity."""
    response = client.post("/api/predict/fertilizer", json={})
    assert response.status_code == 422


def test_fertilizer_prediction_invalid_fields():
    """Verify validation on improper field types."""
    response = client.post(
        "/api/predict/fertilizer",
        json={
            "temperature": "not-a-number",
            "humidity": 50,
            "moisture": 40,
            "soil_type": "Sandy",
            "crop_type": "Maize",
            "nitrogen": 30,
            "potassium": 20,
            "phosphorous": 10,
        },
    )
    assert response.status_code == 422
