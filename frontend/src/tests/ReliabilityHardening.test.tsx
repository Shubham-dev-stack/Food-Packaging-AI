import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { PrimaryRecommendationCard } from '../components/recommendation/PrimaryRecommendationCard';
import { TradeOffAnalysisCard } from '../components/recommendation/trade-off/TradeOffAnalysisCard';
import { StatusBadge } from '../components/recommendation/StatusBadge';
import { UncertaintyNotesCard } from '../components/recommendation/UncertaintyNotesCard';
import type { CandidateEvaluationResponse } from '../types/api';

describe('Phase 9: Frontend Reliability, Empty States & Decision Boundaries', () => {
  it('1. renders graceful empty state when primary recommendation is null', () => {
    render(
      <PrimaryRecommendationCard
        primary={null}
        targetSpecs={null}
      />
    );

    expect(screen.getByText('No Primary Recommendation Identified')).toBeDefined();
    expect(
      screen.getByText(/candidate materials catalog did not yield an eligible material/i)
    ).toBeDefined();
  });

  it('2. renders clear empty state in TradeOffAnalysisCard when ranked candidates is empty', () => {
    render(
      <TradeOffAnalysisCard
        rankedCandidates={[]}
        currentPreference="balanced"
      />
    );

    expect(
      screen.getByText(/No candidate materials satisfied the required barrier and safety constraints/i)
    ).toBeDefined();
  });

  it('3. displays RESEARCH REQUIRED status badge with distinct cautious styling', () => {
    render(<StatusBadge status="RESEARCH_REQUIRED" size="lg" />);
    const badge = screen.getByText('Research Required');
    expect(badge).toBeDefined();
    expect(badge.parentElement?.className).toContain('text-rose-800');
    expect(badge.parentElement?.className).toContain('bg-rose-50');
  });

  it('4. displays CONDITIONAL status badge with warning styling', () => {
    render(<StatusBadge status="CONDITIONAL" size="lg" />);
    const badge = screen.getByText('Conditional Recommendation');
    expect(badge).toBeDefined();
    expect(badge.parentElement?.className).toContain('text-amber-800');
    expect(badge.parentElement?.className).toContain('bg-amber-50');
  });

  it('5. renders uncertainty notes list with cautionary heading', () => {
    const notes = [
      'Extended target shelf life (500 days): Multi-year permeation carries elevated uncertainty.',
      'Active post-harvest produce respiration requires breathable headspace.',
    ];

    render(<UncertaintyNotesCard uncertaintyNotes={notes} status="SUPPORTED" />);
    expect(screen.getByText(/Uncertainty & Evidence Confidence Profile/i)).toBeDefined();
    expect(
      screen.getByText(/Extended target shelf life \(500 days\): Multi-year permeation/i)
    ).toBeDefined();
  });

  it('6. TradeOffAnalysisCard displays hard vs soft constraint boundary note unconditionally', () => {
    const mockCandidate: CandidateEvaluationResponse = {
      material_id: 'MAT_MET_PET',
      trade_code: 'MET-PET/PE',
      material_name: 'Metallized BoPET / PE Laminate',
      material_family: 'metallized_film',
      structure_type: 'multi_layer_laminate',
      eligibility: 'ELIGIBLE',
      rejection_reasons: [],
      condition_notes: [],
      barrier_safety_score: 0.95,
      sustainability_score: 0.50,
      cost_score: 0.476,
      composite_utility_score: 0.7202,
      barrier_contribution: 0.475,
      sustainability_contribution: 0.150,
      cost_contribution: 0.0952,
      rank: 1,
      nominal_thickness_um: 45.0,
      nominal_otr: 1.2,
      nominal_wvtr: 0.9,
      is_mono_material: false,
      is_biodegradable: false,
      relative_cost_multiplier: 2.1,
      evidence_reference_id: 'REF_ROBERTSON_2012',
    };

    render(
      <TradeOffAnalysisCard
        rankedCandidates={[mockCandidate]}
        currentPreference="balanced"
      />
    );

    expect(
      screen.getByText('Critical Boundary: Hard Constraints vs. Soft Preferences')
    ).toBeDefined();
    expect(
      screen.getByText(/Materials that fail hard physical barriers/i)
    ).toBeDefined();
  });
});
