"""Integration tests for validation errors, input boundary checks, and error sanitization."""

import pytest
from data.knowledge_base.seed import seed_database
from fastapi.testclient import TestClient

from backend.app.core.db import Base, SessionLocal, engine
from backend.app.main import app


@pytest.fixture(scope="module")
def client():
    """Create test client with seeded database."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()
    with TestClient(app) as test_client:
        yield test_client


def test_validation_error_structure(client: TestClient):
    """Test that malformed inputs return structured VALIDATION_ERROR with field details."""
    payload = {
        "commodity_id": "COMM_POTATO_CHIPS",
        "desired_shelf_life_days": -5,  # Invalid: ge=1
        "storage_temp_c": 100.0,  # Invalid: le=50.0
        "storage_rh_pct": 120.0,  # Invalid: le=100.0
    }
    response = client.post("/api/recommendations", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert data["error"] == "VALIDATION_ERROR"
    assert "Invalid request input parameters" in data["message"]
    fields = [d["field"] for d in data["details"]]
    assert "desired_shelf_life_days" in fields
    assert "storage_temp_c" in fields
    assert "storage_rh_pct" in fields


def test_storage_type_inconsistency_validation(client: TestClient):
    """Test that conflicting storage type and temperature trigger physical sanity validation."""
    payload = {
        "commodity_id": "COMM_POTATO_CHIPS",
        "desired_shelf_life_days": 30,
        "storage_temp_c": 25.0,  # Inconsistent with 'frozen'
        "storage_rh_pct": 50.0,
        "storage_type": "frozen",
    }
    response = client.post("/api/recommendations", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert data["error"] == "VALIDATION_ERROR"
    issues = [d["issue"] for d in data["details"]]
    assert any("frozen" in issue.lower() and "temperature" in issue.lower() for issue in issues)


def test_ranking_weights_sum_validation(client: TestClient):
    """Test that custom ranking weights not summing to 1.0 are rejected."""
    payload = {
        "commodity_id": "COMM_POTATO_CHIPS",
        "desired_shelf_life_days": 30,
        "storage_temp_c": 20.0,
        "storage_rh_pct": 50.0,
        "custom_weights": {
            "w_barrier": 0.5,
            "w_sustainability": 0.5,
            "w_cost": 0.5,  # Sum is 1.5
        },
    }
    response = client.post("/api/recommendations", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert data["error"] == "VALIDATION_ERROR"


def test_existing_health_check_preserved(client: TestClient):
    """Ensure the existing /api/health and / endpoints are strictly preserved."""
    res_health = client.get("/api/health")
    assert res_health.status_code == 200
    assert res_health.json()["status"] == "healthy"

    res_root = client.get("/")
    assert res_root.status_code == 200
    assert res_root.json()["status"] == "online"
