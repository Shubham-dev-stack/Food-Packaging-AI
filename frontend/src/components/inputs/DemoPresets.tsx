import React from 'react';
import type { OptimizationPreference, StorageType, TransitStress } from '../../types/api';

export interface DemoPreset {
  id: string;
  badge: string;
  title: string;
  description: string;
  commodityId: string;
  shelfLifeDays: number;
  storageType: StorageType;
  storageTempC: number;
  storageRhPct: number;
  transitStress: TransitStress;
  optimizationPreference: OptimizationPreference;
  packageWeightKg: number;
  packageAreaM2: number;
  moistureContentPct?: number | null;
  waterActivityAw?: number | null;
  fatContentPct?: number | null;
  ph?: number | null;
  respirationRateCo2?: number | null;
  sustainabilityPreference?: boolean;
}

export const DEMO_PRESETS: DemoPreset[] = [
  {
    id: 'potato_chips_balanced',
    badge: 'Ambient Crispy',
    title: 'Potato Chips — High Barrier (Balanced)',
    description: '180-day ambient storage requiring rigorous moisture (WVTR ≤ 2.5) & oxygen (OTR ≤ 2.0) barrier to prevent rancidity.',
    commodityId: 'COMM_POTATO_CHIPS',
    shelfLifeDays: 180,
    storageType: 'ambient',
    storageTempC: 25.0,
    storageRhPct: 75.0,
    transitStress: 'rough_terrain_unpaved',
    optimizationPreference: 'balanced',
    packageWeightKg: 0.10,
    packageAreaM2: 0.06,
    sustainabilityPreference: false,
  },
  {
    id: 'potato_chips_sustainability',
    badge: 'Mono-Material',
    title: 'Potato Chips — Recyclable Focus',
    description: 'Evaluates recyclable mono-material trade-offs vs metallized laminates under sustainability priority weights.',
    commodityId: 'COMM_POTATO_CHIPS',
    shelfLifeDays: 120,
    storageType: 'ambient',
    storageTempC: 22.0,
    storageRhPct: 65.0,
    transitStress: 'local_standard',
    optimizationPreference: 'sustainability',
    packageWeightKg: 0.10,
    packageAreaM2: 0.06,
    sustainabilityPreference: true,
  },
  {
    id: 'fresh_broccoli_map',
    badge: 'Chilled Produce',
    title: 'Fresh Broccoli — MAP Microperforation',
    description: 'Chilled high-respiration produce demanding active gas exchange; dense continuous films fail hypoxia checks.',
    commodityId: 'COMM_BROCCOLI',
    shelfLifeDays: 14,
    storageType: 'chilled',
    storageTempC: 4.0,
    storageRhPct: 95.0,
    transitStress: 'long_haul_refrigerated',
    optimizationPreference: 'balanced',
    packageWeightKg: 0.50,
    packageAreaM2: 0.12,
    sustainabilityPreference: false,
  },
  {
    id: 'research_required',
    badge: 'Boundary Refusal',
    title: 'Wild Mushroom — Research Required',
    description: 'Uncharacterized respiring produce lacking vetted MAP gas atmosphere data; safely refuses to hallucinate.',
    commodityId: 'COMM_SMOKE_UNVERIFIED',
    shelfLifeDays: 7,
    storageType: 'chilled',
    storageTempC: 4.0,
    storageRhPct: 92.0,
    transitStress: 'local_standard',
    optimizationPreference: 'balanced',
    packageWeightKg: 0.25,
    packageAreaM2: 0.08,
    sustainabilityPreference: false,
  },
  {
    id: 'extreme_constraints',
    badge: 'Edge Case',
    title: 'Extreme Constraint — Zero Candidates',
    description: 'Excessive shelf life & tropical humidity where no catalog material qualifies, triggering transparent refusal.',
    commodityId: 'COMM_POTATO_CHIPS',
    shelfLifeDays: 720,
    storageType: 'ambient',
    storageTempC: 45.0,
    storageRhPct: 98.0,
    transitStress: 'rough_terrain_unpaved',
    optimizationPreference: 'balanced',
    packageWeightKg: 0.05,
    packageAreaM2: 0.15,
    sustainabilityPreference: false,
  },
];

interface DemoPresetsProps {
  onApplyPreset: (preset: DemoPreset) => void;
  activePresetId?: string | null;
  disabled?: boolean;
}

export const DemoPresets: React.FC<DemoPresetsProps> = ({
  onApplyPreset,
  activePresetId,
  disabled = false,
}) => {
  return (
    <div className="bg-gradient-to-r from-emerald-900 to-slate-900 text-white rounded-2xl p-5 shadow-sm space-y-3">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-emerald-800/60 pb-3">
        <div className="flex items-center space-x-2">
          <span className="px-2 py-0.5 rounded text-[10px] font-bold tracking-wider uppercase bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
            SIH Judge Evaluation
          </span>
          <h3 className="text-sm font-bold text-white tracking-tight">
            1-Click Demonstration Scenarios
          </h3>
        </div>
        <span className="text-[11px] text-emerald-300/80 font-medium">
          Deterministic test cases demonstrating boundary safety & optimization
        </span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-2.5 pt-1">
        {DEMO_PRESETS.map((preset) => {
          const isActive = activePresetId === preset.id;
          return (
            <button
              key={preset.id}
              type="button"
              disabled={disabled}
              onClick={() => onApplyPreset(preset)}
              className={`p-3 rounded-xl text-left transition flex flex-col justify-between cursor-pointer border text-xs ${
                isActive
                  ? 'bg-emerald-800/60 border-emerald-400 text-white shadow-xs ring-1 ring-emerald-400'
                  : 'bg-slate-800/50 hover:bg-slate-800 border-slate-700/70 text-slate-200 hover:border-emerald-500/50'
              } disabled:opacity-50 disabled:cursor-not-allowed`}
            >
              <div>
                <div className="flex items-center justify-between gap-1 mb-1.5">
                  <span className="text-[10px] font-semibold px-1.5 py-0.5 rounded bg-slate-900/60 text-emerald-300">
                    {preset.badge}
                  </span>
                </div>
                <div className="font-bold text-xs text-white leading-snug line-clamp-2">
                  {preset.title}
                </div>
                <div className="text-[11px] text-slate-300/80 mt-1 line-clamp-3 leading-relaxed">
                  {preset.description}
                </div>
              </div>
              <div className="mt-2.5 pt-2 border-t border-slate-700/50 flex items-center justify-between text-[10px] font-medium text-emerald-400">
                <span>Load Scenario</span>
                <span>→</span>
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
};
