import React from 'react';
import type { CandidateEvaluationResponse, CandidateEligibility } from '../../types/api';

interface CandidateComparisonTableProps {
  candidates: CandidateEvaluationResponse[];
}

export const CandidateComparisonTable: React.FC<CandidateComparisonTableProps> = ({
  candidates,
}) => {
  if (candidates.length === 0) {
    return (
      <div className="bg-slate-50 border border-slate-200 rounded-2xl p-6 text-center text-xs text-slate-500">
        No candidate materials were evaluated for this commodity scenario.
      </div>
    );
  }

  const getEligibilityBadge = (eligibility: CandidateEligibility) => {
    switch (eligibility) {
      case 'ELIGIBLE':
        return (
          <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800 border border-emerald-300">
            Eligible
          </span>
        );
      case 'CONDITIONALLY_ELIGIBLE':
        return (
          <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-100 text-amber-800 border border-amber-300">
            Conditional
          </span>
        );
      case 'INSUFFICIENT_EVIDENCE':
        return (
          <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-orange-100 text-orange-800 border border-orange-300">
            Insufficient Evidence
          </span>
        );
      case 'REJECTED':
        return (
          <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-rose-100 text-rose-800 border border-rose-300">
            Rejected
          </span>
        );
      default:
        return (
          <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-100 text-slate-800">
            {eligibility}
          </span>
        );
    }
  };

  return (
    <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs space-y-4">
      <div className="border-b border-slate-200 pb-3">
        <h3 className="text-base font-bold text-slate-900">
          Candidate Materials Comparison Matrix
        </h3>
        <p className="text-xs text-slate-500">
          MCDA composite utility ranking across barrier safety margin, circularity, and relative cost index
        </p>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse text-xs">
          <thead>
            <tr className="border-b border-slate-200 bg-slate-50/80 text-slate-500 font-semibold uppercase tracking-wider text-[10px]">
              <th className="py-3 px-3">Material & Structure</th>
              <th className="py-3 px-2">Eligibility</th>
              <th className="py-3 px-2 text-right">Barrier Safety</th>
              <th className="py-3 px-2 text-right">Circularity</th>
              <th className="py-3 px-2 text-right">Cost Index</th>
              <th className="py-3 px-2 text-right">MCDA Utility</th>
              <th className="py-3 px-2 text-right">Gauge</th>
              <th className="py-3 px-2 text-right">OTR</th>
              <th className="py-3 px-2 text-right">WVTR</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 text-slate-700">
            {candidates.map((c) => (
              <tr key={c.material_id} className="hover:bg-slate-50/50 transition">
                <td className="py-3 px-3">
                  <div className="font-bold text-slate-900">{c.material_name}</div>
                  <div className="text-[11px] text-slate-400">
                    {c.material_family} • {c.structure_type.replace('_', ' ')}
                  </div>
                  {c.condition_notes.length > 0 && (
                    <div className="text-[10px] text-amber-700 mt-1 max-w-xs">
                      • {c.condition_notes[0]}
                    </div>
                  )}
                </td>
                <td className="py-3 px-2 whitespace-nowrap">{getEligibilityBadge(c.eligibility)}</td>
                <td className="py-3 px-2 text-right font-medium">
                  {(c.barrier_safety_score * 100).toFixed(0)}%
                </td>
                <td className="py-3 px-2 text-right font-medium">
                  {(c.sustainability_score * 100).toFixed(0)}%
                </td>
                <td className="py-3 px-2 text-right font-medium">
                  {c.relative_cost_multiplier.toFixed(1)}×
                </td>
                <td className="py-3 px-2 text-right font-bold text-emerald-800">
                  {(c.composite_utility_score * 100).toFixed(1)}
                </td>
                <td className="py-3 px-2 text-right whitespace-nowrap">
                  {c.nominal_thickness_um} μm
                </td>
                <td className="py-3 px-2 text-right whitespace-nowrap font-mono text-[11px]">
                  {c.nominal_otr}
                </td>
                <td className="py-3 px-2 text-right whitespace-nowrap font-mono text-[11px]">
                  {c.nominal_wvtr}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <p className="text-[11px] text-slate-400 italic pt-2">
        Note: Multi-Criteria Decision Analysis (MCDA) scores reflect the configured prototype
        decision criteria (barrier margin, circularity, economic multiplier) rather than absolute
        laboratory certification.
      </p>
    </div>
  );
};
