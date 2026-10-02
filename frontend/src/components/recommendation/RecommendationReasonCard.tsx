import React from 'react';
import type { ExplanationResponse } from '../../types/api';

interface RecommendationReasonCardProps {
  explanation: ExplanationResponse | null;
}

export const RecommendationReasonCard: React.FC<RecommendationReasonCardProps> = ({
  explanation,
}) => {
  if (!explanation) {
    return null;
  }

  return (
    <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs space-y-5">
      {/* Section Header */}
      <div className="border-b border-slate-200 pb-3 flex items-center justify-between">
        <div>
          <h3 className="text-base font-bold text-slate-900">
            Why This Recommendation?
          </h3>
          <p className="text-xs text-slate-500">
            Deterministic explanation synthesized from commodity biology, food physics, and barrier kinetics
          </p>
        </div>
        <span className="px-2.5 py-1 rounded-full text-[10px] font-bold bg-slate-100 text-slate-700 uppercase tracking-wider">
          Decision Rationale
        </span>
      </div>

      {/* Dominant Spoilage Driver */}
      <div className="bg-emerald-50/60 border border-emerald-200 rounded-xl p-4 space-y-1.5">
        <span className="text-[10px] font-bold uppercase tracking-wider text-emerald-800 block">
          Dominant Spoilage Mechanism (Governing Decay Vector)
        </span>
        <p className="text-xs font-semibold text-emerald-950 leading-relaxed">
          {explanation.dominant_spoilage_driver}
        </p>
      </div>

      {/* Selection Rationale */}
      <div className="space-y-1.5">
        <span className="text-xs font-bold uppercase tracking-wider text-slate-500 block">
          Primary Material Selection Rationale
        </span>
        <div className="text-xs text-slate-800 leading-relaxed bg-slate-50 p-4 rounded-xl border border-slate-200 font-medium">
          {explanation.selection_rationale}
        </div>
      </div>

      {/* Alternative Rationale if available */}
      {explanation.alternative_rationale && (
        <div className="space-y-1.5 pt-2 border-t border-slate-100">
          <span className="text-xs font-bold uppercase tracking-wider text-slate-500 block">
            Alternative Selection Rationale (Different Engineering Trade-off)
          </span>
          <div className="text-xs text-slate-700 leading-relaxed bg-slate-50 p-3.5 rounded-xl border border-slate-200">
            {explanation.alternative_rationale}
          </div>
        </div>
      )}
    </div>
  );
};
