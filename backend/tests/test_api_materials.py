"""Integration tests for Packaging Materials API endpoints."""

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


def test_list_materials(client: TestClient):
    """Test GET /api/materials returns seeded packaging material catalog."""
    response = client.get("/api/materials")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 8
    trade_codes = [m["trade_code"] for m in data]
    assert "MET-PET/PE" in trade_codes
    assert "LDPE-25" in trade_codes
    assert "BoPE/PE-Mono" in trade_codes


def test_list_materials_family_filter(client: TestClient):
    """Test filtering packaging materials by polymer family."""
    response = client.get("/api/materials?family=metallized_film")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["material_family"] == "metallized_film"


def test_get_material_detail(client: TestClient):
    """Test GET /api/materials/{id} returns barrier properties and sustainability metrics."""
    response = client.get("/api/materials/MAT_MET_PET_PE")
    assert response.status_code == 200
    data = response.json()
    assert data["material_id"] == "MAT_MET_PET_PE"
    assert data["trade_code"] == "MET-PET/PE"
    assert len(data["barrier_properties"]) > 0
    barrier = data["barrier_properties"][0]
    assert barrier["otr_value"] == 1.2
    assert barrier["test_standard_otr"] == "ASTM D3985"
    assert barrier["wvtr_value"] == 0.9
    assert barrier["test_standard_wvtr"] == "ASTM F1249"
    assert data["sustainability_metric"] is not None
    assert data["cost_index"] is not None
    assert data["cost_index"]["relative_cost_multiplier"] == 2.1


def test_get_material_not_found(client: TestClient):
    """Test GET /api/materials/{id} returns 404 for unknown ID."""
    response = client.get("/api/materials/NON_EXISTENT_MATERIAL")
    assert response.status_code == 404
    error_data = response.json()
    assert error_data["error"] == "NOT_FOUND"
