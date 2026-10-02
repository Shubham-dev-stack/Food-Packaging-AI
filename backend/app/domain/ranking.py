"""Multi-Criteria Decision Analysis (MCDA) utility ranking for viable candidate materials."""

from backend.app.domain.types import (
    SUSTAINABILITY_PRIORITY_WEIGHTS,
    CandidateEligibility,
    CandidateEvaluation,
    RankingWeightsConfig,
    TargetSpecifications,
)


def score_barrier_margin(
    candidate: CandidateEvaluation,
    specs: TargetSpecifications,
) -> float:
    """Calculate barrier performance score (0.0 to 1.0)."""
    score = 0.85  # Base score for meeting hard constraint threshold

    # If conditionally eligible (e.g. requires outer carton), apply modest penalty
    if candidate.eligibility == CandidateEligibility.CONDITIONALLY_ELIGIBLE:
        score -= 0.20

    # If material provides substantial safety margin over minimum targets
    if candidate.nominal_wvtr <= (specs.max_recommended_wvtr * 0.5):
        score += 0.08
    if candidate.nominal_otr <= (specs.max_recommended_otr * 0.5):
        score += 0.07

    return round(max(0.1, min(score, 1.0)), 3)


def score_sustainability(candidate: CandidateEvaluation) -> float:
    """Calculate circularity and sustainability score (0.0 to 1.0).

    Mono-material mechanical recycling: 1.0
    Industrial compostable bio-film: 0.85
    Specialized multi-layer recycling: 0.50
    Unrecyclable multi-material laminate: 0.20
    """
    if candidate.is_mono_material:
        return 1.0
    elif candidate.is_biodegradable:
        return 0.85
    elif candidate.structure_type in ["monolayer", "coextrusion"]:
        return 0.65
    elif candidate.material_family == "metallized_film":
        return 0.50
    else:
        # e.g., aluminum foil polymer laminate (non-recyclable)
        return 0.20


def score_relative_cost(candidate: CandidateEvaluation) -> float:
    """Calculate economic cost score (0.0 to 1.0) using inverse cost index."""
    mult = max(1.0, candidate.relative_cost_multiplier)
    # LDPE baseline 1.0 gives 1.0, foil laminate 3.8 gives ~0.26
    return round(1.0 / mult, 3)


def rank_candidates(
    candidates: list[CandidateEvaluation],
    specs: TargetSpecifications,
    prioritize_sustainability: bool = False,
    weights_config: RankingWeightsConfig | None = None,
) -> tuple[list[CandidateEvaluation], CandidateEvaluation | None, CandidateEvaluation | None]:
    """Score and rank viable candidate materials using multi-attribute utility.

    Decision-support prototype baseline weights: 50% barrier, 30% sustainability, 20% cost.
    (Matches docs/AI_Recommendation_Engine.md Section 3.5 [PROTOTYPE ASSUMPTION]).

    Returns:
        (ranked_candidates, primary_candidate, eco_alternative_candidate)
    """
    if not candidates:
        return [], None, None

    # Configurable weights [PROTOTYPE ASSUMPTION]
    if weights_config is not None:
        cfg = weights_config
    elif prioritize_sustainability:
        cfg = SUSTAINABILITY_PRIORITY_WEIGHTS
    else:
        cfg = RankingWeightsConfig()

    w_barrier = cfg.w_barrier
    w_sust = cfg.w_sustainability
    w_cost = cfg.w_cost

    # Score each candidate
    for cand in candidates:
        cand.barrier_safety_score = score_barrier_margin(cand, specs)
        cand.sustainability_score = score_sustainability(cand)
        cand.cost_score = score_relative_cost(cand)

        utility = (
            (w_barrier * cand.barrier_safety_score)
            + (w_sust * cand.sustainability_score)
            + (w_cost * cand.cost_score)
        )
        cand.composite_utility_score = round(utility, 4)

    # Sort descending: Fully ELIGIBLE candidates precede CONDITIONALLY_ELIGIBLE,
    # then rank by composite utility score (tie-break on sustainability, then cost)
    ranked = sorted(
        candidates,
        key=lambda c: (
            c.eligibility == CandidateEligibility.ELIGIBLE,
            c.composite_utility_score,
            c.sustainability_score,
            c.cost_score,
        ),
        reverse=True,
    )

    primary = ranked[0]

    # Find the top alternative that offers superior sustainability or lower cost
    eco_alt = None
    for alt in ranked[1:]:
        if alt.sustainability_score > primary.sustainability_score:
            eco_alt = alt
            break

    # If primary already has highest sustainability, find the best lower-cost viable alternative
    if not eco_alt and len(ranked) > 1:
        for alt in ranked[1:]:
            if alt.cost_score > primary.cost_score:
                eco_alt = alt
                break

    return ranked, primary, eco_alt
