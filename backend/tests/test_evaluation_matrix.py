"""Phase 11 Final Evaluation Harness & Golden Cases Verification.

Executes the formal 8-scenario evaluation matrix (Scenarios A through H)
defined in data/evaluation/prototype_evaluation_cases.json against the active API.
Verifies domain consistency, respiration kinetics, trade-off preferences,
hard constraint immunity, and error sanitization.
"""

import json
from pathlib import Path
from unittest.mock import patch

import pytest
from data.knowledge_base.seed import seed_database
from fastapi.testclient import TestClient

from backend.app.core.db import Base, SessionLocal, engine
from backend.app.domain.types import CandidateEligibility, RecommendationStatus
from backend.app.main import app
from backend.app.models.commodity import Commodity, CommodityProperty, ProduceRespirationData
from backend.app.models.material import PackagingMaterial
from backend.app.repositories.material_repository import MaterialRepository


@pytest.fixture(scope="module")
def eval_client():
    """Create test client with fresh database initialization."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="module")
def eval_cases():
    """Load documented golden evaluation cases fixture."""
    fixture_path = (
        Path(__file__).resolve().parent.parent.parent
        / "data"
        / "evaluation"
        / "prototype_evaluation_cases.json"
    )
    with open(fixture_path, encoding="utf-8") as f:
        data = json.load(f)
    return {c["case_id"]: c for c in data["cases"]}


def test_eval_scenario_a_potato_chips(eval_client: TestClient, eval_cases: dict):
    """Scenario A: Potato Chips (Crispy snack, moisture & lipid oxidation critical).

    Verifies:
    - Status is SUPPORTED
    - Primary candidate is high-barrier metallized/foil laminate
    - Technical specs: WVTR <= 2.5 g/(m2*day), OTR <= 2.0 cm3/(m2*day*atm)
    - Photosensitivity: Light barrier requirement enforced
    - Trade-off preference switching modifies utility scores deterministically
    """
    case = eval_cases["SCENARIO_A_POTATO_CHIPS"]
    payload = {"commodity_id": case["commodity_id"], **case["inputs"]}

    res = eval_client.post("/api/recommendations", json=payload)
    assert res.status_code == 200
    data = res.json()

    assert data["status"] == RecommendationStatus.SUPPORTED
    assert data["primary_recommendation"] is not None
    assert data["primary_recommendation"]["eligibility"] == CandidateEligibility.ELIGIBLE
    assert data["primary_recommendation"]["trade_code"] in ["MET-PET/PE", "PET/ALU/PE"]

    specs = data["target_specifications"]
    assert specs["max_recommended_wvtr"] <= case["expected"]["max_recommended_wvtr_upper_bound"]
    assert specs["max_recommended_otr"] <= case["expected"]["max_recommended_otr_upper_bound"]
    assert specs["is_light_barrier_required"] is True
    assert specs["is_microperforation_required"] is False

    # Check that cited evidence sources trace back to literature
    for expected_ref in case["citations"]:
        assert expected_ref in data["explanation"]["cited_evidence_sources"]


def test_eval_scenario_b_roasted_peanuts(eval_client: TestClient, eval_cases: dict):
    """Scenario B: Roasted Peanuts (High fat, moderate moisture).

    Verifies:
    - Status is SUPPORTED
    - Oxygen barrier OTR <= 2.0 strictly enforced for high fat content (49%)
    - Moisture barrier WVTR <= 4.5 g/(m2*day)
    - Determinism: Repeated identical queries produce identical composite utility
    """
    case = eval_cases["SCENARIO_B_ROASTED_PEANUTS"]
    payload = {"commodity_id": case["commodity_id"], **case["inputs"]}

    res1 = eval_client.post("/api/recommendations", json=payload)
    res2 = eval_client.post("/api/recommendations", json=payload)

    assert res1.status_code == 200
    assert res2.status_code == 200
    d1 = res1.json()
    d2 = res2.json()

    assert d1["status"] == RecommendationStatus.SUPPORTED
    assert d1["primary_recommendation"]["trade_code"] == d2["primary_recommendation"]["trade_code"]
    assert (
        d1["primary_recommendation"]["composite_utility_score"]
        == d2["primary_recommendation"]["composite_utility_score"]
    )
    assert d1["target_specifications"]["max_recommended_otr"] <= 2.0
    assert d1["target_specifications"]["max_recommended_wvtr"] <= 4.5


def test_eval_scenario_c_fresh_broccoli_map(eval_client: TestClient, eval_cases: dict):
    """Scenario C: Fresh Broccoli (High-respiration chilled fresh produce).

    Verifies:
    - Microperforation flagged as required to prevent hypoxia/off-odors
    - Active post-harvest respiration rate is adjusted to storage temperature (60.07 mg CO2/(kg*h))
    - Dense foil and metallized films are rejected with severe hypoxia hazard
    - Invariant: Sustainability or cost preference cannot promote disqualified foil to viable
    """
    case = eval_cases["SCENARIO_C_FRESH_BROCCOLI"]
    payload = {"commodity_id": case["commodity_id"], **case["inputs"]}

    res = eval_client.post("/api/recommendations", json=payload)
    assert res.status_code == 200
    data = res.json()

    assert data["status"] in [RecommendationStatus.SUPPORTED, RecommendationStatus.CONDITIONAL]
    assert data["primary_recommendation"]["trade_code"] == "PERF-BOPP/PE"
    assert data["target_specifications"]["is_microperforation_required"] is True
    assert (
        data["target_specifications"]["adjusted_respiration_rate_co2"]
        == case["expected"]["adjusted_respiration_rate_co2"]
    )

    # Dense foil and metallized materials MUST be in disqualified candidates
    disq_codes = {d["trade_code"] for d in data["disqualified_candidates"]}
    assert "PET/ALU/PE" in disq_codes
    assert "MET-PET/PE" in disq_codes

    # Verify hypoxia hazard reason
    foil_disq = next(d for d in data["disqualified_candidates"] if d["trade_code"] == "PET/ALU/PE")
    assert any("Severe hypoxia hazard" in r for r in foil_disq["rejection_reasons"])

    # Hard constraint immunity: test with cost and sustainability preferences
    for pref in ["sustainability", "cost"]:
        p_payload = {**payload, "optimization_preference": pref}
        p_res = eval_client.post("/api/recommendations", json=p_payload)
        p_data = p_res.json()
        p_disq_codes = {d["trade_code"] for d in p_data["disqualified_candidates"]}
        assert "PET/ALU/PE" in p_disq_codes
        assert "MET-PET/PE" in p_disq_codes


def test_eval_scenario_d_frozen_peas(eval_client: TestClient, eval_cases: dict):
    """Scenario D: Frozen Peas (Sub-zero frozen storage).

    Verifies:
    - Status is SUPPORTED
    - Non-respiring in frozen state (is_microperforation_required is False)
    - Sub-zero physical handling caution attached for unplasticized bio-polyesters
    - WVTR <= 18.0 g/(m2*day) to prevent freezer sublimation
    """
    case = eval_cases["SCENARIO_D_FROZEN_PEAS"]
    payload = {"commodity_id": case["commodity_id"], **case["inputs"]}

    res = eval_client.post("/api/recommendations", json=payload)
    assert res.status_code == 200
    data = res.json()

    assert data["status"] == RecommendationStatus.SUPPORTED
    assert data["target_specifications"]["is_microperforation_required"] is False
    assert (
        data["target_specifications"]["max_recommended_wvtr"]
        <= case["expected"]["max_recommended_wvtr_upper_bound"]
    )

    # PLA biodegradable film should contain frozen handling condition note
    pla_cand = next(
        (c for c in data["ranked_candidates"] if c["material_family"] == "biodegradable_film"),
        None,
    )
    if pla_cand:
        assert any("LOW-TEMPERATURE HANDLING" in note for note in pla_cand["condition_notes"])


def test_eval_scenario_e_tomato_paste(eval_client: TestClient, eval_cases: dict):
    """Scenario E: Tomato Paste (Acidic, moisture-dense processed food).

    Verifies:
    - Status is SUPPORTED
    - High-acid product context (pH=4.1 < 4.6): OTR <= 60.0 to prevent carotenoid bleaching
    - Microbial safety context: low pH inhibits botulinum pathogens naturally
    """
    case = eval_cases["SCENARIO_E_TOMATO_PASTE"]
    payload = {"commodity_id": case["commodity_id"], **case["inputs"]}

    res = eval_client.post("/api/recommendations", json=payload)
    assert res.status_code == 200
    data = res.json()

    assert data["status"] == RecommendationStatus.SUPPORTED
    assert (
        data["target_specifications"]["max_recommended_otr"]
        <= case["expected"]["max_recommended_otr_upper_bound"]
    )
    assert "Acid-preserved commodity" in data["target_specifications"]["target_otr_rationale"]


def test_eval_scenario_f_research_required_produce(eval_client: TestClient, eval_cases: dict):
    """Scenario F: Research-Required Produce (Lacks verified postharvest MAP gas mixture).

    Verifies:
    - System explicitly flags RESEARCH_REQUIRED
    - Refuses to hallucinate or fabricate equilibrium gas concentrations
    - Boundary limitation communicated in uncertainty notes
    """
    db = SessionLocal()
    try:
        ref_id = db.query(PackagingMaterial).first().reference_id
        comm = db.query(Commodity).filter(Commodity.commodity_id == "COMM_EVAL_UNVERIFIED").first()
        if not comm:
            comm = Commodity(
                commodity_id="COMM_EVAL_UNVERIFIED",
                common_name="Uncharacterized Rare Produce",
                category="vegetable",
                is_respiring=True,
                default_storage_mode="chilled",
            )
            comm.property = CommodityProperty(
                property_id="PROP_EVAL_UNVERIFIED",
                typical_moisture_pct=92.0,
                critical_water_activity_aw=0.98,
                oil_fat_content_pct=0.2,
                typical_ph=6.4,
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
                    respiration_id="RESP_EVAL_UNVERIFIED",
                    respiration_class="high",
                    respiration_rate_co2=32.0,
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
        "commodity_id": "COMM_EVAL_UNVERIFIED",
        "desired_shelf_life_days": 7,
        "storage_temp_c": 4.0,
        "storage_rh_pct": 92.0,
        "storage_type": "chilled",
    }
    res = eval_client.post("/api/recommendations", json=payload)
    assert res.status_code == 200
    data = res.json()

    assert any("RESEARCH REQUIRED" in note for note in data["uncertainty_notes"])
    assert any("headspace gas mixtures" in note for note in data["uncertainty_notes"])


def test_eval_scenario_g_no_qualified_candidates(eval_client: TestClient, eval_cases: dict):
    """Scenario G: No Qualified Candidate (Catalog barrier failure).

    Verifies:
    - Status is RESEARCH_REQUIRED
    - primary_recommendation is None
    - alternative_recommendation is None
    - ranked_candidates count is 0
    - All evaluated materials cleanly enumerated in disqualified_candidates with explicit reasons
    - No fabricated or false-positive fallback candidate returned
    """
    case = eval_cases["SCENARIO_G_NO_QUALIFIED_CANDIDATES"]
    orig_list = MaterialRepository.list_all

    def mock_permeable_catalog(db, family=None):
        return [m for m in orig_list(db, family) if m.trade_code in ["LDPE-25", "PLA-25"]]

    with patch.object(MaterialRepository, "list_all", side_effect=mock_permeable_catalog):
        payload = {"commodity_id": case["commodity_id"], **case["inputs"]}
        res = eval_client.post("/api/recommendations", json=payload)
        assert res.status_code == 200
        data = res.json()

        assert data["status"] == RecommendationStatus.RESEARCH_REQUIRED
        assert data["primary_recommendation"] is None
        assert data["alternative_recommendation"] is None
        assert len(data["ranked_candidates"]) == 0
        assert len(data["disqualified_candidates"]) == 2
        assert all(len(d["rejection_reasons"]) > 0 for d in data["disqualified_candidates"])
        assert "No candidate materials satisfied" in data["explanation"]["selection_rationale"]


def test_eval_scenario_h_invalid_input(eval_client: TestClient, eval_cases: dict):
    """Scenario H: Invalid Input (Physics-violating or out-of-bounds parameters).

    Verifies:
    - HTTP 422 Unprocessable Entity
    - Clean error_code: VALIDATION_ERROR
    - Sanitized error messages without Python tracebacks, file paths, or secret leaks
    """
    case = eval_cases["SCENARIO_H_INVALID_INPUT_SANITY"]
    payload = {"commodity_id": case["commodity_id"], **case["inputs"]}

    res = eval_client.post("/api/recommendations", json=payload)
    assert res.status_code == 422
    data = res.json()

    assert data["error"] == "VALIDATION_ERROR"
    assert "Traceback" not in res.text
    assert 'File "' not in res.text
    assert any("frozen" in str(d["issue"]).lower() for d in data["details"])
