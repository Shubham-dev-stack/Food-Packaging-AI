import React from 'react';
import type { ExplanationResponse } from '../../types/api';

interface UncertaintyNotesCardProps {
  uncertaintyNotes: string[];
  explanation: ExplanationResponse | null;
}

export const UncertaintyNotesCard: React.FC<UncertaintyNotesCardProps> = ({
  uncertaintyNotes,
  explanation,
}) => {
  const assumptions = explanation?.documented_assumptions || [];
  const limitations = explanation?.scientific_limitations || [];

  const hasNotes = uncertaintyNotes.length > 0 || assumptions.length > 0 || limitations.length > 0;

  if (!hasNotes) {
    return null;
  }

  return (
    <div className="bg-slate-50 border border-slate-200 rounded-2xl p-6 shadow-xs space-y-4">
      <div className="border-b border-slate-200 pb-2">
        <h4 className="text-xs font-bold uppercase tracking-wider text-slate-600">
          Scientific Uncertainty, Assumptions & Limitations
        </h4>
        <p className="text-[11px] text-slate-500">
          Transparency log documenting analytical simplifications and experimental boundaries
        </p>
      </div>

      {uncertaintyNotes.length > 0 && (
        <div className="space-y-1.5">
          <span className="text-[11px] font-bold text-slate-700 block">Uncertainty Notes:</span>
          <ul className="list-disc list-inside space-y-1 text-xs text-slate-600">
            {uncertaintyNotes.map((note, idx) => (
              <li key={idx} className="leading-relaxed">
                {note}
              </li>
            ))}
          </ul>
        </div>
      )}

      {assumptions.length > 0 && (
        <div className="space-y-1.5 pt-2 border-t border-slate-200">
          <span className="text-[11px] font-bold text-slate-700 block">
            Documented Engineering Assumptions:
          </span>
          <ul className="list-disc list-inside space-y-1 text-xs text-slate-600">
            {assumptions.map((item, idx) => (
              <li key={idx} className="leading-relaxed">
                {item}
              </li>
            ))}
          </ul>
        </div>
      )}

      {limitations.length > 0 && (
        <div className="space-y-1.5 pt-2 border-t border-slate-200">
          <span className="text-[11px] font-bold text-slate-700 block">
            Scientific Limitations:
          </span>
          <ul className="list-disc list-inside space-y-1 text-xs text-slate-600">
            {limitations.map((item, idx) => (
              <li key={idx} className="leading-relaxed">
                {item}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};
