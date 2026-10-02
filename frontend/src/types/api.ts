/**
 * Canonical TypeScript interfaces reflecting backend Pydantic API schemas.
 * Derived directly from backend/app/schemas/ and backend/app/domain/types.py.
 */

export type RecommendationStatus =
  | 'SUPPORTED'
  | 'CONDITIONAL'
  | 'INSUFFICIENT_EVIDENCE'
  | 'RESEARCH_REQUIRED';

export type CandidateEligibility =
  | 'ELIGIBLE'
  | 'CONDITIONALLY_ELIGIBLE'
  | 'INSUFFICIENT_EVIDENCE'
  | 'REJECTED';

export type StorageType = 'ambient' | 'chilled' | 'frozen';

export type TransitStress =
  | 'local_standard'
  | 'long_haul_refrigerated'
  | 'rough_terrain_unpaved';

export type OptimizationPreference = 'balanced' | 'sustainability' | 'cost';

export interface RankingWeightsResponse {
  w_barrier: number;
  w_sustainability: number;
  w_cost: number;
}

export interface EvidenceSourceResponse {
  reference_id: string;
  citation_short: string;
  title: string;
  authors: string | null;
  publication_year: number | null;
  source_type: string;
  doi_or_standard_number: string | null;
  notes: string | null;
}

export interface CommodityPropertyResponse {
  property_id: string;
  commodity_id: string;
  critical_water_activity_aw: number;
  typical_moisture_pct: number;
  oil_fat_content_pct: number;
  typical_ph: number;
  primary_spoilage_pathways: string[];
  is_light_sensitive: boolean;
  recommended_temp_min_c: number;
  recommended_temp_max_c: number;
  recommended_rh_min_pct: number;
  recommended_rh_max_pct: number;
  reference_id: string;
  evidence_source?: EvidenceSourceResponse | null;
}

export interface ProduceRespirationResponse {
  respiration_id: string;
  commodity_id: string;
  reference_temp_c: number;
  respiration_rate_co2: number;
  respiration_class: string;
  q10_factor: number;
  critical_o2_extinction_pct: number;
  max_tolerable_co2_pct: number;
  condensation_risk_level: string;
  reference_id: string;
  evidence_source?: EvidenceSourceResponse | null;
}

export interface MAPConfigurationResponse {
  map_id: string;
  commodity_id: string;
  recommended_o2_min_pct: number;
  recommended_o2_max_pct: number;
  recommended_co2_min_pct: number;
  recommended_co2_max_pct: number;
  recommended_n2_pct: number | null;
  target_storage_temp_c: number;
  suitability_status: string;
  application_notes: string | null;
  reference_id: string;
  evidence_source?: EvidenceSourceResponse | null;
}

export interface CommodityBriefResponse {
  commodity_id: string;
  common_name: string;
  scientific_name: string | null;
  category: string;
  is_respiring: boolean;
  default_storage_mode: string;
  description: string | null;
}

export interface CommodityDetailResponse extends CommodityBriefResponse {
  property: CommodityPropertyResponse | null;
  respiration_data: ProduceRespirationResponse[];
  map_configuration: MAPConfigurationResponse | null;
}

export interface RankingWeightsRequest {
  w_barrier: number;
  w_sustainability: number;
  w_cost: number;
}

export interface RecommendationCreateRequest {
  commodity_id: string;
  desired_shelf_life_days: number;
  storage_temp_c: number;
  storage_rh_pct: number;
  storage_type: StorageType;
  transit_stress: TransitStress;
  user_sustainability_preference?: boolean;
  optimization_preference?: OptimizationPreference;

  // Optional commodity property overrides
  moisture_pct?: number | null;
  water_activity_aw?: number | null;
  oil_fat_content_pct?: number | null;
  ph?: number | null;
  respiration_rate_co2?: number | null;

  // Geometry & packaging assumptions [Prototype Defaults]
  package_weight_kg?: number;
  package_area_m2?: number;

  // Optional custom ranking weights
  custom_weights?: RankingWeightsRequest | null;
}

export interface TargetSpecificationsResponse {
  max_recommended_wvtr: number;
  max_recommended_otr: number;
  recommended_thickness_um: number;
  sealability_required: string;
  is_light_barrier_required: boolean;
  is_microperforation_required: boolean;
  target_wvtr_rationale: string;
  target_otr_rationale: string;
  thickness_rationale: string;
  adjusted_respiration_rate_co2?: number | null;
}

export interface CandidateEvaluationResponse {
  material_id: string;
  trade_code: string;
  material_name: string;
  material_family: string;
  structure_type: string;
  eligibility: CandidateEligibility;
  rejection_reasons: string[];
  condition_notes: string[];
  barrier_safety_score: number;
  sustainability_score: number;
  cost_score: number;
  composite_utility_score: number;
  barrier_contribution?: number;
  sustainability_contribution?: number;
  cost_contribution?: number;
  rank?: number;
  nominal_thickness_um: number;
  nominal_otr: number;
  nominal_wvtr: number;
  is_mono_material: boolean;
  is_biodegradable: boolean;
  relative_cost_multiplier: number;
  evidence_reference_id: string;
}

export interface ExplanationResponse {
  dominant_spoilage_driver: string;
  critical_factors: string[];
  selection_rationale: string;
  alternative_rationale: string;
  disqualification_summary: Array<Record<string, unknown>>;
  cited_evidence_sources: string[];
  documented_assumptions: string[];
  scientific_limitations: string[];
}

export interface RecommendationResponse {
  request_id: string;
  status: RecommendationStatus;
  commodity_id: string;
  commodity_name: string;
  primary_recommendation: CandidateEvaluationResponse | null;
  alternative_recommendation: CandidateEvaluationResponse | null;
  ranked_candidates: CandidateEvaluationResponse[];
  disqualified_candidates: CandidateEvaluationResponse[];
  target_specifications: TargetSpecificationsResponse | null;
  explanation: ExplanationResponse | null;
  safety_advisory: string | null;
  uncertainty_notes: string[];
  applied_weights?: RankingWeightsResponse | null;
  optimization_preference?: OptimizationPreference;
  created_at: string;
}

export interface ErrorDetail {
  field?: string | null;
  issue: string;
}

export interface ApiErrorResponse {
  error: string;
  message: string;
  details: ErrorDetail[];
  error_id?: string | null;
}
