import React from 'react';
import { StatusBadge } from '../components/recommendation/StatusBadge';
import { PrimaryRecommendationCard } from '../components/recommendation/PrimaryRecommendationCard';
import { AlternativeRecommendationCard } from '../components/recommendation/AlternativeRecommendationCard';
import { TechnicalSpecificationGrid } from '../components/recommendation/TechnicalSpecificationGrid';
import { CandidateComparisonTable } from '../components/recommendation/CandidateComparisonTable';
import { DisqualifiedCandidatesList } from '../components/recommendation/DisqualifiedCandidatesList';
import { SafetyAdvisoryBanner } from '../components/recommendation/SafetyAdvisoryBanner';
import { RecommendationReasonCard } from '../components/recommendation/RecommendationReasonCard';
import { DecisionFactorsCard } from '../components/recommendation/DecisionFactorsCard';
import { EvidenceTracePanel } from '../components/recommendation/EvidenceTracePanel';
import { AssumptionsPanel } from '../components/recommendation/AssumptionsPanel';
import { UncertaintyNotesCard } from '../components/recommendation/UncertaintyNotesCard';
import { LimitationsPanel } from '../components/recommendation/LimitationsPanel';
import type { RecommendationResponse, RecommendationCreateRequest } from '../types/api';

interface RecommendationResultViewProps {
  result: RecommendationResponse;
  submittedInput: RecommendationCreateRequest | null;
  onModifyInputs: () => void;
  onNewEvaluation: () => void;
}

export const RecommendationResultView: React.FC<RecommendationResultViewProps> = ({
  result,
  submittedInput,
  onModifyInputs,
  onNewEvaluation,
}) => {
  const explanation = result.explanation;
  const citedSources = explanation?.cited_evidence_sources || [];
  const assumptions = explanation?.documented_assumptions || [];
  const limitations = explanation?.scientific_limitations || [];

  return (
    <div className="space-y-8 animate-fade-in pb-12">
      {/* 1. Header / Breadcrumb & Action bar */}
      <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="flex items-center space-x-3">
            <h1 className="text-xl font-bold text-slate-900">
              Packaging Recommendation: {result.commodity_name}
            </h1>
          </div>
          <p className="text-xs text-slate-500 font-mono">
            Session Request ID: {result.request_id} • Evaluated:{' '}
            {new Date(result.created_at).toLocaleString()}
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <button
            type="button"
            onClick={onModifyInputs}
            className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded-xl transition cursor-pointer flex items-center space-x-1.5"
          >
            <span>←</span>
            <span>Review & Modify Inputs</span>
          </button>
          <button
            type="button"
            onClick={onNewEvaluation}
            className="px-4 py-2 bg-emerald-700 hover:bg-emerald-800 text-white text-xs font-bold rounded-xl transition cursor-pointer shadow-xs"
          >
            New Evaluation
          </button>
        </div>
      </div>

      {/* Decision Status Semantics Banner */}
      <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="space-y-1">
          <span className="text-[10px] uppercase font-bold tracking-wider text-slate-400 block">
            Scientific Decision Evidence Status
          </span>
          <StatusBadge status={result.status} size="lg" />
        </div>

        {submittedInput && (
          <div className="text-xs text-slate-500 bg-slate-50 p-3 rounded-xl border border-slate-200 space-y-1">
            <span className="font-semibold text-slate-700 block">Submitted Evaluation Context:</span>
            <div className="flex flex-wrap gap-x-4 gap-y-1 text-[11px]">
              <span>Shelf Life: {submittedInput.desired_shelf_life_days} days</span>
              <span>
                Regime: {submittedInput.storage_type} ({submittedInput.storage_temp_c}°C)
              </span>
              <span>RH: {submittedInput.storage_rh_pct}%</span>
              <span>Stress: {submittedInput.transit_stress.replace('_', ' ')}</span>
            </div>
          </div>
        )}
      </div>

      {/* Contextual Food Safety Advisory (if returned) */}
      <SafetyAdvisoryBanner advisory={result.safety_advisory} />

      {/* 2. Primary Recommendation Card */}
      <PrimaryRecommendationCard
        primary={result.primary_recommendation}
        targetSpecs={result.target_specifications}
      />

      {/* 3. Why This Recommendation? (Dominant spoilage driver & selection rationale) */}
      <RecommendationReasonCard
        explanation={explanation}
      />

      {/* 4. Governing Decision Factors & Packaging Constraints */}
      <DecisionFactorsCard
        explanation={explanation}
        targetSpecs={result.target_specifications}
      />

      {/* 5. Technical Specifications Grid (OTR, WVTR, Gauge, Rationale) */}
      <TechnicalSpecificationGrid targetSpecs={result.target_specifications} />

      {/* 6. Alternative Recommendation Card */}
      {result.alternative_recommendation && (
        <div className="space-y-2">
          <AlternativeRecommendationCard alternative={result.alternative_recommendation} />
        </div>
      )}

      {/* 7. Candidate Comparison Matrix */}
      <CandidateComparisonTable candidates={result.ranked_candidates} />

      {/* 8. Disqualified Candidates (Why other candidates were not selected) */}
      <DisqualifiedCandidatesList disqualified={result.disqualified_candidates} />

      {/* 9. Scientific Evidence Traceability Panel & Citation Modal */}
      <EvidenceTracePanel citedSourceIds={citedSources} />

      {/* 10. Documented Engineering Assumptions Panel */}
      <AssumptionsPanel assumptions={assumptions} />

      {/* 11. Uncertainty Profile & Decision Status */}
      <UncertaintyNotesCard
        uncertaintyNotes={result.uncertainty_notes}
        status={result.status}
      />

      {/* 12. Scientific Limitations & Boundaries */}
      <LimitationsPanel limitations={limitations} />
    </div>
  );
};
