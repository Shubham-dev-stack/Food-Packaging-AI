"""Integration and scenario tests for the RecommendationEngine across all commodity branches."""

import sqlite3

import pytest
from data.knowledge_base.seed import seed_database
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from backend.app.core.db import Base
from backend.app.domain.engine import RecommendationEngine
from backend.app.domain.types import (
    RecommendationInput,
    RecommendationStatus,
    StorageType,
    TransitStress,
)
from backend.app.models.commodity import Commodity
from backend.app.models.material import PackagingMaterial
from backend.app.repositories.commodity_repository import CommodityRepository
from backend.app.repositories.material_repository import MaterialRepository


@pytest.fixture
def seeded_db():
    """Create a fully seeded in-memory SQLite database for engine integration testing."""
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

    # Ingest benchmark catalog
    seed_database(session)

    yield session

    session.close()
    Base.metadata.drop_all(bind=test_engine)


def test_dry_crispy_product_potato_chips(seeded_db):
    """Scenario: Fried Potato Chips (COMM_POTATO_CHIPS).

    Must require strict moisture barrier (WVTR <= 2.5) and low OTR (< 2.5).
    Monolayer LDPE and neat PLA must be rejected.
    """
    comm = CommodityRepository.get_by_id(seeded_db, "COMM_POTATO_CHIPS")
    materials = MaterialRepository.list_all(seeded_db)

    inp = RecommendationInput(
        commodity_id="COMM_POTATO_CHIPS",
        desired_shelf_life_days=180,
        storage_temp_c=25.0,
        storage_rh_pct=65.0,
        storage_type=StorageType.AMBIENT,
        transit_stress=TransitStress.ROUGH_TERRAIN_UNPAVED,
        user_sustainability_preference=False,
    )

    result = RecommendationEngine.evaluate(comm, materials, inp)

    assert result.status == RecommendationStatus.SUPPORTED
    assert result.primary_recommendation is not None

    # Primary recommendation must be a high barrier laminate
    assert result.primary_recommendation.trade_code in [
        "MET-PET/PE",
        "PET/ALU/PE",
        "BoPE/PE-Mono",
    ]

    # Inspect disqualified materials
    disq_codes = {d.trade_code for d in result.disqualified_candidates}
    # LDPE has WVTR 16.0 >> 2.5 -> Must be rejected
    assert "LDPE-25" in disq_codes
    # PLA has WVTR 190.0 >> 2.5 -> Must be rejected
    assert "PLA-25" in disq_codes

    # Verify rejection reason for LDPE mentions WVTR
    ldpe_disq = next(d for d in result.disqualified_candidates if d.trade_code == "LDPE-25")
    assert any("nominal WVTR" in r for r in ldpe_disq.rejection_reasons)

    # Explanation must cite moisture/crispness driver
    assert "crispness" in result.explanation.dominant_spoilage_driver.lower()
    assert len(result.explanation.cited_evidence_sources) >= 1
    assert "REF_ROBERTSON_2012" in result.explanation.cited_evidence_sources


def test_high_fat_product_roasted_peanuts(seeded_db):
    """Scenario: Roasted Salted Peanuts (COMM_ROASTED_PEANUTS).

    Fat content 49% mandates high oxygen barrier (OTR <= 2.5).
    LDPE and HDPE must be rejected due to excessive OTR.
    """
    comm = CommodityRepository.get_by_id(seeded_db, "COMM_ROASTED_PEANUTS")
    materials = MaterialRepository.list_all(seeded_db)

    inp = RecommendationInput(
        commodity_id="COMM_ROASTED_PEANUTS",
        desired_shelf_life_days=120,
        storage_temp_c=20.0,
        storage_rh_pct=55.0,
        storage_type=StorageType.AMBIENT,
    )

    result = RecommendationEngine.evaluate(comm, materials, inp)

    assert result.status == RecommendationStatus.SUPPORTED
    assert result.primary_recommendation is not None

    disq_codes = {d.trade_code for d in result.disqualified_candidates}
    # LDPE has OTR 7000 and HDPE has OTR 2000 >> 2.5 -> Must be rejected
    assert "LDPE-25" in disq_codes
    assert "HDPE-25" in disq_codes

    assert result.target_specifications.is_light_barrier_required is True
    assert "lipid oxidation" in result.explanation.dominant_spoilage_driver.lower()


def test_fresh_respiring_produce_broccoli(seeded_db):
    """Scenario: Fresh Broccoli Florets (COMM_BROCCOLI).

    Extremely high respiration rate: non-perforated barrier films MUST be rejected.
    Micro-perforated film (PERF-BOPP/PE) must be selected.
    """
    comm = CommodityRepository.get_by_id(seeded_db, "COMM_BROCCOLI")
    materials = MaterialRepository.list_all(seeded_db)

    inp = RecommendationInput(
        commodity_id="COMM_BROCCOLI",
        desired_shelf_life_days=14,
        storage_temp_c=4.0,
        storage_rh_pct=95.0,
        storage_type=StorageType.CHILLED,
    )

    result = RecommendationEngine.evaluate(comm, materials, inp)

    assert result.status == RecommendationStatus.SUPPORTED
    assert result.primary_recommendation is not None
    # Micro-perforated film must be chosen
    assert result.primary_recommendation.trade_code == "PERF-BOPP/PE"

    # Non-perforated barrier films must be rejected due to hypoxia risk
    disq_codes = {d.trade_code for d in result.disqualified_candidates}
    assert "MET-PET/PE" in disq_codes
    assert "PET/ALU/PE" in disq_codes
    assert "BoPET-12" in disq_codes

    met_disq = next(d for d in result.disqualified_candidates if d.trade_code == "MET-PET/PE")
    assert any("hypoxia" in r.lower() for r in met_disq.rejection_reasons)

    assert result.target_specifications.is_microperforation_required is True


def test_frozen_storage_embrittlement_check(seeded_db):
    """Scenario: Frozen Green Peas (COMM_FROZEN_PEAS).

    Storage mode frozen (-18 C). PLA-25 is disqualified because its high WVTR (190 g)
    exceeds the freezer desiccation limit (<= 18.0 g/(m2*day)).
    """
    comm = CommodityRepository.get_by_id(seeded_db, "COMM_FROZEN_PEAS")
    materials = MaterialRepository.list_all(seeded_db)

    inp = RecommendationInput(
        commodity_id="COMM_FROZEN_PEAS",
        desired_shelf_life_days=180,
        storage_temp_c=-18.0,
        storage_rh_pct=90.0,
        storage_type=StorageType.FROZEN,
    )

    result = RecommendationEngine.evaluate(comm, materials, inp)

    assert result.status == RecommendationStatus.SUPPORTED
    disq_codes = {d.trade_code for d in result.disqualified_candidates}
    assert "PLA-25" in disq_codes
    pla_disq = next(d for d in result.disqualified_candidates if d.trade_code == "PLA-25")
    assert any("nominal WVTR" in r for r in pla_disq.rejection_reasons)


def test_citation_traceability_to_seeded_evidence_sources(seeded_db):
    """Verify that every citation ID generated in recommendations exists in EvidenceSource table."""
    from backend.app.repositories.evidence_repository import EvidenceRepository

    comm = CommodityRepository.get_by_id(seeded_db, "COMM_POTATO_CHIPS")
    materials = MaterialRepository.list_all(seeded_db)

    inp = RecommendationInput(
        commodity_id="COMM_POTATO_CHIPS",
        desired_shelf_life_days=120,
        storage_temp_c=25.0,
        storage_rh_pct=65.0,
    )

    result = RecommendationEngine.evaluate(comm, materials, inp)
    assert len(result.explanation.cited_evidence_sources) > 0

    for ref_id in result.explanation.cited_evidence_sources:
        source = EvidenceRepository.get_by_id(seeded_db, ref_id)
        assert source is not None, f"Cited reference_id '{ref_id}' not found in EvidenceSource!"


def test_processed_high_acid_food_tomato_paste(seeded_db):
    """Scenario: Concentrated Tomato Paste (COMM_TOMATO_PASTE).

    High-acid food (pH 4.1 < 4.6): must NOT trigger Clostridium botulinum ROP advisory.
    """
    comm = CommodityRepository.get_by_id(seeded_db, "COMM_TOMATO_PASTE")
    materials = MaterialRepository.list_all(seeded_db)

    inp = RecommendationInput(
        commodity_id="COMM_TOMATO_PASTE",
        desired_shelf_life_days=90,
        storage_temp_c=20.0,
        storage_rh_pct=60.0,
        storage_type=StorageType.AMBIENT,
    )

    result = RecommendationEngine.evaluate(comm, materials, inp)

    assert result.status in [RecommendationStatus.SUPPORTED, RecommendationStatus.CONDITIONAL]
    assert result.primary_recommendation is not None
    # Botulism ROP advisory should NOT be attached because pH < 4.6
    assert result.safety_advisory is None


def test_missing_commodity_baseline_evidence(seeded_db):
    """Edge Case: Commodity with no baseline property entity -> INSUFFICIENT_EVIDENCE."""
    bare_comm = Commodity(
        commodity_id="COMM_BARE_TEST",
        common_name="Bare Test Item",
        category="snack_fried",
        is_respiring=False,
        default_storage_mode="ambient",
    )
    materials = MaterialRepository.list_all(seeded_db)

    inp = RecommendationInput(
        commodity_id="COMM_BARE_TEST",
        desired_shelf_life_days=60,
        storage_temp_c=20.0,
        storage_rh_pct=50.0,
    )

    result = RecommendationEngine.evaluate(bare_comm, materials, inp)
    assert result.status == RecommendationStatus.INSUFFICIENT_EVIDENCE
    assert result.primary_recommendation is None
    assert any("No baseline" in note for note in result.uncertainty_notes)


def test_respiring_produce_missing_respiration_data(seeded_db):
    """Edge Case: Respiring commodity with no respiration entity -> RESEARCH_REQUIRED."""
    no_resp_comm = Commodity(
        commodity_id="COMM_UNKNOWN_FRUIT",
        common_name="Unknown Exotic Fruit",
        category="fruit",
        is_respiring=True,
        default_storage_mode="chilled",
    )
    # Add dummy property but no ProduceRespirationData
    materials = MaterialRepository.list_all(seeded_db)
    # Get any valid reference ID
    source = seeded_db.query(PackagingMaterial).first().reference_id

    from backend.app.models.commodity import CommodityProperty

    no_resp_comm.property = CommodityProperty(
        property_id="PROP_EXOTIC",
        typical_moisture_pct=85.0,
        critical_water_activity_aw=0.95,
        oil_fat_content_pct=0.2,
        typical_ph=5.0,
        primary_spoilage_pathways=["senescence_fermentation"],
        is_light_sensitive=False,
        recommended_temp_min_c=5.0,
        recommended_temp_max_c=10.0,
        recommended_rh_min_pct=85.0,
        recommended_rh_max_pct=95.0,
        reference_id=source,
    )

    inp = RecommendationInput(
        commodity_id="COMM_UNKNOWN_FRUIT",
        desired_shelf_life_days=10,
        storage_temp_c=8.0,
        storage_rh_pct=90.0,
        storage_type=StorageType.CHILLED,
    )

    result = RecommendationEngine.evaluate(no_resp_comm, materials, inp)
    assert result.status == RecommendationStatus.RESEARCH_REQUIRED
    assert result.primary_recommendation is None
    assert any("RESEARCH REQUIRED" in note for note in result.uncertainty_notes)


def test_sustainability_preference_weight_sensitivity(seeded_db):
    """Verify that enabling user_sustainability_preference elevates sustainable candidates."""
    comm = CommodityRepository.get_by_id(seeded_db, "COMM_TOMATO_PASTE")
    materials = MaterialRepository.list_all(seeded_db)

    # 1. Standard preference (prioritize barrier margin 50%)
    inp_std = RecommendationInput(
        commodity_id="COMM_TOMATO_PASTE",
        desired_shelf_life_days=60,
        storage_temp_c=20.0,
        storage_rh_pct=60.0,
        user_sustainability_preference=False,
    )
    res_std = RecommendationEngine.evaluate(comm, materials, inp_std)

    # 2. Sustainability preference (prioritize circularity 50%)
    inp_sust = RecommendationInput(
        commodity_id="COMM_TOMATO_PASTE",
        desired_shelf_life_days=60,
        storage_temp_c=20.0,
        storage_rh_pct=60.0,
        user_sustainability_preference=True,
    )
    res_sust = RecommendationEngine.evaluate(comm, materials, inp_sust)

    # Find the recyclable mono-material candidate BoPE/PE
    bope_std = next((c for c in res_std.ranked_candidates if c.trade_code == "BoPE/PE-Mono"), None)
    bope_sust = next(
        (c for c in res_sust.ranked_candidates if c.trade_code == "BoPE/PE-Mono"), None
    )

    assert bope_std is not None
    assert bope_sust is not None
    # Utility score under sustainability preference should be higher for mono-material
    assert bope_sust.composite_utility_score > bope_std.composite_utility_score


def test_frozen_storage_temperature_conflict(seeded_db):
    """Edge Case: Frozen storage type with temperature > 0 C triggers uncertainty warning."""
    comm = CommodityRepository.get_by_id(seeded_db, "COMM_FROZEN_PEAS")
    materials = MaterialRepository.list_all(seeded_db)

    inp = RecommendationInput(
        commodity_id="COMM_FROZEN_PEAS",
        desired_shelf_life_days=90,
        storage_temp_c=10.0,  # Conflict: 10 C > 0 C for frozen
        storage_rh_pct=80.0,
        storage_type=StorageType.FROZEN,
    )

    result = RecommendationEngine.evaluate(comm, materials, inp)
    assert any("Conflicting inputs" in note for note in result.uncertainty_notes)
