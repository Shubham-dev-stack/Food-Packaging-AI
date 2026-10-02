import React from 'react';
import type {
  CandidateEvaluationResponse,
  OptimizationPreference,
  RankingWeightsResponse,
} from '../../../types/api';

interface TradeOffAnalysisCardProps {
  rankedCandidates: CandidateEvaluationResponse[];
  currentPreference?: OptimizationPreference;
  appliedWeights?: RankingWeightsResponse | null;
  onPreferenceChange?: (preference: OptimizationPreference) => void;
  isLoading?: boolean;
}

const PRESET_DESCRIPTIONS: Record<
  OptimizationPreference,
  { label: string; weights: string; focus: string; description: string }
> = {
  balanced: {
    label: 'Balanced (Default)',
    weights: 'Barrier 50% • Sustainability 30% • Cost 20%',
    focus: 'Primary focus on barrier safety margin while considering circularity and cost.',
    description:
      'Standard prototype baseline prioritizing product preservation safety while factoring in circularity and economic viability.',
  },
  sustainability: {
    label: 'Sustainability-Focused',
    weights: 'Barrier 40% • Sustainability 45% • Cost 15%',
    focus: 'Elevated priority for recyclable mono-materials and compostable bio-films.',
    description:
      'Circular economy preset favoring mechanically recyclable mono-materials (e.g. BoPE/PE) and biodegradable matrices, provided hard barrier constraints are met.',
  },
  cost: {
    label: 'Cost-Sensitive',
    weights: 'Barrier 40% • Sustainability 15% • Cost 45%',
    focus: 'Elevated priority for economic efficiency and lower conversion overhead.',
    description:
      'Commercial efficiency preset favoring materials with low relative resin cost and established conversion economics, without compromising minimum shelf-life barrier limits.',
  },
};

export const TradeOffAnalysisCard: React.FC<TradeOffAnalysisCardProps> = ({
  rankedCandidates,
  currentPreference = 'balanced',
  appliedWeights,
  onPreferenceChange,
  isLoading = false,
}) => {
  // Resolve active weights (fallback to documented presets if not provided)
  const weights: RankingWeightsResponse = appliedWeights || {
    w_barrier: currentPreference === 'balanced' ? 0.5 : 0.4,
    w_sustainability: currentPreference === 'sustainability' ? 0.45 : currentPreference === 'cost' ? 0.15 : 0.3,
    w_cost: currentPreference === 'cost' ? 0.45 : currentPreference === 'sustainability' ? 0.15 : 0.2,
  };

  const barrierPct = Math.round(weights.w_barrier * 100);
  const sustPct = Math.round(weights.w_sustainability * 100);
  const costPct = Math.round(weights.w_cost * 100);

  const topCandidate = rankedCandidates[0];
  const secondCandidate = rankedCandidates[1];

  // Derive plain-language trade-off observations from real score contributions
  const renderTradeOffRationale = () => {
    if (!topCandidate) {
      return (
        <p className="text-slate-600">
          No candidates satisfied the physical barrier and food safety constraints. Multi-criteria
          preference ranking applies only to qualified candidates.
        </p>
      );
    }

    const marginToSecond =
      secondCandidate !== undefined
        ? (topCandidate.composite_utility_score - secondCandidate.composite_utility_score).toFixed(3)
        : null;

    let driverText = '';
    let sacrificeText = '';

    if (currentPreference === 'sustainability') {
      if (topCandidate.is_mono_material || topCandidate.is_biodegradable) {
        driverText = `"${topCandidate.trade_code}" ranks #1 due to its superior circularity score (${topCandidate.sustainability_score.toFixed(2)}) amplified by the 45% sustainability weighting.`;
      } else {
        driverText = `"${topCandidate.trade_code}" retains top rank because its barrier safety margin dominates, even though circularity is prioritized.`;
      }
      if (topCandidate.relative_cost_multiplier > 1.5) {
        sacrificeText = `Trade-off: Carries an economic premium (relative cost multiplier ${topCandidate.relative_cost_multiplier}× vs commodity LDPE baseline).`;
      }
    } else if (currentPreference === 'cost') {
      if (topCandidate.cost_score > 0.5) {
        driverText = `"${topCandidate.trade_code}" ranks #1 driven by its favorable economic index (relative cost ${topCandidate.relative_cost_multiplier}× baseline) under the 45% cost weighting.`;
      } else {
        driverText = `"${topCandidate.trade_code}" leads because lower-cost alternatives failed hard barrier constraints.`;
      }
      if (!topCandidate.is_mono_material) {
        sacrificeText = `Trade-off: Uses a multi-material or metallized laminate structure with restricted post-consumer recyclability.`;
      }
    } else {
      // Balanced
      driverText = `"${topCandidate.trade_code}" achieves the highest composite score by balancing barrier margin (score ${topCandidate.barrier_safety_score.toFixed(2)} at 50% weight) with circularity and cost.`;
      if (secondCandidate && Math.abs(topCandidate.composite_utility_score - secondCandidate.composite_utility_score) < 0.05) {
        sacrificeText = `Close margin: Candidate "${secondCandidate.trade_code}" is a viable peer within ${marginToSecond} utility points.`;
      }
    }

    return (
      <div className="space-y-2 text-xs text-slate-700">
        <p className="font-semibold text-slate-900">{driverText}</p>
        {sacrificeText && <p className="text-slate-600">{sacrificeText}</p>}
        {marginToSecond !== null && (
          <p className="text-slate-500">
            Score spread: {marginToSecond} utility margin over rank #2 ({secondCandidate?.trade_code}).
          </p>
        )}
      </div>
    );
  };

  return (
    <section
      aria-label="Trade-Off & Multi-Criteria Optimization"
      className="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs space-y-6"
    >
      {/* 1. Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-200 pb-4">
        <div>
          <div className="flex items-center space-x-2">
            <h3 className="text-base font-bold text-slate-900">
              Multi-Criteria Optimization & Trade-Off Analysis
            </h3>
            <span className="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-indigo-100 text-indigo-800 border border-indigo-200">
              Decision Support
            </span>
          </div>
          <p className="text-xs text-slate-500 mt-0.5">
            Evaluate how material rankings shift when prioritizing barrier margin, circularity, or economic cost.
          </p>
        </div>

        {/* Prototype Tag */}
        <span className="self-start sm:self-auto px-2.5 py-1 rounded text-[11px] font-medium bg-slate-100 text-slate-600 border border-slate-200">
          MCDA Utility Model
        </span>
      </div>

      {/* 2. Preference Presets Selector */}
      <div className="space-y-3">
        <label className="text-xs font-bold text-slate-700 uppercase tracking-wider block">
          Optimization Preference Preset:
        </label>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3" role="tablist">
          {(['balanced', 'sustainability', 'cost'] as OptimizationPreference[]).map((pref) => {
            const isSelected = currentPreference === pref;
            const meta = PRESET_DESCRIPTIONS[pref];
            return (
              <button
                key={pref}
                type="button"
                role="tab"
                aria-selected={isSelected}
                disabled={isLoading}
                onClick={() => onPreferenceChange?.(pref)}
                className={`p-3.5 rounded-xl border text-left transition-all relative ${
                  isSelected
                    ? 'border-indigo-600 bg-indigo-50/70 shadow-xs ring-1 ring-indigo-500'
                    : 'border-slate-200 bg-slate-50 hover:bg-white hover:border-slate-300'
                } ${isLoading ? 'opacity-60 cursor-not-allowed' : 'cursor-pointer'}`}
              >
                <div className="flex items-center justify-between mb-1">
                  <span
                    className={`text-xs font-bold ${
                      isSelected ? 'text-indigo-900' : 'text-slate-800'
                    }`}
                  >
                    {meta.label}
                  </span>
                  {isSelected && (
                    <span className="w-2 h-2 rounded-full bg-indigo-600 animate-pulse" />
                  )}
                </div>
                <p className="text-[11px] text-slate-500 mb-1.5 font-mono">{meta.weights}</p>
                <p className="text-[11px] text-slate-600 line-clamp-2 leading-relaxed">
                  {meta.focus}
                </p>
              </button>
            );
          })}
        </div>
      </div>

      {/* 3. Active Weight Distribution Bar */}
      <div className="p-4 bg-slate-50 border border-slate-200 rounded-xl space-y-2.5 text-xs">
        <div className="flex items-center justify-between text-xs font-semibold text-slate-800">
          <span>Active Prototype Weight Distribution</span>
          <span className="font-mono text-slate-500">Total: 100%</span>
        </div>

        {/* Multi-segment distribution bar */}
        <div
          role="progressbar"
          aria-label="Active Weight Distribution"
          className="h-3.5 w-full bg-slate-200 rounded-full overflow-hidden flex shadow-inner"
        >
          <div
            style={{ width: `${barrierPct}%` }}
            className="bg-blue-600 h-full flex items-center justify-center text-[9px] font-bold text-white transition-all duration-300"
            title={`Barrier Margin: ${barrierPct}%`}
          >
            {barrierPct}%
          </div>
          <div
            style={{ width: `${sustPct}%` }}
            className="bg-emerald-600 h-full flex items-center justify-center text-[9px] font-bold text-white transition-all duration-300"
            title={`Circularity: ${sustPct}%`}
          >
            {sustPct}%
          </div>
          <div
            style={{ width: `${costPct}%` }}
            className="bg-amber-500 h-full flex items-center justify-center text-[9px] font-bold text-white transition-all duration-300"
            title={`Cost Index: ${costPct}%`}
          >
            {costPct}%
          </div>
        </div>

        {/* Legend */}
        <div className="flex flex-wrap items-center gap-4 pt-1 text-[11px]">
          <span className="flex items-center space-x-1.5 text-slate-700">
            <span className="w-2.5 h-2.5 rounded-full bg-blue-600" />
            <span>Barrier Performance ({barrierPct}%)</span>
          </span>
          <span className="flex items-center space-x-1.5 text-slate-700">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-600" />
            <span>Sustainability & Circularity ({sustPct}%)</span>
          </span>
          <span className="flex items-center space-x-1.5 text-slate-700">
            <span className="w-2.5 h-2.5 rounded-full bg-amber-500" />
            <span>Economic Cost Index ({costPct}%)</span>
          </span>
        </div>

        <p className="text-[11px] text-slate-500 italic pt-1 border-t border-slate-200">
          [PROTOTYPE ASSUMPTION] Weight presets provide decision-support trade-off modeling, not
          experimentally binding constants. Physical preservation and food safety requirements
          remain non-negotiable hard constraints.
        </p>
      </div>

      {/* 4. Candidate Scoring Matrix Table */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider">
            Qualified Candidate Score Breakdown ({rankedCandidates.length} Viable Materials)
          </h4>
          <span className="text-[11px] text-slate-500">
            Formula: U = w_b·S_b + w_s·S_s + w_c·S_c
          </span>
        </div>

        {rankedCandidates.length === 0 ? (
          <div className="p-6 bg-slate-50 border border-slate-200 rounded-xl text-center text-xs text-slate-500">
            No candidate materials satisfied the required barrier and safety constraints.
          </div>
        ) : (
          <div className="overflow-x-auto border border-slate-200 rounded-xl">
            <table className="w-full text-xs text-left">
              <thead className="bg-slate-50 border-b border-slate-200 text-[10px] font-bold text-slate-500 uppercase tracking-wider">
                <tr>
                  <th scope="col" className="p-3">Rank</th>
                  <th scope="col" className="p-3">Candidate Material</th>
                  <th scope="col" className="p-3 text-right">
                    Barrier Contrib <br />
                    <span className="text-[9px] font-normal lowercase text-slate-400">
                      (w_b={barrierPct}%)
                    </span>
                  </th>
                  <th scope="col" className="p-3 text-right">
                    Circularity Contrib <br />
                    <span className="text-[9px] font-normal lowercase text-slate-400">
                      (w_s={sustPct}%)
                    </span>
                  </th>
                  <th scope="col" className="p-3 text-right">
                    Cost Contrib <br />
                    <span className="text-[9px] font-normal lowercase text-slate-400">
                      (w_c={costPct}%)
                    </span>
                  </th>
                  <th scope="col" className="p-3 text-right">Composite Score (U)</th>
                  <th scope="col" className="p-3 text-center">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {rankedCandidates.map((cand, idx) => {
                  const isTop = idx === 0;
                  const barrierContrib =
                    cand.barrier_contribution !== undefined
                      ? cand.barrier_contribution.toFixed(4)
                      : (weights.w_barrier * cand.barrier_safety_score).toFixed(4);
                  const sustContrib =
                    cand.sustainability_contribution !== undefined
                      ? cand.sustainability_contribution.toFixed(4)
                      : (weights.w_sustainability * cand.sustainability_score).toFixed(4);
                  const costContrib =
                    cand.cost_contribution !== undefined
                      ? cand.cost_contribution.toFixed(4)
                      : (weights.w_cost * cand.cost_score).toFixed(4);

                  return (
                    <tr
                      key={cand.material_id}
                      className={isTop ? 'bg-indigo-50/40 font-medium' : 'hover:bg-slate-50'}
                    >
                      <td className="p-3 font-bold text-slate-900">
                        {isTop ? (
                          <span className="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] bg-indigo-600 text-white font-bold">
                            #1 Top
                          </span>
                        ) : (
                          <span className="text-slate-600 pl-1">#{cand.rank || idx + 1}</span>
                        )}
                      </td>
                      <td className="p-3">
                        <div className="font-semibold text-slate-900">{cand.material_name}</div>
                        <div className="text-[11px] text-slate-500 font-mono">
                          {cand.trade_code} • {cand.structure_type}
                        </div>
                      </td>
                      <td className="p-3 text-right">
                        <span className="font-mono text-blue-700">{barrierContrib}</span>
                        <span className="text-[10px] text-slate-400 block font-mono">
                          (raw: {cand.barrier_safety_score.toFixed(2)})
                        </span>
                      </td>
                      <td className="p-3 text-right">
                        <span className="font-mono text-emerald-700">{sustContrib}</span>
                        <span className="text-[10px] text-slate-400 block font-mono">
                          (raw: {cand.sustainability_score.toFixed(2)})
                        </span>
                      </td>
                      <td className="p-3 text-right">
                        <span className="font-mono text-amber-700">{costContrib}</span>
                        <span className="text-[10px] text-slate-400 block font-mono">
                          (raw: {cand.cost_score.toFixed(2)})
                        </span>
                      </td>
                      <td className="p-3 text-right">
                        <span
                          className={`font-mono text-xs font-bold ${
                            isTop ? 'text-indigo-900' : 'text-slate-800'
                          }`}
                        >
                          {cand.composite_utility_score.toFixed(4)}
                        </span>
                      </td>
                      <td className="p-3 text-center">
                        <span
                          className={`px-2 py-0.5 rounded-full text-[10px] font-semibold uppercase tracking-wider ${
                            cand.eligibility === 'ELIGIBLE'
                              ? 'bg-emerald-100 text-emerald-800'
                              : 'bg-amber-100 text-amber-800'
                          }`}
                        >
                          {cand.eligibility === 'ELIGIBLE' ? 'Eligible' : 'Conditional'}
                        </span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* 5. Trade-Off Rationale & Hard Constraints Distinction */}
      <div className="p-4 bg-indigo-50/50 border border-indigo-200/60 rounded-xl space-y-3">
        <div className="flex items-center space-x-2">
          <span className="font-bold text-xs uppercase tracking-wider text-indigo-950">
            Trade-Off Synthesis & Decision Analysis:
          </span>
        </div>

        {renderTradeOffRationale()}

        <div className="p-3 bg-white rounded-lg border border-indigo-100 text-[11px] text-slate-600 space-y-1">
          <span className="font-bold text-slate-800 block">
            Critical Boundary: Hard Constraints vs. Soft Preferences
          </span>
          <p>
            Preferences (Barrier vs. Sustainability vs. Cost) determine the relative ranking order of
            materials that already qualify. Materials that fail hard physical barriers (e.g. WVTR
            limits, OTR thresholds, micro-perforation breathability) are strictly rejected during
            constraint filtering and <strong>cannot be recommended</strong> regardless of preference weighting.
          </p>
        </div>
      </div>
    </section>
  );
};
