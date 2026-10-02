import React from 'react';
import type { MAPConfigurationResponse } from '../../../types/api';

interface MAPSuitabilityCardProps {
  mapConfig: MAPConfigurationResponse | null;
  storageTempC: number;
}

export const MAPSuitabilityCard: React.FC<MAPSuitabilityCardProps> = ({
  mapConfig,
  storageTempC,
}) => {
  if (!mapConfig) {
    return (
      <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs space-y-3">
        <div className="border-b border-slate-200 pb-2 flex items-center justify-between">
          <h4 className="text-base font-bold text-slate-900">
            Modified Atmosphere Packaging (MAP) Guidance
          </h4>
          <span className="px-2.5 py-0.5 rounded text-[10px] font-bold bg-amber-100 text-amber-800 border border-amber-300">
            Research Required
          </span>
        </div>
        <p className="text-xs text-slate-600 leading-relaxed">
          Commodity-specific MAP gas composition tolerances are not registered in the scientific
          catalog for this item. Active atmosphere flushing is NOT recommended without dedicated
          post-harvest trial data.
        </p>
      </div>
    );
  }

  const isSuitable = mapConfig.suitability_status === 'suitable';
  const isVentilatedOnly = mapConfig.suitability_status === 'ventilated_only';

  const getStatusBadge = () => {
    if (isSuitable) {
      return (
        <span className="px-2.5 py-1 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800 border border-emerald-300">
          MAP Recommended
        </span>
      );
    }
    if (isVentilatedOnly) {
      return (
        <span className="px-2.5 py-1 rounded-full text-[10px] font-bold bg-rose-100 text-rose-800 border border-rose-300">
          Ventilated Only (No Gas Flush)
        </span>
      );
    }
    return (
      <span className="px-2.5 py-1 rounded-full text-[10px] font-bold bg-amber-100 text-amber-800 border border-amber-300 capitalize">
        {mapConfig.suitability_status.replace('_', ' ')}
      </span>
    );
  };

  return (
    <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs space-y-5">
      {/* Header */}
      <div className="border-b border-slate-200 pb-3 flex items-center justify-between">
        <div>
          <h4 className="text-base font-bold text-slate-900">
            Modified Atmosphere Packaging (MAP) Headspace Targets
          </h4>
          <p className="text-xs text-slate-500">
            Evidence-backed target equilibrium gas window (O₂, CO₂, N₂) for senescence delay
          </p>
        </div>
        {getStatusBadge()}
      </div>

      {/* Target Gas Composition Breakdown */}
      {isSuitable ? (
        <div className="space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            {/* O2 Window */}
            <div className="p-4 bg-sky-50 border border-sky-200 rounded-xl space-y-1.5 text-xs">
              <div className="flex items-center justify-between text-sky-900 font-bold">
                <span>Oxygen (O₂)</span>
                <span className="font-mono text-[11px] bg-sky-200/70 px-1.5 py-0.5 rounded">
                  Aerobic Window
                </span>
              </div>
              <div className="text-xl font-bold text-sky-950">
                {mapConfig.recommended_o2_min_pct}% – {mapConfig.recommended_o2_max_pct}%
              </div>
              <p className="text-[11px] text-sky-800 leading-snug">
                Suppresses respiration while maintaining aerobic respiration above extinction.
              </p>
            </div>

            {/* CO2 Window */}
            <div className="p-4 bg-purple-50 border border-purple-200 rounded-xl space-y-1.5 text-xs">
              <div className="flex items-center justify-between text-purple-900 font-bold">
                <span>Carbon Dioxide (CO₂)</span>
                <span className="font-mono text-[11px] bg-purple-200/70 px-1.5 py-0.5 rounded">
                  Senescence Brake
                </span>
              </div>
              <div className="text-xl font-bold text-purple-950">
                {mapConfig.recommended_co2_min_pct}% – {mapConfig.recommended_co2_max_pct}%
              </div>
              <p className="text-[11px] text-purple-800 leading-snug">
                Retards chlorophyll degradation and mold growth without physiological injury.
              </p>
            </div>

            {/* Nitrogen Balance */}
            <div className="p-4 bg-slate-50 border border-slate-200 rounded-xl space-y-1.5 text-xs">
              <div className="flex items-center justify-between text-slate-700 font-bold">
                <span>Nitrogen (N₂)</span>
                <span className="font-mono text-[11px] bg-slate-200 px-1.5 py-0.5 rounded text-slate-700">
                  Inert Filler
                </span>
              </div>
              <div className="text-xl font-bold text-slate-800">
                {mapConfig.recommended_n2_pct ? `~${mapConfig.recommended_n2_pct}%` : 'Balance'}
              </div>
              <p className="text-[11px] text-slate-500 leading-snug">
                Inert gas buffer maintaining package cushion and volume.
              </p>
            </div>
          </div>

          {/* Target Atmosphere Bar Visual */}
          <div className="space-y-1.5 pt-1">
            <div className="flex justify-between text-[11px] font-semibold text-slate-600">
              <span>Target Headspace Proportions:</span>
              <span>
                O₂ ({mapConfig.recommended_o2_min_pct}–{mapConfig.recommended_o2_max_pct}%) • CO₂ (
                {mapConfig.recommended_co2_min_pct}–{mapConfig.recommended_co2_max_pct}%) • Balance N₂
              </span>
            </div>
            <div className="w-full h-3 rounded-full overflow-hidden flex bg-slate-200">
              <div
                style={{ width: `${mapConfig.recommended_o2_max_pct}%` }}
                className="bg-sky-500 h-full"
                title={`Target O2: ${mapConfig.recommended_o2_max_pct}%`}
              />
              <div
                style={{ width: `${mapConfig.recommended_co2_max_pct}%` }}
                className="bg-purple-500 h-full"
                title={`Target CO2: ${mapConfig.recommended_co2_max_pct}%`}
              />
              <div
                style={{
                  width: `${100 - (mapConfig.recommended_o2_max_pct + mapConfig.recommended_co2_max_pct)}%`,
                }}
                className="bg-slate-400 h-full"
                title="Balance Nitrogen"
              />
            </div>
          </div>
        </div>
      ) : (
        <div className="p-4 bg-rose-50 border border-rose-200 rounded-xl text-xs text-rose-900 space-y-1">
          <span className="font-bold block">Advisory: Gas Packaging Prohibited</span>
          <p className="leading-relaxed">
            This commodity is prone to severe physiological breakdown (such as blackheart, internal
            browning, or soft rot) under enclosed or gas-flushed packaging. Requires open macro-vented
            storage with dark ambient airflow.
          </p>
        </div>
      )}

      {/* Application Notes */}
      {mapConfig.application_notes && (
        <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200 text-xs text-slate-700 space-y-1">
          <span className="font-bold text-slate-900 text-[11px] block">
            Post-Harvest Application & Handling Notes:
          </span>
          <p className="leading-relaxed">{mapConfig.application_notes}</p>
        </div>
      )}

      {/* Target Storage Temperature Check */}
      <div className="text-[11px] text-slate-500 flex flex-col sm:flex-row sm:items-center justify-between gap-1 pt-1 border-t border-slate-100">
        <span>
          Optimal Equilibrium Temp: {mapConfig.target_storage_temp_c}°C (Selected Storage:{' '}
          {storageTempC}°C)
        </span>
        {mapConfig.reference_id && (
          <span className="font-mono bg-slate-100 px-2 py-0.5 rounded text-slate-700">
            Ref: {mapConfig.reference_id}
          </span>
        )}
      </div>
    </div>
  );
};
