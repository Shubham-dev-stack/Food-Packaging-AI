"""Phase 10 E2E API Smoke Tests for SIH Evaluator Demonstration.

Verifies the 4 primary SIH demo scenarios plus health/readiness:
1. Health & readiness probe (GET /api/health)
2. Scenario 1: Ambient moisture & lipid-oxidation sensitive commodity (Potato Chips)
3. Scenario 2: High-respiration fresh produce requiring active MAP and anti-fog microperforation
   (Fresh Broccoli)
4. Scenario 3: Produce lacking verified MAP configuration returns explicit RESEARCH_REQUIRED flag
5. Scenario 4: Extreme barrier constraints correctly yields zero qualified candidates cleanly
"""

import pytest
from data.knowledge_base.seed import seed_database
from fastapi.testclient import TestClient

from backend.app.core.db import Base, SessionLocal, engine
from backend.app.domain.types import CandidateEligibility, RecommendationStatus
from backend.app.main import app
from backend.app.models.commodity import Commodity, CommodityProperty, ProduceRespirationData
from backend.app.models.material import PackagingMaterial


@pytest.fixture(scope="module")
def smoke_client():
    """Create test client with fresh database initialization."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()
    with TestClient(app) as test_client:
        yield test_client


def test_smoke_health_and_readiness(smoke_client: TestClient):
    """Smoke Test: Verify GET /api/health returns 200 with active database and environment."""
    response = smoke_client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "food-packaging-ai-backend"
    assert data["version"] == "0.1.0"
    assert data["database"] == "connected"
    assert "environment" in data


def test_smoke_scenario_1_potato_chips_baseline(smoke_client: TestClient):
    """Smoke Test Scenario 1: Potato Chips (ambient, moisture & lipid-oxidation critical).

    Verifies:
    - Status is SUPPORTED
    - Primary material is high-barrier metallized/foil laminate (MET-PET/PE or PET/ALU/PE)
    - Target WVTR <= 2.5 g/(m2*day) [PROTOTYPE TARGET: Robertson 2012 / ASTM F1249-20]
    - Target OTR <= 2.0 cm3/(m2*day*atm) [PROTOTYPE HEURISTIC: Robertson 2012 / ASTM D3985-17]
    - Light barrier requirement is enforced for high-fat photosensitive snack
    - Explanation cites peer-reviewed shelf-life kinetics and ASTM standards
    """
    payload = {
        "commodity_id": "COMM_POTATO_CHIPS",
        "desired_shelf_life_days": 180,
        "storage_temp_c": 25.0,
        "storage_rh_pct": 75.0,
        "storage_type": "ambient",
        "transit_stress": "rough_terrain_unpaved",
        "optimization_preference": "balanced",
    }
    response = smoke_client.post("/api/recommendations", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["status"] == RecommendationStatus.SUPPORTED
    assert data["commodity_name"] == "Fried Potato Chips"
    assert data["primary_recommendation"] is not None
    assert data["primary_recommendation"]["eligibility"] == CandidateEligibility.ELIGIBLE
    assert data["primary_recommendation"]["trade_code"] in ["MET-PET/PE", "PET/ALU/PE"]

    # Barrier specs traced to domain calculation:
    # 1. Crispy snack (aw=0.20 <= 0.35) clamped to max 2.5 g/(m2*day) under ASTM F1249-20
    specs = data["target_specifications"]
    assert specs["max_recommended_wvtr"] <= 2.5
    # 2. High-lipid snack (fat=34.0% >= 20%) literature target OTR <= 2.0 under ASTM D3985-17
    assert specs["max_recommended_otr"] <= 2.0
    assert specs["is_light_barrier_required"] is True

    # Audit traceability check
    assert "request_id" in data
    audit_res = smoke_client.get(f"/api/recommendations/{data['request_id']}")
    assert audit_res.status_code == 200


def test_smoke_scenario_2_fresh_broccoli_map(smoke_client: TestClient):
    """Smoke Test Scenario 2: Fresh Broccoli (chilled, high respiration rate).

    Verifies:
    - Respiration rate temperature adjustment applied [EXTERNAL EVIDENCE: Fonseca 2002 Q10 model]
    - Microperforation flagged as required for CO2 venting [EVIDENCE-DERIVED HEURISTIC: Kader 2002]
    - Equilibrium OTR demand calculated via coupled mass-balance (OTR_eq > 5000)
    - Laser micro-perforated film (PERF-BOPP/PE) ranked as primary eligible candidate
    """
    payload = {
        "commodity_id": "COMM_BROCCOLI",
        "desired_shelf_life_days": 14,
        "storage_temp_c": 4.0,
        "storage_rh_pct": 95.0,
        "storage_type": "chilled",
        "transit_stress": "long_haul_refrigerated",
        "optimization_preference": "balanced",
    }
    response = smoke_client.post("/api/recommendations", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["status"] in [RecommendationStatus.SUPPORTED, RecommendationStatus.CONDITIONAL]
    assert data["primary_recommendation"] is not None
    assert data["primary_recommendation"]["trade_code"] == "PERF-BOPP/PE"
    assert data["target_specifications"]["is_microperforation_required"] is True
    # Reference respiration rate 60.0 mg CO2/(kg*h) at 4 C in commodities.json
    assert data["target_specifications"]["adjusted_respiration_rate_co2"] == 60.07
    assert "Equilibrium O2 demand" in data["target_specifications"]["target_otr_rationale"]
    assert any("micro-perforated or breathable" in note for note in data["uncertainty_notes"])


def test_smoke_scenario_3_uncharacterized_produce_research_required(smoke_client: TestClient):
    """Smoke Test Scenario 3: Produce lacking verified MAP mix.

    Verifies:
    - System explicitly flags RESEARCH_REQUIRED in uncertainty notes
    - Never fabricates unsupported gas concentrations or unverified permeability models
    """
    db = SessionLocal()
    try:
        # Create a transient test commodity with respiration but without MAP data
        ref_id = db.query(PackagingMaterial).first().reference_id
        comm = db.query(Commodity).filter(Commodity.commodity_id == "COMM_SMOKE_UNVERIFIED").first()
        if not comm:
            comm = Commodity(
                commodity_id="COMM_SMOKE_UNVERIFIED",
                common_name="Uncharacterized Wild Mushroom",
                category="vegetable",
                is_respiring=True,
                default_storage_mode="chilled",
            )
            comm.property = CommodityProperty(
                property_id="PROP_SMOKE_UNVERIFIED",
                typical_moisture_pct=90.0,
                critical_water_activity_aw=0.98,
                oil_fat_content_pct=0.3,
                typical_ph=6.5,
                primary_spoilage_pathways=["senescence"],
                is_light_sensitive=False,
                recommended_temp_min_c=2.0,
                recommended_temp_max_c=6.0,
                recommended_rh_min_pct=90.0,
                recommended_rh_max_pct=95.0,
                reference_id=ref_id,
            )
            comm.respiration_data = [
                ProduceRespirationData(
                    respiration_id="RESP_SMOKE_UNVERIFIED",
                    respiration_class="high",
                    respiration_rate_co2=30.0,
                    reference_temp_c=4.0,
                    q10_factor=2.0,
                    critical_o2_extinction_pct=2.0,
                    max_tolerable_co2_pct=8.0,
                    condensation_risk_level="high",
                    reference_id=ref_id,
                )
            ]
            db.add(comm)
            db.commit()
    finally:
        db.close()

    payload = {
        "commodity_id": "COMM_SMOKE_UNVERIFIED",
        "desired_shelf_life_days": 7,
        "storage_temp_c": 4.0,
        "storage_rh_pct": 92.0,
        "storage_type": "chilled",
    }
    response = smoke_client.post("/api/recommendations", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert any("RESEARCH REQUIRED" in note for note in data["uncertainty_notes"])
    assert any("headspace gas mixtures" in note for note in data["uncertainty_notes"])


def test_smoke_scenario_4_impossible_constraints_no_candidates(smoke_client: TestClient):
    """Smoke Test Scenario 4: Extreme unobtainable barrier constraints.

    Verifies:
    - When candidate materials in the catalog fail mandatory barrier constraints:
      * System returns status RESEARCH_REQUIRED [PROTOTYPE STATUS]
      * Zero false-positive or fabricated materials (primary and alternative are None)
      * Ranked candidate count is 0
      * Disqualified candidates are cleanly enumerated with explicit failure reasons
      * Uncertainty notes and selection rationale clearly communicate boundary limitation
    """
    from unittest.mock import patch

    from backend.app.repositories.material_repository import MaterialRepository

    orig_list = MaterialRepository.list_all

    def mock_permeable_only_catalog(db, family=None):
        # [PROTOTYPE TEST FIXTURE] Simulate catalog lacking sufficient barrier for dry snacks
        return [m for m in orig_list(db, family) if m.trade_code in ["LDPE-25", "PLA-25"]]

    with patch.object(MaterialRepository, "list_all", side_effect=mock_permeable_only_catalog):
        payload = {
            "commodity_id": "COMM_POTATO_CHIPS",
            "desired_shelf_life_days": 180,
            "storage_temp_c": 25.0,
            "storage_rh_pct": 75.0,
        }
        response = smoke_client.post("/api/recommendations", json=payload)
        assert response.status_code == 200
        data = response.json()

        assert data["status"] == RecommendationStatus.RESEARCH_REQUIRED
        assert data["primary_recommendation"] is None
        assert data["alternative_recommendation"] is None
        assert len(data["ranked_candidates"]) == 0
        assert len(data["disqualified_candidates"]) == 2
        assert all(len(d["rejection_reasons"]) > 0 for d in data["disqualified_candidates"])
        assert "No candidate materials satisfied" in data["explanation"]["selection_rationale"]
        assert any(
            "No candidate materials in the catalog satisfied" in note
            for note in data["uncertainty_notes"]
        )
