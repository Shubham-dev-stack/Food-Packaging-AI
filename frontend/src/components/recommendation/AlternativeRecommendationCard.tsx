import React from 'react';
import type { CandidateEvaluationResponse } from '../../types/api';

interface AlternativeRecommendationCardProps {
  alternative: CandidateEvaluationResponse | null;
}

export const AlternativeRecommendationCard: React.FC<AlternativeRecommendationCardProps> = ({
  alternative,
}) => {
  if (!alternative) {
    return null;
  }

  const isConditional = alternative.eligibility === 'CONDITIONALLY_ELIGIBLE';

  return (
    <div className="bg-slate-50 border border-slate-300 rounded-2xl p-6 shadow-xs space-y-5">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-2 border-b border-slate-200 pb-4">
        <div>
          <div className="flex items-center space-x-2">
            <span className="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-slate-200 text-slate-800 border border-slate-300">
              Alternative Recommendation
            </span>
            <span className="text-xs text-slate-500 italic">
              Alternative option for a different engineering or circularity trade-off
            </span>
          </div>
          <h3 className="text-lg font-bold text-slate-900 mt-1">{alternative.material_name}</h3>
          <p className="text-xs text-slate-500 mt-0.5">
            Polymer Family: <span className="font-semibold text-slate-700">{alternative.material_family}</span> • Structure:{' '}
            <span className="font-semibold text-slate-700">{alternative.structure_type.replace('_', ' ')}</span>
          </p>
        </div>

        <div className="flex flex-col items-start sm:items-end">
          <span
            className={`px-2.5 py-0.5 rounded-full text-xs font-bold border ${
              isConditional
                ? 'bg-amber-50 text-amber-800 border-amber-300'
                : 'bg-emerald-50 text-emerald-800 border-emerald-300'
            }`}
          >
            {isConditional ? 'Conditional Option' : 'Eligible Alternative'}
          </span>
          <span className="text-[10px] text-slate-400 mt-0.5 font-mono">
            Trade Code: {alternative.trade_code || 'N/A'}
          </span>
        </div>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-white p-3.5 rounded-xl border border-slate-200 text-xs">
        <div>
          <span className="text-[10px] uppercase font-bold text-slate-400 block">Nominal Gauge</span>
          <span className="font-bold text-slate-800 text-sm">{alternative.nominal_thickness_um} μm</span>
        </div>
        <div>
          <span className="text-[10px] uppercase font-bold text-slate-400 block">OTR</span>
          <span className="font-bold text-slate-800 text-sm">{alternative.nominal_otr}</span>
          <span className="text-[9px] text-slate-400 block">cm³/(m²·day·atm)</span>
        </div>
        <div>
          <span className="text-[10px] uppercase font-bold text-slate-400 block">WVTR</span>
          <span className="font-bold text-slate-800 text-sm">{alternative.nominal_wvtr}</span>
          <span className="text-[9px] text-slate-400 block">g/(m²·day)</span>
        </div>
        <div>
          <span className="text-[10px] uppercase font-bold text-slate-400 block">MCDA Utility</span>
          <span className="font-bold text-emerald-700 text-sm">
            {(alternative.composite_utility_score * 100).toFixed(1)} / 100
          </span>
        </div>
      </div>

      {/* Sustainability & Cost Highlights */}
      <div className="flex flex-wrap gap-2 text-xs">
        {alternative.is_mono_material && (
          <span className="px-2.5 py-1 bg-emerald-100/80 text-emerald-900 rounded-lg font-semibold border border-emerald-200">
            ♻ Recyclable Mono-material
          </span>
        )}
        {alternative.is_biodegradable && (
          <span className="px-2.5 py-1 bg-teal-100/80 text-teal-900 rounded-lg font-semibold border border-teal-200">
            🌱 Bio-based / Biodegradable
          </span>
        )}
        <span className="px-2.5 py-1 bg-slate-200 text-slate-700 rounded-lg font-medium">
          Cost Index: {alternative.relative_cost_multiplier}× LDPE
        </span>
      </div>

      {/* Condition Notes */}
      {alternative.condition_notes.length > 0 && (
        <div className="bg-amber-50/70 border border-amber-200 rounded-xl p-3 text-xs space-y-1">
          <span className="font-bold text-amber-900 block">Trade-off Considerations:</span>
          <ul className="list-disc list-inside space-y-0.5 text-amber-800">
            {alternative.condition_notes.map((note, idx) => (
              <li key={idx}>{note}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};
