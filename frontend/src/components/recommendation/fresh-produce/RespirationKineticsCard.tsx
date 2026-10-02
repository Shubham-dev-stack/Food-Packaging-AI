import React from 'react';
import type { ProduceRespirationResponse } from '../../../types/api';

interface RespirationKineticsCardProps {
  respirationData: ProduceRespirationResponse | null;
  storageTempC: number;
}

export const RespirationKineticsCard: React.FC<RespirationKineticsCardProps> = ({
  respirationData,
  storageTempC,
}) => {
  if (!respirationData) {
    return (
      <div className="p-4 bg-amber-50 border border-amber-200 rounded-xl text-xs text-amber-900 space-y-1">
        <span className="font-bold block">Respiration Data Incomplete</span>
        <p>
          Specific post-harvest respiration rates for this cultivar are not registered in the
          published compendium. Laboratory respirometry required.
        </p>
      </div>
    );
  }

  // Calculate temperature scaled estimate using Q10 formula from Fonseca 2002: R(T) = R_ref * Q10^((T - T_ref)/10)
  const tempDiff = storageTempC - respirationData.reference_temp_c;
  const scaledRate = (
    respirationData.respiration_rate_co2 * Math.pow(respirationData.q10_factor, tempDiff / 10.0)
  ).toFixed(1);

  const isFreezing = storageTempC < 0.0;
  const isHeatAbuse = storageTempC > 25.0;

  return (
    <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs space-y-5">
      <div className="border-b border-slate-200 pb-3 flex items-center justify-between">
        <div>
          <h4 className="text-base font-bold text-slate-900">
            Post-Harvest Respiration Kinetics
          </h4>
          <p className="text-xs text-slate-500">
            Active metabolic respiration scaled from empirical reference baseline via Q₁₀ temperature model
          </p>
        </div>
        <span className="px-2.5 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider bg-emerald-100 text-emerald-800 border border-emerald-300">
          Class: {respirationData.respiration_class.replace('_', ' ')}
        </span>
      </div>

      {/* Temperature Scaling Flow Visual */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        {/* Baseline Reference */}
        <div className="p-4 bg-slate-50 border border-slate-200 rounded-xl space-y-1 text-xs">
          <span className="text-[10px] uppercase font-bold text-slate-400 block tracking-wider">
            Baseline Reference Rate
          </span>
          <div className="text-lg font-bold text-slate-900">
            {respirationData.respiration_rate_co2}{' '}
            <span className="text-xs font-normal text-slate-500">mg CO₂/(kg·h)</span>
          </div>
          <p className="text-[11px] text-slate-500">
            Measured at {respirationData.reference_temp_c}°C baseline reference
          </p>
        </div>

        {/* Temperature Sensitivity Q10 */}
        <div className="p-4 bg-slate-50 border border-slate-200 rounded-xl space-y-1 text-xs">
          <span className="text-[10px] uppercase font-bold text-slate-400 block tracking-wider">
            Thermal Sensitivity (Q₁₀)
          </span>
          <div className="text-lg font-bold text-slate-900">
            Q₁₀ = {respirationData.q10_factor}
          </div>
          <p className="text-[11px] text-slate-500">
            Metabolic acceleration per 10°C temperature rise (Fonseca 2002)
          </p>
        </div>

        {/* Scaled Estimate at Target Storage */}
        <div className="p-4 bg-emerald-50 border border-emerald-200 rounded-xl space-y-1 text-xs">
          <span className="text-[10px] uppercase font-bold text-emerald-800 block tracking-wider">
            Adjusted Rate at {storageTempC}°C
          </span>
          <div className="text-lg font-bold text-emerald-950">
            ~{scaledRate}{' '}
            <span className="text-xs font-normal text-emerald-700">mg CO₂/(kg·h)</span>
          </div>
          <p className="text-[11px] text-emerald-700">
            Estimated metabolic load at target storage temperature
          </p>
        </div>
      </div>

      {/* Temperature Abuse Warnings if applicable */}
      {isFreezing && (
        <div className="p-3 bg-rose-50 border border-rose-200 rounded-xl text-xs text-rose-900 flex items-start space-x-2">
          <span>⚠</span>
          <span>
            Storage temperature ({storageTempC}°C) is below freezing. Produce suffers lethal
            chilling injury, ice crystallization, and tissue collapse.
          </span>
        </div>
      )}

      {isHeatAbuse && (
        <div className="p-3 bg-amber-50 border border-amber-200 rounded-xl text-xs text-amber-900 flex items-start space-x-2">
          <span>⚠</span>
          <span>
            Storage temperature ({storageTempC}°C) exceeds recommended post-harvest limits.
            Exponential respiration acceleration risks rapid oxygen depletion and fermentation.
          </span>
        </div>
      )}

      {/* Physiological Limits */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs pt-1">
        <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl flex items-center justify-between">
          <span className="text-slate-600 font-medium">Critical O₂ Extinction Limit:</span>
          <span className="font-bold text-slate-800">
            {respirationData.critical_o2_extinction_pct}% O₂ (Hypoxia threshold)
          </span>
        </div>

        <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl flex items-center justify-between">
          <span className="text-slate-600 font-medium">Max Tolerable CO₂ Limit:</span>
          <span className="font-bold text-slate-800">
            {respirationData.max_tolerable_co2_pct}% CO₂ (Injury threshold)
          </span>
        </div>
      </div>

      {/* Evidence Source Reference */}
      {respirationData.reference_id && (
        <div className="pt-2 border-t border-slate-100 flex items-center justify-between text-[11px] text-slate-500">
          <span>Respiration Evidence Source:</span>
          <span className="font-mono bg-slate-100 px-2 py-0.5 rounded text-slate-700">
            {respirationData.reference_id}
          </span>
        </div>
      )}
    </div>
  );
};
