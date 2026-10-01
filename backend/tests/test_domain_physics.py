"""Unit tests for unit-safe physical calculations, Tetens equation, respiration, and safety."""

import pytest

from backend.app.domain.barrier import (
    estimate_otr_target_range,
    estimate_recommended_thickness_um,
    estimate_wvtr_target_range,
)
from backend.app.domain.respiration import (
    adjust_respiration_rate_for_temperature,
    calculate_equilibrium_required_otr,
    evaluate_microperforation_need,
)
from backend.app.domain.safety import evaluate_food_safety_advisory
from backend.app.domain.types import (
    RecommendationInput,
    TargetSpecifications,
    TransitStress,
)
from backend.app.domain.units import (
    calculate_saturated_vapor_pressure_kpa,
    calculate_vapor_pressure_gradient_kpa,
    celsius_to_kelvin,
    mil_to_um,
    um_to_mil,
)


def test_unit_conversions():
    """Verify Celsius-Kelvin and gauge conversions."""
    assert celsius_to_kelvin(0.0) == 273.15
    assert celsius_to_kelvin(25.0) == 298.15
    assert celsius_to_kelvin(-20.0) == 253.15

    # 1 mil = 25.4 um
    assert round(um_to_mil(25.4), 3) == 1.000
    assert round(mil_to_um(1.0), 3) == 25.4
    assert round(um_to_mil(12.7), 3) == 0.500

    with pytest.raises(ValueError):
        um_to_mil(-5.0)
    with pytest.raises(ValueError):
        mil_to_um(-2.0)


def test_saturated_vapor_pressure_tetens():
    """Verify Tetens equation across freezing, ambient, and tropical conditions."""
    # At 0.0 C, pure water vapor pressure is ~0.611 kPa
    p0 = calculate_saturated_vapor_pressure_kpa(0.0)
    assert round(p0, 3) == 0.611

    # At 25.0 C, p_sat is ~3.17 kPa
    p25 = calculate_saturated_vapor_pressure_kpa(25.0)
    assert 3.10 <= p25 <= 3.25

    # At 37.8 C (tropical test), p_sat is ~6.55 kPa
    p38 = calculate_saturated_vapor_pressure_kpa(37.8)
    assert 6.45 <= p38 <= 6.65

    # At -18.0 C (frozen food), p_sat over ice is ~0.125 kPa
    p_frozen = calculate_saturated_vapor_pressure_kpa(-18.0)
    assert 0.10 <= p_frozen <= 0.16

    # Outside validity bounds
    with pytest.raises(ValueError):
        calculate_saturated_vapor_pressure_kpa(-50.0)
    with pytest.raises(ValueError):
        calculate_saturated_vapor_pressure_kpa(75.0)


def test_vapor_pressure_gradient():
    """Verify partial vapor pressure gradient calculation Delta p_w."""
    # Ambient 25 C, 80% RH, dry food with aw = 0.30 -> positive moisture driving force inward
    grad_inward = calculate_vapor_pressure_gradient_kpa(temp_c=25.0, rh_ext_pct=80.0, food_aw=0.30)
    assert grad_inward > 0.0
    p25 = calculate_saturated_vapor_pressure_kpa(25.0)
    expected_grad = p25 * (0.80 - 0.30)
    assert abs(grad_inward - expected_grad) < 1e-4

    # Desiccation scenario: ambient 25 C, 40% RH, fresh produce with aw = 0.95 -> outward gradient
    grad_outward = calculate_vapor_pressure_gradient_kpa(temp_c=25.0, rh_ext_pct=40.0, food_aw=0.95)
    assert grad_outward < 0.0

    # Bounds checking
    with pytest.raises(ValueError):
        calculate_vapor_pressure_gradient_kpa(25.0, 110.0, 0.5)
    with pytest.raises(ValueError):
        calculate_vapor_pressure_gradient_kpa(25.0, 50.0, 1.2)


def test_respiration_q10_temperature_scaling():
    """Verify produce respiration rate scaling using Q10 kinetics."""
    # At ref 5.0 C, base rate is 65.0 mg CO2/(kg*h). At 15.0 C with Q10 = 2.0, rate should double
    scaled, warnings = adjust_respiration_rate_for_temperature(
        rate_at_ref=65.0, temp_ref_c=5.0, storage_temp_c=15.0, q10_factor=2.0
    )
    assert scaled == 130.0
    assert len(warnings) == 0

    # Temperature abuse test (> 25 C) triggers warning
    scaled_abuse, abuse_warnings = adjust_respiration_rate_for_temperature(
        rate_at_ref=65.0, temp_ref_c=5.0, storage_temp_c=30.0, q10_factor=2.2
    )
    assert scaled_abuse > 300.0
    assert any("ambient heat abuse" in w for w in abuse_warnings)

    # Sub-zero produce chilling test (< 0 C) triggers warning
    _, freeze_warnings = adjust_respiration_rate_for_temperature(
        rate_at_ref=65.0, temp_ref_c=5.0, storage_temp_c=-2.0, q10_factor=2.0
    )
    assert any("below freezing" in w for w in freeze_warnings)


def test_equilibrium_required_otr_calculation():
    """Verify equilibrium oxygen demand for a 100g produce package."""
    # R_CO2 = 65 mg/(kg*h), pkg = 0.1 kg, area = 0.06 m2, target O2 = 3%
    eq_otr = calculate_equilibrium_required_otr(
        respiration_rate_co2=65.0,
        package_weight_kg=0.10,
        package_area_m2=0.06,
        target_o2_fraction=0.03,
    )
    # Daily O2 demand ~79 cm3, across 0.06 m2 * 0.18 driving force -> ~7300 cm3/(m2*day*atm)
    assert 6500.0 <= eq_otr <= 8500.0

    with pytest.raises(ValueError):
        calculate_equilibrium_required_otr(65.0, 0.0, 0.06)


def test_microperforation_evaluation():
    """Verify evaluation of micro-perforation necessity based on respiration class."""
    needs_perf_high, note_high = evaluate_microperforation_need(
        respiration_class="extremely_high",
        respiration_rate_co2=65.0,
        max_tolerable_co2_pct=15.0,
    )
    assert needs_perf_high is True
    assert "micro-perforated" in note_high

    needs_perf_low, _ = evaluate_microperforation_need(
        respiration_class="low",
        respiration_rate_co2=8.0,
        max_tolerable_co2_pct=20.0,
    )
    assert needs_perf_low is False


def test_wvtr_target_range_dry_goods():
    """Verify WVTR target range for dry crispy snacks vs high-moisture foods."""
    inp_dry = RecommendationInput(
        commodity_id="COMM_POTATO_CHIPS",
        desired_shelf_life_days=180,
        storage_temp_c=25.0,
        storage_rh_pct=65.0,
    )
    wvtr_target, rationale = estimate_wvtr_target_range(inp_dry, food_aw=0.40, is_respiring=False)
    # Should require high barrier (<= 2.5 g/(m2*day))
    assert wvtr_target <= 2.5
    assert "Crispy texture retention" in rationale

    # High moisture non-respiring food
    inp_moist = RecommendationInput(
        commodity_id="COMM_TOMATO_PASTE",
        desired_shelf_life_days=90,
        storage_temp_c=20.0,
        storage_rh_pct=50.0,
    )
    wvtr_target_moist, _ = estimate_wvtr_target_range(inp_moist, food_aw=0.93, is_respiring=False)
    assert wvtr_target_moist >= 15.0


def test_otr_target_range_fat_sensitivity():
    """Verify OTR targets based on lipid auto-oxidation risk."""
    inp = RecommendationInput(
        commodity_id="COMM_ROASTED_PEANUTS",
        desired_shelf_life_days=120,
        storage_temp_c=20.0,
        storage_rh_pct=50.0,
    )
    # High fat (49% fat)
    otr_target, light_req, rationale = estimate_otr_target_range(
        inp, fat_pct=49.0, ph=6.5, is_respiring=False
    )
    assert otr_target <= 2.5
    assert light_req is True
    assert "High lipid fraction" in rationale

    # Low fat (0.4% fat, non-acid) with short shelf life (30d)
    inp_short = RecommendationInput(
        commodity_id="COMM_LOW_FAT",
        desired_shelf_life_days=30,
        storage_temp_c=20.0,
        storage_rh_pct=50.0,
    )
    otr_low_fat, light_low, _ = estimate_otr_target_range(
        inp_short, fat_pct=0.4, ph=6.5, is_respiring=False
    )
    assert otr_low_fat >= 100.0
    assert light_low is False


def test_recommended_thickness_transit():
    """Verify thickness gauge based on transit mechanical stress profiles."""
    gauge_std, _ = estimate_recommended_thickness_um(TransitStress.LOCAL_STANDARD, False)
    assert gauge_std == 30.0

    gauge_rough, note_rough = estimate_recommended_thickness_um(
        TransitStress.ROUGH_TERRAIN_UNPAVED, False
    )
    assert gauge_rough >= 60.0
    assert "Rough terrain" in note_rough


def test_food_safety_advisory_interceptor():
    """Verify Reduced-Oxygen Packaging (ROP) safety advisory triggers correctly."""
    inp = RecommendationInput(
        commodity_id="COMM_LOW_ACID_TEST",
        desired_shelf_life_days=60,
        storage_temp_c=5.0,
        storage_rh_pct=85.0,
    )
    specs_tight = TargetSpecifications(
        max_recommended_wvtr=2.0,
        max_recommended_otr=1.0,  # Tight oxygen barrier
        recommended_thickness_um=50.0,
        sealability_required="excellent",
        is_light_barrier_required=False,
        is_microperforation_required=False,
        target_wvtr_rationale="",
        target_otr_rationale="",
        thickness_rationale="",
    )

    # 1. High moisture (aw 0.95), low acid (pH 6.0), tight OTR -> MUST trigger advisory
    advisory = evaluate_food_safety_advisory(
        inp=inp,
        food_aw=0.95,
        ph=6.0,
        moisture_pct=80.0,
        specs=specs_tight,
    )
    assert advisory is not None
    assert "Clostridium botulinum" in advisory
    assert "REDUCED-OXYGEN PACKAGING" in advisory

    # 2. High-acid food (pH 4.1 < 4.6) -> MUST NOT trigger botulism advisory
    advisory_acid = evaluate_food_safety_advisory(
        inp=inp,
        food_aw=0.95,
        ph=4.1,
        moisture_pct=80.0,
        specs=specs_tight,
    )
    assert advisory_acid is None

    # 3. Dry crispy food (aw 0.40) -> MUST NOT trigger botulism advisory
    advisory_dry = evaluate_food_safety_advisory(
        inp=inp,
        food_aw=0.40,
        ph=6.0,
        moisture_pct=3.0,
        specs=specs_tight,
    )
    assert advisory_dry is None
