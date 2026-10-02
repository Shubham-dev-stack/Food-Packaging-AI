import React from 'react';
import type { TargetSpecificationsResponse } from '../../types/api';

interface TechnicalSpecificationGridProps {
  targetSpecs: TargetSpecificationsResponse | null;
}

export const TechnicalSpecificationGrid: React.FC<TechnicalSpecificationGridProps> = ({
  targetSpecs,
}) => {
  if (!targetSpecs) {
    return (
      <div className="bg-slate-50 border border-slate-200 rounded-2xl p-6 text-center text-xs text-slate-500">
        Technical target specifications are not available for this evaluation context.
      </div>
    );
  }

  const renderValue = (val: number | string | null | undefined, unit?: string) => {
    if (val === null || val === undefined) {
      return <span className="text-slate-400 italic font-normal">Not available</span>;
    }
    return (
      <span>
        {val} {unit && <span className="text-xs text-slate-500 font-normal">{unit}</span>}
      </span>
    );
  };

  return (
    <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs space-y-6">
      <div className="border-b border-slate-200 pb-3">
        <h3 className="text-base font-bold text-slate-900">
          Target Engineering Specifications
        </h3>
        <p className="text-xs text-slate-500">
          Target packaging performance limits derived from commodity shelf life and storage conditions
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* WVTR Card */}
        <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-500">
              Moisture Barrier (WVTR)
            </span>
            <span className="text-[10px] bg-slate-200 text-slate-700 px-1.5 py-0.5 rounded font-mono font-semibold">
              ASTM F1249
            </span>
          </div>
          <div className="text-xl font-bold text-slate-900">
            {renderValue(targetSpecs.max_recommended_wvtr, 'g/(m²·day)')}
          </div>
          <p className="text-[11px] text-slate-600 leading-relaxed border-t border-slate-200 pt-2">
            <span className="font-semibold text-slate-700">Analytical Rationale: </span>
            {targetSpecs.target_wvtr_rationale || 'Derived from permissible water loss/gain mass balance.'}
          </p>
        </div>

        {/* OTR Card */}
        <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-500">
              Oxygen Barrier (OTR)
            </span>
            <span className="text-[10px] bg-slate-200 text-slate-700 px-1.5 py-0.5 rounded font-mono font-semibold">
              ASTM D3985
            </span>
          </div>
          <div className="text-xl font-bold text-slate-900">
            {renderValue(targetSpecs.max_recommended_otr, 'cm³/(m²·day·atm)')}
          </div>
          <p className="text-[11px] text-slate-600 leading-relaxed border-t border-slate-200 pt-2">
            <span className="font-semibold text-slate-700">Oxidation Rationale: </span>
            {targetSpecs.target_otr_rationale || 'Derived from commodity lipid sensitivity and respiration rate.'}
          </p>
        </div>

        {/* Thickness Card */}
        <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-500">
              Recommended Gauge
            </span>
            <span className="text-[10px] bg-slate-200 text-slate-700 px-1.5 py-0.5 rounded font-mono font-semibold">
              ASTM D4169 / F1306
            </span>
          </div>
          <div className="text-xl font-bold text-slate-900">
            {renderValue(targetSpecs.recommended_thickness_um, 'μm')}
          </div>
          <p className="text-[11px] text-slate-600 leading-relaxed border-t border-slate-200 pt-2">
            <span className="font-semibold text-slate-700">Mechanical Rationale: </span>
            {targetSpecs.thickness_rationale || 'Sized to withstand transit vibration, drop, and puncture stress.'}
          </p>
        </div>
      </div>

      {/* Auxiliary Engineering Requirements */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-2">
        <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl flex items-center justify-between text-xs">
          <span className="text-slate-600 font-medium">Sealability Requirement:</span>
          <span className="font-bold text-slate-800 capitalize">
            {targetSpecs.sealability_required || 'Standard'}
          </span>
        </div>

        <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl flex items-center justify-between text-xs">
          <span className="text-slate-600 font-medium">Light Barrier Needed:</span>
          <span
            className={`font-bold ${
              targetSpecs.is_light_barrier_required ? 'text-amber-800' : 'text-slate-700'
            }`}
          >
            {targetSpecs.is_light_barrier_required ? 'Yes (Photosensitive)' : 'No (Standard)'}
          </span>
        </div>

        <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl flex items-center justify-between text-xs">
          <span className="text-slate-600 font-medium">Micro-perforation Needed:</span>
          <span
            className={`font-bold ${
              targetSpecs.is_microperforation_required ? 'text-teal-800' : 'text-slate-700'
            }`}
          >
            {targetSpecs.is_microperforation_required ? 'Yes (Gas Permeability)' : 'No (Dense Film)'}
          </span>
        </div>
      </div>
    </div>
  );
};
