"""Produce post-harvest respiration kinetics and equilibrium MAP evaluation."""

import math


def adjust_respiration_rate_for_temperature(
    rate_at_ref: float,
    temp_ref_c: float,
    storage_temp_c: float,
    q10_factor: float = 2.0,
) -> tuple[float, list[str]]:
    """Adjust produce respiration rate from reference temperature to storage temperature using Q10.

    Equation: R(T) = R(T_ref) * Q10^((T - T_ref) / 10) [EXTERNAL EVIDENCE: Fonseca 2002]
    Valid temperature range: 0.0 C <= storage_temp_c <= 25.0 C.

    Returns:
        (adjusted_respiration_rate, warnings)
    """
    warnings: list[str] = []
    if storage_temp_c < 0.0:
        warnings.append(
            f"Storage temperature ({storage_temp_c} C) is below freezing. "
            "Fresh produce suffers lethal chilling injury, ice nucleation, and tissue breakdown."
        )
    elif storage_temp_c > 25.0:
        warnings.append(
            f"Storage temperature ({storage_temp_c} C) represents severe ambient heat abuse. "
            "Respiration accelerates exponentially, risking rapid hypoxia and fermentation."
        )

    temp_diff = storage_temp_c - temp_ref_c
    scaled_rate = rate_at_ref * math.pow(q10_factor, temp_diff / 10.0)
    return round(scaled_rate, 2), warnings


def calculate_equilibrium_required_otr(
    respiration_rate_co2: float,
    package_weight_kg: float,
    package_area_m2: float,
    target_o2_fraction: float = 0.03,  # 3% equilibrium O2 target [Kader 2002]
    respiratory_quotient: float = 1.0,  # RQ = CO2 emitted / O2 consumed
) -> float:
    """Calculate the required OTR to maintain equilibrium O2 headspace without hypoxia.

    Coupled System Equilibrium Mass-Balance (Fonseca et al. 2002, Kader 2002):
        R_O2 (cm3/(kg*h)) = (respiration_rate_co2 / 44.01 mg/mmol) * 22.4 cm3/mmol / RQ
        Daily_O2 (cm3/day) = R_O2 * 24 h * package_weight_kg
        Delta_O2 = 0.209 - target_o2_fraction (driving force in atm)
        OTR_eq = Daily_O2 / (package_area_m2 * Delta_O2) [cm3 / (m2 * day * atm)]

    Returns:
        required_otr in cm3 / (m2 * day * atm)
    """
    if package_area_m2 <= 0.0 or package_weight_kg <= 0.0:
        raise ValueError("Package weight and area must be greater than zero.")

    # Convert mg CO2 to cm3 O2 at STP (44.01 mg/mmol, 22.4 cm3/mmol)
    r_o2_cm3_kg_h = (respiration_rate_co2 / 44.01) * 22.4 / max(0.5, respiratory_quotient)
    daily_o2_cm3 = r_o2_cm3_kg_h * 24.0 * package_weight_kg
    delta_o2 = max(0.01, 0.209 - target_o2_fraction)

    required_otr = daily_o2_cm3 / (package_area_m2 * delta_o2)
    return round(required_otr, 1)


def evaluate_microperforation_need(
    respiration_class: str,
    respiration_rate_co2: float,
    max_tolerable_co2_pct: float,
    eq_otr: float | None = None,
) -> tuple[bool, str]:
    """Evaluate whether produce demands micro-perforations to prevent toxic CO2 buildup or hypoxia.

    Physiological Basis (Fonseca et al. 2002; Kader 2002):
    Continuous polymer films have permselectivity beta = CTR/OTR ~ 3 to 6. When RQ ~ 1,
    the equilibrium CO2 inside a package is: y_CO2 ~ (0.209 - y_O2) / beta.
    For high-respiration produce or when required OTR exceeds standard continuous film
    capabilities (> 5000-8000 cm3/(m2*day*atm)), micro-perforations (pore diffusion ratio ~ 0.81)
    or breathable membranes are necessary to vent CO2 and prevent sulfur off-odors.

    Returns:
        (needs_microperforation, rationale)
    """
    # Check if respiration demand exceeds typical continuous polyolefin film limits
    exceeds_continuous_capacity = eq_otr is not None and eq_otr > 6000.0

    is_high_respiration = (
        respiration_class in ["high", "very_high", "extremely_high"] or respiration_rate_co2 >= 40.0
    )

    if is_high_respiration or exceeds_continuous_capacity:
        return (
            True,
            f"[EVIDENCE-DERIVED HEURISTIC: Fonseca 2002 / Kader 2002] Produce respiration "
            f"({respiration_rate_co2:.1f} mg CO2/(kg*h)) requires micro-perforated or "
            f"breathable packaging to vent CO2 and prevent toxic off-odors "
            f"(max tolerable CO2: {max_tolerable_co2_pct:.1f}%).",
        )
    return (
        False,
        "[EVIDENCE-DERIVED HEURISTIC: Fonseca 2002] Moderate produce respiration can be "
        "maintained with continuous permeable film under uncompromised chilling.",
    )
