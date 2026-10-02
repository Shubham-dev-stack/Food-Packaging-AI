"""Integration tests for Recommendation API endpoints, service orchestration, and audit logging."""

import pytest
from data.knowledge_base.seed import seed_database
from fastapi.testclient import TestClient

from backend.app.core.db import Base, SessionLocal, engine
from backend.app.domain.types import CandidateEligibility, RecommendationStatus
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


def test_recommendation_potato_chips(client: TestClient):
    """Test recommendation generation for Potato Chips (lipid oxidation & moisture sensitive)."""
    payload = {
        "commodity_id": "COMM_POTATO_CHIPS",
        "desired_shelf_life_days": 180,
        "storage_temp_c": 25.0,
        "storage_rh_pct": 75.0,
        "storage_type": "ambient",
        "transit_stress": "rough_terrain_unpaved",
        "user_sustainability_preference": False,
    }
    response = client.post("/api/recommendations", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["status"] == RecommendationStatus.SUPPORTED
    assert data["commodity_name"] == "Fried Potato Chips"
    assert data["primary_recommendation"] is not None
    assert data["primary_recommendation"]["trade_code"] in ["MET-PET/PE", "PET/ALU/PE"]
    assert data["primary_recommendation"]["eligibility"] == CandidateEligibility.ELIGIBLE

    # Check target specifications
    specs = data["target_specifications"]
    assert specs is not None
    assert specs["max_recommended_wvtr"] < 5.0
    assert specs["max_recommended_otr"] < 10.0
    assert specs["is_light_barrier_required"] is True

    # Check explanation and citations
    expl = data["explanation"]
    assert expl is not None
    assert (
        "moisture" in expl["dominant_spoilage_driver"].lower()
        or "oxidation" in expl["dominant_spoilage_driver"].lower()
    )
    assert len(expl["cited_evidence_sources"]) > 0

    # Verify audit retrieval works
    request_id = data["request_id"]
    get_res = client.get(f"/api/recommendations/{request_id}")
    assert get_res.status_code == 200
    audit_data = get_res.json()
    assert audit_data["request_id"] == request_id
    assert audit_data["commodity_id"] == "COMM_POTATO_CHIPS"


def test_recommendation_fresh_broccoli(client: TestClient):
    """Test recommendation generation for Fresh Broccoli (high respiration produce)."""
    payload = {
        "commodity_id": "COMM_BROCCOLI",
        "desired_shelf_life_days": 14,
        "storage_temp_c": 4.0,
        "storage_rh_pct": 95.0,
        "storage_type": "chilled",
        "transit_stress": "long_haul_refrigerated",
    }
    response = client.post("/api/recommendations", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["status"] in [RecommendationStatus.SUPPORTED, RecommendationStatus.CONDITIONAL]
    assert data["primary_recommendation"] is not None
    # Pre-perforated film is expected to be eligible
    assert data["primary_recommendation"]["trade_code"] == "PERF-BOPP/PE"
    assert data["target_specifications"]["is_microperforation_required"] is True


def test_recommendation_safety_advisory(client: TestClient):
    """Test contextual ROP safety advisory is triggered for low-acid high-moisture commodity."""
    payload = {
        "commodity_id": "COMM_FROZEN_PEAS",
        "desired_shelf_life_days": 60,
        "storage_temp_c": 5.0,
        "storage_rh_pct": 85.0,
        "storage_type": "chilled",
        "ph": 6.2,  # Low acid (>= 4.6)
        "water_activity_aw": 0.95,  # High moisture (>= 0.92)
        "moisture_pct": 80.0,
        "oil_fat_content_pct": 25.0,  # High fat requires tight OTR (<= 10.0)
    }
    response = client.post("/api/recommendations", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["safety_advisory"] is not None
    assert "CONTEXTUAL FOOD SAFETY ADVISORY" in data["safety_advisory"]
    assert "botulinum" in data["safety_advisory"].lower()


def test_recommendation_unknown_commodity(client: TestClient):
    """Test 404 response when querying recommendation for nonexistent commodity."""
    payload = {
        "commodity_id": "COMM_UNKNOWN_999",
        "desired_shelf_life_days": 30,
        "storage_temp_c": 20.0,
        "storage_rh_pct": 50.0,
    }
    response = client.post("/api/recommendations", json=payload)
    assert response.status_code == 404
    error_data = response.json()
    assert error_data["error"] == "NOT_FOUND"


def test_recommendation_audit_not_found(client: TestClient):
    """Test 404 response when fetching nonexistent recommendation audit session."""
    response = client.get("/api/recommendations/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
    error_data = response.json()
    assert error_data["error"] == "NOT_FOUND"
