"""Unit tests for relational data models, constraints, and foreign-key integrity."""

import sqlite3

import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from backend.app.core.db import Base
from backend.app.models.commodity import (
    Commodity,
    CommodityProperty,
    MAPConfiguration,
    ProduceRespirationData,
)
from backend.app.models.evidence import EvidenceSource
from backend.app.models.material import (
    CostIndex,
    PackagingBarrierProperty,
    PackagingMaterial,
    SustainabilityMetric,
)


@pytest.fixture
def db_session():
    """Create an isolated in-memory SQLite database with strictly enforced foreign keys."""
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

    yield session

    session.close()
    Base.metadata.drop_all(bind=test_engine)


def test_evidence_source_creation(db_session):
    """Verify creating and retrieving an EvidenceSource entity."""
    source = EvidenceSource(
        reference_id="REF_TEST_2026",
        citation_short="Test Author 2026",
        title="Experimental Testing of Polymer Transmission",
        authors="Test Author",
        publication_year=2026,
        source_type="peer_reviewed_journal",
        doi_or_standard_number="10.1000/182",
        notes="Control specimen test data",
    )
    db_session.add(source)
    db_session.commit()

    retrieved = (
        db_session.query(EvidenceSource)
        .filter(EvidenceSource.reference_id == "REF_TEST_2026")
        .first()
    )
    assert retrieved is not None
    assert retrieved.citation_short == "Test Author 2026"
    assert retrieved.publication_year == 2026


def test_foreign_key_enforcement_without_evidence(db_session):
    """Verify that referencing a non-existent EvidenceSource raises an IntegrityError."""
    comm = Commodity(
        commodity_id="COMM_INVALID_EVIDENCE",
        common_name="Invalid Test Item",
        category="snack_fried",
        is_respiring=False,
        default_storage_mode="ambient",
    )
    db_session.add(comm)
    db_session.commit()

    prop = CommodityProperty(
        property_id="PROP_INVALID",
        commodity_id="COMM_INVALID_EVIDENCE",
        typical_moisture_pct=5.0,
        critical_water_activity_aw=0.5,
        oil_fat_content_pct=10.0,
        typical_ph=6.0,
        primary_spoilage_pathways=["moisture_gain"],
        is_light_sensitive=False,
        recommended_temp_min_c=10.0,
        recommended_temp_max_c=20.0,
        recommended_rh_min_pct=40.0,
        recommended_rh_max_pct=60.0,
        reference_id="NON_EXISTENT_REF_ID",  # Violates foreign key
    )
    db_session.add(prop)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_commodity_and_property_relationships(db_session):
    """Verify 1-to-1 relationship between Commodity and CommodityProperty."""
    evidence = EvidenceSource(
        reference_id="REF_SNACK_2012",
        citation_short="Robertson 2012",
        title="Food Packaging Principles",
        source_type="textbook",
    )
    db_session.add(evidence)
    db_session.commit()

    comm = Commodity(
        commodity_id="COMM_TEST_CHIPS",
        common_name="Crispy Potato Chips",
        category="snack_fried",
        is_respiring=False,
        default_storage_mode="ambient",
    )
    prop = CommodityProperty(
        property_id="PROP_TEST_CHIPS",
        typical_moisture_pct=2.0,
        critical_water_activity_aw=0.40,
        oil_fat_content_pct=35.0,
        typical_ph=6.0,
        primary_spoilage_pathways=["moisture_gain", "oxidation"],
        is_light_sensitive=True,
        recommended_temp_min_c=15.0,
        recommended_temp_max_c=25.0,
        recommended_rh_min_pct=40.0,
        recommended_rh_max_pct=65.0,
        reference_id="REF_SNACK_2012",
    )
    comm.property = prop
    db_session.add(comm)
    db_session.commit()

    retrieved = (
        db_session.query(Commodity).filter(Commodity.commodity_id == "COMM_TEST_CHIPS").first()
    )
    assert retrieved is not None
    assert retrieved.property is not None
    assert retrieved.property.critical_water_activity_aw == 0.40
    assert retrieved.property.evidence_source.citation_short == "Robertson 2012"


def test_physical_constraints_moisture_and_aw(db_session):
    """Verify database-level check constraints on moisture % and water activity."""
    evidence = EvidenceSource(
        reference_id="REF_BOUNDS_TEST",
        citation_short="Bounds Ref",
        title="Bounds Test Title",
        source_type="textbook",
    )
    comm = Commodity(
        commodity_id="COMM_BOUNDS",
        common_name="Bounds Item",
        category="snack_fried",
        is_respiring=False,
        default_storage_mode="ambient",
    )
    db_session.add_all([evidence, comm])
    db_session.commit()

    # Test moisture > 100%
    prop_bad_moisture = CommodityProperty(
        property_id="PROP_BAD_M",
        commodity_id="COMM_BOUNDS",
        typical_moisture_pct=105.0,  # Invalid
        critical_water_activity_aw=0.5,
        oil_fat_content_pct=10.0,
        typical_ph=6.0,
        primary_spoilage_pathways=["oxidation"],
        is_light_sensitive=False,
        recommended_temp_min_c=10.0,
        recommended_temp_max_c=20.0,
        recommended_rh_min_pct=40.0,
        recommended_rh_max_pct=60.0,
        reference_id="REF_BOUNDS_TEST",
    )
    db_session.add(prop_bad_moisture)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()

    # Test water activity > 1.0
    prop_bad_aw = CommodityProperty(
        property_id="PROP_BAD_AW",
        commodity_id="COMM_BOUNDS",
        typical_moisture_pct=10.0,
        critical_water_activity_aw=1.5,  # Invalid
        oil_fat_content_pct=10.0,
        typical_ph=6.0,
        primary_spoilage_pathways=["oxidation"],
        is_light_sensitive=False,
        recommended_temp_min_c=10.0,
        recommended_temp_max_c=20.0,
        recommended_rh_min_pct=40.0,
        recommended_rh_max_pct=60.0,
        reference_id="REF_BOUNDS_TEST",
    )
    db_session.add(prop_bad_aw)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_temperature_range_constraint(db_session):
    """Verify constraint where recommended_temp_min_c must be <= recommended_temp_max_c."""
    evidence = EvidenceSource(
        reference_id="REF_TEMP_TEST",
        citation_short="Temp Ref",
        title="Temp Test Title",
        source_type="textbook",
    )
    comm = Commodity(
        commodity_id="COMM_TEMP_TEST",
        common_name="Temp Test Item",
        category="vegetable",
        is_respiring=False,
        default_storage_mode="ambient",
    )
    db_session.add_all([evidence, comm])
    db_session.commit()

    prop_bad_temp = CommodityProperty(
        property_id="PROP_BAD_TEMP",
        commodity_id="COMM_TEMP_TEST",
        typical_moisture_pct=80.0,
        critical_water_activity_aw=0.9,
        oil_fat_content_pct=0.5,
        typical_ph=6.0,
        primary_spoilage_pathways=["mold_yeast"],
        is_light_sensitive=False,
        recommended_temp_min_c=25.0,  # Min > Max is invalid
        recommended_temp_max_c=15.0,
        recommended_rh_min_pct=40.0,
        recommended_rh_max_pct=60.0,
        reference_id="REF_TEMP_TEST",
    )
    db_session.add(prop_bad_temp)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_produce_respiration_constraints(db_session):
    """Verify respiration data relationships and check constraints."""
    evidence = EvidenceSource(
        reference_id="REF_RESP_TEST",
        citation_short="Resp Ref",
        title="Postharvest Physiology",
        source_type="textbook",
    )
    comm = Commodity(
        commodity_id="COMM_BROCCOLI_TEST",
        common_name="Broccoli Test",
        category="vegetable",
        is_respiring=True,
        default_storage_mode="chilled",
    )
    db_session.add_all([evidence, comm])
    db_session.commit()

    # Valid respiration entry
    resp = ProduceRespirationData(
        respiration_id="RESP_BROC_1",
        commodity_id="COMM_BROCCOLI_TEST",
        reference_temp_c=5.0,
        respiration_rate_co2=65.0,
        respiration_class="extremely_high",
        q10_factor=2.2,
        critical_o2_extinction_pct=1.0,
        max_tolerable_co2_pct=15.0,
        condensation_risk_level="high",
        reference_id="REF_RESP_TEST",
    )
    db_session.add(resp)
    db_session.commit()

    assert len(comm.respiration_data) == 1
    assert comm.respiration_data[0].respiration_rate_co2 == 65.0

    # Invalid negative respiration rate
    bad_resp = ProduceRespirationData(
        respiration_id="RESP_BAD",
        commodity_id="COMM_BROCCOLI_TEST",
        reference_temp_c=5.0,
        respiration_rate_co2=-10.0,  # Invalid
        respiration_class="low",
        q10_factor=2.0,
        critical_o2_extinction_pct=1.0,
        max_tolerable_co2_pct=10.0,
        condensation_risk_level="low",
        reference_id="REF_RESP_TEST",
    )
    db_session.add(bad_resp)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_map_configuration_gas_sum_constraint(db_session):
    """Verify constraint where recommended O2 max + CO2 max cannot exceed 100%."""
    evidence = EvidenceSource(
        reference_id="REF_MAP_TEST",
        citation_short="MAP Ref",
        title="MAP Technology",
        source_type="textbook",
    )
    comm = Commodity(
        commodity_id="COMM_MAP_TEST",
        common_name="MAP Commodity",
        category="vegetable",
        is_respiring=True,
        default_storage_mode="chilled",
    )
    db_session.add_all([evidence, comm])
    db_session.commit()

    # Invalid gas sum: 60% O2 + 50% CO2 = 110% > 100%
    bad_map = MAPConfiguration(
        map_id="MAP_BAD",
        commodity_id="COMM_MAP_TEST",
        recommended_o2_min_pct=10.0,
        recommended_o2_max_pct=60.0,
        recommended_co2_min_pct=20.0,
        recommended_co2_max_pct=50.0,
        target_storage_temp_c=4.0,
        suitability_status="suitable",
        reference_id="REF_MAP_TEST",
    )
    db_session.add(bad_map)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_packaging_material_cascade_and_metrics(db_session):
    """Verify PackagingMaterial relationships with Barrier, Sustainability, and Cost."""
    evidence = EvidenceSource(
        reference_id="REF_MAT_TEST",
        citation_short="Mat Ref",
        title="Packaging Science",
        source_type="textbook",
    )
    db_session.add(evidence)
    db_session.commit()

    mat = PackagingMaterial(
        material_id="MAT_TEST_LDPE",
        name="Test Low-Density Polyethylene",
        trade_code="LDPE-TEST",
        material_family="LDPE",
        structure_type="monolayer",
        density_g_cm3=0.92,
        is_biodegradable=False,
        recyclability_category="mono_material_recyclable",
        food_contact_compliant=True,
        sealability_rating="excellent",
        reference_id="REF_MAT_TEST",
    )

    barrier = PackagingBarrierProperty(
        barrier_id="BAR_TEST_LDPE",
        nominal_thickness_um=25.0,
        nominal_thickness_mil=0.984,
        otr_value=7000.0,
        wvtr_value=16.0,
        tensile_strength_md_mpa=22.0,
        elongation_at_break_pct=350.0,
        puncture_resistance_n=15.0,
        reference_id="REF_MAT_TEST",
    )
    mat.barrier_properties.append(barrier)

    mat.sustainability_metric = SustainabilityMetric(
        sustainability_id="SUST_TEST_LDPE",
        carbon_footprint_kgco2e_per_kg=2.0,
        circularity_tier="high_circularity",
        is_mono_material=True,
        reference_id="REF_MAT_TEST",
    )

    mat.cost_index = CostIndex(
        cost_id="COST_TEST_LDPE",
        relative_cost_multiplier=1.0,
        conversion_complexity="low",
        reference_id="REF_MAT_TEST",
    )

    db_session.add(mat)
    db_session.commit()

    # Query material and verify joined entities
    queried = (
        db_session.query(PackagingMaterial)
        .filter(PackagingMaterial.material_id == "MAT_TEST_LDPE")
        .first()
    )
    assert queried is not None
    assert len(queried.barrier_properties) == 1
    assert queried.barrier_properties[0].otr_value == 7000.0
    assert queried.sustainability_metric.circularity_tier == "high_circularity"
    assert queried.cost_index.relative_cost_multiplier == 1.0

    # Verify cascading delete
    db_session.delete(queried)
    db_session.commit()

    assert (
        db_session.query(PackagingBarrierProperty)
        .filter(PackagingBarrierProperty.barrier_id == "BAR_TEST_LDPE")
        .first()
        is None
    )
    assert (
        db_session.query(SustainabilityMetric)
        .filter(SustainabilityMetric.sustainability_id == "SUST_TEST_LDPE")
        .first()
        is None
    )
    assert db_session.query(CostIndex).filter(CostIndex.cost_id == "COST_TEST_LDPE").first() is None
