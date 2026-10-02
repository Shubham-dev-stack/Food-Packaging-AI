import React from 'react';
import type { ExplanationResponse, TargetSpecificationsResponse } from '../../types/api';

interface DecisionFactorsCardProps {
  explanation: ExplanationResponse | null;
  targetSpecs: TargetSpecificationsResponse | null;
}

export const DecisionFactorsCard: React.FC<DecisionFactorsCardProps> = ({
  explanation,
  targetSpecs,
}) => {
  const factors = explanation?.critical_factors || [];

  if (factors.length === 0 && !targetSpecs) {
    return null;
  }

  return (
    <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs space-y-5">
      <div className="border-b border-slate-200 pb-3">
        <h3 className="text-base font-bold text-slate-900">
          Governing Decision Factors & Constraints
        </h3>
        <p className="text-xs text-slate-500">
          Critical commodity parameters and distribution conditions that constrained candidate selection
        </p>
      </div>

      {/* Critical Factors List */}
      <div className="space-y-3">
        <span className="text-xs font-bold uppercase tracking-wider text-slate-500 block">
          Commodity & Storage Constraints:
        </span>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {factors.map((factor, idx) => (
            <div
              key={idx}
              className="p-3 bg-slate-50 rounded-xl border border-slate-200 text-xs text-slate-700 font-medium flex items-start space-x-2.5"
            >
              <span className="text-emerald-600 font-bold mt-0.5">•</span>
              <span className="leading-relaxed">{factor}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Key Packaging Constraints Breakdown */}
      {targetSpecs && (
        <div className="pt-2 border-t border-slate-200 space-y-3">
          <span className="text-xs font-bold uppercase tracking-wider text-slate-500 block">
            Derived Packaging Constraints:
          </span>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
            <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 space-y-1">
              <span className="text-[10px] font-bold uppercase tracking-wider text-slate-500 block">
                Moisture Bound
              </span>
              <span className="font-bold text-slate-900 block">
                WVTR ≤ {targetSpecs.max_recommended_wvtr} g/(m²·day)
              </span>
              <span className="text-[11px] text-slate-500 block">
                Permissible hydration gain/loss limit
              </span>
            </div>

            <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 space-y-1">
              <span className="text-[10px] font-bold uppercase tracking-wider text-slate-500 block">
                Oxygen Bound
              </span>
              <span className="font-bold text-slate-900 block">
                OTR ≤ {targetSpecs.max_recommended_otr} cm³/(m²·day·atm)
              </span>
              <span className="text-[11px] text-slate-500 block">
                Lipid preservation / respiration cutoff
              </span>
            </div>

            <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 space-y-1">
              <span className="text-[10px] font-bold uppercase tracking-wider text-slate-500 block">
                Gauge Baseline
              </span>
              <span className="font-bold text-slate-900 block">
                Thickness ≥ {targetSpecs.recommended_thickness_um} μm
              </span>
              <span className="text-[11px] text-slate-500 block">
                Transit stress & puncture integrity
              </span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
