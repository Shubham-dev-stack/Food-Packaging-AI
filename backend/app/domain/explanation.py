"""Synthesis of structured, traceable explanation cards and disqualification logs."""

from backend.app.domain.types import (
    CandidateEvaluation,
    ExplanationData,
    RecommendationInput,
    TargetSpecifications,
)
from backend.app.models.commodity import Commodity


def determine_dominant_spoilage_driver(
    commodity: Commodity,
    inp: RecommendationInput,
    food_aw: float,
    fat_pct: float,
    is_respiring: bool,
) -> str:
    """Determine the primary physicochemical or biological degradation vulnerability."""
    if is_respiring:
        return (
            "Aerobic produce respiration and transpirational water loss. "
            "Requires balanced gas transmission to prevent both tissue suffocation (anaerobiosis) "
            "and excessive moisture condensation."
        )
    elif food_aw <= 0.40 and fat_pct >= 20.0:
        return (
            f"Dual vulnerability: moisture-induced loss of crispness (critical aw={food_aw:.2f}) "
            f"combined with free-radical lipid oxidation of unsaturated oils ({fat_pct:.1f}% fat)."
        )
    elif food_aw <= 0.40:
        return (
            "Moisture-driven texture loss: rapid loss of crispness occurs if moisture "
            f"ingress raises water activity past the critical threshold (aw={food_aw:.2f})."
        )
    elif fat_pct >= 20.0:
        return (
            f"Lipid oxidation and rancidity: high lipid content ({fat_pct:.1f}% fat) reacts "
            "with atmospheric oxygen, generating volatile hexanals and rancid off-odors."
        )
    elif inp.storage_type.value == "frozen":
        return (
            "Sublimation and surface dehydration: temperature fluctuations in frozen storage cause "
            "ice crystal migration, surface desiccation (freezer burn), and textural toughening."
        )
    elif commodity.property and commodity.property.typical_ph < 4.6:
        return (
            f"High-acid preservation: low pH ({commodity.property.typical_ph:.2f}) controls "
            "spore-forming pathogens, leaving mold, yeast, and oxygen-induced carotenoid "
            "bleaching as the primary degradation routes."
        )
    else:
        return "General microbial, mold, and atmospheric moisture degradation."


def synthesize_explanation(
    commodity: Commodity,
    inp: RecommendationInput,
    specs: TargetSpecifications,
    primary: CandidateEvaluation | None,
    alternative: CandidateEvaluation | None,
    disqualified: list[CandidateEvaluation],
    food_aw: float,
    fat_pct: float,
    is_respiring: bool,
    extra_sources: list[str] | None = None,
) -> ExplanationData:
    """Synthesize complete structured explanation payload."""
    dominant_driver = determine_dominant_spoilage_driver(
        commodity, inp, food_aw, fat_pct, is_respiring
    )

    factors = [
        f"Storage mode: {inp.storage_type.value.capitalize()} at {inp.storage_temp_c} C, "
        f"{inp.storage_rh_pct}% RH.",
        f"Target shelf life: {inp.desired_shelf_life_days} days.",
        f"Food water activity: aw = {food_aw:.2f}; Fat content: {fat_pct:.1f}%.",
    ]
    if is_respiring:
        factors.append("Active post-harvest produce respiration requires breathable headspace.")

    # Selection rationale
    if primary:
        sel_rationale = (
            f"Selected {primary.material_name} as primary recommendation because its nominal "
            f"barrier (OTR={primary.nominal_otr:.1f}, WVTR={primary.nominal_wvtr:.1f}) meets "
            f"target requirements (OTR <= {specs.max_recommended_otr:.1f}, "
            f"WVTR <= {specs.max_recommended_wvtr:.2f}) with the highest composite utility "
            f"score ({primary.composite_utility_score:.4f})."
        )
    else:
        sel_rationale = (
            "No candidate materials satisfied all mandatory physical barrier and safety "
            "constraints."
        )

    # Alternative rationale
    if alternative:
        alt_rationale = (
            f"Recommended {alternative.material_name} as an alternative because it achieves "
            f"a superior sustainability/circularity score ({alternative.sustainability_score:.2f}) "
            f"or favorable cost index ({alternative.relative_cost_multiplier:.2f}x) while "
            "satisfying barrier constraints."
        )
    else:
        alt_rationale = "No distinct secondary viable candidate met constraint thresholds."

    # Disqualification summary
    disq_summary = [
        {
            "material_id": d.material_id,
            "trade_code": d.trade_code,
            "name": d.material_name,
            "reasons": d.rejection_reasons,
        }
        for d in disqualified
    ]

    # Traceable evidence references
    sources = set(extra_sources or [])
    if commodity.property:
        sources.add(commodity.property.reference_id)
    if primary and primary.evidence_reference_id:
        sources.add(primary.evidence_reference_id)
    if alternative and alternative.evidence_reference_id:
        sources.add(alternative.evidence_reference_id)

    # Add standards reference IDs based on context
    if is_respiring:
        sources.add("REF_KADER_2002")
        sources.add("REF_FONSECA_2002")
    else:
        sources.add("REF_ROBERTSON_2012")
        sources.add("REF_ASTM_F1249")
        sources.add("REF_ASTM_D3985")

    assumptions = [
        "[PROTOTYPE ASSUMPTION] Steady-state isothermal mass transfer (no thermal cycling).",
        (
            f"[PROTOTYPE ASSUMPTION] Standard pouch geometry baseline "
            f"({inp.package_weight_kg * 1000:.0f}g food / {inp.package_area_m2:.2f} m2 area)."
        ),
        (
            "[PROTOTYPE ASSUMPTION] Linear water vapor permeance scaling across vapor pressure "
            "gradient."
        ),
        "[PROTOTYPE ASSUMPTION] Relative economic index normalized to baseline LDPE film (= 1.0).",
    ]

    limitations = [
        (
            "Recommendations represent engineering decision-support estimates and do NOT "
            "constitute accredited laboratory test validation or shelf-life certification."
        ),
        (
            "Standard test methods: OTR measured under ASTM D3985-17 (23 C, 0% RH); "
            "WVTR measured under ASTM F1249-20 (37.8 C, 90% RH). Commercial implementation "
            "requires physical testing (ASLT) and regulatory food migration compliance."
        ),
    ]

    return ExplanationData(
        dominant_spoilage_driver=dominant_driver,
        critical_factors=factors,
        selection_rationale=sel_rationale,
        alternative_rationale=alt_rationale,
        disqualification_summary=disq_summary,
        cited_evidence_sources=sorted(sources),
        documented_assumptions=assumptions,
        scientific_limitations=limitations,
    )
