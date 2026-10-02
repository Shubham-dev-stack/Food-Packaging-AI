import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { TradeOffAnalysisCard } from '../components/recommendation/trade-off/TradeOffAnalysisCard';
import { RecommendationResultView } from '../pages/RecommendationResultView';
import type {
  RecommendationResponse,
  CandidateEvaluationResponse,
  RecommendationCreateRequest,
} from '../types/api';

const mockRankedCandidates: CandidateEvaluationResponse[] = [
  {
    material_id: 'MAT_BOPE_PE',
    trade_code: 'BoPE/PE-Mono',
    material_name: 'Biaxially Oriented All-PE Mono-Material',
    material_family: 'polyethylene_mono',
    structure_type: 'laminate',
    eligibility: 'ELIGIBLE',
    rejection_reasons: [],
    condition_notes: [],
    barrier_safety_score: 0.85,
    sustainability_score: 1.0,
    cost_score: 0.526,
    composite_utility_score: 0.7877,
    barrier_contribution: 0.34,
    sustainability_contribution: 0.45,
    cost_contribution: 0.0789,
    rank: 1,
    nominal_thickness_um: 50.0,
    nominal_otr: 45.0,
    nominal_wvtr: 1.2,
    is_mono_material: true,
    is_biodegradable: false,
    relative_cost_multiplier: 1.9,
    evidence_reference_id: 'REF_ROBERTSON_2012',
  },
  {
    material_id: 'MAT_MET_PET_PE',
    trade_code: 'MET-PET/PE',
    material_name: 'Vacuum Metallized BoPET/PE Laminate',
    material_family: 'metallized_film',
    structure_type: 'laminate',
    eligibility: 'ELIGIBLE',
    rejection_reasons: [],
    condition_notes: [],
    barrier_safety_score: 1.0,
    sustainability_score: 0.5,
    cost_score: 0.476,
    composite_utility_score: 0.7214,
    barrier_contribution: 0.40,
    sustainability_contribution: 0.225,
    cost_contribution: 0.0714,
    rank: 2,
    nominal_thickness_um: 45.0,
    nominal_otr: 1.0,
    nominal_wvtr: 0.8,
    is_mono_material: false,
    is_biodegradable: false,
    relative_cost_multiplier: 2.1,
    evidence_reference_id: 'REF_ROBERTSON_2012',
  },
];

const mockDisqualifiedCandidates: CandidateEvaluationResponse[] = [
  {
    material_id: 'MAT_LDPE_25',
    trade_code: 'LDPE-25',
    material_name: 'Monolayer Low-Density Polyethylene',
    material_family: 'polyolefin',
    structure_type: 'monolayer',
    eligibility: 'REJECTED',
    rejection_reasons: [
      'Nominal WVTR (16.0 g/(m²·day)) exceeds supported requirement limit (≤ 2.5 g/(m²·day)).',
    ],
    condition_notes: [],
    barrier_safety_score: 0.1,
    sustainability_score: 1.0,
    cost_score: 1.0,
    composite_utility_score: 0.45,
    rank: 0,
    nominal_thickness_um: 25.0,
    nominal_otr: 450.0,
    nominal_wvtr: 16.0,
    is_mono_material: true,
    is_biodegradable: false,
    relative_cost_multiplier: 1.0,
    evidence_reference_id: 'REF_ASTM_F1249',
  },
];

const mockFullRecommendation: RecommendationResponse = {
  request_id: 'test-req-phase8-001',
  status: 'SUPPORTED',
  commodity_id: 'COMM_POTATO_CHIPS',
  commodity_name: 'Fried Potato Chips',
  primary_recommendation: mockRankedCandidates[0],
  alternative_recommendation: mockRankedCandidates[1],
  ranked_candidates: mockRankedCandidates,
  disqualified_candidates: mockDisqualifiedCandidates,
  target_specifications: {
    max_recommended_wvtr: 2.5,
    max_recommended_otr: 2.5,
    recommended_thickness_um: 65.0,
    sealability_required: 'excellent',
    is_light_barrier_required: true,
    is_microperforation_required: false,
    target_wvtr_rationale: 'Crispness preservation requiring strict moisture barrier.',
    target_otr_rationale: 'Lipid oxidation suppression.',
    thickness_rationale: 'Transport handling puncture baseline.',
  },
  explanation: {
    dominant_spoilage_driver: 'Moisture uptake risks sogginess loss.',
    critical_factors: ['Moisture sensitivity (aw < 0.25)', 'High lipid rancidity risk'],
    selection_rationale: 'BoPE/PE provides verified barrier protection with mono-material circularity.',
    alternative_rationale: 'MET-PET/PE offers higher barrier margin with metallized laminate structure.',
    disqualification_summary: [],
    cited_evidence_sources: ['REF_ROBERTSON_2012'],
    documented_assumptions: ['Nominal pouch geometry: 100g weight.'],
    scientific_limitations: ['ASTM lab tests at 23C/37.8C.'],
  },
  safety_advisory: null,
  uncertainty_notes: [],
  applied_weights: {
    w_barrier: 0.40,
    w_sustainability: 0.45,
    w_cost: 0.15,
  },
  optimization_preference: 'sustainability',
  created_at: new Date().toISOString(),
};

const mockSubmittedInput: RecommendationCreateRequest = {
  commodity_id: 'COMM_POTATO_CHIPS',
  desired_shelf_life_days: 180,
  storage_temp_c: 25.0,
  storage_rh_pct: 65.0,
  storage_type: 'ambient',
  transit_stress: 'local_standard',
  optimization_preference: 'sustainability',
};

describe('Phase 8: Multi-Criteria Optimization & Trade-Off Analysis', () => {
  it('1. renders TradeOffAnalysisCard with section header and MCDA tag', () => {
    render(
      <TradeOffAnalysisCard
        rankedCandidates={mockRankedCandidates}
        currentPreference="sustainability"
        appliedWeights={mockFullRecommendation.applied_weights}
      />
    );

    expect(
      screen.getByText(/Multi-Criteria Optimization & Trade-Off Analysis/i)
    ).toBeDefined();
    expect(screen.getByText(/MCDA Utility Model/i)).toBeDefined();
  });

  it('2. displays active preference preset and weight distribution bar', () => {
    render(
      <TradeOffAnalysisCard
        rankedCandidates={mockRankedCandidates}
        currentPreference="sustainability"
        appliedWeights={{ w_barrier: 0.4, w_sustainability: 0.45, w_cost: 0.15 }}
      />
    );

    // Active weights in legend and bar
    expect(screen.getByText(/Barrier Performance \(40%\)/i)).toBeDefined();
    expect(screen.getByText(/Sustainability & Circularity \(45%\)/i)).toBeDefined();
    expect(screen.getByText(/Economic Cost Index \(15%\)/i)).toBeDefined();
  });

  it('3. renders candidate factor contributions from API data in breakdown table', () => {
    render(
      <TradeOffAnalysisCard
        rankedCandidates={mockRankedCandidates}
        currentPreference="sustainability"
        appliedWeights={{ w_barrier: 0.4, w_sustainability: 0.45, w_cost: 0.15 }}
      />
    );

    // Rank 1 candidate trade code
    expect(screen.getByText('BoPE/PE-Mono • laminate')).toBeDefined();
    // Rank 2 candidate trade code
    expect(screen.getByText('MET-PET/PE • laminate')).toBeDefined();

    // Check contribution values rendered
    expect(screen.getByText('0.3400')).toBeDefined(); // barrier contrib
    expect(screen.getByText('0.4500')).toBeDefined(); // sust contrib
    expect(screen.getByText('0.7877')).toBeDefined(); // composite utility score
  });

  it('4. invokes onPreferenceChange callback when preference tab is clicked', () => {
    const handlePrefChange = vi.fn();
    render(
      <TradeOffAnalysisCard
        rankedCandidates={mockRankedCandidates}
        currentPreference="balanced"
        appliedWeights={{ w_barrier: 0.5, w_sustainability: 0.3, w_cost: 0.2 }}
        onPreferenceChange={handlePrefChange}
      />
    );

    const sustButton = screen.getByRole('tab', { name: /Sustainability-Focused/i });
    fireEvent.click(sustButton);

    expect(handlePrefChange).toHaveBeenCalledTimes(1);
    expect(handlePrefChange).toHaveBeenCalledWith('sustainability');
  });

  it('5. hard-disqualified candidates do NOT appear in the qualified trade-off matrix', () => {
    render(
      <TradeOffAnalysisCard
        rankedCandidates={mockRankedCandidates}
        currentPreference="balanced"
      />
    );

    // LDPE-25 was rejected for potato chips; must not be in the trade-off qualified table
    expect(screen.queryByText('LDPE-25')).toBeNull();
  });

  it('6. renders clear distinction between hard constraints and soft preferences', () => {
    render(
      <TradeOffAnalysisCard
        rankedCandidates={mockRankedCandidates}
        currentPreference="cost"
        appliedWeights={{ w_barrier: 0.4, w_sustainability: 0.15, w_cost: 0.45 }}
      />
    );

    expect(
      screen.getByText(/Critical Boundary: Hard Constraints vs. Soft Preferences/i)
    ).toBeDefined();
    expect(
      screen.getByText(/cannot be recommended/i)
    ).toBeDefined();
  });

  it('7. integrates cleanly into RecommendationResultView alongside explainability panels', () => {
    render(
      <RecommendationResultView
        result={mockFullRecommendation}
        submittedInput={mockSubmittedInput}
        onModifyInputs={vi.fn()}
        onNewEvaluation={vi.fn()}
        onPreferenceChange={vi.fn()}
      />
    );

    // Trade-off card must be present
    expect(
      screen.getByText(/Multi-Criteria Optimization & Trade-Off Analysis/i)
    ).toBeDefined();

    // Explainability panels must remain present without regression
    expect(screen.getByText(/Why This Recommendation\?/i)).toBeDefined();
    expect(screen.getByText(/Governing Decision Factors & Constraints/i)).toBeDefined();
    expect(screen.getByText(/Target Engineering Specifications/i)).toBeDefined();
    expect(screen.getByText(/Documented Engineering Assumptions/i)).toBeDefined();
    expect(screen.getByText(/Scientific Limitations & Testing Boundaries/i)).toBeDefined();
  });
});
