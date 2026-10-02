import React from 'react';
import type { CommodityDetailResponse } from '../../types/api';

interface BaselinePreviewCardProps {
  commodity: CommodityDetailResponse | null;
  loading: boolean;
}

export const BaselinePreviewCard: React.FC<BaselinePreviewCardProps> = ({ commodity, loading }) => {
  if (loading) {
    return (
      <div className="p-4 bg-slate-50 border border-slate-200 rounded-xl flex items-center space-x-2 text-xs text-slate-500">
        <div className="w-3.5 h-3.5 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin" />
        <span>Loading reference properties...</span>
      </div>
    );
  }

  if (!commodity || !commodity.property) {
    return null;
  }

  const prop = commodity.property;
  const resp = commodity.respiration_data[0];

  return (
    <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 text-xs space-y-3">
      <div className="flex items-center justify-between border-b border-slate-200 pb-2">
        <div>
          <span className="font-bold text-slate-800 text-sm">{commodity.common_name}</span>
          {commodity.scientific_name && (
            <span className="text-slate-500 italic ml-2">({commodity.scientific_name})</span>
          )}
        </div>
        <span className="px-2 py-0.5 rounded text-[11px] font-semibold bg-emerald-100 text-emerald-800 border border-emerald-200">
          {commodity.category.replace('_', ' ')}
        </span>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
        <div className="bg-white p-2 rounded-lg border border-slate-200">
          <span className="text-slate-500 block text-[10px] uppercase font-semibold">Typical Moisture</span>
          <span className="font-bold text-slate-800 text-sm">{prop.typical_moisture_pct}%</span>
        </div>
        <div className="bg-white p-2 rounded-lg border border-slate-200">
          <span className="text-slate-500 block text-[10px] uppercase font-semibold">Critical aw</span>
          <span className="font-bold text-slate-800 text-sm">{prop.critical_water_activity_aw}</span>
        </div>
        <div className="bg-white p-2 rounded-lg border border-slate-200">
          <span className="text-slate-500 block text-[10px] uppercase font-semibold">Fat / Oil</span>
          <span className="font-bold text-slate-800 text-sm">{prop.oil_fat_content_pct}%</span>
        </div>
        <div className="bg-white p-2 rounded-lg border border-slate-200">
          <span className="text-slate-500 block text-[10px] uppercase font-semibold">Typical pH</span>
          <span className="font-bold text-slate-800 text-sm">{prop.typical_ph}</span>
        </div>
      </div>

      {resp && (
        <div className="bg-emerald-50 border border-emerald-200 p-2.5 rounded-lg flex items-center justify-between text-[11px] text-emerald-900">
          <div>
            <span className="font-bold">Active Respiration: </span>
            <span>{resp.respiration_rate_co2} mg CO₂/(kg·h) at {resp.reference_temp_c}°C</span>
          </div>
          <span className="font-semibold uppercase tracking-wider text-[10px] bg-emerald-200 px-1.5 py-0.5 rounded">
            Q₁₀ = {resp.q10_factor}
          </span>
        </div>
      )}

      <div className="text-[11px] text-slate-500 flex items-center justify-between pt-1">
        <span>Recommended Regime: {prop.recommended_temp_min_c}°C – {prop.recommended_temp_max_c}°C ({prop.recommended_rh_min_pct}%–{prop.recommended_rh_max_pct}% RH)</span>
        <span className="font-mono text-[10px] bg-slate-200 px-1.5 py-0.5 rounded text-slate-700">Ref: {prop.reference_id}</span>
      </div>
    </div>
  );
};
