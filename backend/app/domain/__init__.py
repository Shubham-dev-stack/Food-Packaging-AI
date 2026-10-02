"""Food preservation physics, respiration kinetics, and recommendation engine domain package."""

from backend.app.domain.engine import RecommendationEngine
from backend.app.domain.types import (
    SUSTAINABILITY_PRIORITY_WEIGHTS,
    CandidateEligibility,
    CandidateEvaluation,
    ExplanationData,
    RankingWeightsConfig,
    RecommendationInput,
    RecommendationResultDomain,
    RecommendationStatus,
    StorageType,
    TargetSpecifications,
    TransitGaugeConfig,
    TransitStress,
)

__all__ = [
    "RecommendationEngine",
    "RecommendationInput",
    "RecommendationResultDomain",
    "RecommendationStatus",
    "CandidateEligibility",
    "CandidateEvaluation",
    "TargetSpecifications",
    "ExplanationData",
    "StorageType",
    "TransitStress",
    "RankingWeightsConfig",
    "TransitGaugeConfig",
    "SUSTAINABILITY_PRIORITY_WEIGHTS",
]
