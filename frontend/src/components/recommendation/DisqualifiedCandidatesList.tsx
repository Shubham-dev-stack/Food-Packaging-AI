import React, { useState } from 'react';
import type { CandidateEvaluationResponse } from '../../types/api';

interface DisqualifiedCandidatesListProps {
  disqualified: CandidateEvaluationResponse[];
}

export const DisqualifiedCandidatesList: React.FC<DisqualifiedCandidatesListProps> = ({
  disqualified,
}) => {
  const [isOpen, setIsOpen] = useState(false);

  if (disqualified.length === 0) {
    return null;
  }

  return (
    <div className="border border-slate-200 rounded-2xl bg-white shadow-xs overflow-hidden">
      {/* Header Accordion Toggle */}
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center justify-between px-6 py-4 bg-slate-50 hover:bg-slate-100 transition cursor-pointer text-left"
      >
        <div className="flex items-center space-x-3">
          <span className="text-sm font-bold text-slate-800">
            Why Other Candidates Were Not Selected
          </span>
          <span className="px-2 py-0.5 rounded text-[11px] font-semibold bg-rose-100 text-rose-800 border border-rose-200">
            {disqualified.length} Disqualified / Filtered
          </span>
        </div>
        <div className="flex items-center space-x-2 text-slate-500 text-xs font-medium">
          <span>{isOpen ? 'Hide Disqualifications' : 'Inspect Audit Log'}</span>
          <svg
            className={`w-4 h-4 transform transition-transform ${isOpen ? 'rotate-180' : ''}`}
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
          </svg>
        </div>
      </button>

      {/* Body */}
      {isOpen && (
        <div className="p-6 space-y-4 divide-y divide-slate-100">
          <p className="text-xs text-slate-500 pb-2">
            The deterministic constraint satisfaction filter evaluated these materials and ruled
            them ineligible based on physics, barrier limits, thermal operating ranges, or chemical
            incompatibilities:
          </p>

          {disqualified.map((item) => (
            <div key={item.material_id} className="pt-4 first:pt-0 space-y-2">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1">
                <div>
                  <span className="font-bold text-slate-900 text-sm">{item.material_name}</span>
                  <span className="text-xs text-slate-500 ml-2 font-mono">
                    ({item.trade_code} • {item.material_family})
                  </span>
                </div>
                <span className="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-bold bg-rose-50 text-rose-700 border border-rose-200">
                  REJECTED
                </span>
              </div>

              {/* Rejection Reasons from backend */}
              {item.rejection_reasons.length > 0 && (
                <div className="space-y-1">
                  <span className="text-[11px] font-bold uppercase tracking-wider text-rose-800 block">
                    Disqualification Reasons:
                  </span>
                  <ul className="list-disc list-inside space-y-1 text-xs text-rose-900 bg-rose-50/50 p-3 rounded-lg border border-rose-100">
                    {item.rejection_reasons.map((reason, idx) => (
                      <li key={idx} className="leading-relaxed">
                        {reason}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Barrier snapshot */}
              <div className="flex items-center space-x-4 text-[11px] text-slate-500 pt-1">
                <span>Thickness: {item.nominal_thickness_um} μm</span>
                <span>OTR: {item.nominal_otr} cm³/(m²·day·atm)</span>
                <span>WVTR: {item.nominal_wvtr} g/(m²·day)</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
