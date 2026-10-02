import React from 'react';
import { RespirationKineticsCard } from './RespirationKineticsCard';
import { MAPSuitabilityCard } from './MAPSuitabilityCard';
import { VentilationGuidanceCard } from './VentilationGuidanceCard';
import type { CommodityDetailResponse, TargetSpecificationsResponse } from '../../../types/api';

interface FreshProduceDashboardProps {
  commodityDetail: CommodityDetailResponse | null;
  targetSpecs: TargetSpecificationsResponse | null;
  storageTempC: number;
}

export const FreshProduceDashboard: React.FC<FreshProduceDashboardProps> = ({
  commodityDetail,
  targetSpecs,
  storageTempC,
}) => {
  // Guard condition: only render for respiring fresh produce commodities
  if (!commodityDetail || !commodityDetail.is_respiring) {
    return null;
  }

  const primaryRespData =
    commodityDetail.respiration_data && commodityDetail.respiration_data.length > 0
      ? commodityDetail.respiration_data[0]
      : null;

  return (
    <section
      aria-label="Fresh Produce Respiration and MAP Optimization"
      className="space-y-6 bg-gradient-to-b from-emerald-50/40 to-slate-50 border-2 border-emerald-500/30 rounded-2xl p-6 shadow-xs"
    >
      {/* Section Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-emerald-200/60 pb-3">
        <div className="flex items-center space-x-2.5">
          <span className="w-8 h-8 rounded-lg bg-emerald-600 text-white flex items-center justify-center font-bold text-sm shadow-xs">
            🌿
          </span>
          <div>
            <h3 className="text-base font-bold text-slate-900">
              Fresh Produce Respiration & Atmosphere Management
            </h3>
            <p className="text-xs text-slate-500">
              Post-harvest physiological kinetics, Q₁₀ thermal scaling, and gas-exchange requirements
            </p>
          </div>
        </div>
        <span className="self-start sm:self-auto px-2.5 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-emerald-100 text-emerald-800 border border-emerald-300">
          Respiring Crop Active
        </span>
      </div>

      {/* Gas-Exchange Interaction Flow Explanation */}
      <div className="p-4 bg-white rounded-xl border border-emerald-200/70 shadow-2xs space-y-2">
        <span className="text-[11px] font-bold uppercase tracking-wider text-emerald-800 block">
          Coupled Gas-Exchange Interaction:
        </span>
        <div className="grid grid-cols-1 sm:grid-cols-5 gap-2 text-center text-xs font-semibold items-center text-slate-700">
          <div className="bg-slate-50 p-2.5 rounded-lg border border-slate-200">
            <span className="text-[10px] text-slate-400 block font-bold">METABOLISM</span>
            Produce Consumes O₂ & Emits CO₂
          </div>
          <span className="text-emerald-600 font-bold hidden sm:inline">+</span>
          <div className="bg-slate-50 p-2.5 rounded-lg border border-slate-200">
            <span className="text-[10px] text-slate-400 block font-bold">ENVIRONMENT</span>
            Storage Temperature ({storageTempC}°C)
          </div>
          <span className="text-emerald-600 font-bold hidden sm:inline">+</span>
          <div className="bg-slate-50 p-2.5 rounded-lg border border-slate-200">
            <span className="text-[10px] text-slate-400 block font-bold">PACKAGE</span>
            Film Barrier Permeability & Geometry
          </div>
        </div>
        <p className="text-[11px] text-slate-500 pt-1 leading-relaxed">
          Packaging must establish a dynamic equilibrium where oxygen ingress precisely equals
          consumption without falling below the critical extinction threshold (~1–2% O₂), while
          retaining sufficient gas transmission to prevent toxic CO₂ accumulation.
        </p>
      </div>

      {/* Respiration Kinetics Card */}
      <RespirationKineticsCard
        respirationData={primaryRespData}
        storageTempC={storageTempC}
      />

      {/* MAP Suitability & Headspace Gas Target Card */}
      <MAPSuitabilityCard
        mapConfig={commodityDetail.map_configuration}
        storageTempC={storageTempC}
      />

      {/* Ventilation & Micro-perforation Breathability Card */}
      <VentilationGuidanceCard targetSpecs={targetSpecs} />
    </section>
  );
};
