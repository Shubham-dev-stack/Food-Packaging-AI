from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_health_check():
    """Test that the GET /api/health endpoint returns 200 and healthy status."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "food-packaging-ai-backend"
    assert data["database"] == "connected"
    assert "environment" in data
    assert "version" in data


def test_root_endpoint():
    """Test root endpoint returns 200 and correct status payload."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert data["health_check"] == "/api/health"
