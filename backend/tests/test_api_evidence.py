"""Integration tests for Evidence Sources API endpoints."""

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


def test_list_evidence(client: TestClient):
    """Test GET /api/evidence returns seeded evidence citations."""
    response = client.get("/api/evidence")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 8
    refs = [e["reference_id"] for e in data]
    assert "REF_ROBERTSON_2012" in refs
    assert "REF_ASTM_D3985" in refs
    assert "REF_ASTM_F1249" in refs


def test_get_evidence_detail(client: TestClient):
    """Test GET /api/evidence/{id} returns bibliographic citation detail."""
    response = client.get("/api/evidence/REF_ROBERTSON_2012")
    assert response.status_code == 200
    data = response.json()
    assert data["reference_id"] == "REF_ROBERTSON_2012"
    assert "Robertson" in data["citation_short"]
    assert data["publication_year"] == 2012
    assert data["source_type"] == "textbook"


def test_get_evidence_not_found(client: TestClient):
    """Test GET /api/evidence/{id} returns 404 for unknown ID."""
    response = client.get("/api/evidence/NON_EXISTENT_REF")
    assert response.status_code == 404
    error_data = response.json()
    assert error_data["error"] == "NOT_FOUND"
