import React from 'react';
import { FormField } from '../common/FormField';
import type { StorageType, TransitStress } from '../../types/api';

interface EnvironmentalInputsProps {
  shelfLifeDays: number;
  storageType: StorageType;
  storageTempC: number;
  storageRhPct: number;
  transitStress: TransitStress;
  onShelfLifeChange: (val: number) => void;
  onStorageTypeChange: (val: StorageType) => void;
  onStorageTempChange: (val: number) => void;
  onStorageRhChange: (val: number) => void;
  onTransitStressChange: (val: TransitStress) => void;
  errors: Record<string, string>;
}

export const EnvironmentalInputs: React.FC<EnvironmentalInputsProps> = ({
  shelfLifeDays,
  storageType,
  storageTempC,
  storageRhPct,
  transitStress,
  onShelfLifeChange,
  onStorageTypeChange,
  onStorageTempChange,
  onStorageRhChange,
  onTransitStressChange,
  errors,
}) => {
  return (
    <div className="space-y-4">
      <div className="border-b border-slate-200 pb-2">
        <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500">
          Distribution & Storage Conditions
        </h3>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {/* Storage Regime Selector */}
        <FormField
          label="Storage Regime"
          sublabel="Governs physical state and biological kinetics"
          required
          error={errors.storage_type}
        >
          <div className="grid grid-cols-3 gap-1 bg-slate-100 p-1 rounded-xl">
            {(['ambient', 'chilled', 'frozen'] as StorageType[]).map((type) => (
              <button
                key={type}
                type="button"
                onClick={() => onStorageTypeChange(type)}
                className={`py-2 text-xs font-semibold rounded-lg capitalize transition cursor-pointer ${
                  storageType === type
                    ? 'bg-white text-emerald-800 shadow-xs'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                {type}
              </button>
            ))}
          </div>
        </FormField>

        {/* Desired Shelf Life */}
        <FormField
          label="Target Shelf Life (Days)"
          sublabel="Distribution requirement (1 to 730 days)"
          required
          error={errors.desired_shelf_life_days}
        >
          <input
            type="number"
            min={1}
            max={730}
            value={shelfLifeDays}
            onChange={(e) => onShelfLifeChange(Number(e.target.value))}
            className="w-full px-3 py-2 bg-white border border-slate-300 rounded-xl text-sm font-medium focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
          />
        </FormField>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {/* Storage Temperature Slider & Input */}
        <FormField
          label={`Storage Temperature (${storageTempC}°C)`}
          sublabel="Ambient: ≥5°C • Chilled: -2°C to 15°C • Frozen: ≤0°C"
          required
          error={errors.storage_temp_c}
        >
          <div className="space-y-2">
            <input
              type="range"
              min={-25}
              max={50}
              step={0.5}
              value={storageTempC}
              onChange={(e) => onStorageTempChange(Number(e.target.value))}
              className="w-full accent-emerald-600 cursor-pointer"
            />
            <div className="flex justify-between text-[10px] text-slate-400">
              <span>-25°C (Deep Freeze)</span>
              <span>0°C</span>
              <span>25°C (Ambient)</span>
              <span>50°C</span>
            </div>
          </div>
        </FormField>

        {/* Relative Humidity Slider & Input */}
        <FormField
          label={`Relative Humidity (${storageRhPct}% RH)`}
          sublabel="Governs water vapor driving force differential Δpw"
          required
          error={errors.storage_rh_pct}
        >
          <div className="space-y-2">
            <input
              type="range"
              min={10}
              max={100}
              step={1}
              value={storageRhPct}
              onChange={(e) => onStorageRhChange(Number(e.target.value))}
              className="w-full accent-emerald-600 cursor-pointer"
            />
            <div className="flex justify-between text-[10px] text-slate-400">
              <span>10% RH (Arid)</span>
              <span>65% RH (Standard)</span>
              <span>95% RH (Tropical/Chilled)</span>
            </div>
          </div>
        </FormField>
      </div>

      {/* Transit Stress Profile */}
      <FormField
        label="Transit Mechanical Stress"
        sublabel="Derives recommended film gauge and puncture resistance expectations"
        required
        error={errors.transit_stress}
      >
        <select
          value={transitStress}
          onChange={(e) => onTransitStressChange(e.target.value as TransitStress)}
          className="w-full px-3 py-2 bg-white border border-slate-300 rounded-xl text-sm font-medium focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
        >
          <option value="local_standard">Local Standard Distribution (Paved Roads, 30 μm baseline)</option>
          <option value="long_haul_refrigerated">Long-Haul Refrigerated Fleet (Cold Chain, 45 μm baseline)</option>
          <option value="rough_terrain_unpaved">Rough Terrain / High Mechanical Stress (Unpaved, 65 μm baseline)</option>
        </select>
      </FormField>
    </div>
  );
};
