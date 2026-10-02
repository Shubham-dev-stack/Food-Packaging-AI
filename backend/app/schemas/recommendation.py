"""Pydantic schemas for recommendation requests, responses, and calculations."""

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field, model_validator

from backend.app.domain.types import (
    CandidateEligibility,
    OptimizationPreference,
    RecommendationStatus,
    StorageType,
    TransitStress,
)


class RankingWeightsRequest(BaseModel):
    """User-specified weighting for multi-attribute utility ranking."""

    w_barrier: float = Field(default=0.50, ge=0.0, le=1.0, description="Barrier margin weight")
    w_sustainability: float = Field(
        default=0.30, ge=0.0, le=1.0, description="Circularity and sustainability weight"
    )
    w_cost: float = Field(default=0.20, ge=0.0, le=1.0, description="Cost index weight")

    @model_validator(mode="after")
    def validate_sum(self) -> "RankingWeightsRequest":
        total = self.w_barrier + self.w_sustainability + self.w_cost
        if not (0.999 <= total <= 1.001):
            raise ValueError(f"Ranking weights must sum to 1.0 (got {total:.4f})")
        return self


class RankingWeightsResponse(BaseModel):
    """Weighting factors applied during multi-attribute utility ranking [PROTOTYPE ASSUMPTION]."""

    w_barrier: float = Field(..., description="Weight allocated to barrier margin (0.0 to 1.0)")
    w_sustainability: float = Field(
        ..., description="Weight allocated to circularity/sustainability (0.0 to 1.0)"
    )
    w_cost: float = Field(..., description="Weight allocated to economic cost index (0.0 to 1.0)")


class RecommendationCreateRequest(BaseModel):
    """Input payload representing commodity and storage context for packaging evaluation."""

    commodity_id: str = Field(..., description="Target commodity identifier from knowledge base")
    desired_shelf_life_days: int = Field(
        ...,
        ge=1,
        le=730,
        description="Target distribution shelf life (1 to 730 days) [INPUT SANITY BOUND]",
    )
    storage_temp_c: float = Field(
        ...,
        ge=-25.0,
        le=50.0,
        description="Target storage temperature in °C (-25°C to 50°C) [INPUT SANITY BOUND]",
    )
    storage_rh_pct: float = Field(
        ...,
        ge=10.0,
        le=100.0,
        description="Ambient relative humidity percentage (10% to 100%) [INPUT SANITY BOUND]",
    )
    storage_type: StorageType = Field(
        default=StorageType.AMBIENT,
        description="Storage regime classification ('ambient', 'chilled', 'frozen')",
    )
    transit_stress: TransitStress = Field(
        default=TransitStress.LOCAL_STANDARD,
        description="Transit mechanical stress profile ('local_standard', etc.)",
    )
    user_sustainability_preference: bool = Field(
        default=False,
        description="Whether to prioritize circularity/compostability over cost",
    )
    optimization_preference: OptimizationPreference = Field(
        default=OptimizationPreference.BALANCED,
        description="Preference preset ('balanced', 'sustainability', 'cost')",
    )

    # Optional property overrides
    moisture_pct: float | None = Field(
        default=None,
        ge=0.0,
        le=100.0,
        description="Optional override for commodity moisture content percentage (0% to 100%)",
    )
    water_activity_aw: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Optional override for commodity water activity (0.0 to 1.0)",
    )
    oil_fat_content_pct: float | None = Field(
        default=None,
        ge=0.0,
        le=100.0,
        description="Optional override for commodity lipid/fat percentage (0% to 100%)",
    )
    ph: float | None = Field(
        default=None,
        ge=0.0,
        le=14.0,
        description="Optional override for commodity pH (0.0 to 14.0)",
    )
    respiration_rate_co2: float | None = Field(
        default=None,
        ge=0.0,
        description="Optional override for respiration rate in mg CO2/(kg*h)",
    )

    # Geometry & packaging assumptions [PROTOTYPE ASSUMPTION]
    package_weight_kg: float = Field(
        default=0.10,
        gt=0.0,
        le=50.0,
        description="Nominal product weight per package (kg) [PROTOTYPE ASSUMPTION]",
    )
    package_area_m2: float = Field(
        default=0.06,
        gt=0.0,
        le=5.0,
        description="Total package film surface area in m2 [PROTOTYPE ASSUMPTION]",
    )

    # Optional custom ranking weights
    custom_weights: RankingWeightsRequest | None = Field(
        default=None,
        description="Optional custom weights for ranking; defaults to 50/30/20 baseline",
    )

    @model_validator(mode="after")
    def validate_storage_consistency(self) -> "RecommendationCreateRequest":
        """Verify consistency between storage type and temperature [PHYSICAL SANITY]."""
        if self.storage_type == StorageType.FROZEN and self.storage_temp_c > 0.0:
            msg = (
                f"Storage type 'frozen' is physically inconsistent with "
                f"temperature {self.storage_temp_c}°C (must be <= 0.0°C)"
            )
            raise ValueError(msg)
        if self.storage_type == StorageType.CHILLED and (
            self.storage_temp_c < -2.0 or self.storage_temp_c > 15.0
        ):
            msg = (
                f"Storage type 'chilled' is inconsistent with "
                f"temperature {self.storage_temp_c}°C (expected -2.0°C to 15.0°C)"
            )
            raise ValueError(msg)
        if self.storage_type == StorageType.AMBIENT and self.storage_temp_c < 5.0:
            msg = (
                f"Storage type 'ambient' is inconsistent with sub-refrigeration "
                f"temperature {self.storage_temp_c}°C (expected >= 5.0°C)"
            )
            raise ValueError(msg)
        return self


class TargetSpecificationsResponse(BaseModel):
    """Estimated target engineering specification ranges in standard ASTM units."""

    max_recommended_wvtr: float = Field(
        ...,
        description="Max allowable WVTR in g/(m2*day) under ASTM F1249 [PROTOTYPE TARGET]",
    )
    max_recommended_otr: float = Field(
        ...,
        description="Max allowable OTR in cm3/(m2*day*atm) under ASTM D3985 [PROTOTYPE TARGET]",
    )
    recommended_thickness_um: float = Field(
        ...,
        description="Recommended nominal thickness in micrometers [PROTOTYPE ASSUMPTION]",
    )

    sealability_required: str = Field(
        ..., description="Required sealability rating (e.g. 'excellent', 'good')"
    )
    is_light_barrier_required: bool = Field(..., description="Whether commodity is photosensitive")
    is_microperforation_required: bool = Field(
        ..., description="Whether microperforation is required for respiration"
    )
    target_wvtr_rationale: str = Field(
        ..., description="Analytical derivation context for moisture barrier"
    )
    target_otr_rationale: str = Field(..., description="Evidence context for oxygen barrier cutoff")
    thickness_rationale: str = Field(..., description="Mechanical transit stress justification")
    adjusted_respiration_rate_co2: float | None = Field(
        default=None,
        description="Respiration rate at storage temperature in mg CO2/(kg*h)",
    )


class CandidateEvaluationResponse(BaseModel):
    """Detailed evaluation result for a candidate packaging material."""

    material_id: str
    trade_code: str
    material_name: str
    material_family: str
    structure_type: str
    eligibility: CandidateEligibility
    rejection_reasons: list[str] = Field(default_factory=list)
    condition_notes: list[str] = Field(default_factory=list)

    # Scored metrics
    barrier_safety_score: float = 0.0
    sustainability_score: float = 0.0
    cost_score: float = 0.0
    composite_utility_score: float = 0.0

    # Score breakdown contributions [PROTOTYPE WEIGHTS]
    barrier_contribution: float = 0.0
    sustainability_contribution: float = 0.0
    cost_contribution: float = 0.0
    rank: int = 0

    # Snapshot of physical attributes
    nominal_thickness_um: float = 0.0
    nominal_otr: float = 0.0
    nominal_wvtr: float = 0.0
    is_mono_material: bool = False
    is_biodegradable: bool = False
    relative_cost_multiplier: float = 1.0
    evidence_reference_id: str = ""


class ExplanationResponse(BaseModel):
    """Structured, explainable decision trace synthesized for user inspection."""

    dominant_spoilage_driver: str
    critical_factors: list[str] = Field(default_factory=list)
    selection_rationale: str = ""
    alternative_rationale: str = ""
    disqualification_summary: list[dict[str, Any]] = Field(default_factory=list)
    cited_evidence_sources: list[str] = Field(default_factory=list)
    documented_assumptions: list[str] = Field(default_factory=list)
    scientific_limitations: list[str] = Field(default_factory=list)


class RecommendationResponse(BaseModel):
    """Complete, self-contained response payload returned for a recommendation session."""

    request_id: str = Field(..., description="Unique audit session identifier")
    status: RecommendationStatus = Field(..., description="Overall decision status")
    commodity_id: str = Field(..., description="Target commodity identifier")
    commodity_name: str = Field(..., description="Target commodity common name")
    primary_recommendation: CandidateEvaluationResponse | None = None
    alternative_recommendation: CandidateEvaluationResponse | None = None
    ranked_candidates: list[CandidateEvaluationResponse] = Field(default_factory=list)
    disqualified_candidates: list[CandidateEvaluationResponse] = Field(default_factory=list)
    target_specifications: TargetSpecificationsResponse | None = None
    explanation: ExplanationResponse | None = None
    safety_advisory: str | None = None
    uncertainty_notes: list[str] = Field(default_factory=list)
    applied_weights: RankingWeightsResponse | None = Field(
        default=None, description="Prototype weighting factors applied during candidate ranking"
    )
    optimization_preference: OptimizationPreference = Field(
        default=OptimizationPreference.BALANCED,
        description="Active multi-criteria optimization preference preset",
    )
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
