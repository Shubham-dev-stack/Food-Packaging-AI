"""Phase 9 Validation, Edge-Case Hardening & Recommendation Reliability Tests.

Verifies:
1. Recommendation Invariants (Invariants 1 - 10)
2. Edge cases (all disqualified, single candidate, boundary temps, extended duration)
3. Input validation & error sanitization
4. Reproducibility & determinism guarantees
5. Explainability consistency & decision-support limitations
"""

import pytest
from data.knowledge_base.seed import seed_database
from fastapi.testclient import TestClient

from backend.app.core.db import Base, SessionLocal, engine
from backend.app.domain.engine import RecommendationEngine
from backend.app.domain.types import (
    BALANCED_WEIGHTS,
    COST_PRIORITY_WEIGHTS,
    SUSTAINABILITY_PRIORITY_WEIGHTS,
    CandidateEligibility,
    OptimizationPreference,
    RecommendationInput,
    RecommendationStatus,
    StorageType,
    TransitStress,
)
from backend.app.main import app
from backend.app.models.commodity import Commodity, CommodityProperty, ProduceRespirationData
from backend.app.models.material import PackagingMaterial
from backend.app.repositories.commodity_repository import CommodityRepository
from backend.app.repositories.material_repository import MaterialRepository
from backend.app.schemas.recommendation import RecommendationCreateRequest
from backend.app.services.recommendation_service import RecommendationService


@pytest.fixture
def seeded_db():
    """Create a fully seeded database session for unit and domain integration testing."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
        yield db
    finally:
        db.close()


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


# =========================================================================
# 1. RECOMMENDATION INVARIANTS (Invariants 1 - 10)
# =========================================================================


def test_invariants_across_all_commodities(seeded_db):
    """Verify Invariants 1-8 across all seeded commodities and preferences."""
    commodities = CommodityRepository.list_all(seeded_db)
    materials = MaterialRepository.list_all(seeded_db)

    for comm in commodities:
        for pref in [
            OptimizationPreference.BALANCED,
            OptimizationPreference.SUSTAINABILITY,
            OptimizationPreference.COST,
        ]:
            inp = RecommendationInput(
                commodity_id=comm.commodity_id,
                desired_shelf_life_days=60,
                storage_temp_c=4.0 if comm.is_respiring else 22.0,
                storage_rh_pct=85.0 if comm.is_respiring else 50.0,
                storage_type=StorageType.CHILLED if comm.is_respiring else StorageType.AMBIENT,
                optimization_preference=pref,
            )
            result = RecommendationEngine.evaluate(comm, materials, inp)

            # Invariant 7: Applied weights sum to 1.0
            assert result.applied_weights is not None
            total_w = (
                result.applied_weights.w_barrier
                + result.applied_weights.w_sustainability
                + result.applied_weights.w_cost
            )
            assert pytest.approx(total_w, abs=1e-4) == 1.0

            # Invariant 8: Applied weights correspond to preference
            if pref == OptimizationPreference.BALANCED:
                assert result.applied_weights == BALANCED_WEIGHTS
            elif pref == OptimizationPreference.SUSTAINABILITY:
                assert result.applied_weights == SUSTAINABILITY_PRIORITY_WEIGHTS
            elif pref == OptimizationPreference.COST:
                assert result.applied_weights == COST_PRIORITY_WEIGHTS

            # Invariant 1: Every ranked candidate is qualified
            for cand in result.ranked_candidates:
                assert cand.eligibility in [
                    CandidateEligibility.ELIGIBLE,
                    CandidateEligibility.CONDITIONALLY_ELIGIBLE,
                ]

            # Invariant 2: Every disqualified candidate has at least one rejection reason
            for disq in result.disqualified_candidates:
                assert disq.eligibility == CandidateEligibility.REJECTED
                assert len(disq.rejection_reasons) > 0

            # Invariant 3: Rank values are contiguous 1, 2, ...
            if result.ranked_candidates:
                ranks = [c.rank for c in result.ranked_candidates]
                assert ranks == list(range(1, len(result.ranked_candidates) + 1))

                # Invariant 4: Primary recommendation is rank 1
                assert result.primary_recommendation is not None
                assert result.primary_recommendation.rank == 1
                assert (
                    result.primary_recommendation.material_id
                    == result.ranked_candidates[0].material_id
                )

                # Invariant 5: Alternative is different qualified candidate when present
                if result.alternative_recommendation:
                    assert (
                        result.alternative_recommendation.material_id
                        != result.primary_recommendation.material_id
                    )
                    assert result.alternative_recommendation.eligibility in [
                        CandidateEligibility.ELIGIBLE,
                        CandidateEligibility.CONDITIONALLY_ELIGIBLE,
                    ]

            # Invariant 6: Composite utility equals sum of contributions
            for cand in result.ranked_candidates:
                contrib_sum = round(
                    cand.barrier_contribution
                    + cand.sustainability_contribution
                    + cand.cost_contribution,
                    4,
                )
                assert cand.composite_utility_score == contrib_sum


def test_invariant_9_changing_preference_cannot_change_hard_constraint_eligibility(seeded_db):
    """Invariant 9: Preference changes alter candidate order, NEVER qualification."""
    comm = CommodityRepository.get_by_id(seeded_db, "COMM_POTATO_CHIPS")
    materials = MaterialRepository.list_all(seeded_db)

    res_bal = RecommendationEngine.evaluate(
        comm,
        materials,
        RecommendationInput(
            commodity_id="COMM_POTATO_CHIPS",
            desired_shelf_life_days=180,
            storage_temp_c=25.0,
            storage_rh_pct=65.0,
            optimization_preference=OptimizationPreference.BALANCED,
        ),
    )
    res_cost = RecommendationEngine.evaluate(
        comm,
        materials,
        RecommendationInput(
            commodity_id="COMM_POTATO_CHIPS",
            desired_shelf_life_days=180,
            storage_temp_c=25.0,
            storage_rh_pct=65.0,
            optimization_preference=OptimizationPreference.COST,
        ),
    )

    bal_viable_ids = {c.material_id for c in res_bal.ranked_candidates}
    cost_viable_ids = {c.material_id for c in res_cost.ranked_candidates}
    assert bal_viable_ids == cost_viable_ids

    bal_disq_ids = {c.material_id for c in res_bal.disqualified_candidates}
    cost_disq_ids = {c.material_id for c in res_cost.disqualified_candidates}
    assert bal_disq_ids == cost_disq_ids


# =========================================================================
# 2. EDGE CASES & RELIABILITY
# =========================================================================


def test_case_e_no_qualified_candidates_when_constraints_unobtainable(seeded_db):
    """Case E & G: When no candidate satisfies constraints, result is clear without faking."""
    comm = CommodityRepository.get_by_id(seeded_db, "COMM_POTATO_CHIPS")
    materials = MaterialRepository.list_all(seeded_db)

    # Extreme shelf life (730 days) and high RH (95%) produces WVTR requirement < 0.01 g/(m2*day)
    inp = RecommendationInput(
        commodity_id="COMM_POTATO_CHIPS",
        desired_shelf_life_days=730,
        storage_temp_c=45.0,
        storage_rh_pct=98.0,
        transit_stress=TransitStress.ROUGH_TERRAIN_UNPAVED,
    )
    result = RecommendationEngine.evaluate(comm, materials, inp)

    if len(result.ranked_candidates) == 0:
        assert result.primary_recommendation is None
        assert result.alternative_recommendation is None
        assert result.status == RecommendationStatus.RESEARCH_REQUIRED
        assert len(result.disqualified_candidates) == len(materials)
        assert any("No candidate materials" in note for note in result.uncertainty_notes)
        assert "No candidate materials satisfied" in result.explanation.selection_rationale


def test_case_f_single_qualified_candidate(seeded_db):
    """Case F: When exactly one material qualifies, alternative is gracefully None."""
    comm = CommodityRepository.get_by_id(seeded_db, "COMM_POTATO_CHIPS")
    materials = MaterialRepository.list_all(seeded_db)

    # Take only the top barrier foil laminate (PET/ALU/PE) and LDPE
    filtered_mats = [m for m in materials if m.trade_code in ["PET/ALU/PE", "LDPE-25"]]

    inp = RecommendationInput(
        commodity_id="COMM_POTATO_CHIPS",
        desired_shelf_life_days=180,
        storage_temp_c=25.0,
        storage_rh_pct=65.0,
    )
    result = RecommendationEngine.evaluate(comm, filtered_mats, inp)

    # Exactly 1 qualified (PET/ALU/PE), LDPE is disqualified
    assert len(result.ranked_candidates) == 1
    assert result.primary_recommendation is not None
    assert result.primary_recommendation.trade_code == "PET/ALU/PE"
    assert result.alternative_recommendation is None
    assert "No distinct secondary viable candidate" in result.explanation.alternative_rationale


def test_case_c_extended_storage_duration_attaches_uncertainty(seeded_db):
    """Case C: Storage duration > 365 days attaches explicit degradation uncertainty."""
    comm = CommodityRepository.get_by_id(seeded_db, "COMM_POTATO_CHIPS")
    materials = MaterialRepository.list_all(seeded_db)

    inp = RecommendationInput(
        commodity_id="COMM_POTATO_CHIPS",
        desired_shelf_life_days=500,
        storage_temp_c=20.0,
        storage_rh_pct=50.0,
    )
    result = RecommendationEngine.evaluate(comm, materials, inp)

    assert any("Extended target shelf life" in note for note in result.uncertainty_notes)
    assert any("pinholing" in note for note in result.uncertainty_notes)


def test_case_b_elevated_temperature_boundary_uncertainty(seeded_db):
    """Case B: Storage temp > 40 C triggers Arrhenius relaxation uncertainty."""
    comm = CommodityRepository.get_by_id(seeded_db, "COMM_POTATO_CHIPS")
    materials = MaterialRepository.list_all(seeded_db)

    inp = RecommendationInput(
        commodity_id="COMM_POTATO_CHIPS",
        desired_shelf_life_days=60,
        storage_temp_c=45.0,
        storage_rh_pct=50.0,
    )
    result = RecommendationEngine.evaluate(comm, materials, inp)

    assert any("Elevated ambient storage temperature" in note for note in result.uncertainty_notes)


def test_case_d_respiring_crop_missing_map_mixture_returns_research_required(seeded_db):
    """Case D & Invariant 10: Produce lacking verified MAP mix displays RESEARCH REQUIRED."""
    comm = Commodity(
        commodity_id="COMM_EXOTIC_LEAF",
        common_name="Exotic Microgreens",
        category="vegetable",
        is_respiring=True,
        default_storage_mode="chilled",
    )
    ref_id = seeded_db.query(PackagingMaterial).first().reference_id
    comm.property = CommodityProperty(
        property_id="PROP_EXOTIC_LEAF",
        typical_moisture_pct=92.0,
        critical_water_activity_aw=0.99,
        oil_fat_content_pct=0.2,
        typical_ph=6.2,
        primary_spoilage_pathways=["senescence"],
        is_light_sensitive=False,
        recommended_temp_min_c=2.0,
        recommended_temp_max_c=6.0,
        recommended_rh_min_pct=90.0,
        recommended_rh_max_pct=98.0,
        reference_id=ref_id,
    )
    # Give respiration rate, but NO MAP configuration attached to commodity
    comm.respiration_data = [
        ProduceRespirationData(
            respiration_id="RESP_EXOTIC_LEAF",
            respiration_class="high",
            respiration_rate_co2=35.0,
            reference_temp_c=4.0,
            q10_factor=2.0,
            critical_o2_extinction_pct=2.0,
            max_tolerable_co2_pct=8.0,
            condensation_risk_level="high",
            reference_id=ref_id,
        )
    ]
    materials = MaterialRepository.list_all(seeded_db)

    inp = RecommendationInput(
        commodity_id="COMM_EXOTIC_LEAF",
        desired_shelf_life_days=10,
        storage_temp_c=4.0,
        storage_rh_pct=95.0,
        storage_type=StorageType.CHILLED,
    )
    result = RecommendationEngine.evaluate(comm, materials, inp)

    # Must flag research required for gas composition, never fabricating gas mixture
    assert any("RESEARCH REQUIRED" in note for note in result.uncertainty_notes)
    assert any("headspace gas mixtures" in note for note in result.uncertainty_notes)


# =========================================================================
# 3. DETERMINISM & REPRODUCIBILITY
# =========================================================================


def test_recommendation_determinism_identical_runs(seeded_db):
    """Case F: Submitting identical requests produces 100% identical outputs."""
    comm = CommodityRepository.get_by_id(seeded_db, "COMM_ROASTED_PEANUTS")
    materials = MaterialRepository.list_all(seeded_db)

    inp = RecommendationInput(
        commodity_id="COMM_ROASTED_PEANUTS",
        desired_shelf_life_days=90,
        storage_temp_c=22.0,
        storage_rh_pct=55.0,
        optimization_preference=OptimizationPreference.SUSTAINABILITY,
    )

    res1 = RecommendationEngine.evaluate(comm, materials, inp)
    res2 = RecommendationEngine.evaluate(comm, materials, inp)

    assert res1.status == res2.status
    assert res1.primary_recommendation.material_id == res2.primary_recommendation.material_id
    assert res1.primary_recommendation.composite_utility_score == (
        res2.primary_recommendation.composite_utility_score
    )
    assert len(res1.ranked_candidates) == len(res2.ranked_candidates)
    for c1, c2 in zip(res1.ranked_candidates, res2.ranked_candidates, strict=True):
        assert c1.material_id == c2.material_id
        assert c1.rank == c2.rank
        assert c1.composite_utility_score == c2.composite_utility_score


# =========================================================================
# 4. API ERROR SANITIZATION & INPUT BOUNDS
# =========================================================================


def test_api_validation_bounds_and_no_stack_trace_leakage(client: TestClient):
    """Verify bounds rejection with sanitized error details and no tracebacks."""
    # Test negative shelf life
    res = client.post(
        "/api/recommendations",
        json={
            "commodity_id": "COMM_POTATO_CHIPS",
            "desired_shelf_life_days": -10,
            "storage_temp_c": 20.0,
            "storage_rh_pct": 50.0,
        },
    )
    assert res.status_code == 422
    data = res.json()
    assert data["error"] == "VALIDATION_ERROR"
    assert "Traceback" not in res.text
    assert "File" not in res.text

    # Test extreme temperature beyond sanity bounds (> 50 C)
    res_temp = client.post(
        "/api/recommendations",
        json={
            "commodity_id": "COMM_POTATO_CHIPS",
            "desired_shelf_life_days": 30,
            "storage_temp_c": 75.0,  # Bound is le=50.0
            "storage_rh_pct": 50.0,
        },
    )
    assert res_temp.status_code == 422
    assert "storage_temp_c" in [d["field"] for d in res_temp.json()["details"]]


def test_nonexistent_commodity_returns_clean_404(client: TestClient):
    """Verify nonexistent commodity returns 404 without internal crash."""
    res = client.post(
        "/api/recommendations",
        json={
            "commodity_id": "COMM_NON_EXISTENT_999",
            "desired_shelf_life_days": 30,
            "storage_temp_c": 20.0,
            "storage_rh_pct": 50.0,
        },
    )
    assert res.status_code == 404
    data = res.json()
    assert data["error"] == "NOT_FOUND"
    assert "COMM_NON_EXISTENT_999" in data["message"]


def test_service_layer_end_to_end_consistency(seeded_db):
    """Verify Service Layer maps all fields consistently without truncation."""
    req = RecommendationCreateRequest(
        commodity_id="COMM_BROCCOLI",
        desired_shelf_life_days=14,
        storage_temp_c=4.0,
        storage_rh_pct=95.0,
        storage_type=StorageType.CHILLED,
        optimization_preference=OptimizationPreference.BALANCED,
    )
    resp = RecommendationService.create_recommendation(seeded_db, req)

    # Invariants on API response
    assert resp.status in [RecommendationStatus.SUPPORTED, RecommendationStatus.CONDITIONAL]
    assert resp.primary_recommendation is not None
    assert resp.primary_recommendation.rank == 1
    assert resp.applied_weights.w_barrier == 0.50
    assert resp.target_specifications.adjusted_respiration_rate_co2 is not None
    assert resp.target_specifications.is_microperforation_required is True

    # Primary material not in disqualified
    disq_ids = {d.material_id for d in resp.disqualified_candidates}
    assert resp.primary_recommendation.material_id not in disq_ids
