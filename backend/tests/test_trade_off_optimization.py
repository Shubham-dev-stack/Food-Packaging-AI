"""Phase 8 tests: Multi-criteria optimization, trade-offs, and preferences."""

import sqlite3

import pytest
from data.knowledge_base.seed import seed_database
from pydantic import ValidationError
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from backend.app.core.db import Base
from backend.app.domain.engine import RecommendationEngine
from backend.app.domain.types import (
    BALANCED_WEIGHTS,
    COST_PRIORITY_WEIGHTS,
    SUSTAINABILITY_PRIORITY_WEIGHTS,
    CandidateEligibility,
    OptimizationPreference,
    RankingWeightsConfig,
    RecommendationInput,
    RecommendationStatus,
    StorageType,
)
from backend.app.repositories.commodity_repository import CommodityRepository
from backend.app.repositories.material_repository import MaterialRepository
from backend.app.schemas.recommendation import (
    RankingWeightsRequest,
    RecommendationCreateRequest,
)
from backend.app.services.recommendation_service import RecommendationService


@pytest.fixture
def seeded_db():
    """Create a seeded in-memory SQLite database for trade-off testing."""
    test_engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )

    @event.listens_for(test_engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        if isinstance(dbapi_connection, sqlite3.Connection):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    Base.metadata.create_all(bind=test_engine)
    session_factory = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    session = session_factory()

    seed_database(session)

    yield session

    session.close()
    Base.metadata.drop_all(bind=test_engine)


def test_preset_weights_values_and_bounds():
    """Verify exact documented prototype weights for balanced, sustainability, and cost presets."""
    # Balanced baseline: 50% barrier, 30% sustainability, 20% cost
    assert BALANCED_WEIGHTS.w_barrier == 0.50
    assert BALANCED_WEIGHTS.w_sustainability == 0.30
    assert BALANCED_WEIGHTS.w_cost == 0.20
    assert (
        round(
            BALANCED_WEIGHTS.w_barrier
            + BALANCED_WEIGHTS.w_sustainability
            + BALANCED_WEIGHTS.w_cost,
            4,
        )
        == 1.00
    )

    # Sustainability preset: 40% barrier, 45% sustainability, 15% cost
    assert SUSTAINABILITY_PRIORITY_WEIGHTS.w_barrier == 0.40
    assert SUSTAINABILITY_PRIORITY_WEIGHTS.w_sustainability == 0.45
    assert SUSTAINABILITY_PRIORITY_WEIGHTS.w_cost == 0.15
    assert (
        round(
            SUSTAINABILITY_PRIORITY_WEIGHTS.w_barrier
            + SUSTAINABILITY_PRIORITY_WEIGHTS.w_sustainability
            + SUSTAINABILITY_PRIORITY_WEIGHTS.w_cost,
            4,
        )
        == 1.00
    )

    # Cost-sensitive preset: 40% barrier, 15% sustainability, 45% cost
    assert COST_PRIORITY_WEIGHTS.w_barrier == 0.40
    assert COST_PRIORITY_WEIGHTS.w_sustainability == 0.15
    assert COST_PRIORITY_WEIGHTS.w_cost == 0.45
    assert (
        round(
            COST_PRIORITY_WEIGHTS.w_barrier
            + COST_PRIORITY_WEIGHTS.w_sustainability
            + COST_PRIORITY_WEIGHTS.w_cost,
            4,
        )
        == 1.00
    )


def test_candidate_score_breakdown_sums_correctly(seeded_db):
    """Requirement 5: Candidate score breakdown sums exactly to composite_utility_score."""
    comm = CommodityRepository.get_by_id(seeded_db, "COMM_POTATO_CHIPS")
    materials = MaterialRepository.list_all(seeded_db)

    inp = RecommendationInput(
        commodity_id="COMM_POTATO_CHIPS",
        desired_shelf_life_days=180,
        storage_temp_c=25.0,
        storage_rh_pct=65.0,
        storage_type=StorageType.AMBIENT,
        optimization_preference=OptimizationPreference.BALANCED,
    )

    res = RecommendationEngine.evaluate(comm, materials, inp)
    assert res.status == RecommendationStatus.SUPPORTED
    assert len(res.ranked_candidates) > 0

    for cand in res.ranked_candidates:
        calculated_sum = round(
            cand.barrier_contribution + cand.sustainability_contribution + cand.cost_contribution,
            4,
        )
        assert cand.composite_utility_score == calculated_sum
        assert cand.rank >= 1

    # Ranks must be 1, 2, 3, ... sequentially
    ranks = [c.rank for c in res.ranked_candidates]
    assert ranks == list(range(1, len(res.ranked_candidates) + 1))


def test_preference_switching_changes_ranking_responsibly(seeded_db):
    """Requirements 1, 2, 3: Compare balanced vs sustainability vs cost ranking behavior."""
    comm = CommodityRepository.get_by_id(seeded_db, "COMM_TOMATO_PASTE")
    materials = MaterialRepository.list_all(seeded_db)

    # 1. Balanced
    inp_bal = RecommendationInput(
        commodity_id="COMM_TOMATO_PASTE",
        desired_shelf_life_days=60,
        storage_temp_c=20.0,
        storage_rh_pct=60.0,
        optimization_preference=OptimizationPreference.BALANCED,
    )
    res_bal = RecommendationEngine.evaluate(comm, materials, inp_bal)

    # 2. Sustainability-focused
    inp_sust = RecommendationInput(
        commodity_id="COMM_TOMATO_PASTE",
        desired_shelf_life_days=60,
        storage_temp_c=20.0,
        storage_rh_pct=60.0,
        optimization_preference=OptimizationPreference.SUSTAINABILITY,
    )
    res_sust = RecommendationEngine.evaluate(comm, materials, inp_sust)

    # 3. Cost-sensitive
    inp_cost = RecommendationInput(
        commodity_id="COMM_TOMATO_PASTE",
        desired_shelf_life_days=60,
        storage_temp_c=20.0,
        storage_rh_pct=60.0,
        optimization_preference=OptimizationPreference.COST,
    )
    res_cost = RecommendationEngine.evaluate(comm, materials, inp_cost)

    # Check applied weights
    assert res_bal.applied_weights == BALANCED_WEIGHTS
    assert res_sust.applied_weights == SUSTAINABILITY_PRIORITY_WEIGHTS
    assert res_cost.applied_weights == COST_PRIORITY_WEIGHTS

    # Find BoPE/PE-Mono (high sustainability: 1.0, moderate cost: ~0.53, good barrier)
    bope_bal = next((c for c in res_bal.ranked_candidates if c.trade_code == "BoPE/PE-Mono"), None)
    bope_sust = next(
        (c for c in res_sust.ranked_candidates if c.trade_code == "BoPE/PE-Mono"), None
    )
    bope_cost = next(
        (c for c in res_cost.ranked_candidates if c.trade_code == "BoPE/PE-Mono"), None
    )

    assert bope_bal is not None
    assert bope_sust is not None
    assert bope_cost is not None

    # Sustainability contribution must be highest under sustainability preference
    assert bope_sust.sustainability_contribution > bope_bal.sustainability_contribution
    assert bope_sust.sustainability_contribution > bope_cost.sustainability_contribution

    # Cost contribution must be highest under cost preference
    assert bope_cost.cost_contribution > bope_bal.cost_contribution
    assert bope_cost.cost_contribution > bope_sust.cost_contribution


def test_hard_constraint_failure_cannot_be_overridden_by_preference(seeded_db):
    """Requirement 4: Disqualified material cannot qualify due to sustainability or cost."""
    comm = CommodityRepository.get_by_id(seeded_db, "COMM_POTATO_CHIPS")
    materials = MaterialRepository.list_all(seeded_db)

    # LDPE is cheap and recyclable mono-material, but fails moisture barrier (WVTR 16.0 >> 2.5).
    for pref in [
        OptimizationPreference.BALANCED,
        OptimizationPreference.SUSTAINABILITY,
        OptimizationPreference.COST,
    ]:
        inp = RecommendationInput(
            commodity_id="COMM_POTATO_CHIPS",
            desired_shelf_life_days=180,
            storage_temp_c=25.0,
            storage_rh_pct=65.0,
            optimization_preference=pref,
        )
        res = RecommendationEngine.evaluate(comm, materials, inp)

        # LDPE must remain disqualified under every single preference!
        assert not any(c.trade_code == "LDPE-25" for c in res.ranked_candidates)
        disq = next(d for d in res.disqualified_candidates if d.trade_code == "LDPE-25")
        assert disq.eligibility == CandidateEligibility.REJECTED
        assert any("WVTR" in r for r in disq.rejection_reasons)

        # Primary recommendation must NEVER be LDPE
        assert res.primary_recommendation is not None
        assert res.primary_recommendation.trade_code != "LDPE-25"


def test_ranking_determinism(seeded_db):
    """Requirement 6: Ranking order is completely deterministic across repeated evaluations."""
    comm = CommodityRepository.get_by_id(seeded_db, "COMM_ROASTED_PEANUTS")
    materials = MaterialRepository.list_all(seeded_db)

    inp = RecommendationInput(
        commodity_id="COMM_ROASTED_PEANUTS",
        desired_shelf_life_days=90,
        storage_temp_c=25.0,
        storage_rh_pct=60.0,
        optimization_preference=OptimizationPreference.COST,
    )

    res1 = RecommendationEngine.evaluate(comm, materials, inp)
    res2 = RecommendationEngine.evaluate(comm, materials, inp)

    codes1 = [c.trade_code for c in res1.ranked_candidates]
    codes2 = [c.trade_code for c in res2.ranked_candidates]
    assert codes1 == codes2

    scores1 = [c.composite_utility_score for c in res1.ranked_candidates]
    scores2 = [c.composite_utility_score for c in res2.ranked_candidates]
    assert scores1 == scores2


def test_fresh_produce_constraints_enforced_under_all_preferences(seeded_db):
    """Requirement 8: Respiring produce constraints remain enforced under all preferences."""
    comm = CommodityRepository.get_by_id(seeded_db, "COMM_BROCCOLI")
    materials = MaterialRepository.list_all(seeded_db)

    for pref in [
        OptimizationPreference.BALANCED,
        OptimizationPreference.SUSTAINABILITY,
        OptimizationPreference.COST,
    ]:
        inp = RecommendationInput(
            commodity_id="COMM_BROCCOLI",
            desired_shelf_life_days=14,
            storage_temp_c=4.0,
            storage_rh_pct=95.0,
            storage_type=StorageType.CHILLED,
            optimization_preference=pref,
        )
        res = RecommendationEngine.evaluate(comm, materials, inp)

        assert res.status == RecommendationStatus.SUPPORTED
        assert res.target_specifications is not None
        assert res.target_specifications.is_microperforation_required is True
        assert res.target_specifications.adjusted_respiration_rate_co2 is not None

        # Aluminum foil laminate must be disqualified due to zero breathability
        disq_codes = {d.trade_code for d in res.disqualified_candidates}
        assert "PET/ALU/PE" in disq_codes


def test_invalid_preference_and_custom_weights_validation():
    """Requirement 9: Malformed or invalid weights cannot influence ranking."""
    # Weights not summing to 1.0 must fail validation
    with pytest.raises(ValueError, match="must sum to 1.0"):
        RankingWeightsConfig(w_barrier=0.8, w_sustainability=0.5, w_cost=0.2)

    with pytest.raises(ValueError, match="must sum to 1.0"):
        RankingWeightsRequest(w_barrier=0.3, w_sustainability=0.3, w_cost=0.3)

    # Negative weights must fail Pydantic bounds
    with pytest.raises(ValidationError):
        RankingWeightsRequest(w_barrier=-0.1, w_sustainability=0.6, w_cost=0.5)


def test_service_layer_and_api_payload_compatibility(seeded_db):
    """Requirements 7 & 10: RecommendationService accepts preference and returns breakdown."""
    req = RecommendationCreateRequest(
        commodity_id="COMM_POTATO_CHIPS",
        desired_shelf_life_days=180,
        storage_temp_c=25.0,
        storage_rh_pct=65.0,
        storage_type=StorageType.AMBIENT,
        optimization_preference=OptimizationPreference.COST,
    )

    resp = RecommendationService.create_recommendation(seeded_db, req)
    assert resp.status == RecommendationStatus.SUPPORTED
    assert resp.optimization_preference == OptimizationPreference.COST
    assert resp.applied_weights is not None
    assert resp.applied_weights.w_barrier == 0.40
    assert resp.applied_weights.w_sustainability == 0.15
    assert resp.applied_weights.w_cost == 0.45

    primary = resp.primary_recommendation
    assert primary is not None
    assert primary.rank == 1
    assert primary.barrier_contribution > 0
    assert primary.sustainability_contribution > 0
    assert primary.cost_contribution > 0
    assert primary.composite_utility_score == round(
        primary.barrier_contribution
        + primary.sustainability_contribution
        + primary.cost_contribution,
        4,
    )
