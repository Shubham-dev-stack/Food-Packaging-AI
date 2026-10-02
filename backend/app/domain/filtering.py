"""Candidate material filtering and constraint satisfaction evaluation."""

from backend.app.domain.types import (
    CandidateEligibility,
    CandidateEvaluation,
    RecommendationInput,
    StorageType,
    TargetSpecifications,
)
from backend.app.models.material import PackagingMaterial


def evaluate_material_candidate(
    material: PackagingMaterial,
    inp: RecommendationInput,
    specs: TargetSpecifications,
    is_respiring: bool,
) -> CandidateEvaluation:
    """Evaluate a single PackagingMaterial entity against target specifications."""
    # Find nominal barrier property record
    if not material.barrier_properties:
        return CandidateEvaluation(
            material_id=material.material_id,
            trade_code=material.trade_code,
            material_name=material.name,
            material_family=material.material_family,
            structure_type=material.structure_type,
            eligibility=CandidateEligibility.INSUFFICIENT_EVIDENCE,
            rejection_reasons=["No ASTM barrier test data available for this material."],
        )

    bp = material.barrier_properties[0]
    sm = material.sustainability_metric
    ci = material.cost_index

    eval_result = CandidateEvaluation(
        material_id=material.material_id,
        trade_code=material.trade_code,
        material_name=material.name,
        material_family=material.material_family,
        structure_type=material.structure_type,
        eligibility=CandidateEligibility.ELIGIBLE,
        nominal_thickness_um=bp.nominal_thickness_um,
        nominal_otr=bp.otr_value,
        nominal_wvtr=bp.wvtr_value,
        is_mono_material=sm.is_mono_material if sm else False,
        is_biodegradable=material.is_biodegradable,
        relative_cost_multiplier=ci.relative_cost_multiplier if ci else 1.0,
        evidence_reference_id=material.reference_id,
    )

    rejections: list[str] = []
    conditions: list[str] = []

    # 1. Produce Respiration Constraints (Coupled System Physics)
    if is_respiring:
        is_dense_barrier = (
            material.material_family
            in [
                "metallized_film",
                "aluminum_foil_laminate",
            ]
            or bp.otr_value <= 50.0
        )

        is_permeable_or_perforated = bp.is_microperforated or bp.is_breathable

        # Dense foil/metallized films are physically incompatible with fresh produce respiration
        if is_dense_barrier and not is_permeable_or_perforated:
            rejections.append(
                "Severe hypoxia hazard: non-perforated barrier/metallized film inhibits "
                "respiratory gas exchange, inducing rapid anaerobiosis and foul off-odors."
            )
        elif not is_permeable_or_perforated:
            # Check if continuous film provides < 20% of required equilibrium OTR
            if bp.otr_value < (0.20 * specs.max_recommended_otr):
                rejections.append(
                    f"Severe hypoxia risk: continuous film OTR ({bp.otr_value:.1f} "
                    f"cm3/(m2*day*atm)) provides <20% of equilibrium demand (OTR_eq = "
                    f"{specs.max_recommended_otr:.1f} cm3/(m2*day*atm))."
                )
            elif specs.is_microperforation_required:
                # Continuous film is permeable, but produce requires micro-perforations to vent CO2
                conditions.append(
                    "Produce breathability condition: high produce respiration requires "
                    "laser/mechanical micro-perforations or breathable patch on this continuous "
                    "web to vent CO2 and prevent sulfur off-odors."
                )

    # 2. Dry / Processed Goods Barrier Constraints
    else:
        # Check Water Vapor Transmission Rate (WVTR under ASTM F1249-20)
        if bp.wvtr_value > specs.max_recommended_wvtr:
            rejections.append(
                f"Moisture barrier insufficient: nominal WVTR ({bp.wvtr_value:.1f} g/(m2*day)) "
                f"exceeds allowable range (<= {specs.max_recommended_wvtr:.2f} g/(m2*day)), "
                "risking premature texture softening and moisture gain."
            )

        # Check Oxygen Transmission Rate (OTR under ASTM D3985-17)
        if bp.otr_value > specs.max_recommended_otr:
            rejections.append(
                f"Oxygen barrier insufficient: nominal OTR ({bp.otr_value:.1f} cm3/(m2*day*atm)) "
                f"exceeds allowable range (<= {specs.max_recommended_otr:.1f} cm3/(m2*day*atm)), "
                "accelerating oxidative rancidity and off-flavor generation."
            )

        # Check Light Sensitivity Protection (Based on photo-sensitivity, not day threshold)
        if specs.is_light_barrier_required:
            is_opaque_or_metal = material.material_family in [
                "metallized_film",
                "aluminum_foil_laminate",
            ]
            if not is_opaque_or_metal:
                conditions.append(
                    "Light barrier consideration: commodity has documented photo-sensitivity "
                    "(lipid auto-oxidation / pigment bleaching). Transparent film requires "
                    "secondary opaque outer packaging (e.g. carton) or UV-blocking additives if "
                    "exposed to display lighting."
                )

    # 3. Sub-Zero Frozen Storage Compatibility (Qualitative Concern, not automatic binary failure)
    if inp.storage_type == StorageType.FROZEN and material.material_family == "biodegradable_film":
        conditions.append(
            "[QUALITATIVE CONCERN - LOW-TEMPERATURE HANDLING] Neat PLA and rigid bio-polyesters "
            "exhibit high glass transition temperatures (Tg ~ 55-60 C) and may suffer brittle "
            "fracture under impact in sub-zero frozen storage unless plasticized or modified "
            "with co-polyesters (e.g. PBAT blend). Grade-specific low-temperature impact testing "
            "(ASTM D1709) is recommended before frozen distribution."
        )

    # 4. Sealability Check
    if specs.sealability_required == "excellent" and material.sealability_rating == "poor":
        rejections.append(
            "Material exhibits poor heat-sealability to itself and cannot form hermetic "
            "seams without a sealant layer."
        )

    # Finalize eligibility state
    if rejections:
        eval_result.eligibility = CandidateEligibility.REJECTED
        eval_result.rejection_reasons = rejections
    elif conditions:
        eval_result.eligibility = CandidateEligibility.CONDITIONALLY_ELIGIBLE
        eval_result.condition_notes = conditions
    else:
        eval_result.eligibility = CandidateEligibility.ELIGIBLE

    return eval_result


def filter_candidate_materials(
    materials: list[PackagingMaterial],
    inp: RecommendationInput,
    specs: TargetSpecifications,
    is_respiring: bool,
) -> tuple[list[CandidateEvaluation], list[CandidateEvaluation]]:
    """Filter all available packaging materials into viable candidates and disqualified candidates.

    Returns:
        (viable_candidates, disqualified_candidates)
    """
    viable: list[CandidateEvaluation] = []
    disqualified: list[CandidateEvaluation] = []

    for mat in materials:
        evaluation = evaluate_material_candidate(mat, inp, specs, is_respiring)
        if evaluation.eligibility in [
            CandidateEligibility.ELIGIBLE,
            CandidateEligibility.CONDITIONALLY_ELIGIBLE,
        ]:
            viable.append(evaluation)
        else:
            disqualified.append(evaluation)

    return viable, disqualified
