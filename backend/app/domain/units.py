"""Unit conversions, psychrometric helpers, and thermodynamic equations."""

import math


def celsius_to_kelvin(temp_c: float) -> float:
    """Convert Celsius to absolute temperature in Kelvin."""
    return round(temp_c + 273.15, 2)


def um_to_mil(um: float) -> float:
    """Convert micrometers (gauge) to thousandths of an inch (mil)."""
    if um < 0:
        raise ValueError("Thickness cannot be negative.")
    return um / 25.4


def mil_to_um(mil: float) -> float:
    """Convert mil to micrometers (gauge)."""
    if mil < 0:
        raise ValueError("Thickness cannot be negative.")
    return mil * 25.4


def calculate_saturated_vapor_pressure_kpa(temp_c: float) -> float:
    """Calculate saturation water vapor pressure p_sat(T) in kPa using the Tetens equation.

    Validity range: -40 deg C <= temp_c <= 60 deg C.
    Uses Tetens equation for water (> 0 C) and over ice (<= 0 C).
    """
    if temp_c < -40.0 or temp_c > 60.0:
        raise ValueError(f"Temperature {temp_c} C is outside valid Tetens boundary (-40 to 60 C).")

    if temp_c >= 0.0:
        # Standard Tetens equation for liquid water
        return 0.61078 * math.exp((17.27 * temp_c) / (temp_c + 237.3))
    else:
        # Tetens formulation for saturation over ice (frozen storage)
        return 0.61078 * math.exp((21.875 * temp_c) / (temp_c + 265.5))


def calculate_vapor_pressure_gradient_kpa(
    temp_c: float, rh_ext_pct: float, food_aw: float
) -> float:
    """Calculate the partial water vapor pressure driving force Delta p_w across packaging film.

    Delta p_w = p_sat(T) * (RH_ext / 100 - food_aw) [kPa]
    - Positive: external humidity drives moisture into food (moisture gain/sogginess risk).
    - Negative: food vapor pressure drives moisture outward (moisture loss/desiccation risk).
    """
    if not (0.0 <= rh_ext_pct <= 100.0):
        raise ValueError(f"Relative humidity {rh_ext_pct}% must be between 0.0 and 100.0%.")
    if not (0.0 <= food_aw <= 1.0):
        raise ValueError(f"Water activity {food_aw} must be between 0.0 and 1.0.")

    p_sat = calculate_saturated_vapor_pressure_kpa(temp_c)
    driving_fraction = (rh_ext_pct / 100.0) - food_aw
    return p_sat * driving_fraction
