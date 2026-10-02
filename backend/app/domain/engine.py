"""Core recommendation engine coordinating physical calculations, filtering, ranking, and safety."""

from backend.app.domain.barrier import derive_target_specifications
from backend.app.domain.explanation import synthesize_explanation
from backend.app.domain.filtering import filter_candidate_materials
from backend.app.domain.ranking import rank_candidates
from backend.app.domain.respiration import (
    adjust_respiration_rate_for_temperature,
    calculate_equilibrium_required_otr,
    evaluate_microperforation_need,
)
from backend.app.domain.safety import evaluate_food_safety_advisory
from backend.app.domain.types import (
    CandidateEligibility,
    OptimizationPreference,
    RankingWeightsConfig,
    RecommendationInput,
    RecommendationResultDomain,
    RecommendationStatus,
    StorageType,
    TargetSpecifications,
    TransitGaugeConfig,
)
from backend.app.models.commodity import Commodity
from backend.app.models.material import PackagingMaterial


class RecommendationEngine:
    """Pure, deterministic food packaging recommendation and decision-support engine."""

    @staticmethod
    def evaluate(
        commodity: Commodity,
        materials: list[PackagingMaterial],
        inp: RecommendationInput,
        weights_config: RankingWeightsConfig | None = None,
        gauge_config: TransitGaugeConfig | None = None,
    ) -> RecommendationResultDomain:
        """Execute complete recommendation pipeline for a given commodity and user input."""
        uncertainties: list[str] = []
        actual_gauge_cfg = gauge_config if gauge_config is not None else TransitGaugeConfig()

        # 1. Commodity baseline property resolution
        prop = commodity.property
        if not prop:
            return RecommendationResultDomain(
                status=RecommendationStatus.INSUFFICIENT_EVIDENCE,
                commodity_id=commodity.commodity_id,
                commodity_name=commodity.common_name,
                primary_recommendation=None,
                alternative_recommendation=None,
                uncertainty_notes=[
                    "No baseline physicochemical properties registered for commodity "
                    f"'{commodity.common_name}'."
                ],
            )

        # Apply overrides if provided, else use literature reference baseline
        moisture_pct = (
            inp.moisture_pct if inp.moisture_pct is not None else prop.typical_moisture_pct
        )
        food_aw = (
            inp.water_activity_aw
            if inp.water_activity_aw is not None
            else prop.critical_water_activity_aw
        )
        fat_pct = (
            inp.oil_fat_content_pct
            if inp.oil_fat_content_pct is not None
            else prop.oil_fat_content_pct
        )
        ph = inp.ph if inp.ph is not None else prop.typical_ph

        is_respiring = commodity.is_respiring
        extra_sources: list[str] = [prop.reference_id]

        # 2. Fresh Produce Respiration Branch
        if is_respiring:
            if not commodity.respiration_data:
                return RecommendationResultDomain(
                    status=RecommendationStatus.RESEARCH_REQUIRED,
                    commodity_id=commodity.commodity_id,
                    commodity_name=commodity.common_name,
                    primary_recommendation=None,
                    alternative_recommendation=None,
                    uncertainty_notes=[
                        f"Post-harvest respiration rate data for '{commodity.common_name}' "
                        "is currently unavailable in published compendiums. [RESEARCH REQUIRED]."
                    ],
                )

            resp_ref = commodity.respiration_data[0]
            extra_sources.append(resp_ref.reference_id)

            # Adjust respiration for storage temperature
            base_rate = (
                inp.respiration_rate_co2
                if inp.respiration_rate_co2 is not None
                else resp_ref.respiration_rate_co2
            )
            adj_rate, resp_warnings = adjust_respiration_rate_for_temperature(
                rate_at_ref=base_rate,
                temp_ref_c=resp_ref.reference_temp_c,
                storage_temp_c=inp.storage_temp_c,
                q10_factor=resp_ref.q10_factor,
            )
            uncertainties.extend(resp_warnings)

            # Calculate equilibrium OTR demand (Coupled mass balance)
            eq_otr = calculate_equilibrium_required_otr(
                respiration_rate_co2=adj_rate,
                package_weight_kg=inp.package_weight_kg,
                package_area_m2=inp.package_area_m2,
            )

            # Evaluate microperforation requirement
            needs_perf, perf_rationale = evaluate_microperforation_need(
                respiration_class=resp_ref.respiration_class,
                respiration_rate_co2=adj_rate,
                max_tolerable_co2_pct=resp_ref.max_tolerable_co2_pct,
                eq_otr=eq_otr,
            )

            specs = TargetSpecifications(
                max_recommended_wvtr=40.0,
                max_recommended_otr=eq_otr,
                recommended_thickness_um=35.0,
                sealability_required="excellent",
                is_light_barrier_required=False,
                is_microperforation_required=needs_perf,
                target_wvtr_rationale=(
                    "Moderate-to-high water vapor transmission to prevent condensation droplets."
                ),
                target_otr_rationale=(
                    f"Equilibrium O2 demand calculated at {inp.storage_temp_c} C: "
                    f"OTR >= {eq_otr:.1f} cm3/(m2*day*atm) under coupled mass balance."
                ),
                thickness_rationale="Gauge balanced for breathable web stability (30-40 um).",
                adjusted_respiration_rate_co2=adj_rate,
            )
            if perf_rationale:
                uncertainties.append(perf_rationale)

            if commodity.map_configuration:
                extra_sources.append(commodity.map_configuration.reference_id)
                map_conf = commodity.map_configuration
                if map_conf.suitability_status == "ventilated_only":
                    uncertainties.append(
                        f"MAP Advisory: {commodity.common_name} requires dark ambient "
                        "ventilation. Hermetic or gas packaging causes physiological decay "
                        "(soft rot/blackheart)."
                    )

        # 3. Dry / Processed Goods Branch
        else:
            specs = derive_target_specifications(
                inp=inp,
                food_aw=food_aw,
                fat_pct=fat_pct,
                ph=ph,
                is_respiring=False,
                is_light_sensitive=prop.is_light_sensitive,
                gauge_config=actual_gauge_cfg,
            )

        # 4. Storage mode validation
        if inp.storage_type == StorageType.FROZEN and inp.storage_temp_c > 0.0:
            uncertainties.append(
                f"Conflicting inputs: storage type is 'frozen' but temperature is "
                f"{inp.storage_temp_c} C (> 0 C)."
            )

        # 5. Candidate Filtering
        viable, disqualified = filter_candidate_materials(materials, inp, specs, is_respiring)

        # 6. Multi-Attribute Ranking
        effective_pref = inp.optimization_preference
        if inp.user_sustainability_preference and effective_pref == OptimizationPreference.BALANCED:
            effective_pref = OptimizationPreference.SUSTAINABILITY

        ranked, primary, alternative, applied_weights = rank_candidates(
            candidates=viable,
            specs=specs,
            prioritize_sustainability=inp.user_sustainability_preference,
            weights_config=weights_config,
            preference=effective_pref,
        )

        # 7. Food Safety Advisory Interceptor
        safety_advisory = evaluate_food_safety_advisory(
            inp=inp,
            food_aw=food_aw,
            ph=ph,
            moisture_pct=moisture_pct,
            specs=specs,
        )

        # 8. Explainability Synthesis
        explanation = synthesize_explanation(
            commodity=commodity,
            inp=inp,
            specs=specs,
            primary=primary,
            alternative=alternative,
            disqualified=disqualified,
            food_aw=food_aw,
            fat_pct=fat_pct,
            is_respiring=is_respiring,
            extra_sources=extra_sources,
        )

        # 9. Determine overall recommendation status
        if not ranked:
            overall_status = RecommendationStatus.RESEARCH_REQUIRED
            uncertainties.append(
                "No candidate materials in the catalog satisfied the necessary barrier "
                "and safety constraints."
            )
        elif primary and primary.eligibility == CandidateEligibility.CONDITIONALLY_ELIGIBLE:
            overall_status = RecommendationStatus.CONDITIONAL
        else:
            overall_status = RecommendationStatus.SUPPORTED

        return RecommendationResultDomain(
            status=overall_status,
            commodity_id=commodity.commodity_id,
            commodity_name=commodity.common_name,
            primary_recommendation=primary,
            alternative_recommendation=alternative,
            ranked_candidates=ranked,
            disqualified_candidates=disqualified,
            target_specifications=specs,
            explanation=explanation,
            safety_advisory=safety_advisory,
            uncertainty_notes=uncertainties,
            applied_weights=applied_weights,
            optimization_preference=effective_pref,
        )
