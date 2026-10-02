import React from 'react';
import type { TargetSpecificationsResponse } from '../../../types/api';

interface VentilationGuidanceCardProps {
  targetSpecs: TargetSpecificationsResponse | null;
}

export const VentilationGuidanceCard: React.FC<VentilationGuidanceCardProps> = ({
  targetSpecs,
}) => {
  if (!targetSpecs) {
    return null;
  }

  const needsMicroperf = targetSpecs.is_microperforation_required;

  return (
    <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs space-y-4">
      <div className="border-b border-slate-200 pb-3 flex items-center justify-between">
        <div>
          <h4 className="text-base font-bold text-slate-900">
            Package Gas Exchange & Breathability Evaluation
          </h4>
          <p className="text-xs text-slate-500">
            Coupled mass-balance requirement for oxygen ingress and carbon dioxide venting
          </p>
        </div>
        <span
          className={`px-2.5 py-1 rounded-full text-[10px] font-bold border ${
            needsMicroperf
              ? 'bg-teal-50 text-teal-800 border-teal-300'
              : 'bg-blue-50 text-blue-800 border-blue-300'
          }`}
        >
          {needsMicroperf ? 'Ventilation / Micro-perforation Required' : 'Continuous Permeable Film'}
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
        {/* Equilibrium OTR Requirement */}
        <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-1.5">
          <span className="text-[10px] font-bold uppercase tracking-wider text-slate-500 block">
            Target Equilibrium Oxygen Transmission Rate
          </span>
          <div className="text-lg font-bold text-slate-900">
            {targetSpecs.max_recommended_otr}{' '}
            <span className="text-xs font-normal text-slate-500">cm³/(m²·day·atm)</span>
          </div>
          <p className="text-[11px] text-slate-600 leading-relaxed">
            {targetSpecs.target_otr_rationale}
          </p>
        </div>

        {/* Moisture Condensation Control (WVTR) */}
        <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-1.5">
          <span className="text-[10px] font-bold uppercase tracking-wider text-slate-500 block">
            Transpiration & Condensation Moisture Limit
          </span>
          <div className="text-lg font-bold text-slate-900">
            {targetSpecs.max_recommended_wvtr}{' '}
            <span className="text-xs font-normal text-slate-500">g/(m²·day)</span>
          </div>
          <p className="text-[11px] text-slate-600 leading-relaxed">
            {targetSpecs.target_wvtr_rationale}
          </p>
        </div>
      </div>

      {/* Physiological Mechanism Description */}
      <div
        className={`p-4 rounded-xl border text-xs space-y-1 leading-relaxed ${
          needsMicroperf
            ? 'bg-teal-50/50 border-teal-200 text-teal-950'
            : 'bg-slate-50 border-slate-200 text-slate-700'
        }`}
      >
        <span className="font-bold block">
          {needsMicroperf
            ? 'Engineering Basis for Micro-perforation:'
            : 'Continuous Film Breathability:'}
        </span>
        <p>
          {needsMicroperf
            ? 'Continuous polymer films exhibit a permselectivity ratio (CO₂/O₂) between 3 and 6. For high-respiration produce, continuous barriers cannot vent generated CO₂ fast enough without suffocating the crop, causing toxic ethanolic fermentation and off-odors. Laser or mechanical micro-perforations (pore diffusion ratio ~0.81) or microporous breathable membranes are necessary to sustain equilibrium.'
            : 'The commodity respiration rate is moderate and can be sustained by continuous high-permeability polyolefin films (such as LDPE or BOPP) under steady cold-chain control without requiring perforations.'}
        </p>
      </div>
    </div>
  );
};
