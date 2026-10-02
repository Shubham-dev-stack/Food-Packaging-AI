import React from 'react';
import type { RecommendationStatus } from '../../types/api';

interface UncertaintyNotesCardProps {
  uncertaintyNotes: string[];
  status: RecommendationStatus;
}

export const UncertaintyNotesCard: React.FC<UncertaintyNotesCardProps> = ({
  uncertaintyNotes,
  status,
}) => {
  const statusContext: Record<
    RecommendationStatus,
    { badge: string; description: string; border: string; bg: string; text: string }
  > = {
    SUPPORTED: {
      badge: 'SUPPORTED',
      description:
        'Sufficient published scientific evidence exists for this decision. Target barrier values align with empirical literature standards.',
      border: 'border-emerald-200',
      bg: 'bg-emerald-50/50',
      text: 'text-emerald-900',
    },
    CONDITIONAL: {
      badge: 'CONDITIONAL',
      description:
        'Recommendation is valid subject to documented operational conditions (e.g. macro/micro-perforation venting, chilled cold-chain control, light shielding).',
      border: 'border-amber-200',
      bg: 'bg-amber-50/50',
      text: 'text-amber-900',
    },
    INSUFFICIENT_EVIDENCE: {
      badge: 'INSUFFICIENT_EVIDENCE',
      description:
        'Baseline physicochemical data or published barrier studies are incomplete. Calculations rely on baseline prototype defaults.',
      border: 'border-orange-200',
      bg: 'bg-orange-50/50',
      text: 'text-orange-900',
    },
    RESEARCH_REQUIRED: {
      badge: 'RESEARCH_REQUIRED',
      description:
        'An explicit research or empirical data gap exists. The system does NOT synthesize fabricated values; laboratory permeability testing is required.',
      border: 'border-rose-200',
      bg: 'bg-rose-50/50',
      text: 'text-rose-900',
    },
  };

  const currentCtx = statusContext[status] || statusContext.SUPPORTED;

  return (
    <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs space-y-4">
      <div className="border-b border-slate-200 pb-3 flex items-center justify-between">
        <div>
          <h3 className="text-base font-bold text-slate-900">
            Uncertainty & Evidence Confidence Profile
          </h3>
          <p className="text-xs text-slate-500">
            Auditing decision certainty, evidence completeness, and analytical bounds
          </p>
        </div>
        <span
          className={`px-2.5 py-1 rounded-full text-[10px] font-bold border ${currentCtx.bg} ${currentCtx.text} ${currentCtx.border}`}
        >
          Status: {currentCtx.badge}
        </span>
      </div>

      {/* Decision Status Confidence Description */}
      <div className={`p-4 rounded-xl border ${currentCtx.border} ${currentCtx.bg} space-y-1`}>
        <span className="text-[11px] font-bold uppercase tracking-wider block">
          Confidence State Evaluation:
        </span>
        <p className="text-xs leading-relaxed">{currentCtx.description}</p>
      </div>

      {/* Specific Uncertainty Notes from Backend */}
      {uncertaintyNotes.length > 0 && (
        <div className="space-y-2 pt-2">
          <span className="text-xs font-bold uppercase tracking-wider text-slate-500 block">
            Contextual Uncertainty Factors:
          </span>
          <ul className="space-y-1.5">
            {uncertaintyNotes.map((note, idx) => (
              <li
                key={idx}
                className="p-3 bg-slate-50 rounded-xl border border-slate-200 text-xs text-slate-700 leading-relaxed flex items-start space-x-2"
              >
                <span className="text-slate-400 font-bold mt-0.5">•</span>
                <span>{note}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};
