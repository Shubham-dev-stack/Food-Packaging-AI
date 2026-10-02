"""Application service layer connecting API schemas, database, and domain engine."""

import logging
import uuid
from datetime import UTC, datetime

from sqlalchemy.orm import Session

from backend.app.domain.engine import RecommendationEngine
from backend.app.domain.types import (
    CandidateEligibility,
    RankingWeightsConfig,
    RecommendationInput,
    RecommendationResultDomain,
    RecommendationStatus,
)
from backend.app.models.recommendation import RecommendationRequest, RecommendationResult
from backend.app.repositories.commodity_repository import CommodityRepository
from backend.app.repositories.material_repository import MaterialRepository
from backend.app.repositories.recommendation_repository import RecommendationRepository
from backend.app.schemas.recommendation import (
    CandidateEvaluationResponse,
    ExplanationResponse,
    RecommendationCreateRequest,
    RecommendationResponse,
    TargetSpecificationsResponse,
)

logger = logging.getLogger(__name__)


class RecommendationService:
    """Orchestrates candidate retrieval, pure domain execution, and audit logging."""

    @staticmethod
    def create_recommendation(
        db: Session,
        request_data: RecommendationCreateRequest,
    ) -> RecommendationResponse:
        """Execute recommendation evaluation pipeline and persist audit log."""
        # 1. Fetch commodity with joined properties
        commodity = CommodityRepository.get_by_id(db, commodity_id=request_data.commodity_id)
        if not commodity:
            raise ValueError(f"Commodity with ID '{request_data.commodity_id}' not found.")

        # 2. Fetch all candidate packaging materials with barrier, eco, and cost data
        materials = MaterialRepository.list_all(db)

        # 3. Build pure domain input payload
        domain_input = RecommendationInput(
            commodity_id=request_data.commodity_id,
            desired_shelf_life_days=request_data.desired_shelf_life_days,
            storage_temp_c=request_data.storage_temp_c,
            storage_rh_pct=request_data.storage_rh_pct,
            storage_type=request_data.storage_type,
            transit_stress=request_data.transit_stress,
            user_sustainability_preference=request_data.user_sustainability_preference,
            moisture_pct=request_data.moisture_pct,
            water_activity_aw=request_data.water_activity_aw,
            oil_fat_content_pct=request_data.oil_fat_content_pct,
            ph=request_data.ph,
            respiration_rate_co2=request_data.respiration_rate_co2,
            package_weight_kg=request_data.package_weight_kg,
            package_area_m2=request_data.package_area_m2,
        )

        # 4. Resolve custom weights if provided
        weights_cfg: RankingWeightsConfig | None = None
        if request_data.custom_weights:
            weights_cfg = RankingWeightsConfig(
                w_barrier=request_data.custom_weights.w_barrier,
                w_sustainability=request_data.custom_weights.w_sustainability,
                w_cost=request_data.custom_weights.w_cost,
            )

        # 5. Invoke pure domain recommendation engine (zero database/HTTP side effects)
        domain_result: RecommendationResultDomain = RecommendationEngine.evaluate(
            commodity=commodity,
            materials=materials,
            inp=domain_input,
            weights_config=weights_cfg,
        )

        # 6. Generate audit session identifier and persist audit log
        request_id = str(uuid.uuid4())
        created_at = datetime.now(UTC)

        # Resolve inputs for persistence
        prop = commodity.property
        persisted_moisture = (
            request_data.moisture_pct
            if request_data.moisture_pct is not None
            else (prop.typical_moisture_pct if prop else 0.0)
        )
        persisted_fat = (
            request_data.oil_fat_content_pct
            if request_data.oil_fat_content_pct is not None
            else (prop.oil_fat_content_pct if prop else 0.0)
        )
        persisted_ph = (
            request_data.ph if request_data.ph is not None else (prop.typical_ph if prop else 7.0)
        )

        db_request = RecommendationRequest(
            request_id=request_id,
            commodity_id=commodity.commodity_id,
            input_moisture_pct=persisted_moisture,
            input_fat_pct=persisted_fat,
            input_ph=persisted_ph,
            input_respiration_rate=request_data.respiration_rate_co2,
            desired_shelf_life_days=request_data.desired_shelf_life_days,
            storage_temp_c=request_data.storage_temp_c,
            storage_rh_pct=request_data.storage_rh_pct,
            transit_stress_profile=request_data.transit_stress.value,
            storage_type=request_data.storage_type.value,
            user_sustainability_preference=request_data.user_sustainability_preference,
            created_at=created_at,
        )
        RecommendationRepository.create_request(db, db_request)

        # Persist result if a candidate was evaluated
        primary = domain_result.primary_recommendation
        alt = domain_result.alternative_recommendation
        specs = domain_result.target_specifications
        explanation = domain_result.explanation

        if primary and specs:
            result_id = str(uuid.uuid4())
            db_result = RecommendationResult(
                result_id=result_id,
                request_id=request_id,
                primary_material_id=primary.material_id,
                alternative_material_id=alt.material_id if alt else None,
                required_otr_target=specs.max_recommended_otr,
                required_wvtr_target=specs.max_recommended_wvtr,
                recommended_thickness_um=specs.recommended_thickness_um,
                recommended_sealability=specs.sealability_required,
                recommended_mechanical_notes=specs.thickness_rationale,
                map_configuration_id=(
                    commodity.map_configuration.map_id if commodity.map_configuration else None
                ),
                state_status=domain_result.status.value.lower(),
                explanation_summary=(
                    explanation.dominant_spoilage_driver if explanation else "Evaluation completed."
                ),
                disqualified_materials_log=(
                    explanation.disqualification_summary if explanation else []
                ),
                safety_advisory=domain_result.safety_advisory,
            )
            RecommendationRepository.create_result(db, db_result)

        # 7. Map domain outputs to API response model
        primary_resp = (
            CandidateEvaluationResponse(
                material_id=primary.material_id,
                trade_code=primary.trade_code,
                material_name=primary.material_name,
                material_family=primary.material_family,
                structure_type=primary.structure_type,
                eligibility=primary.eligibility,
                rejection_reasons=primary.rejection_reasons,
                condition_notes=primary.condition_notes,
                barrier_safety_score=primary.barrier_safety_score,
                sustainability_score=primary.sustainability_score,
                cost_score=primary.cost_score,
                composite_utility_score=primary.composite_utility_score,
                nominal_thickness_um=primary.nominal_thickness_um,
                nominal_otr=primary.nominal_otr,
                nominal_wvtr=primary.nominal_wvtr,
                is_mono_material=primary.is_mono_material,
                is_biodegradable=primary.is_biodegradable,
                relative_cost_multiplier=primary.relative_cost_multiplier,
                evidence_reference_id=primary.evidence_reference_id,
            )
            if primary
            else None
        )

        alt_resp = (
            CandidateEvaluationResponse(
                material_id=alt.material_id,
                trade_code=alt.trade_code,
                material_name=alt.material_name,
                material_family=alt.material_family,
                structure_type=alt.structure_type,
                eligibility=alt.eligibility,
                rejection_reasons=alt.rejection_reasons,
                condition_notes=alt.condition_notes,
                barrier_safety_score=alt.barrier_safety_score,
                sustainability_score=alt.sustainability_score,
                cost_score=alt.cost_score,
                composite_utility_score=alt.composite_utility_score,
                nominal_thickness_um=alt.nominal_thickness_um,
                nominal_otr=alt.nominal_otr,
                nominal_wvtr=alt.nominal_wvtr,
                is_mono_material=alt.is_mono_material,
                is_biodegradable=alt.is_biodegradable,
                relative_cost_multiplier=alt.relative_cost_multiplier,
                evidence_reference_id=alt.evidence_reference_id,
            )
            if alt
            else None
        )

        ranked_resp = [
            CandidateEvaluationResponse(
                material_id=c.material_id,
                trade_code=c.trade_code,
                material_name=c.material_name,
                material_family=c.material_family,
                structure_type=c.structure_type,
                eligibility=c.eligibility,
                rejection_reasons=c.rejection_reasons,
                condition_notes=c.condition_notes,
                barrier_safety_score=c.barrier_safety_score,
                sustainability_score=c.sustainability_score,
                cost_score=c.cost_score,
                composite_utility_score=c.composite_utility_score,
                nominal_thickness_um=c.nominal_thickness_um,
                nominal_otr=c.nominal_otr,
                nominal_wvtr=c.nominal_wvtr,
                is_mono_material=c.is_mono_material,
                is_biodegradable=c.is_biodegradable,
                relative_cost_multiplier=c.relative_cost_multiplier,
                evidence_reference_id=c.evidence_reference_id,
            )
            for c in domain_result.ranked_candidates
        ]

        disqualified_resp = [
            CandidateEvaluationResponse(
                material_id=c.material_id,
                trade_code=c.trade_code,
                material_name=c.material_name,
                material_family=c.material_family,
                structure_type=c.structure_type,
                eligibility=c.eligibility,
                rejection_reasons=c.rejection_reasons,
                condition_notes=c.condition_notes,
                barrier_safety_score=c.barrier_safety_score,
                sustainability_score=c.sustainability_score,
                cost_score=c.cost_score,
                composite_utility_score=c.composite_utility_score,
                nominal_thickness_um=c.nominal_thickness_um,
                nominal_otr=c.nominal_otr,
                nominal_wvtr=c.nominal_wvtr,
                is_mono_material=c.is_mono_material,
                is_biodegradable=c.is_biodegradable,
                relative_cost_multiplier=c.relative_cost_multiplier,
                evidence_reference_id=c.evidence_reference_id,
            )
            for c in domain_result.disqualified_candidates
        ]

        specs_resp = (
            TargetSpecificationsResponse(
                max_recommended_wvtr=specs.max_recommended_wvtr,
                max_recommended_otr=specs.max_recommended_otr,
                recommended_thickness_um=specs.recommended_thickness_um,
                sealability_required=specs.sealability_required,
                is_light_barrier_required=specs.is_light_barrier_required,
                is_microperforation_required=specs.is_microperforation_required,
                target_wvtr_rationale=specs.target_wvtr_rationale,
                target_otr_rationale=specs.target_otr_rationale,
                thickness_rationale=specs.thickness_rationale,
            )
            if specs
            else None
        )

        expl_resp = (
            ExplanationResponse(
                dominant_spoilage_driver=explanation.dominant_spoilage_driver,
                critical_factors=explanation.critical_factors,
                selection_rationale=explanation.selection_rationale,
                alternative_rationale=explanation.alternative_rationale,
                disqualification_summary=explanation.disqualification_summary,
                cited_evidence_sources=explanation.cited_evidence_sources,
                documented_assumptions=explanation.documented_assumptions,
                scientific_limitations=explanation.scientific_limitations,
            )
            if explanation
            else None
        )

        return RecommendationResponse(
            request_id=request_id,
            status=domain_result.status,
            commodity_id=domain_result.commodity_id,
            commodity_name=domain_result.commodity_name,
            primary_recommendation=primary_resp,
            alternative_recommendation=alt_resp,
            ranked_candidates=ranked_resp,
            disqualified_candidates=disqualified_resp,
            target_specifications=specs_resp,
            explanation=expl_resp,
            safety_advisory=domain_result.safety_advisory,
            uncertainty_notes=domain_result.uncertainty_notes,
            created_at=created_at,
        )

    @staticmethod
    def get_recommendation_by_id(
        db: Session,
        request_id: str,
    ) -> RecommendationResponse | None:
        """Retrieve a previously evaluated recommendation audit session."""
        db_request = RecommendationRepository.get_request_by_id(db, request_id)
        if not db_request:
            return None

        commodity = db_request.commodity
        db_result = db_request.result

        # Reconstruct response model from persisted audit record
        specs_resp: TargetSpecificationsResponse | None = None
        primary_resp: CandidateEvaluationResponse | None = None
        alt_resp: CandidateEvaluationResponse | None = None
        expl_resp: ExplanationResponse | None = None

        if db_result:
            specs_resp = TargetSpecificationsResponse(
                max_recommended_wvtr=db_result.required_wvtr_target,
                max_recommended_otr=db_result.required_otr_target,
                recommended_thickness_um=db_result.recommended_thickness_um,
                sealability_required=db_result.recommended_sealability,
                is_light_barrier_required=commodity.property.is_light_sensitive
                if commodity and commodity.property
                else False,
                is_microperforation_required=commodity.is_respiring if commodity else False,
                target_wvtr_rationale="Retrieved from persisted audit record.",
                target_otr_rationale="Retrieved from persisted audit record.",
                thickness_rationale=db_result.recommended_mechanical_notes,
            )

            pm = db_result.primary_material
            if pm:
                primary_resp = CandidateEvaluationResponse(
                    material_id=pm.material_id,
                    trade_code=pm.trade_code,
                    material_name=pm.name,
                    material_family=pm.material_family,
                    structure_type=pm.structure_type,
                    eligibility=CandidateEligibility.ELIGIBLE,
                    composite_utility_score=0.0,
                )

            alt_m = db_result.alternative_material
            if alt_m:
                alt_resp = CandidateEvaluationResponse(
                    material_id=alt_m.material_id,
                    trade_code=alt_m.trade_code,
                    material_name=alt_m.name,
                    material_family=alt_m.material_family,
                    structure_type=alt_m.structure_type,
                    eligibility=CandidateEligibility.ELIGIBLE,
                    composite_utility_score=0.0,
                )

            expl_resp = ExplanationResponse(
                dominant_spoilage_driver=db_result.explanation_summary,
                disqualification_summary=db_result.disqualified_materials_log or [],
            )

        return RecommendationResponse(
            request_id=db_request.request_id,
            status=RecommendationStatus.SUPPORTED
            if db_result
            else RecommendationStatus.INSUFFICIENT_EVIDENCE,
            commodity_id=db_request.commodity_id,
            commodity_name=commodity.common_name if commodity else db_request.commodity_id,
            primary_recommendation=primary_resp,
            alternative_recommendation=alt_resp,
            ranked_candidates=[primary_resp] if primary_resp else [],
            disqualified_candidates=[],
            target_specifications=specs_resp,
            explanation=expl_resp,
            safety_advisory=None,
            uncertainty_notes=[],
            created_at=db_request.created_at,
        )
