import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { RecommendationResultView } from '../pages/RecommendationResultView';
import { api } from '../services/api';
import type { RecommendationResponse, RecommendationCreateRequest } from '../types/api';

const mockRecommendationResponse: RecommendationResponse = {
  request_id: 'REQ-TEST-1234',
  status: 'SUPPORTED',
  commodity_id: 'potato_chips',
  commodity_name: 'Potato Chips',
  primary_recommendation: {
    material_id: 'mat_met_bopet_pe',
    trade_code: 'MET-PET-12',
    material_name: 'Metallized BoPET / PE Laminate',
    material_family: 'metallized_film',
    structure_type: 'multi_layer_laminate',
    eligibility: 'ELIGIBLE',
    rejection_reasons: [],
    condition_notes: ['Ensure hermetic seal integrity to preserve nitrogen flush headspace.'],
    barrier_safety_score: 0.95,
    sustainability_score: 0.40,
    cost_score: 0.70,
    composite_utility_score: 0.735,
    nominal_thickness_um: 47.0,
    nominal_otr: 1.2,
    nominal_wvtr: 0.8,
    is_mono_material: false,
    is_biodegradable: false,
    relative_cost_multiplier: 1.45,
    evidence_reference_id: 'REF_ROBERTSON_2012',
  },
  alternative_recommendation: {
    material_id: 'mat_bope_pe',
    trade_code: 'BOPE-PE-RECYCLE',
    material_name: 'Biaxially Oriented PE / PE Mono-material',
    material_family: 'polyolefin_monomaterial',
    structure_type: 'coextrusion',
    eligibility: 'CONDITIONALLY_ELIGIBLE',
    rejection_reasons: [],
    condition_notes: ['High barrier coating required for shelf life exceeding 90 days.'],
    barrier_safety_score: 0.78,
    sustainability_score: 0.90,
    cost_score: 0.80,
    composite_utility_score: 0.82,
    nominal_thickness_um: 50.0,
    nominal_otr: 15.0,
    nominal_wvtr: 2.5,
    is_mono_material: true,
    is_biodegradable: false,
    relative_cost_multiplier: 1.30,
    evidence_reference_id: 'REF_MARSH_BUGUSU_2007',
  },
  ranked_candidates: [],
  disqualified_candidates: [
    {
      material_id: 'mat_plain_ldpe',
      trade_code: 'LDPE-STD-50',
      material_name: 'Low-Density Polyethylene (LDPE) Monolayer Film',
      material_family: 'LDPE',
      structure_type: 'monolayer',
      eligibility: 'REJECTED',
      rejection_reasons: [
        'WVTR (18.00 g/(m2*day)) exceeds maximum allowable moisture barrier target (1.20 g/(m2*day)).',
      ],
      condition_notes: [],
      barrier_safety_score: 0.0,
      sustainability_score: 0.80,
      cost_score: 1.0,
      composite_utility_score: 0.0,
      nominal_thickness_um: 50.0,
      nominal_otr: 2200.0,
      nominal_wvtr: 18.0,
      is_mono_material: true,
      is_biodegradable: false,
      relative_cost_multiplier: 1.0,
      evidence_reference_id: 'REF_ROBERTSON_2012',
    },
  ],
  target_specifications: {
    max_recommended_wvtr: 1.2,
    max_recommended_otr: 2.0,
    recommended_thickness_um: 45.0,
    sealability_required: 'excellent',
    is_light_barrier_required: true,
    is_microperforation_required: false,
    target_wvtr_rationale: 'Derived from permissible water loss/gain mass balance.',
    target_otr_rationale: 'High lipid sensitivity requires strict oxygen barrier.',
    thickness_rationale: 'Local standard transit mechanical baseline.',
  },
  explanation: {
    dominant_spoilage_driver:
      'Dual vulnerability: moisture-induced loss of crispness combined with lipid oxidation of unsaturated oils.',
    critical_factors: [
      'Storage mode: Ambient at 23 C, 65% RH.',
      'Target shelf life: 180 days.',
      'Food water activity: aw = 0.25; Fat content: 32.0%.',
    ],
    selection_rationale:
      'Selected Metallized BoPET / PE Laminate as primary recommendation because its nominal barrier meets target requirements.',
    alternative_rationale:
      'Recommended Biaxially Oriented PE / PE Mono-material as an alternative because it achieves a superior sustainability score.',
    disqualification_summary: [],
    cited_evidence_sources: ['REF_ROBERTSON_2012', 'REF_ASTM_F1249'],
    documented_assumptions: [
      '[PROTOTYPE ASSUMPTION] Steady-state isothermal mass transfer (no thermal cycling).',
      '[PROTOTYPE ASSUMPTION] Standard pouch geometry baseline (100g food / 0.06 m2 area).',
    ],
    scientific_limitations: [
      'Recommendations represent engineering decision-support estimates and do NOT constitute accredited laboratory test validation.',
      'Standard test methods: OTR measured under ASTM D3985-17; WVTR measured under ASTM F1249-20.',
    ],
  },
  safety_advisory: 'Advisory: Verify hermetic seal testing to prevent Clostridium botulinum risk.',
  uncertainty_notes: [
    'Empirical Arrhenius acceleration assumes constant moisture isotherm slope over duration.',
  ],
  created_at: '2026-10-02T12:00:00Z',
};

const mockSubmittedInput: RecommendationCreateRequest = {
  commodity_id: 'potato_chips',
  desired_shelf_life_days: 180,
  storage_temp_c: 23.0,
  storage_rh_pct: 65.0,
  storage_type: 'ambient',
  transit_stress: 'local_standard',
};

describe('Phase 6: Recommendation Result & Explainability Experience', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
    vi.spyOn(api, 'getEvidence').mockImplementation(async (refId: string) => {
      if (refId === 'REF_ROBERTSON_2012') {
        return {
          reference_id: 'REF_ROBERTSON_2012',
          citation_short: 'Robertson 2012',
          title: 'Food Packaging: Principles and Practice, 3rd Edition',
          authors: 'Gordon L. Robertson',
          publication_year: 2012,
          source_type: 'textbook',
          doi_or_standard_number: 'ISBN 978-1439862414',
          notes: 'Foundational textbook reference on polymer barrier physics.',
        };
      }
      if (refId === 'REF_ASTM_F1249') {
        return {
          reference_id: 'REF_ASTM_F1249',
          citation_short: 'ASTM F1249 (2020)',
          title: 'Standard Test Method for Water Vapor Transmission Rate',
          authors: 'ASTM Committee F02',
          publication_year: 2020,
          source_type: 'standards_document',
          doi_or_standard_number: 'ASTM F1249-20',
          notes: 'Infrared modulated sensor test method.',
        };
      }
      throw new Error('Not found');
    });
  });

  it('1. renders recommendation result, status semantics, and commodity name', () => {
    render(
      <RecommendationResultView
        result={mockRecommendationResponse}
        submittedInput={mockSubmittedInput}
        onModifyInputs={vi.fn()}
        onNewEvaluation={vi.fn()}
      />
    );

    expect(screen.getByText(/Packaging Recommendation: Potato Chips/i)).toBeDefined();
    expect(screen.getByText(/Supported Recommendation/i)).toBeDefined();
    expect(screen.getByText(/Session Request ID: REQ-TEST-1234/i)).toBeDefined();
  });

  it('2. renders selection rationale and dominant spoilage driver in "Why this recommendation?"', () => {
    render(
      <RecommendationResultView
        result={mockRecommendationResponse}
        submittedInput={mockSubmittedInput}
        onModifyInputs={vi.fn()}
        onNewEvaluation={vi.fn()}
      />
    );

    expect(screen.getByText(/Why This Recommendation\?/i)).toBeDefined();
    expect(
      screen.getByText(/Dual vulnerability: moisture-induced loss of crispness combined with lipid oxidation/i)
    ).toBeDefined();
    expect(
      screen.getByText(/Selected Metallized BoPET \/ PE Laminate as primary recommendation/i)
    ).toBeDefined();
  });

  it('3. renders governing decision factors and constraints', () => {
    render(
      <RecommendationResultView
        result={mockRecommendationResponse}
        submittedInput={mockSubmittedInput}
        onModifyInputs={vi.fn()}
        onNewEvaluation={vi.fn()}
      />
    );

    expect(screen.getByText(/Governing Decision Factors & Constraints/i)).toBeDefined();
    expect(screen.getByText(/Storage mode: Ambient at 23 C, 65% RH\./i)).toBeDefined();
    expect(screen.getByText(/Food water activity: aw = 0\.25; Fat content: 32\.0%\./i)).toBeDefined();
  });

  it('4. renders why other candidates were rejected in disqualified candidates list', () => {
    render(
      <RecommendationResultView
        result={mockRecommendationResponse}
        submittedInput={mockSubmittedInput}
        onModifyInputs={vi.fn()}
        onNewEvaluation={vi.fn()}
      />
    );

    expect(screen.getByText(/Why Other Candidates Were Not Selected/i)).toBeDefined();
    // Expand accordion
    const toggleBtn = screen.getByText(/Why Other Candidates Were Not Selected/i);
    fireEvent.click(toggleBtn);

    expect(screen.getByText(/Low-Density Polyethylene \(LDPE\) Monolayer Film/i)).toBeDefined();
    expect(
      screen.getByText(/WVTR \(18\.00 g\/\(m2\*day\)\) exceeds maximum allowable moisture barrier target/i)
    ).toBeDefined();
  });

  it('5. resolves evidence citations through API and renders metadata', async () => {
    render(
      <RecommendationResultView
        result={mockRecommendationResponse}
        submittedInput={mockSubmittedInput}
        onModifyInputs={vi.fn()}
        onNewEvaluation={vi.fn()}
      />
    );

    expect(screen.getByText(/Scientific Evidence Traceability/i)).toBeDefined();

    await waitFor(() => {
      expect(screen.getByText(/Robertson 2012/i)).toBeDefined();
      expect(screen.getByText(/ASTM F1249 \(2020\)/i)).toBeDefined();
    });

    expect(
      screen.getByText(/Food Packaging: Principles and Practice, 3rd Edition/i)
    ).toBeDefined();
  });

  it('6. handles missing or unresolvable evidence gracefully without crashing', async () => {
    const responseWithMissingEvidence: RecommendationResponse = {
      ...mockRecommendationResponse,
      explanation: {
        ...mockRecommendationResponse.explanation!,
        cited_evidence_sources: ['REF_UNKNOWN_NONEXISTENT'],
      },
    };

    render(
      <RecommendationResultView
        result={responseWithMissingEvidence}
        submittedInput={mockSubmittedInput}
        onModifyInputs={vi.fn()}
        onNewEvaluation={vi.fn()}
      />
    );

    await waitFor(() => {
      expect(screen.getByText(/REF_UNKNOWN_NONEXISTENT/i)).toBeDefined();
      expect(screen.getByText(/Unresolved Reference/i)).toBeDefined();
    });
  });

  it('7. renders documented assumptions panel', () => {
    render(
      <RecommendationResultView
        result={mockRecommendationResponse}
        submittedInput={mockSubmittedInput}
        onModifyInputs={vi.fn()}
        onNewEvaluation={vi.fn()}
      />
    );

    expect(screen.getByText(/Documented Engineering Assumptions/i)).toBeDefined();
    const btn = screen.getByText(/Documented Engineering Assumptions/i);
    fireEvent.click(btn);

    expect(
      screen.getByText(/Steady-state isothermal mass transfer \(no thermal cycling\)\./i)
    ).toBeDefined();
  });

  it('8. renders scientific limitations and boundaries panel', () => {
    render(
      <RecommendationResultView
        result={mockRecommendationResponse}
        submittedInput={mockSubmittedInput}
        onModifyInputs={vi.fn()}
        onNewEvaluation={vi.fn()}
      />
    );

    expect(screen.getByText(/Scientific Limitations & Testing Boundaries/i)).toBeDefined();
    const btn = screen.getByText(/Scientific Limitations & Testing Boundaries/i);
    fireEvent.click(btn);

    expect(
      screen.getByText(
        /Recommendations represent engineering decision-support estimates and do NOT constitute accredited laboratory test validation/i
      )
    ).toBeDefined();
  });

  it('9. renders contextual safety advisory banner when returned', () => {
    render(
      <RecommendationResultView
        result={mockRecommendationResponse}
        submittedInput={mockSubmittedInput}
        onModifyInputs={vi.fn()}
        onNewEvaluation={vi.fn()}
      />
    );

    expect(
      screen.getByText(/Contextual Food Safety Advisory \(Decision-Support Warning\)/i)
    ).toBeDefined();
    expect(
      screen.getByText(/Advisory: Verify hermetic seal testing to prevent Clostridium botulinum risk\./i)
    ).toBeDefined();
  });

  it('10. renders uncertainty notes and confidence evaluation', () => {
    render(
      <RecommendationResultView
        result={mockRecommendationResponse}
        submittedInput={mockSubmittedInput}
        onModifyInputs={vi.fn()}
        onNewEvaluation={vi.fn()}
      />
    );

    expect(screen.getByText(/Uncertainty & Evidence Confidence Profile/i)).toBeDefined();
    expect(
      screen.getByText(
        /Empirical Arrhenius acceleration assumes constant moisture isotherm slope over duration\./i
      )
    ).toBeDefined();
  });
});
