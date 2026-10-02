"""Food safety guardrails and Reduced-Oxygen Packaging (ROP) contextual advisory interceptor."""

from backend.app.domain.types import RecommendationInput, TargetSpecifications


def evaluate_food_safety_advisory(
    inp: RecommendationInput,
    food_aw: float,
    ph: float,
    moisture_pct: float,
    specs: TargetSpecifications,
) -> str | None:
    """Evaluate whether commodity characteristics warrant a conservative Food Safety Advisory.

    Contextual Risk Indicator (NOT a binary food-safety classifier or regulatory certification):
        - High water activity / moisture: aw >= 0.92 OR moisture >= 60.0%
        - Low acidity: pH >= 4.6 (FDA 21 CFR 114 low-acid food boundary)
        - Reduced-oxygen format: target OTR <= 10.0 cm3/(m2*day*atm) or hermetic barrier

    Returns:
        Structured contextual advisory string or None.
    """
    is_high_moisture = food_aw >= 0.92 or moisture_pct >= 60.0
    is_low_acid = ph >= 4.6
    is_reduced_oxygen = specs.max_recommended_otr <= 10.0

    if is_high_moisture and is_low_acid and is_reduced_oxygen:
        advisory = (
            "[CONTEXTUAL FOOD SAFETY ADVISORY - REDUCED-OXYGEN PACKAGING]\n"
            "Risk Profile: This commodity combines low acidity (pH >= 4.6) and high moisture "
            "(aw >= 0.92) with a high oxygen barrier specification. Under reduced-oxygen or "
            "anaerobic packaging conditions, non-proteolytic and proteolytic strains of "
            "Clostridium botulinum present a severe neurotoxin risk without overt sensory "
            "spoilage indicators.\n"
            "- DISCLAIMER: This software provides physical barrier decision-support only and "
            "does NOT certify commercial food safety or replace regulatory challenge testing.\n"
            "- Regulatory Requirements: Commercial implementation mandates verified multi-hurdle "
            "preservation controls (e.g., thermal retort sterilization, validated acidification to "
            "pH < 4.6, validated aw reduction < 0.92, or continuous uncompromised refrigeration "
            "strictly below 3.0 C) in accordance with FDA 21 CFR 114 / CFSAN 2011 and FSSAI "
            "Packaging Regulations. Professional process validation by an accredited process "
            "authority is mandatory before commercial distribution."
        )
        if inp.storage_temp_c > 4.0:
            advisory += (
                f"\n- TEMPERATURE ABUSE WARNING: Storage temperature ({inp.storage_temp_c} C) "
                "exceeds the safe chilling threshold (<= 3.0-4.0 C), exponentially elevating "
                "anaerobic spore germination hazard."
            )
        return advisory

    return None
