"""Integration tests for JSON fixture ingestion, repositories, and database reset."""

import sqlite3

import pytest
from data.knowledge_base.seed import seed_database
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from backend.app.core.db import Base
from backend.app.models.commodity import Commodity
from backend.app.models.evidence import EvidenceSource
from backend.app.models.material import PackagingMaterial
from backend.app.repositories.commodity_repository import CommodityRepository
from backend.app.repositories.evidence_repository import EvidenceRepository
from backend.app.repositories.material_repository import MaterialRepository


@pytest.fixture
def clean_db():
    """Create a clean isolated SQLite database for seed testing."""
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

    yield session, test_engine

    session.close()
    Base.metadata.drop_all(bind=test_engine)


def test_deterministic_seed_execution(clean_db):
    """Verify that seed_database populates all required entities with valid foreign keys."""
    session, _ = clean_db
    results = seed_database(session)

    assert results["evidence_sources"] >= 8
    assert results["packaging_materials"] >= 8
    assert results["commodities"] >= 5

    # Verify EvidenceSource ingestion
    sources = session.query(EvidenceSource).all()
    assert len(sources) >= 8
    ref_ids = {s.reference_id for s in sources}
    assert "REF_ROBERTSON_2012" in ref_ids
    assert "REF_USDA_HB66_2016" in ref_ids
    assert "REF_KADER_2002" in ref_ids
    assert "REF_ASTM_D3985" in ref_ids
    assert "REF_ASTM_F1249" in ref_ids

    # Verify Commodities ingestion & branch coverage
    commodities = session.query(Commodity).all()
    assert len(commodities) >= 5
    comm_ids = {c.commodity_id for c in commodities}

    # 1. Moisture-sensitive dry product
    assert "COMM_POTATO_CHIPS" in comm_ids
    chips = CommodityRepository.get_by_id(session, "COMM_POTATO_CHIPS")
    assert chips is not None
    assert chips.property.critical_water_activity_aw == 0.40
    assert chips.property.oil_fat_content_pct == 35.0
    assert chips.property.is_light_sensitive is True

    # 2. High-fat product
    assert "COMM_ROASTED_PEANUTS" in comm_ids
    peanuts = CommodityRepository.get_by_id(session, "COMM_ROASTED_PEANUTS")
    assert peanuts is not None
    assert peanuts.property.oil_fat_content_pct == 49.0

    # 3. Respiring fresh produce
    assert "COMM_BROCCOLI" in comm_ids
    broccoli = CommodityRepository.get_by_id(session, "COMM_BROCCOLI")
    assert broccoli is not None
    assert broccoli.is_respiring is True
    assert len(broccoli.respiration_data) >= 1
    assert broccoli.respiration_data[0].respiration_rate_co2 == 65.0
    assert broccoli.map_configuration is not None
    assert broccoli.map_configuration.suitability_status == "suitable"
    assert broccoli.map_configuration.recommended_o2_min_pct == 1.0

    # 4. Frozen product
    assert "COMM_FROZEN_PEAS" in comm_ids
    peas = CommodityRepository.get_by_id(session, "COMM_FROZEN_PEAS")
    assert peas is not None
    assert peas.default_storage_mode == "frozen"
    assert peas.property.recommended_temp_max_c <= -18.0

    # 5. Processed high-acid food (pH < 4.6)
    assert "COMM_TOMATO_PASTE" in comm_ids
    paste = CommodityRepository.get_by_id(session, "COMM_TOMATO_PASTE")
    assert paste is not None
    assert paste.property.typical_ph < 4.6


def test_packaging_materials_seed_verification(clean_db):
    """Verify that all representative packaging materials from SIH26236 are seeded."""
    session, _ = clean_db
    seed_database(session)

    materials = session.query(PackagingMaterial).all()
    assert len(materials) >= 8
    trade_codes = {m.trade_code for m in materials}

    # Check key material representations from SIH problem statement
    assert "LDPE-25" in trade_codes
    assert "HDPE-25" in trade_codes
    assert "BoPET-12" in trade_codes
    assert "MET-PET/PE" in trade_codes
    assert "PET/ALU/PE" in trade_codes
    assert "PLA-25" in trade_codes
    assert "PERF-BOPP/PE" in trade_codes
    assert "BoPE/PE-Mono" in trade_codes

    # Verify barrier and sustainability attributes
    ldpe = MaterialRepository.get_by_trade_code(session, "LDPE-25")
    assert ldpe is not None
    assert len(ldpe.barrier_properties) == 1
    assert ldpe.barrier_properties[0].otr_value == 7000.0
    assert ldpe.barrier_properties[0].wvtr_value == 16.0
    assert ldpe.sustainability_metric.is_mono_material is True
    assert ldpe.cost_index.relative_cost_multiplier == 1.0

    alu = MaterialRepository.get_by_trade_code(session, "PET/ALU/PE")
    assert alu is not None
    assert alu.barrier_properties[0].otr_value == 0.02
    assert alu.barrier_properties[0].wvtr_value == 0.02
    assert alu.sustainability_metric.circularity_tier == "linear_landfill"

    pla = MaterialRepository.get_by_trade_code(session, "PLA-25")
    assert pla is not None
    assert pla.is_biodegradable is True
    assert pla.recyclability_category == "industrial_compostable"


def test_repeated_seed_idempotency(clean_db):
    """Verify that running seed_database repeatedly causes no errors and inserts 0 duplicates."""
    session, _ = clean_db

    first_run = seed_database(session)
    assert first_run["evidence_sources"] >= 8

    # Second run on the same session
    second_run = seed_database(session)
    assert second_run["evidence_sources"] == 0
    assert second_run["packaging_materials"] == 0
    assert second_run["commodities"] == 0


def test_database_reset_and_reinitialize(clean_db):
    """Verify clean drop and recreate behavior."""
    session, test_engine = clean_db
    seed_database(session)

    # Count prior to drop
    assert session.query(Commodity).count() >= 5

    # Drop all tables
    Base.metadata.drop_all(bind=test_engine)

    # Re-create all tables
    Base.metadata.create_all(bind=test_engine)

    # Verify tables are empty
    assert session.query(Commodity).count() == 0

    # Re-seed
    reseed_results = seed_database(session)
    assert reseed_results["commodities"] >= 5
    assert session.query(Commodity).count() >= 5


def test_evidence_repository_methods(clean_db):
    """Verify query methods in EvidenceRepository."""
    session, _ = clean_db
    seed_database(session)

    item = EvidenceRepository.get_by_id(session, "REF_ROBERTSON_2012")
    assert item is not None
    assert item.publication_year == 2012

    all_items = EvidenceRepository.list_all(session)
    assert len(all_items) >= 8


def test_commodity_repository_methods(clean_db):
    """Verify query methods in CommodityRepository."""
    session, _ = clean_db
    seed_database(session)

    by_name = CommodityRepository.get_by_name(session, "Fried Potato Chips")
    assert by_name is not None
    assert by_name.commodity_id == "COMM_POTATO_CHIPS"

    snacks = CommodityRepository.list_all(session, category="snack_fried")
    assert len(snacks) >= 2  # Potato chips and roasted peanuts


def test_material_repository_methods(clean_db):
    """Verify query methods in MaterialRepository."""
    session, _ = clean_db
    seed_database(session)

    mat = MaterialRepository.get_by_id(session, "MAT_MET_PET_PE")
    assert mat is not None
    assert mat.material_family == "metallized_film"

    monolayers = MaterialRepository.list_all(session, family="LDPE")
    assert len(monolayers) >= 1
