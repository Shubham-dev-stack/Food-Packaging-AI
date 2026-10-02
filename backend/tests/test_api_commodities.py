"""Integration tests for Commodities API endpoints."""

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


def test_list_commodities(client: TestClient):
    """Test GET /api/commodities returns seeded commodity catalog."""
    response = client.get("/api/commodities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 5
    names = [c["common_name"] for c in data]
    assert "Fried Potato Chips" in names
    assert "Fresh Broccoli Florets" in names


def test_list_commodities_category_filter(client: TestClient):
    """Test filtering commodities by category."""
    response = client.get("/api/commodities?category=snack_fried")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert any("Fried Potato Chips" in c["common_name"] for c in data)


def test_get_commodity_detail(client: TestClient):
    """Test GET /api/commodities/{id} returns nested properties and respiration."""
    response = client.get("/api/commodities/COMM_BROCCOLI")
    assert response.status_code == 200
    data = response.json()
    assert data["commodity_id"] == "COMM_BROCCOLI"
    assert data["is_respiring"] is True
    assert data["property"] is not None
    assert data["property"]["typical_moisture_pct"] == 90.0
    assert len(data["respiration_data"]) > 0
    assert data["map_configuration"] is not None
    assert data["map_configuration"]["suitability_status"] == "suitable"


def test_get_commodity_not_found(client: TestClient):
    """Test GET /api/commodities/{id} returns 404 for unknown ID."""
    response = client.get("/api/commodities/NON_EXISTENT_CROP")
    assert response.status_code == 404
    error_data = response.json()
    assert error_data["error"] == "NOT_FOUND"
    assert "not found" in error_data["message"].lower()
