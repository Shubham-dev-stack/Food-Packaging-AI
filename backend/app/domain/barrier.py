"""Estimation of water vapor and oxygen barrier target requirement ranges."""

from backend.app.domain.types import (
    RecommendationInput,
    TargetSpecifications,
    TransitGaugeConfig,
    TransitStress,
)
from backend.app.domain.units import (
    calculate_saturated_vapor_pressure_kpa,
    calculate_vapor_pressure_gradient_kpa,
)


def calculate_mass_balance_moisture_flux(
    delta_m_grams: float,
    package_area_m2: float,
    shelf_life_days: int,
) -> float:
    """Calculate the maximum allowable average moisture ingress flux under storage conditions.

    Dimensional Derivation:
        delta_m_grams: Permissible moisture mass gain in [g]
        package_area_m2: Package permeable surface area in [m2]
        shelf_life_days: Required shelf life duration in [days]

    Resulting Unit:
        J_allowable = delta_m_grams / (package_area_m2 * shelf_life_days)
                    = [g / (m2 * day)] at actual storage temperature and RH.

    Note: This is the mass-balance flux required under actual storage conditions.
    It is NOT identical to an ASTM F1249 test rating (37.8 C, 90% RH) unless
    scaled by the relevant water vapor permeance relationship.
    """
    if package_area_m2 <= 0.0 or shelf_life_days <= 0:
        raise ValueError("Package area and shelf-life days must be strictly positive.")
    return delta_m_grams / (package_area_m2 * float(shelf_life_days))


def estimate_wvtr_target_range(
    inp: RecommendationInput,
    food_aw: float,
    is_respiring: bool,
) -> tuple[float, str]:
    """Estimate indicative maximum allowable WVTR target range under ASTM F1249-20 (37.8 C, 90% RH).

    Step-by-Step Unit & Methodological Derivation:
    1. Mass Balance Flux Requirement:
       J_allowable = Delta_M_crit / (Area * Days)   [g / (m2 * day)] at storage (T, RH).
       Delta_M_crit is estimated at 1.5 - 2.0 g per 100g product [PROTOTYPE ASSUMPTION].
    2. Linear Permeance Scaling [PROTOTYPE ASSUMPTION]:
       Assuming constant Fickian permeance (ignoring polymer Arrhenius activation energy Ep
       and sorption isotherm non-linearities):
       WVTR_ASTM_est = J_allowable * (Delta_p_ref / Delta_p_storage)
       where Delta_p_ref = p_sat(37.8 C) * 0.90 ~ 5.86 kPa (ASTM F1249 test condition).
    3. Literature-Grounded Target Range Clamping:
       Real-world snack food shelf-life studies (Robertson 2012, Labuza & Hyman 1998)
       demonstrate that crispy snacks (aw <= 0.35) require ASTM F1249 WVTR <= 0.5 - 2.5 g/(m2*day).
       Therefore, the calculation serves as decision-support guidance clamped within
       empirically supported bounds, NOT an exact unverified laboratory cutoff.

    Returns:
        (max_allowable_wvtr, rationale_string)
    """
    if is_respiring:
        return (
            50.0,
            "Fresh produce transpiration requires moderate-to-high water vapor transmission "
            "(WVTR <= 50 g/(m2*day)) to avoid internal condensation and mold growth.",
        )

    # Dry crispy goods (aw <= 0.40)
    if food_aw <= 0.40:
        delta_p = calculate_vapor_pressure_gradient_kpa(
            inp.storage_temp_c, inp.storage_rh_pct, food_aw
        )
        p_sat_standard = calculate_saturated_vapor_pressure_kpa(37.8)
        standard_driving_force = p_sat_standard * 0.90  # ~5.86 kPa standard gradient

        # Engineering steady-state mass transfer approximation
        # Permissible moisture gain Delta M_crit ~ 0.02 (20 g/kg) [PROTOTYPE ASSUMPTION]
        delta_m_crit_g = 2.0  # 2.0 g water per 100g product
        days = max(inp.desired_shelf_life_days, 1)
        area = max(inp.package_area_m2, 0.01)

        raw_flux = calculate_mass_balance_moisture_flux(delta_m_crit_g, area, days)

        if delta_p > 0.05:
            # Scale steady-state transfer to ASTM standard gradient via linear permeance
            raw_target = raw_flux * (standard_driving_force / delta_p)
            # Bound strictly within peer-reviewed literature limits for crispy snacks (0.5 to 2.5)
            clamped_target = max(0.5, min(raw_target, 2.5))
        else:
            clamped_target = 2.0

        return (
            round(clamped_target, 2),
            f"[PROTOTYPE ASSUMPTION: Linear permeance scaling & Robertson 2012 benchmark] "
            f"Crispy texture retention (critical aw={food_aw:.2f}) across "
            f"{inp.desired_shelf_life_days}d at {inp.storage_temp_c} C / {inp.storage_rh_pct}% RH: "
            f"target requirement range WVTR <= {clamped_target:.2f} g/(m2*day) "
            "(ASTM F1249-20). Physical barrier testing (ASTM F1249) is required for "
            "commercial validation.",
        )

    elif food_aw <= 0.60:
        # Moderate moisture sensitivity (biscuits, dry pasta, powders)
        clamped_target = 4.5
        return (
            clamped_target,
            f"[PROTOTYPE HEURISTIC: Robertson 2012] Moderate moisture sensitivity "
            f"(aw={food_aw:.2f}): literature benchmark indicates standard moisture barrier "
            f"(target WVTR <= {clamped_target} g/(m2*day) under ASTM F1249-20) to prevent "
            "staling/caking.",
        )
    else:
        # High moisture foods (pastes, frozen items): prevent drying out / freezer burn
        clamped_target = 18.0
        return (
            clamped_target,
            f"[PROTOTYPE HEURISTIC: Robertson 2012] High moisture food (aw={food_aw:.2f}): "
            f"moderate barrier (target WVTR <= {clamped_target} g/(m2*day) under ASTM F1249-20) "
            "to prevent surface desiccation and freezer sublimation.",
        )


def estimate_otr_target_range(
    inp: RecommendationInput,
    fat_pct: float,
    ph: float,
    is_respiring: bool,
) -> tuple[float, bool, str]:
    """Estimate the indicative maximum allowable OTR target range under ASTM D3985-17 (23 C, 0% RH).

    Returns:
        (max_allowable_otr, is_light_barrier_required, rationale_string)
    """
    if is_respiring:
        return (
            15000.0,
            False,
            "Fresh produce respiration requires high oxygen ingress to prevent "
            "anaerobic fermentation. OTR is governed by coupled respiration kinetics.",
        )

    # High fat content: free-radical auto-oxidation risk
    if fat_pct >= 20.0 or (fat_pct >= 10.0 and inp.desired_shelf_life_days >= 60):
        target_otr = 2.0
        return (
            target_otr,
            True,
            f"[PROTOTYPE HEURISTIC: Robertson 2012 / Marsh & Bugusu 2007] High lipid fraction "
            f"({fat_pct:.1f}%) and shelf life ({inp.desired_shelf_life_days}d): literature "
            f"benchmark indicates high oxygen barrier (target OTR <= {target_otr} "
            "cm3/(m2*day*atm) at 23 C, ASTM D3985-17) and optical opacity to mitigate "
            "rancidity. Actual threshold depends on specific fatty acid profile.",
        )
    elif fat_pct >= 5.0 or inp.desired_shelf_life_days >= 90:
        target_otr = 25.0
        return (
            target_otr,
            False,
            f"[PROTOTYPE HEURISTIC: Robertson 2012] Moderate lipid fraction ({fat_pct:.1f}%): "
            "literature benchmark indicates intermediate oxygen barrier (target OTR <= "
            f"{target_otr} cm3/(m2*day*atm) at 23 C, ASTM D3985-17) to reduce oxidative flavor "
            "deterioration.",
        )
    elif ph < 4.6:
        # High-acid food: microbial pathogens inhibited by acid, but carotenoids/flavor oxidize
        target_otr = 60.0
        return (
            target_otr,
            True,
            f"[PROTOTYPE HEURISTIC: Robertson 2012] Acid-preserved commodity (pH={ph:.2f}): "
            f"primary microbial pathogens inhibited; target OTR <= {target_otr} cm3/(m2*day*atm) "
            "(ASTM D3985-17) and UV protection mitigate carotenoid bleaching and aerobic mold.",
        )
    else:
        # Low risk commodity: mold suppression
        target_otr = 120.0
        return (
            target_otr,
            False,
            f"[PROTOTYPE HEURISTIC] Low fat ({fat_pct:.1f}%) commodity: baseline oxygen barrier "
            f"(target OTR <= {target_otr} cm3/(m2*day*atm) under ASTM D3985-17) for general mold "
            "suppression.",
        )


def estimate_recommended_thickness_um(
    transit_stress: TransitStress,
    is_foil_required: bool,
    config: TransitGaugeConfig | None = None,
) -> tuple[float, str]:
    """Determine baseline recommended thickness gauge based on transit mechanical stress.

    Returns:
        (recommended_gauge_um, rationale_string)
    """
    cfg = config if config is not None else TransitGaugeConfig()

    if transit_stress == TransitStress.ROUGH_TERRAIN_UNPAVED:
        gauge = cfg.rough_terrain_unpaved_um
        stress_desc = "Rough terrain unpaved"
    elif transit_stress == TransitStress.LONG_HAUL_REFRIGERATED:
        gauge = cfg.long_haul_refrigerated_um
        stress_desc = "Long-haul refrigerated"
    else:
        gauge = cfg.local_standard_um
        stress_desc = "Local standard"

    rationale = (
        f"[PROTOTYPE ASSUMPTION] Nominal transit mechanical gauge baseline: {gauge:.0f} um "
        f"for {stress_desc} transit. Commercial distribution requires ASTM F1306 slow rate "
        "puncture and ASTM D4169 distribution cycle testing."
    )

    if is_foil_required and gauge < cfg.foil_backing_min_um:
        gauge = cfg.foil_backing_min_um
        rationale += (
            f" Foil laminate incorporates minimum {cfg.foil_backing_min_um:.0f} um backing "
            "web to protect aluminum layer against pinhole flex-cracking."
        )

    return gauge, rationale


def derive_target_specifications(
    inp: RecommendationInput,
    food_aw: float,
    fat_pct: float,
    ph: float,
    is_respiring: bool,
    is_light_sensitive: bool,
    gauge_config: TransitGaugeConfig | None = None,
) -> TargetSpecifications:
    """Synthesize complete technical target specification ranges for candidate filtering."""
    wvtr_target, wvtr_rationale = estimate_wvtr_target_range(inp, food_aw, is_respiring)
    otr_target, light_needed_fat, otr_rationale = estimate_otr_target_range(
        inp, fat_pct, ph, is_respiring
    )
    light_barrier_required = is_light_sensitive or light_needed_fat

    is_foil_needed = otr_target <= 0.1 and wvtr_target <= 0.1
    thickness_um, thickness_rationale = estimate_recommended_thickness_um(
        inp.transit_stress, is_foil_needed, gauge_config
    )

    return TargetSpecifications(
        max_recommended_wvtr=wvtr_target,
        max_recommended_otr=otr_target,
        recommended_thickness_um=thickness_um,
        sealability_required="excellent" if (otr_target <= 10.0 or is_respiring) else "good",
        is_light_barrier_required=light_barrier_required,
        is_microperforation_required=False,
        target_wvtr_rationale=wvtr_rationale,
        target_otr_rationale=otr_rationale,
        thickness_rationale=thickness_rationale,
    )
