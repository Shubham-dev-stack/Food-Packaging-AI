"""Commodity and produce physiological ORM models."""

from typing import Any

from sqlalchemy import (
    JSON,
    Boolean,
    CheckConstraint,
    Float,
    ForeignKey,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.core.db import Base
from backend.app.models.evidence import EvidenceSource


class Commodity(Base):
    """Core food or agricultural commodity entity."""

    __tablename__ = "commodities"

    commodity_id: Mapped[str] = mapped_column(String(64), primary_key=True, index=True)
    common_name: Mapped[str] = mapped_column(String(128), unique=True, nullable=False, index=True)
    scientific_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    category: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        index=True,
        # e.g., 'fruit', 'vegetable', 'grain_cereal', 'bakery', 'snack_fried',
        # 'dairy_powder', 'meat_poultry', 'seafood', 'spices_condiments', 'processed_food'
    )
    is_respiring: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    default_storage_mode: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="ambient",
        # 'ambient', 'chilled', 'frozen'
    )
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    property: Mapped["CommodityProperty | None"] = relationship(
        "CommodityProperty",
        back_populates="commodity",
        uselist=False,
        cascade="all, delete-orphan",
    )
    respiration_data: Mapped[list["ProduceRespirationData"]] = relationship(
        "ProduceRespirationData",
        back_populates="commodity",
        cascade="all, delete-orphan",
    )
    map_configuration: Mapped["MAPConfiguration | None"] = relationship(
        "MAPConfiguration",
        back_populates="commodity",
        uselist=False,
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Commodity(id='{self.commodity_id}', name='{self.common_name}')>"


class CommodityProperty(Base):
    """Physicochemical degradation characteristics of a food commodity."""

    __tablename__ = "commodity_properties"
    __table_args__ = (
        CheckConstraint(
            "typical_moisture_pct >= 0.0 AND typical_moisture_pct <= 100.0",
            name="chk_commodity_moisture_pct",
        ),
        CheckConstraint(
            "critical_water_activity_aw >= 0.0 AND critical_water_activity_aw <= 1.0",
            name="chk_commodity_critical_aw",
        ),
        CheckConstraint(
            "oil_fat_content_pct >= 0.0 AND oil_fat_content_pct <= 100.0",
            name="chk_commodity_fat_pct",
        ),
        CheckConstraint(
            "typical_ph >= 1.0 AND typical_ph <= 14.0",
            name="chk_commodity_ph",
        ),
        CheckConstraint(
            "recommended_temp_min_c <= recommended_temp_max_c",
            name="chk_commodity_temp_range",
        ),
        CheckConstraint(
            "recommended_rh_min_pct >= 0.0 AND recommended_rh_min_pct <= recommended_rh_max_pct "
            "AND recommended_rh_max_pct <= 100.0",
            name="chk_commodity_rh_range",
        ),
    )

    property_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    commodity_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("commodities.commodity_id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )
    typical_moisture_pct: Mapped[float] = mapped_column(Float, nullable=False)
    critical_water_activity_aw: Mapped[float] = mapped_column(Float, nullable=False)
    oil_fat_content_pct: Mapped[float] = mapped_column(Float, nullable=False)
    typical_ph: Mapped[float] = mapped_column(Float, nullable=False)
    primary_spoilage_pathways: Mapped[list[str] | Any] = mapped_column(JSON, nullable=False)
    is_light_sensitive: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    recommended_temp_min_c: Mapped[float] = mapped_column(Float, nullable=False)
    recommended_temp_max_c: Mapped[float] = mapped_column(Float, nullable=False)
    recommended_rh_min_pct: Mapped[float] = mapped_column(Float, nullable=False)
    recommended_rh_max_pct: Mapped[float] = mapped_column(Float, nullable=False)
    reference_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("evidence_sources.reference_id"),
        nullable=False,
    )

    # Relationships
    commodity: Mapped["Commodity"] = relationship("Commodity", back_populates="property")
    evidence_source: Mapped["EvidenceSource"] = relationship("EvidenceSource")

    def __repr__(self) -> str:
        return f"<CommodityProperty(commodity_id='{self.commodity_id}')>"


class ProduceRespirationData(Base):
    """Post-harvest respiration and physiological parameters for fresh produce."""

    __tablename__ = "produce_respiration_data"
    __table_args__ = (
        CheckConstraint("respiration_rate_co2 >= 0.0", name="chk_respiration_rate_positive"),
        CheckConstraint("q10_factor >= 1.0", name="chk_q10_factor_min"),
        CheckConstraint(
            "critical_o2_extinction_pct >= 0.0 AND critical_o2_extinction_pct <= 21.0",
            name="chk_o2_extinction_bounds",
        ),
        CheckConstraint(
            "max_tolerable_co2_pct >= 0.0 AND max_tolerable_co2_pct <= 100.0",
            name="chk_max_co2_bounds",
        ),
    )

    respiration_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    commodity_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("commodities.commodity_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    reference_temp_c: Mapped[float] = mapped_column(Float, nullable=False)
    respiration_rate_co2: Mapped[float] = mapped_column(Float, nullable=False)  # mg CO2/(kg*h)
    respiration_class: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        # 'very_low', 'low', 'moderate', 'high', 'very_high', 'extremely_high'
    )
    q10_factor: Mapped[float] = mapped_column(Float, nullable=False, default=2.0)
    critical_o2_extinction_pct: Mapped[float] = mapped_column(Float, nullable=False)
    max_tolerable_co2_pct: Mapped[float] = mapped_column(Float, nullable=False)
    condensation_risk_level: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        # 'low', 'medium', 'high'
    )
    reference_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("evidence_sources.reference_id"),
        nullable=False,
    )

    # Relationships
    commodity: Mapped["Commodity"] = relationship("Commodity", back_populates="respiration_data")
    evidence_source: Mapped["EvidenceSource"] = relationship("EvidenceSource")

    def __repr__(self) -> str:
        return (
            f"<ProduceRespirationData(id='{self.respiration_id}', "
            f"commodity='{self.commodity_id}', class='{self.respiration_class}')>"
        )


class MAPConfiguration(Base):
    """Evidence-backed Modified Atmosphere Packaging gas targets."""

    __tablename__ = "map_configurations"
    __table_args__ = (
        CheckConstraint(
            "recommended_o2_min_pct >= 0.0 AND recommended_o2_min_pct <= recommended_o2_max_pct",
            name="chk_map_o2_range",
        ),
        CheckConstraint(
            "recommended_co2_min_pct >= 0.0 AND recommended_co2_min_pct <= recommended_co2_max_pct",
            name="chk_map_co2_range",
        ),
        CheckConstraint(
            "recommended_o2_max_pct + recommended_co2_max_pct <= 100.0",
            name="chk_map_gas_sum",
        ),
    )

    map_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    commodity_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("commodities.commodity_id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )
    recommended_o2_min_pct: Mapped[float] = mapped_column(Float, nullable=False)
    recommended_o2_max_pct: Mapped[float] = mapped_column(Float, nullable=False)
    recommended_co2_min_pct: Mapped[float] = mapped_column(Float, nullable=False)
    recommended_co2_max_pct: Mapped[float] = mapped_column(Float, nullable=False)
    recommended_n2_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    target_storage_temp_c: Mapped[float] = mapped_column(Float, nullable=False)
    suitability_status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        # 'suitable', 'not_recommended', 'ventilated_only', 'conditional'
    )
    application_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    reference_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("evidence_sources.reference_id"),
        nullable=False,
    )

    # Relationships
    commodity: Mapped["Commodity"] = relationship("Commodity", back_populates="map_configuration")
    evidence_source: Mapped["EvidenceSource"] = relationship("EvidenceSource")

    def __repr__(self) -> str:
        return f"<MAPConfiguration(id='{self.map_id}', commodity='{self.commodity_id}')>"
