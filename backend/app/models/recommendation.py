"""Audit and persistence ORM models for recommendation requests and results."""

from datetime import UTC, datetime
from typing import Any

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.core.db import Base
from backend.app.models.commodity import Commodity, MAPConfiguration
from backend.app.models.material import PackagingMaterial


class RecommendationRequest(Base):
    """Encapsulates evaluated user input payload for a recommendation session."""

    __tablename__ = "recommendation_requests"

    request_id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    commodity_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("commodities.commodity_id"),
        nullable=False,
    )
    input_moisture_pct: Mapped[float] = mapped_column(Float, nullable=False)
    input_fat_pct: Mapped[float] = mapped_column(Float, nullable=False)
    input_ph: Mapped[float] = mapped_column(Float, nullable=False)
    input_respiration_rate: Mapped[float | None] = mapped_column(Float, nullable=True)
    desired_shelf_life_days: Mapped[int] = mapped_column(Integer, nullable=False)
    storage_temp_c: Mapped[float] = mapped_column(Float, nullable=False)
    storage_rh_pct: Mapped[float] = mapped_column(Float, nullable=False)
    transit_stress_profile: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        # 'local_standard', 'long_haul_refrigerated', 'rough_terrain_unpaved'
    )
    storage_type: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        # 'ambient', 'chilled', 'frozen'
    )
    user_sustainability_preference: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )

    # Relationships
    commodity: Mapped["Commodity"] = relationship("Commodity")
    result: Mapped["RecommendationResult | None"] = relationship(
        "RecommendationResult",
        back_populates="request",
        uselist=False,
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<RecommendationRequest(id='{self.request_id}', commodity='{self.commodity_id}')>"


class RecommendationResult(Base):
    """Structured recommendation payload logged for auditability and verification."""

    __tablename__ = "recommendation_results"

    result_id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    request_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("recommendation_requests.request_id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    primary_material_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("packaging_materials.material_id"),
        nullable=False,
    )
    alternative_material_id: Mapped[str | None] = mapped_column(
        String(64),
        ForeignKey("packaging_materials.material_id"),
        nullable=True,
    )
    required_otr_target: Mapped[float] = mapped_column(Float, nullable=False)
    required_wvtr_target: Mapped[float] = mapped_column(Float, nullable=False)
    recommended_thickness_um: Mapped[float] = mapped_column(Float, nullable=False)
    recommended_sealability: Mapped[str] = mapped_column(String(64), nullable=False)
    recommended_mechanical_notes: Mapped[str] = mapped_column(Text, nullable=False)
    map_configuration_id: Mapped[str | None] = mapped_column(
        String(64),
        ForeignKey("map_configurations.map_id"),
        nullable=True,
    )
    state_status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        # 'supported', 'conditional', 'insufficient_evidence', 'research_required'
    )
    explanation_summary: Mapped[str] = mapped_column(Text, nullable=False)
    disqualified_materials_log: Mapped[list[dict[str, Any]] | Any] = mapped_column(
        JSON, nullable=False
    )
    safety_advisory: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )

    # Relationships
    request: Mapped["RecommendationRequest"] = relationship(
        "RecommendationRequest", back_populates="result"
    )
    primary_material: Mapped["PackagingMaterial"] = relationship(
        "PackagingMaterial", foreign_keys=[primary_material_id]
    )
    alternative_material: Mapped["PackagingMaterial | None"] = relationship(
        "PackagingMaterial", foreign_keys=[alternative_material_id]
    )
    map_configuration: Mapped["MAPConfiguration | None"] = relationship("MAPConfiguration")

    def __repr__(self) -> str:
        return f"<RecommendationResult(id='{self.result_id}', status='{self.state_status}')>"
