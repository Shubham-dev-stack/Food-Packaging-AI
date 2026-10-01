"""Packaging material, barrier property, sustainability, and cost index ORM models."""

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.core.db import Base
from backend.app.models.evidence import EvidenceSource


class PackagingMaterial(Base):
    """Catalog of polymeric films, laminates, and barrier structures."""

    __tablename__ = "packaging_materials"
    __table_args__ = (
        CheckConstraint(
            "density_g_cm3 >= 0.5 AND density_g_cm3 <= 3.0",
            name="chk_material_density",
        ),
    )

    material_id: Mapped[str] = mapped_column(String(64), primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    trade_code: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    material_family: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        index=True,
        # 'LDPE', 'HDPE', 'PET', 'metallized_film', 'aluminum_foil_laminate',
        # 'biodegradable_film', 'breathable_film', 'polyolefin_monomaterial'
    )
    structure_type: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        # 'monolayer', 'coextrusion', 'multi_layer_laminate',
        # 'perforated_film', 'microporous_membrane'
    )
    density_g_cm3: Mapped[float] = mapped_column(Float, nullable=False)
    is_biodegradable: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    recyclability_category: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        # 'mono_material_recyclable', 'specialized_recycling',
        # 'industrial_compostable', 'non_recyclable_landfill'
    )
    food_contact_compliant: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    sealability_rating: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        # 'excellent', 'good', 'moderate', 'poor', 'non_sealable'
    )
    seal_initiation_temp_c: Mapped[float | None] = mapped_column(Float, nullable=True)
    reference_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("evidence_sources.reference_id"),
        nullable=False,
    )

    # Relationships
    barrier_properties: Mapped[list["PackagingBarrierProperty"]] = relationship(
        "PackagingBarrierProperty",
        back_populates="material",
        cascade="all, delete-orphan",
    )
    sustainability_metric: Mapped["SustainabilityMetric | None"] = relationship(
        "SustainabilityMetric",
        back_populates="material",
        uselist=False,
        cascade="all, delete-orphan",
    )
    cost_index: Mapped["CostIndex | None"] = relationship(
        "CostIndex",
        back_populates="material",
        uselist=False,
        cascade="all, delete-orphan",
    )
    evidence_source: Mapped["EvidenceSource"] = relationship("EvidenceSource")

    def __repr__(self) -> str:
        return f"<PackagingMaterial(id='{self.material_id}', code='{self.trade_code}')>"


class PackagingBarrierProperty(Base):
    """Standardized barrier and mechanical specifications measured under ASTM/ISO standards."""

    __tablename__ = "packaging_barrier_properties"
    __table_args__ = (
        CheckConstraint("nominal_thickness_um > 0.0", name="chk_thickness_positive"),
        CheckConstraint("otr_value >= 0.0", name="chk_otr_non_negative"),
        CheckConstraint("wvtr_value >= 0.0", name="chk_wvtr_non_negative"),
        CheckConstraint("tensile_strength_md_mpa >= 0.0", name="chk_tensile_non_negative"),
        CheckConstraint("elongation_at_break_pct >= 0.0", name="chk_elongation_non_negative"),
        CheckConstraint("puncture_resistance_n >= 0.0", name="chk_puncture_non_negative"),
    )

    barrier_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    material_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("packaging_materials.material_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    nominal_thickness_um: Mapped[float] = mapped_column(Float, nullable=False)
    nominal_thickness_mil: Mapped[float | None] = mapped_column(Float, nullable=True)
    otr_value: Mapped[float] = mapped_column(Float, nullable=False)  # cm3/(m2*day*atm)
    otr_test_temp_c: Mapped[float] = mapped_column(Float, nullable=False, default=23.0)
    otr_test_rh_pct: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    wvtr_value: Mapped[float] = mapped_column(Float, nullable=False)  # g/(m2*day)
    wvtr_test_temp_c: Mapped[float] = mapped_column(Float, nullable=False, default=37.8)
    wvtr_test_rh_pct: Mapped[float] = mapped_column(Float, nullable=False, default=90.0)
    co2_tr_value: Mapped[float | None] = mapped_column(Float, nullable=True)
    tensile_strength_md_mpa: Mapped[float] = mapped_column(Float, nullable=False)
    elongation_at_break_pct: Mapped[float] = mapped_column(Float, nullable=False)
    puncture_resistance_n: Mapped[float] = mapped_column(Float, nullable=False)
    is_breathable: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_microperforated: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    microperforation_density_per_m2: Mapped[int | None] = mapped_column(Integer, nullable=True)
    test_standard_otr: Mapped[str] = mapped_column(String(64), nullable=False, default="ASTM D3985")
    test_standard_wvtr: Mapped[str] = mapped_column(
        String(64), nullable=False, default="ASTM F1249"
    )
    reference_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("evidence_sources.reference_id"),
        nullable=False,
    )

    # Relationships
    material: Mapped["PackagingMaterial"] = relationship(
        "PackagingMaterial", back_populates="barrier_properties"
    )
    evidence_source: Mapped["EvidenceSource"] = relationship("EvidenceSource")

    def __repr__(self) -> str:
        return (
            f"<PackagingBarrierProperty(material='{self.material_id}', "
            f"gauge='{self.nominal_thickness_um}um', otr={self.otr_value}, wvtr={self.wvtr_value})>"
        )


class SustainabilityMetric(Base):
    """Environmental impact and circular economy classification for packaging materials."""

    __tablename__ = "sustainability_metrics"
    __table_args__ = (
        CheckConstraint("carbon_footprint_kgco2e_per_kg >= 0.0", name="chk_carbon_positive"),
    )

    sustainability_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    material_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("packaging_materials.material_id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )
    carbon_footprint_kgco2e_per_kg: Mapped[float] = mapped_column(Float, nullable=False)
    circularity_tier: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        # 'high_circularity', 'medium_circularity', 'low_circularity', 'linear_landfill'
    )
    is_mono_material: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    epr_category_india: Mapped[str | None] = mapped_column(String(64), nullable=True)
    reference_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("evidence_sources.reference_id"),
        nullable=False,
    )

    # Relationships
    material: Mapped["PackagingMaterial"] = relationship(
        "PackagingMaterial", back_populates="sustainability_metric"
    )
    evidence_source: Mapped["EvidenceSource"] = relationship("EvidenceSource")

    def __repr__(self) -> str:
        return f"<SustainabilityMetric(mat='{self.material_id}', tier='{self.circularity_tier}')>"


class CostIndex(Base):
    """Relative economic cost multiplier normalized to baseline LDPE film (= 1.0)."""

    __tablename__ = "cost_indices"
    __table_args__ = (
        CheckConstraint("relative_cost_multiplier >= 1.0", name="chk_cost_multiplier_min"),
    )

    cost_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    material_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("packaging_materials.material_id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )
    relative_cost_multiplier: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    conversion_complexity: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        # 'low', 'medium', 'high', 'specialized'
    )
    reference_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("evidence_sources.reference_id"),
        nullable=False,
    )

    # Relationships
    material: Mapped["PackagingMaterial"] = relationship(
        "PackagingMaterial", back_populates="cost_index"
    )
    evidence_source: Mapped["EvidenceSource"] = relationship("EvidenceSource")

    def __repr__(self) -> str:
        return f"<CostIndex(material='{self.material_id}', mult={self.relative_cost_multiplier})>"
