import React from 'react';
import type { CandidateEvaluationResponse, TargetSpecificationsResponse } from '../../types/api';

interface PrimaryRecommendationCardProps {
  primary: CandidateEvaluationResponse | null;
  targetSpecs: TargetSpecificationsResponse | null;
}

export const PrimaryRecommendationCard: React.FC<PrimaryRecommendationCardProps> = ({
  primary,
  targetSpecs,
}) => {
  if (!primary) {
    return (
      <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs text-center space-y-2">
        <span className="text-2xl">🔍</span>
        <h3 className="text-base font-bold text-slate-800">No Primary Recommendation Identified</h3>
        <p className="text-xs text-slate-500 max-w-md mx-auto">
          The candidate materials catalog did not yield an eligible material meeting the specified
          barrier, temperature, or chemical criteria. Inspect the disqualified candidates and
          uncertainty notes below.
        </p>
      </div>
    );
  }

  const isConditional = primary.eligibility === 'CONDITIONALLY_ELIGIBLE';

  return (
    <div className="bg-white border-2 border-emerald-600/80 rounded-2xl p-6 shadow-sm space-y-6 relative overflow-hidden">
      {/* Header Accent Bar */}
      <div className="absolute top-0 left-0 right-0 h-1.5 bg-gradient-to-r from-emerald-600 to-teal-500" />

      {/* Title & Eligibility */}
      <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-3">
        <div>
          <div className="flex items-center space-x-2">
            <span className="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-emerald-100 text-emerald-800 border border-emerald-300">
              Primary Recommendation
            </span>
            <span className="text-xs text-slate-400 font-mono">
              Trade Code: {primary.trade_code || 'N/A'}
            </span>
          </div>
          <h2 className="text-xl font-bold text-slate-900 mt-1">{primary.material_name}</h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Polymer Family: <span className="font-semibold text-slate-700">{primary.material_family}</span> • Structure:{' '}
            <span className="font-semibold text-slate-700">{primary.structure_type.replace('_', ' ')}</span>
          </p>
        </div>

        <div className="flex flex-col items-start sm:items-end">
          <span
            className={`px-3 py-1 rounded-full text-xs font-bold border ${
              isConditional
                ? 'bg-amber-50 text-amber-800 border-amber-300'
                : 'bg-emerald-50 text-emerald-800 border-emerald-300'
            }`}
          >
            {isConditional ? 'Conditional Recommendation' : 'Eligible Candidate'}
          </span>
          <span className="text-[10px] text-slate-400 mt-1">Prototype Estimate</span>
        </div>
      </div>

      {/* Key Metric Highlights Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-slate-50 p-4 rounded-xl border border-slate-200">
        <div>
          <span className="text-[10px] uppercase font-bold text-slate-400 block tracking-wider">
            Nominal Gauge
          </span>
          <span className="text-base font-bold text-slate-800">{primary.nominal_thickness_um} μm</span>
          <span className="text-[10px] text-slate-400 block">
            {(primary.nominal_thickness_um / 25.4).toFixed(2)} mil
          </span>
        </div>

        <div>
          <span className="text-[10px] uppercase font-bold text-slate-400 block tracking-wider">
            OTR Value
          </span>
          <span className="text-base font-bold text-slate-800">{primary.nominal_otr}</span>
          <span className="text-[10px] text-slate-400 block">cm³/(m²·day·atm)</span>
        </div>

        <div>
          <span className="text-[10px] uppercase font-bold text-slate-400 block tracking-wider">
            WVTR Value
          </span>
          <span className="text-base font-bold text-slate-800">{primary.nominal_wvtr}</span>
          <span className="text-[10px] text-slate-400 block">g/(m²·day)</span>
        </div>

        <div>
          <span className="text-[10px] uppercase font-bold text-slate-400 block tracking-wider">
            MCDA Utility
          </span>
          <span className="text-base font-bold text-emerald-700">
            {(primary.composite_utility_score * 100).toFixed(1)} / 100
          </span>
          <span className="text-[10px] text-slate-400 block">Configured weighting</span>
        </div>
      </div>

      {/* Technical Specifications Summary */}
      <div className="space-y-3">
        <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500">
          Technical Properties & Conversion Context
        </h4>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
          <div className="flex items-center justify-between p-2.5 bg-white border border-slate-200 rounded-lg">
            <span className="text-slate-600 font-medium">Circularity / Mono-Material:</span>
            <span className="font-semibold text-slate-800">
              {primary.is_mono_material ? 'Yes (Mono-material)' : 'Multi-layer laminate'}
            </span>
          </div>

          <div className="flex items-center justify-between p-2.5 bg-white border border-slate-200 rounded-lg">
            <span className="text-slate-600 font-medium">Biodegradability:</span>
            <span className="font-semibold text-slate-800">
              {primary.is_biodegradable ? 'Industrial Compostable / Biodegradable' : 'Non-biodegradable polymer'}
            </span>
          </div>

          <div className="flex items-center justify-between p-2.5 bg-white border border-slate-200 rounded-lg">
            <span className="text-slate-600 font-medium">Relative Economic Index:</span>
            <span className="font-semibold text-slate-800">
              {primary.relative_cost_multiplier}× LDPE baseline
            </span>
          </div>

          <div className="flex items-center justify-between p-2.5 bg-white border border-slate-200 rounded-lg">
            <span className="text-slate-600 font-medium">Sealability Requirement:</span>
            <span className="font-semibold text-slate-800 capitalize">
              {targetSpecs ? targetSpecs.sealability_required : 'Standard'}
            </span>
          </div>
        </div>
      </div>

      {/* Condition Notes where applicable */}
      {primary.condition_notes.length > 0 && (
        <div className="bg-amber-50/70 border border-amber-200 rounded-xl p-3.5 space-y-1.5">
          <div className="flex items-center space-x-1.5 text-xs font-bold text-amber-900">
            <span>⚠</span>
            <span>Application Conditions & Engineering Assumptions:</span>
          </div>
          <ul className="list-disc list-inside space-y-1 text-xs text-amber-800">
            {primary.condition_notes.map((note, idx) => (
              <li key={idx} className="leading-relaxed">
                {note}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Scientific Citation Provenance */}
      {primary.evidence_reference_id && (
        <div className="pt-2 border-t border-slate-100 flex items-center justify-between text-[11px] text-slate-500">
          <span>Evidence Citation:</span>
          <span className="font-mono bg-slate-100 px-2 py-0.5 rounded text-slate-700">
            {primary.evidence_reference_id}
          </span>
        </div>
      )}
    </div>
  );
};
