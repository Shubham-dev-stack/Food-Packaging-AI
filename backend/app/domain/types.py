"""Domain data types, enums, and structured payloads for the recommendation engine."""

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class RecommendationStatus(StrEnum):
    """Overall status of the recommendation evaluation."""

    SUPPORTED = "SUPPORTED"
    CONDITIONAL = "CONDITIONAL"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"
    RESEARCH_REQUIRED = "RESEARCH_REQUIRED"


class CandidateEligibility(StrEnum):
    """Eligibility status of an individual packaging candidate material."""

    ELIGIBLE = "ELIGIBLE"
    CONDITIONALLY_ELIGIBLE = "CONDITIONALLY_ELIGIBLE"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"
    REJECTED = "REJECTED"


class StorageType(StrEnum):
    """Storage regime classification."""

    AMBIENT = "ambient"
    CHILLED = "chilled"
    FROZEN = "frozen"


class TransitStress(StrEnum):
    """Transportation mechanical stress profile."""

    LOCAL_STANDARD = "local_standard"
    LONG_HAUL_REFRIGERATED = "long_haul_refrigerated"
    ROUGH_TERRAIN_UNPAVED = "rough_terrain_unpaved"


@dataclass(frozen=True)
class RecommendationInput:
    """Validated domain input payload representing commodity and storage context."""

    commodity_id: str
    desired_shelf_life_days: int
    storage_temp_c: float
    storage_rh_pct: float
    storage_type: StorageType = StorageType.AMBIENT
    transit_stress: TransitStress = TransitStress.LOCAL_STANDARD
    user_sustainability_preference: bool = False

    # Optional commodity property overrides (if None, reference baseline is used)
    moisture_pct: float | None = None
    water_activity_aw: float | None = None
    oil_fat_content_pct: float | None = None
    ph: float | None = None
    respiration_rate_co2: float | None = None  # mg CO2 / (kg * h)

    # Geometry & packaging assumptions [PROTOTYPE ASSUMPTION]
    package_weight_kg: float = 0.10  # 100g nominal pouch
    package_area_m2: float = 0.06  # 0.06 m2 surface area


@dataclass(frozen=True)
class TargetSpecifications:
    """Estimated target engineering specification ranges in standard ASTM units."""

    max_recommended_wvtr: float  # g / (m2 * day) under ASTM F1249 (37.8C, 90% RH)
    max_recommended_otr: float  # cm3 / (m2 * day * atm) under ASTM D3985 (23C, 0% RH)
    recommended_thickness_um: float  # micrometers
    sealability_required: str  # e.g., 'excellent', 'good'
    is_light_barrier_required: bool  # True if food is light/photo-oxidation sensitive
    is_microperforation_required: bool  # True for high-respiration produce
    target_wvtr_rationale: str
    target_otr_rationale: str
    thickness_rationale: str


@dataclass
class CandidateEvaluation:
    """Detailed evaluation result for a candidate packaging material."""

    material_id: str
    trade_code: str
    material_name: str
    material_family: str
    structure_type: str
    eligibility: CandidateEligibility
    rejection_reasons: list[str] = field(default_factory=list)
    condition_notes: list[str] = field(default_factory=list)

    # Scored metrics
    barrier_safety_score: float = 0.0
    sustainability_score: float = 0.0
    cost_score: float = 0.0
    composite_utility_score: float = 0.0

    # Material attributes snapshot
    nominal_thickness_um: float = 0.0
    nominal_otr: float = 0.0
    nominal_wvtr: float = 0.0
    is_mono_material: bool = False
    is_biodegradable: bool = False
    relative_cost_multiplier: float = 1.0
    evidence_reference_id: str = ""


@dataclass
class ExplanationData:
    """Structured, explainable decision trace synthesized for user inspection."""

    dominant_spoilage_driver: str
    critical_factors: list[str] = field(default_factory=list)
    selection_rationale: str = ""
    alternative_rationale: str = ""
    disqualification_summary: list[dict[str, Any]] = field(default_factory=list)
    cited_evidence_sources: list[str] = field(default_factory=list)
    documented_assumptions: list[str] = field(default_factory=list)
    scientific_limitations: list[str] = field(default_factory=list)


@dataclass
class RecommendationResultDomain:
    """Complete, self-contained result payload produced by the recommendation engine."""

    status: RecommendationStatus
    commodity_id: str
    commodity_name: str
    primary_recommendation: CandidateEvaluation | None
    alternative_recommendation: CandidateEvaluation | None
    ranked_candidates: list[CandidateEvaluation] = field(default_factory=list)
    disqualified_candidates: list[CandidateEvaluation] = field(default_factory=list)
    target_specifications: TargetSpecifications | None = None
    explanation: ExplanationData | None = None
    safety_advisory: str | None = None
    uncertainty_notes: list[str] = field(default_factory=list)
