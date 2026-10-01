"""Database seeding and knowledge-base ingestion engine.

Reads validated JSON fixtures from data/processed/ and populates the relational database
with complete foreign-key integrity and citations traceability.
"""

import json
from pathlib import Path

from sqlalchemy.orm import Session

from backend.app.core.db import SessionLocal, init_db
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


def get_default_fixtures_dir() -> Path:
    """Resolve the default data/processed directory from repository structure."""
    return Path(__file__).resolve().parent.parent / "processed"


def seed_evidence_sources(db: Session, fixtures_dir: Path) -> int:
    """Ingest evidence sources from JSON fixture."""
    file_path = fixtures_dir / "evidence_sources.json"
    if not file_path.exists():
        raise FileNotFoundError(f"Fixture not found: {file_path}")

    with open(file_path, encoding="utf-8") as f:
        data = json.load(f)

    count = 0
    for item in data:
        existing = (
            db.query(EvidenceSource)
            .filter(EvidenceSource.reference_id == item["reference_id"])
            .first()
        )
        if not existing:
            source = EvidenceSource(
                reference_id=item["reference_id"],
                citation_short=item["citation_short"],
                title=item["title"],
                authors=item.get("authors"),
                publication_year=item.get("publication_year"),
                source_type=item["source_type"],
                doi_or_standard_number=item.get("doi_or_standard_number"),
                notes=item.get("notes"),
            )
            db.add(source)
            count += 1
    db.commit()
    return count


def seed_packaging_materials(db: Session, fixtures_dir: Path) -> int:
    """Ingest packaging materials, barrier properties, sustainability, and cost data."""
    file_path = fixtures_dir / "packaging_materials.json"
    if not file_path.exists():
        raise FileNotFoundError(f"Fixture not found: {file_path}")

    with open(file_path, encoding="utf-8") as f:
        data = json.load(f)

    count = 0
    for item in data:
        existing = (
            db.query(PackagingMaterial)
            .filter(PackagingMaterial.material_id == item["material_id"])
            .first()
        )
        if not existing:
            mat = PackagingMaterial(
                material_id=item["material_id"],
                name=item["name"],
                trade_code=item["trade_code"],
                material_family=item["material_family"],
                structure_type=item["structure_type"],
                density_g_cm3=item["density_g_cm3"],
                is_biodegradable=item["is_biodegradable"],
                recyclability_category=item["recyclability_category"],
                food_contact_compliant=item["food_contact_compliant"],
                sealability_rating=item["sealability_rating"],
                seal_initiation_temp_c=item.get("seal_initiation_temp_c"),
                reference_id=item["reference_id"],
            )

            # Ingest associated barrier properties
            for bp in item.get("barrier_properties", []):
                mat.barrier_properties.append(
                    PackagingBarrierProperty(
                        barrier_id=bp["barrier_id"],
                        nominal_thickness_um=bp["nominal_thickness_um"],
                        nominal_thickness_mil=bp.get("nominal_thickness_mil"),
                        otr_value=bp["otr_value"],
                        otr_test_temp_c=bp.get("otr_test_temp_c", 23.0),
                        otr_test_rh_pct=bp.get("otr_test_rh_pct", 0.0),
                        wvtr_value=bp["wvtr_value"],
                        wvtr_test_temp_c=bp.get("wvtr_test_temp_c", 37.8),
                        wvtr_test_rh_pct=bp.get("wvtr_test_rh_pct", 90.0),
                        co2_tr_value=bp.get("co2_tr_value"),
                        tensile_strength_md_mpa=bp["tensile_strength_md_mpa"],
                        elongation_at_break_pct=bp["elongation_at_break_pct"],
                        puncture_resistance_n=bp["puncture_resistance_n"],
                        is_breathable=bp.get("is_breathable", False),
                        is_microperforated=bp.get("is_microperforated", False),
                        microperforation_density_per_m2=bp.get(
                            "microperforation_density_per_m2"
                        ),
                        test_standard_otr=bp.get("test_standard_otr", "ASTM D3985"),
                        test_standard_wvtr=bp.get("test_standard_wvtr", "ASTM F1249"),
                        reference_id=bp["reference_id"],
                    )
                )

            # Ingest sustainability metric
            if "sustainability_metric" in item:
                sm = item["sustainability_metric"]
                mat.sustainability_metric = SustainabilityMetric(
                    sustainability_id=sm["sustainability_id"],
                    carbon_footprint_kgco2e_per_kg=sm["carbon_footprint_kgco2e_per_kg"],
                    circularity_tier=sm["circularity_tier"],
                    is_mono_material=sm["is_mono_material"],
                    epr_category_india=sm.get("epr_category_india"),
                    reference_id=sm["reference_id"],
                )

            # Ingest cost index
            if "cost_index" in item:
                ci = item["cost_index"]
                mat.cost_index = CostIndex(
                    cost_id=ci["cost_id"],
                    relative_cost_multiplier=ci["relative_cost_multiplier"],
                    conversion_complexity=ci["conversion_complexity"],
                    reference_id=ci["reference_id"],
                )

            db.add(mat)
            count += 1
    db.commit()
    return count


def seed_commodities(db: Session, fixtures_dir: Path) -> int:
    """Ingest commodities, physicochemical properties, respiration data, and MAP."""
    file_path = fixtures_dir / "commodities.json"
    if not file_path.exists():
        raise FileNotFoundError(f"Fixture not found: {file_path}")

    with open(file_path, encoding="utf-8") as f:
        data = json.load(f)

    count = 0
    for item in data:
        existing = (
            db.query(Commodity)
            .filter(Commodity.commodity_id == item["commodity_id"])
            .first()
        )
        if not existing:
            comm = Commodity(
                commodity_id=item["commodity_id"],
                common_name=item["common_name"],
                scientific_name=item.get("scientific_name"),
                category=item["category"],
                is_respiring=item["is_respiring"],
                default_storage_mode=item["default_storage_mode"],
                description=item.get("description"),
            )

            # Ingest property
            if "property" in item:
                prop = item["property"]
                comm.property = CommodityProperty(
                    property_id=prop["property_id"],
                    typical_moisture_pct=prop["typical_moisture_pct"],
                    critical_water_activity_aw=prop["critical_water_activity_aw"],
                    oil_fat_content_pct=prop["oil_fat_content_pct"],
                    typical_ph=prop["typical_ph"],
                    primary_spoilage_pathways=prop["primary_spoilage_pathways"],
                    is_light_sensitive=prop["is_light_sensitive"],
                    recommended_temp_min_c=prop["recommended_temp_min_c"],
                    recommended_temp_max_c=prop["recommended_temp_max_c"],
                    recommended_rh_min_pct=prop["recommended_rh_min_pct"],
                    recommended_rh_max_pct=prop["recommended_rh_max_pct"],
                    reference_id=prop["reference_id"],
                )

            # Ingest respiration data
            for resp in item.get("respiration_data", []):
                comm.respiration_data.append(
                    ProduceRespirationData(
                        respiration_id=resp["respiration_id"],
                        reference_temp_c=resp["reference_temp_c"],
                        respiration_rate_co2=resp["respiration_rate_co2"],
                        respiration_class=resp["respiration_class"],
                        q10_factor=resp.get("q10_factor", 2.0),
                        critical_o2_extinction_pct=resp["critical_o2_extinction_pct"],
                        max_tolerable_co2_pct=resp["max_tolerable_co2_pct"],
                        condensation_risk_level=resp["condensation_risk_level"],
                        reference_id=resp["reference_id"],
                    )
                )

            # Ingest MAP configuration
            if "map_configuration" in item:
                map_conf = item["map_configuration"]
                comm.map_configuration = MAPConfiguration(
                    map_id=map_conf["map_id"],
                    recommended_o2_min_pct=map_conf["recommended_o2_min_pct"],
                    recommended_o2_max_pct=map_conf["recommended_o2_max_pct"],
                    recommended_co2_min_pct=map_conf["recommended_co2_min_pct"],
                    recommended_co2_max_pct=map_conf["recommended_co2_max_pct"],
                    recommended_n2_pct=map_conf.get("recommended_n2_pct"),
                    target_storage_temp_c=map_conf["target_storage_temp_c"],
                    suitability_status=map_conf["suitability_status"],
                    application_notes=map_conf.get("application_notes"),
                    reference_id=map_conf["reference_id"],
                )

            db.add(comm)
            count += 1
    db.commit()
    return count


def seed_database(db: Session, fixtures_dir: Path | None = None) -> dict[str, int]:
    """Execute complete initial knowledge base ingestion in proper dependency order."""
    target_dir = fixtures_dir or get_default_fixtures_dir()
    ev_count = seed_evidence_sources(db, target_dir)
    mat_count = seed_packaging_materials(db, target_dir)
    comm_count = seed_commodities(db, target_dir)
    return {
        "evidence_sources": ev_count,
        "packaging_materials": mat_count,
        "commodities": comm_count,
    }


if __name__ == "__main__":
    print("Initializing database tables...")
    init_db()
    print("Seeding curated knowledge base...")
    session = SessionLocal()
    try:
        results = seed_database(session)
        print(f"Database seeded successfully: {results}")
    finally:
        session.close()
