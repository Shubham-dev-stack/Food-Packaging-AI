"""Estimation of water vapor and oxygen barrier target requirement ranges."""

from backend.app.domain.types import (
    RecommendationInput,
    TargetSpecifications,
    TransitStress,
)
from backend.app.domain.units import (
    calculate_saturated_vapor_pressure_kpa,
    calculate_vapor_pressure_gradient_kpa,
)


def estimate_wvtr_target_range(
    inp: RecommendationInput,
    food_aw: float,
    is_respiring: bool,
) -> tuple[float, str]:
    """Estimate the maximum allowable WVTR target range under ASTM F1249 (37.8 C, 90% RH).

    Returns:
        (max_allowable_wvtr, rationale_string)
    """
    if is_respiring:
        # Fresh produce transpires moisture continuously. Ultra-high water vapor barrier
        # causes high internal humidity, condensation, and rapid microbial rotting.
        return (
            50.0,
            "Fresh produce transpiration requires moderate-to-high water vapor transmission "
            "(WVTR <= 50 g/(m2*day)) to avoid condensation and fungal decay.",
        )

    # Dry crispy goods (aw <= 0.40)
    if food_aw <= 0.40:
        delta_p = calculate_vapor_pressure_gradient_kpa(
            inp.storage_temp_c, inp.storage_rh_pct, food_aw
        )
        p_sat_standard = calculate_saturated_vapor_pressure_kpa(37.8)
        standard_driving_force = p_sat_standard * 0.90  # ~5.9 kPa standard gradient

        # Engineering steady-state mass transfer approximation
        # Permissible moisture gain Delta M_crit ~ 0.02 (20 g/kg) [PROTOTYPE ASSUMPTION]
        delta_m_crit_g = 2.0  # 2.0 g water per 100g product
        days = max(inp.desired_shelf_life_days, 1)
        area = max(inp.package_area_m2, 0.01)

        if delta_p > 0.05:
            # Scale steady-state transfer to ASTM standard gradient
            raw_target = (delta_m_crit_g / (area * days)) * (standard_driving_force / delta_p)
            # Bound strictly within peer-reviewed literature limits for crispy snacks (0.5 to 2.5)
            clamped_target = max(0.5, min(raw_target, 2.5))
        else:
            clamped_target = 2.0

        return (
            round(clamped_target, 2),
            f"Crispy texture retention (critical aw={food_aw:.2f}) across "
            f"{inp.desired_shelf_life_days} days requires strict moisture barrier "
            f"(WVTR <= {clamped_target:.2f} g/(m2*day)).",
        )

    elif food_aw <= 0.60:
        # Moderate moisture sensitivity (biscuits, dry pasta, powders)
        clamped_target = 4.5
        return (
            clamped_target,
            f"Moderate moisture sensitivity (aw={food_aw:.2f}) requires standard moisture barrier "
            f"(WVTR <= {clamped_target} g/(m2*day)) to prevent staling and lump formation.",
        )
    else:
        # High moisture foods (pastes, frozen items): prevent drying out / freezer burn
        clamped_target = 18.0
        return (
            clamped_target,
            f"High moisture food (aw={food_aw:.2f}) requires moderate barrier "
            f"(WVTR <= {clamped_target} g/(m2*day)) to prevent surface desiccation and freezer "
            "sublimation.",
        )


def estimate_otr_target_range(
    inp: RecommendationInput,
    fat_pct: float,
    ph: float,
    is_respiring: bool,
) -> tuple[float, bool, str]:
    """Estimate the maximum allowable OTR target range under ASTM D3985 (23 C, 0% RH).

    Returns:
        (max_allowable_otr, is_light_barrier_required, rationale_string)
    """
    if is_respiring:
        # Respiring commodities must have their OTR governed by respiration equilibrium
        return (
            15000.0,
            False,
            "Fresh produce respiration requires high oxygen ingress to prevent "
            "anaerobic fermentation.",
        )

    # High fat content: free-radical auto-oxidation risk
    if fat_pct >= 20.0 or (fat_pct >= 10.0 and inp.desired_shelf_life_days >= 60):
        target_otr = 2.0
        return (
            target_otr,
            True,
            f"High lipid fraction ({fat_pct:.1f}%) and extended shelf life "
            f"({inp.desired_shelf_life_days}d) require high oxygen barrier "
            f"(OTR <= {target_otr} cm3/(m2*day*atm)) and optical opacity "
            "to prevent rancidity and photo-oxidation.",
        )
    elif fat_pct >= 5.0 or inp.desired_shelf_life_days >= 90:
        target_otr = 25.0
        return (
            target_otr,
            False,
            f"Moderate lipid fraction ({fat_pct:.1f}%) requires intermediate oxygen barrier "
            f"(OTR <= {target_otr} cm3/(m2*day*atm)) to prevent oxidative flavor changes.",
        )
    elif ph < 4.6:
        # High-acid food: microbial pathogens inhibited by acid, but carotenoids/flavor oxidize
        target_otr = 60.0
        return (
            target_otr,
            True,
            f"High-acid commodity (pH={ph:.2f}) requires OTR <= {target_otr} cm3/(m2*day*atm) "
            "and UV protection to prevent carotenoid pigment bleaching and mold growth.",
        )
    else:
        # Low risk commodity: mold suppression
        target_otr = 120.0
        return (
            target_otr,
            False,
            f"Low fat ({fat_pct:.1f}%) commodity requires baseline oxygen barrier "
            f"(OTR <= {target_otr} cm3/(m2*day*atm)) for mold suppression.",
        )


def estimate_recommended_thickness_um(
    transit_stress: TransitStress,
    is_foil_required: bool,
) -> tuple[float, str]:
    """Determine baseline recommended thickness gauge based on transit mechanical stress.

    Returns:
        (recommended_gauge_um, rationale_string)
    """
    if transit_stress == TransitStress.ROUGH_TERRAIN_UNPAVED:
        gauge = 65.0
        rationale = (
            "Rough terrain transport requires heavy-gauge material (>= 60-70 um) "
            "or reinforced laminate to prevent flex-cracking and puncture failures."
        )
    elif transit_stress == TransitStress.LONG_HAUL_REFRIGERATED:
        gauge = 45.0
        rationale = (
            "Long-haul refrigerated transit requires intermediate gauge (>= 40-50 um) "
            "for structural seam durability under temperature and vibration cycles."
        )
    else:
        gauge = 30.0
        rationale = "Local standard transit requires standard gauge (>= 25-35 um)."

    if is_foil_required and gauge < 60.0:
        gauge = 70.0
        rationale += " Foil laminate requires minimum 70 um backing to support the aluminum web."

    return gauge, rationale


def derive_target_specifications(
    inp: RecommendationInput,
    food_aw: float,
    fat_pct: float,
    ph: float,
    is_respiring: bool,
    is_light_sensitive: bool,
) -> TargetSpecifications:
    """Synthesize complete technical target specification ranges for candidate filtering."""
    wvtr_target, wvtr_rationale = estimate_wvtr_target_range(inp, food_aw, is_respiring)
    otr_target, light_needed_fat, otr_rationale = estimate_otr_target_range(
        inp, fat_pct, ph, is_respiring
    )
    light_barrier_required = is_light_sensitive or light_needed_fat

    is_foil_needed = otr_target <= 0.1 and wvtr_target <= 0.1
    thickness_um, thickness_rationale = estimate_recommended_thickness_um(
        inp.transit_stress, is_foil_needed
    )

    return TargetSpecifications(
        max_recommended_wvtr=wvtr_target,
        max_recommended_otr=otr_target,
        recommended_thickness_um=thickness_um,
        sealability_required="excellent" if (otr_target <= 10.0 or is_respiring) else "good",
        is_light_barrier_required=light_barrier_required,
        is_microperforation_required=is_respiring,
        target_wvtr_rationale=wvtr_rationale,
        target_otr_rationale=otr_rationale,
        thickness_rationale=thickness_rationale,
    )
