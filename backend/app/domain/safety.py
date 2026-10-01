"""Food safety guardrails and Reduced-Oxygen Packaging (ROP) advisory interceptor."""

from backend.app.domain.types import RecommendationInput, TargetSpecifications


def evaluate_food_safety_advisory(
    inp: RecommendationInput,
    food_aw: float,
    ph: float,
    moisture_pct: float,
    specs: TargetSpecifications,
) -> str | None:
    """Evaluate whether candidate evaluation triggers a mandatory Food Safety Advisory.

    Trigger condition:
        - High moisture: aw >= 0.92 OR moisture >= 60.0%
        - Low acidity: pH >= 4.6 (FDA 21 CFR 114 low-acid boundary)
        - Reduced-oxygen format: target OTR <= 10.0 cm3/(m2*day*atm) OR hermetic vacuum pack

    Returns:
        Formatted safety advisory string or None.
    """
    is_high_moisture = food_aw >= 0.92 or moisture_pct >= 60.0
    is_low_acid = ph >= 4.6
    is_reduced_oxygen = specs.max_recommended_otr <= 10.0

    if is_high_moisture and is_low_acid and is_reduced_oxygen:
        advisory = (
            "[MANDATORY FOOD SAFETY ADVISORY - REDUCED-OXYGEN PACKAGING]\n"
            "This commodity combines low acidity (pH >= 4.6) and high moisture (aw >= 0.92) "
            "with a high oxygen barrier specification. Under reduced-oxygen or anaerobic "
            "conditions, non-proteolytic and proteolytic strains of Clostridium botulinum present "
            "a severe neurotoxin risk without overt sensory signs of spoilage.\n"
            "- CRITICAL REQUIREMENT: This software provides physical barrier decision-support only "
            "and does NOT certify commercial food safety.\n"
            "- Commercial implementation mandates verified multi-hurdle preservation controls "
            "(e.g., thermal retort sterilization, validated acidification to pH < 4.6, water "
            "activity reduction aw < 0.92, or continuous uncompromised refrigeration strictly "
            "below 3.0 C) in accordance with FDA 21 CFR 114 / FSSAI Packaging Regulations. "
            "Professional process validation by an accredited food authority is required."
        )
        if inp.storage_temp_c > 4.0:
            advisory += (
                f"\n- WARNING: Selected storage temperature ({inp.storage_temp_c} C) exceeds the "
                "safe chilling threshold (<= 3.0-4.0 C), exponentially elevating anaerobic "
                "pathogen germination risk."
            )
        return advisory

    return None
