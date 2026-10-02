import React, { useState } from 'react';
import { FormField } from '../common/FormField';
import type { CommodityDetailResponse } from '../../types/api';

interface PropertyOverridesProps {
  commodity: CommodityDetailResponse | null;
  moistureContentPct: number | null;
  waterActivityAw: number | null;
  fatContentPct: number | null;
  ph: number | null;
  respirationRateCo2: number | null;
  packageWeightKg: number;
  packageAreaM2: number;
  sustainabilityPreference: boolean;
  onMoistureChange: (val: number | null) => void;
  onWaterActivityChange: (val: number | null) => void;
  onFatChange: (val: number | null) => void;
  onPhChange: (val: number | null) => void;
  onRespirationRateChange: (val: number | null) => void;
  onPackageWeightChange: (val: number) => void;
  onPackageAreaChange: (val: number) => void;
  onSustainabilityPreferenceChange: (val: boolean) => void;
  errors: Record<string, string>;
}

export const PropertyOverrides: React.FC<PropertyOverridesProps> = ({
  commodity,
  moistureContentPct,
  waterActivityAw,
  fatContentPct,
  ph,
  respirationRateCo2,
  packageWeightKg,
  packageAreaM2,
  sustainabilityPreference,
  onMoistureChange,
  onWaterActivityChange,
  onFatChange,
  onPhChange,
  onRespirationRateChange,
  onPackageWeightChange,
  onPackageAreaChange,
  onSustainabilityPreferenceChange,
  errors,
}) => {
  const [isOpen, setIsOpen] = useState(false);

  const hasAnyOverride =
    moistureContentPct !== null ||
    waterActivityAw !== null ||
    fatContentPct !== null ||
    ph !== null ||
    respirationRateCo2 !== null;

  const prop = commodity?.property;
  const primaryResp = commodity?.respiration_data?.[0];

  return (
    <div className="border border-slate-200 rounded-2xl bg-white shadow-xs overflow-hidden">
      {/* Accordion Header */}
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center justify-between px-5 py-4 bg-slate-50 hover:bg-slate-100 transition cursor-pointer text-left"
      >
        <div className="flex items-center space-x-3">
          <span className="text-base font-semibold text-slate-800">
            Advanced Properties & Package Geometry
          </span>
          {hasAnyOverride && (
            <span className="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-bold bg-amber-100 text-amber-800 border border-amber-300">
              Overrides Active
            </span>
          )}
        </div>
        <div className="flex items-center space-x-2 text-slate-500 text-xs font-medium">
          <span>{isOpen ? 'Collapse' : 'Configure Overrides'}</span>
          <svg
            className={`w-4 h-4 transform transition-transform ${isOpen ? 'rotate-180' : ''}`}
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
          </svg>
        </div>
      </button>

      {/* Accordion Body */}
      {isOpen && (
        <div className="p-5 space-y-6">
          <div className="text-xs text-slate-500 bg-slate-50 p-3 rounded-xl border border-slate-200">
            <span className="font-semibold text-slate-700">Optional Overrides: </span>
            Leave fields blank to use scientific baseline values from the literature repository.
            Entering values overrides the commodity defaults for barrier calculations.
          </div>

          {/* Physicochemical Overrides */}
          <div className="space-y-4">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500">
              Physicochemical Property Overrides
            </h4>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {/* Moisture Content Override */}
              <FormField
                label="Moisture Content (%)"
                sublabel={
                  prop
                    ? `Baseline: ${prop.typical_moisture_pct}%`
                    : 'Reference percentage'
                }
                isOverride={moistureContentPct !== null}
                onResetOverride={() => onMoistureChange(null)}
                error={errors.moisture_pct}
              >
                <div className="relative">
                  <input
                    type="number"
                    step="0.1"
                    min="0"
                    max="100"
                    placeholder={
                      prop != null
                        ? String(prop.typical_moisture_pct)
                        : 'e.g. 14.5'
                    }
                    value={moistureContentPct !== null ? moistureContentPct : ''}
                    onChange={(e) =>
                      onMoistureChange(e.target.value === '' ? null : Number(e.target.value))
                    }
                    className="w-full px-3 py-2 bg-white border border-slate-300 rounded-xl text-sm font-medium focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
                  />
                  {moistureContentPct !== null && (
                    <button
                      type="button"
                      onClick={() => onMoistureChange(null)}
                      className="absolute right-2.5 top-2.5 text-xs text-slate-400 hover:text-slate-600 cursor-pointer"
                      title="Reset to baseline"
                    >
                      Reset
                    </button>
                  )}
                </div>
              </FormField>

              {/* Water Activity (aw) Override */}
              <FormField
                label="Critical Water Activity (aw)"
                sublabel={
                  prop
                    ? `Baseline: ${prop.critical_water_activity_aw}`
                    : 'Governs microbial shelf life'
                }
                isOverride={waterActivityAw !== null}
                onResetOverride={() => onWaterActivityChange(null)}
                error={errors.water_activity_aw}
              >
                <div className="relative">
                  <input
                    type="number"
                    step="0.01"
                    min="0.1"
                    max="1.0"
                    placeholder={
                      prop != null
                        ? String(prop.critical_water_activity_aw)
                        : 'e.g. 0.65'
                    }
                    value={waterActivityAw !== null ? waterActivityAw : ''}
                    onChange={(e) =>
                      onWaterActivityChange(e.target.value === '' ? null : Number(e.target.value))
                    }
                    className="w-full px-3 py-2 bg-white border border-slate-300 rounded-xl text-sm font-medium focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
                  />
                  {waterActivityAw !== null && (
                    <button
                      type="button"
                      onClick={() => onWaterActivityChange(null)}
                      className="absolute right-2.5 top-2.5 text-xs text-slate-400 hover:text-slate-600 cursor-pointer"
                      title="Reset to baseline"
                    >
                      Reset
                    </button>
                  )}
                </div>
              </FormField>

              {/* Fat Content Override */}
              <FormField
                label="Fat / Oil Content (%)"
                sublabel={
                  prop
                    ? `Baseline: ${prop.oil_fat_content_pct}%`
                    : 'Reference percentage'
                }
                isOverride={fatContentPct !== null}
                onResetOverride={() => onFatChange(null)}
                error={errors.oil_fat_content_pct}
              >
                <div className="relative">
                  <input
                    type="number"
                    step="0.1"
                    min="0"
                    max="100"
                    placeholder={
                      prop != null
                        ? String(prop.oil_fat_content_pct)
                        : 'e.g. 2.0'
                    }
                    value={fatContentPct !== null ? fatContentPct : ''}
                    onChange={(e) =>
                      onFatChange(e.target.value === '' ? null : Number(e.target.value))
                    }
                    className="w-full px-3 py-2 bg-white border border-slate-300 rounded-xl text-sm font-medium focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
                  />
                  {fatContentPct !== null && (
                    <button
                      type="button"
                      onClick={() => onFatChange(null)}
                      className="absolute right-2.5 top-2.5 text-xs text-slate-400 hover:text-slate-600 cursor-pointer"
                      title="Reset to baseline"
                    >
                      Reset
                    </button>
                  )}
                </div>
              </FormField>

              {/* pH Override */}
              <FormField
                label="Product pH"
                sublabel={
                  prop
                    ? `Baseline: ${prop.typical_ph}`
                    : 'Governs acid food classification (pH < 4.6)'
                }
                isOverride={ph !== null}
                onResetOverride={() => onPhChange(null)}
                error={errors.ph}
              >
                <div className="relative">
                  <input
                    type="number"
                    step="0.05"
                    min="1"
                    max="14"
                    placeholder={
                      prop != null
                        ? String(prop.typical_ph)
                        : 'e.g. 6.2'
                    }
                    value={ph !== null ? ph : ''}
                    onChange={(e) =>
                      onPhChange(e.target.value === '' ? null : Number(e.target.value))
                    }
                    className="w-full px-3 py-2 bg-white border border-slate-300 rounded-xl text-sm font-medium focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
                  />
                  {ph !== null && (
                    <button
                      type="button"
                      onClick={() => onPhChange(null)}
                      className="absolute right-2.5 top-2.5 text-xs text-slate-400 hover:text-slate-600 cursor-pointer"
                      title="Reset to baseline"
                    >
                      Reset
                    </button>
                  )}
                </div>
              </FormField>

              {/* Respiration Rate Override (only if respiring commodity) */}
              <FormField
                label="Respiration Rate (mg CO₂/kg·h)"
                sublabel={
                  commodity?.is_respiring && primaryResp
                    ? `Baseline: ${primaryResp.respiration_rate_co2} at ${primaryResp.reference_temp_c}°C`
                    : 'Not active for non-respiring commodities'
                }
                isOverride={respirationRateCo2 !== null}
                onResetOverride={() => onRespirationRateChange(null)}
                error={errors.respiration_rate_co2}
              >
                <div className="relative">
                  <input
                    type="number"
                    step="1"
                    min="0"
                    disabled={!commodity?.is_respiring}
                    placeholder={
                      primaryResp != null
                        ? String(primaryResp.respiration_rate_co2)
                        : 'N/A (Non-respiring)'
                    }
                    value={respirationRateCo2 !== null ? respirationRateCo2 : ''}
                    onChange={(e) =>
                      onRespirationRateChange(
                        e.target.value === '' ? null : Number(e.target.value)
                      )
                    }
                    className="w-full px-3 py-2 bg-white border border-slate-300 rounded-xl text-sm font-medium focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 disabled:bg-slate-100 disabled:cursor-not-allowed"
                  />
                  {respirationRateCo2 !== null && (
                    <button
                      type="button"
                      onClick={() => onRespirationRateChange(null)}
                      className="absolute right-2.5 top-2.5 text-xs text-slate-400 hover:text-slate-600 cursor-pointer"
                      title="Reset to baseline"
                    >
                      Reset
                    </button>
                  )}
                </div>
              </FormField>
            </div>
          </div>

          {/* Prototype Geometry */}
          <div className="space-y-4 pt-4 border-t border-slate-200">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500">
              Prototype Geometry Assumptions
            </h4>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <FormField
                label="Pack Net Weight (kg)"
                sublabel="Mass of food enclosed (default: 0.10 kg / 100g)"
                required
                error={errors.package_weight_kg}
              >
                <input
                  type="number"
                  step="0.01"
                  min="0.001"
                  max="100"
                  value={packageWeightKg}
                  onChange={(e) => onPackageWeightChange(Number(e.target.value))}
                  className="w-full px-3 py-2 bg-white border border-slate-300 rounded-xl text-sm font-medium focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
                />
              </FormField>

              <FormField
                label="Pack Permeation Area (m²)"
                sublabel="Effective packaging surface area (default: 0.06 m²)"
                required
                error={errors.package_area_m2}
              >
                <input
                  type="number"
                  step="0.005"
                  min="0.001"
                  max="10"
                  value={packageAreaM2}
                  onChange={(e) => onPackageAreaChange(Number(e.target.value))}
                  className="w-full px-3 py-2 bg-white border border-slate-300 rounded-xl text-sm font-medium focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
                />
              </FormField>
            </div>
          </div>

          {/* User Preferences */}
          <div className="pt-4 border-t border-slate-200">
            <div className="flex items-start space-x-3 bg-emerald-50/50 p-4 rounded-xl border border-emerald-100">
              <input
                id="sustainabilityPreference"
                type="checkbox"
                checked={sustainabilityPreference}
                onChange={(e) => onSustainabilityPreferenceChange(e.target.checked)}
                className="mt-0.5 h-4 w-4 rounded border-slate-300 text-emerald-600 focus:ring-emerald-500 cursor-pointer"
              />
              <label
                htmlFor="sustainabilityPreference"
                className="text-xs font-medium text-slate-700 cursor-pointer leading-relaxed"
              >
                <span className="font-semibold text-slate-900 block">
                  Prioritize Bio-based & Circular Substrates (MCDA Eco Weight Boost)
                </span>
                Applies higher weighting to compostable, biodegradable, and recyclable mono-materials
                during multi-criteria decision analysis.
              </label>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
