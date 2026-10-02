import React, { useState, useEffect } from 'react';
import { CommodityPicker } from '../components/inputs/CommodityPicker';
import { BaselinePreviewCard } from '../components/inputs/BaselinePreviewCard';
import { EnvironmentalInputs } from '../components/inputs/EnvironmentalInputs';
import { PropertyOverrides } from '../components/inputs/PropertyOverrides';
import { RecommendationResultView } from './RecommendationResultView';
import { Alert } from '../components/common/Alert';
import { api, ApiError } from '../services/api';
import type {
  CommodityDetailResponse,
  CommodityBriefResponse,
  StorageType,
  TransitStress,
  RecommendationResponse,
  RecommendationCreateRequest,
} from '../types/api';

type WorkflowStep = 'input' | 'result';

export const Workspace: React.FC = () => {
  // Navigation / Workflow view state
  const [currentStep, setCurrentStep] = useState<WorkflowStep>('input');

  // Commodity state
  const [commodities, setCommodities] = useState<CommodityBriefResponse[]>([]);
  const [selectedCommodityId, setSelectedCommodityId] = useState<string>('');
  const [commodityDetail, setCommodityDetail] = useState<CommodityDetailResponse | null>(null);
  const [loadingCommodities, setLoadingCommodities] = useState<boolean>(true);
  const [loadingDetail, setLoadingDetail] = useState<boolean>(false);

  // Environmental inputs state
  const [shelfLifeDays, setShelfLifeDays] = useState<number>(180);
  const [storageType, setStorageType] = useState<StorageType>('ambient');
  const [storageTempC, setStorageTempC] = useState<number>(23.0);
  const [storageRhPct, setStorageRhPct] = useState<number>(65.0);
  const [transitStress, setTransitStress] = useState<TransitStress>('local_standard');

  // Overrides & Geometry state
  const [moistureContentPct, setMoistureContentPct] = useState<number | null>(null);
  const [waterActivityAw, setWaterActivityAw] = useState<number | null>(null);
  const [fatContentPct, setFatContentPct] = useState<number | null>(null);
  const [ph, setPh] = useState<number | null>(null);
  const [respirationRateCo2, setRespirationRateCo2] = useState<number | null>(null);
  const [packageWeightKg, setPackageWeightKg] = useState<number>(0.10);
  const [packageAreaM2, setPackageAreaM2] = useState<number>(0.06);
  const [sustainabilityPreference, setSustainabilityPreference] = useState<boolean>(false);

  // Form submission, audit snapshot & feedback state
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [generalError, setGeneralError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState<boolean>(false);
  const [lastSubmittedPayload, setLastSubmittedPayload] = useState<RecommendationCreateRequest | null>(null);
  const [recommendationResult, setRecommendationResult] = useState<RecommendationResponse | null>(null);

  // Initial load: Fetch commodities
  const fetchCommodities = async () => {
    try {
      setLoadingCommodities(true);
      setGeneralError(null);
      const list = await api.getCommodities();
      setCommodities(list);
      // Auto-select first commodity if available
      if (list.length > 0 && !selectedCommodityId) {
        setSelectedCommodityId(list[0].commodity_id);
      }
    } catch (err) {
      if (err instanceof ApiError) {
        setGeneralError(`Failed to load commodities: ${err.message}`);
      } else {
        setGeneralError('Network error connecting to backend service.');
      }
    } finally {
      setLoadingCommodities(false);
    }
  };

  useEffect(() => {
    fetchCommodities();
  }, []);

  // Fetch detail when selected commodity changes
  useEffect(() => {
    if (!selectedCommodityId) {
      setCommodityDetail(null);
      return;
    }

    let isMounted = true;
    const fetchDetail = async () => {
      try {
        setLoadingDetail(true);
        const detail = await api.getCommodity(selectedCommodityId);
        if (isMounted) {
          setCommodityDetail(detail);

          // Reset overrides when commodity changes
          setMoistureContentPct(null);
          setWaterActivityAw(null);
          setFatContentPct(null);
          setPh(null);
          setRespirationRateCo2(null);

          // Populate intelligent defaults from commodity recommended storage
          if (detail.property) {
            const tempMid =
              (detail.property.recommended_temp_min_c + detail.property.recommended_temp_max_c) / 2;
            setStorageTempC(tempMid);
            if (tempMid <= 0) {
              setStorageType('frozen');
            } else if (tempMid <= 12) {
              setStorageType('chilled');
            } else {
              setStorageType('ambient');
            }

            const rhMid =
              (detail.property.recommended_rh_min_pct + detail.property.recommended_rh_max_pct) / 2;
            setStorageRhPct(Math.round(rhMid));
          }
        }
      } catch (err) {
        if (isMounted) {
          setGeneralError(err instanceof Error ? err.message : 'Failed to fetch commodity details');
        }
      } finally {
        if (isMounted) setLoadingDetail(false);
      }
    };

    fetchDetail();
    return () => {
      isMounted = false;
    };
  }, [selectedCommodityId]);

  // Adjust temperature defaults when storage type button clicked
  const handleStorageTypeChange = (type: StorageType) => {
    setStorageType(type);
    if (type === 'frozen' && storageTempC > 0) {
      setStorageTempC(-18.0);
    } else if (type === 'chilled' && (storageTempC < -2 || storageTempC > 15)) {
      setStorageTempC(4.0);
    } else if (type === 'ambient' && storageTempC < 5) {
      setStorageTempC(23.0);
    }
  };

  // Client-side validation matching backend constraints
  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!selectedCommodityId) {
      newErrors.commodity_id = 'A commodity must be selected.';
    }

    if (!shelfLifeDays || shelfLifeDays < 1 || shelfLifeDays > 730) {
      newErrors.desired_shelf_life_days = 'Target shelf life must be between 1 and 730 days.';
    }

    if (storageTempC < -25 || storageTempC > 50) {
      newErrors.storage_temp_c = 'Storage temperature must be between -25°C and 50°C.';
    }

    // Storage regime coherence validation
    if (storageType === 'frozen' && storageTempC > 0.0) {
      newErrors.storage_temp_c = 'Frozen storage requires temperature ≤ 0.0°C.';
    } else if (storageType === 'chilled' && (storageTempC < -2.0 || storageTempC > 15.0)) {
      newErrors.storage_temp_c = 'Chilled storage requires temperature between -2.0°C and 15.0°C.';
    } else if (storageType === 'ambient' && storageTempC < 5.0) {
      newErrors.storage_temp_c = 'Ambient storage requires temperature ≥ 5.0°C.';
    }

    if (storageRhPct < 10 || storageRhPct > 100) {
      newErrors.storage_rh_pct = 'Relative humidity must be between 10% and 100%.';
    }

    if (packageWeightKg <= 0 || packageWeightKg > 100) {
      newErrors.package_weight_kg = 'Package weight must be between 0.001 and 100 kg.';
    }

    if (packageAreaM2 <= 0 || packageAreaM2 > 10) {
      newErrors.package_area_m2 = 'Permeation area must be between 0.001 and 10 m².';
    }

    if (moistureContentPct !== null && (moistureContentPct < 0 || moistureContentPct > 100)) {
      newErrors.moisture_pct = 'Moisture content must be between 0% and 100%.';
    }

    if (waterActivityAw !== null && (waterActivityAw < 0.1 || waterActivityAw > 1.0)) {
      newErrors.water_activity_aw = 'Water activity (aw) must be between 0.1 and 1.0.';
    }

    if (fatContentPct !== null && (fatContentPct < 0 || fatContentPct > 100)) {
      newErrors.oil_fat_content_pct = 'Fat content must be between 0% and 100%.';
    }

    if (ph !== null && (ph < 1 || ph > 14)) {
      newErrors.ph = 'pH must be between 1.0 and 14.0.';
    }

    if (respirationRateCo2 !== null && respirationRateCo2 < 0) {
      newErrors.respiration_rate_co2 = 'Respiration rate cannot be negative.';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setGeneralError(null);

    if (!validateForm()) {
      return;
    }

    const payload: RecommendationCreateRequest = {
      commodity_id: selectedCommodityId,
      desired_shelf_life_days: shelfLifeDays,
      storage_temp_c: storageTempC,
      storage_rh_pct: storageRhPct,
      storage_type: storageType,
      transit_stress: transitStress,
      user_sustainability_preference: sustainabilityPreference,
      package_weight_kg: packageWeightKg,
      package_area_m2: packageAreaM2,
    };

    if (moistureContentPct !== null) payload.moisture_pct = moistureContentPct;
    if (waterActivityAw !== null) payload.water_activity_aw = waterActivityAw;
    if (fatContentPct !== null) payload.oil_fat_content_pct = fatContentPct;
    if (ph !== null) payload.ph = ph;
    if (respirationRateCo2 !== null) payload.respiration_rate_co2 = respirationRateCo2;

    try {
      setSubmitting(true);
      setLastSubmittedPayload(payload);
      const result = await api.createRecommendation(payload);
      setRecommendationResult(result);
      setCurrentStep('result');
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (err) {
      if (err instanceof ApiError) {
        if (err.response && Array.isArray(err.response.details)) {
          const apiFieldErrors: Record<string, string> = {};
          err.response.details.forEach((d) => {
            const field = d.field || 'general';
            apiFieldErrors[field] = d.issue || 'Invalid input';
          });
          setErrors(apiFieldErrors);
        }
        setGeneralError(`Recommendation evaluation error: ${err.message}`);
      } else {
        setGeneralError('An unexpected error occurred while communicating with the engine.');
      }
    } finally {
      setSubmitting(false);
    }
  };

  const handleResetForNewEvaluation = () => {
    setRecommendationResult(null);
    setCurrentStep('input');
    setGeneralError(null);
    setErrors({});
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col font-sans text-slate-800">
      {/* Top Navigation Bar */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-30 shadow-2xs">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <span className="w-8 h-8 rounded-lg bg-emerald-700 text-white flex items-center justify-center font-bold text-sm shadow-xs">
              AI
            </span>
            <div>
              <div className="flex items-center space-x-2">
                <span className="text-sm font-bold tracking-tight text-slate-900">
                  SIH26236 Food Packaging Recommendation Engine
                </span>
                <span className="px-1.5 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800 uppercase tracking-wider">
                  Phase 5 Decision Workstation
                </span>
              </div>
              <p className="text-xs text-slate-500">
                Deterministic barrier requirement modeling & multi-criteria optimization
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-3 text-xs">
            {recommendationResult && (
              <div className="flex items-center space-x-1 bg-slate-100 p-1 rounded-xl">
                <button
                  type="button"
                  onClick={() => setCurrentStep('input')}
                  className={`px-3 py-1 font-semibold rounded-lg transition cursor-pointer ${
                    currentStep === 'input'
                      ? 'bg-white text-emerald-800 shadow-2xs'
                      : 'text-slate-600 hover:text-slate-900'
                  }`}
                >
                  1. Input Parameters
                </button>
                <button
                  type="button"
                  onClick={() => setCurrentStep('result')}
                  className={`px-3 py-1 font-semibold rounded-lg transition cursor-pointer ${
                    currentStep === 'result'
                      ? 'bg-white text-emerald-800 shadow-2xs'
                      : 'text-slate-600 hover:text-slate-900'
                  }`}
                >
                  2. Recommendation Result
                </button>
              </div>
            )}
            <span className="hidden sm:inline-flex items-center px-2 py-1 rounded-md bg-slate-100 text-slate-600 font-mono">
              API: /api
            </span>
          </div>
        </div>
      </header>

      {/* Main Container */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex-1 w-full">
        {generalError && (
          <div className="mb-6">
            <Alert type="error" title="Engine Evaluation Alert">
              {generalError}
            </Alert>
          </div>
        )}

        {/* WORKFLOW VIEW 2: RECOMMENDATION RESULT DASHBOARD */}
        {currentStep === 'result' && recommendationResult ? (
          <RecommendationResultView
            result={recommendationResult}
            submittedInput={lastSubmittedPayload}
            onModifyInputs={() => setCurrentStep('input')}
            onNewEvaluation={handleResetForNewEvaluation}
          />
        ) : (
          /* WORKFLOW VIEW 1: INPUT WORKSPACE */
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            {/* Left Column: Input Workstation Form (7 cols on large screens) */}
            <div className="lg:col-span-7 space-y-6">
              <form onSubmit={handleSubmit} className="space-y-6">
                {/* Commodity Selector Card */}
                <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs space-y-4">
                  <div className="flex items-center justify-between border-b border-slate-200 pb-3">
                    <div>
                      <h2 className="text-base font-bold text-slate-900">
                        1. Target Commodity Selection
                      </h2>
                      <p className="text-xs text-slate-500">
                        Select food commodity to load baseline literature properties
                      </p>
                    </div>
                    <span className="text-xs font-semibold text-slate-400">Step 1 of 3</span>
                  </div>

                  <CommodityPicker
                    commodities={commodities}
                    selectedCommodityId={selectedCommodityId}
                    loading={loadingCommodities}
                    error={errors.commodity_id || null}
                    onSelectCommodity={(id: string) => setSelectedCommodityId(id)}
                    onRetry={fetchCommodities}
                  />
                </div>

                {/* Environmental & Distribution Conditions Card */}
                <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs space-y-4">
                  <div className="flex items-center justify-between border-b border-slate-200 pb-3">
                    <div>
                      <h2 className="text-base font-bold text-slate-900">
                        2. Environmental & Supply Chain Conditions
                      </h2>
                      <p className="text-xs text-slate-500">
                        Specify cold chain logistics, ambient storage, and distribution stressors
                      </p>
                    </div>
                    <span className="text-xs font-semibold text-slate-400">Step 2 of 3</span>
                  </div>

                  <EnvironmentalInputs
                    shelfLifeDays={shelfLifeDays}
                    storageType={storageType}
                    storageTempC={storageTempC}
                    storageRhPct={storageRhPct}
                    transitStress={transitStress}
                    onShelfLifeChange={setShelfLifeDays}
                    onStorageTypeChange={handleStorageTypeChange}
                    onStorageTempChange={setStorageTempC}
                    onStorageRhChange={setStorageRhPct}
                    onTransitStressChange={setTransitStress}
                    errors={errors}
                  />
                </div>

                {/* Property Overrides & Geometry Card */}
                <div className="space-y-2">
                  <div className="flex items-center justify-between px-1">
                    <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500">
                      3. Overrides & Packaging Geometry
                    </h3>
                    <span className="text-xs font-semibold text-slate-400">Step 3 of 3</span>
                  </div>

                  <PropertyOverrides
                    commodity={commodityDetail}
                    moistureContentPct={moistureContentPct}
                    waterActivityAw={waterActivityAw}
                    fatContentPct={fatContentPct}
                    ph={ph}
                    respirationRateCo2={respirationRateCo2}
                    packageWeightKg={packageWeightKg}
                    packageAreaM2={packageAreaM2}
                    sustainabilityPreference={sustainabilityPreference}
                    onMoistureChange={setMoistureContentPct}
                    onWaterActivityChange={setWaterActivityAw}
                    onFatChange={setFatContentPct}
                    onPhChange={setPh}
                    onRespirationRateChange={setRespirationRateCo2}
                    onPackageWeightChange={setPackageWeightKg}
                    onPackageAreaChange={setPackageAreaM2}
                    onSustainabilityPreferenceChange={setSustainabilityPreference}
                    errors={errors}
                  />
                </div>

                {/* Submission Button */}
                <div className="pt-2">
                  <button
                    type="submit"
                    disabled={submitting || loadingCommodities || !selectedCommodityId}
                    className="w-full py-4 px-6 rounded-xl font-bold text-sm text-white bg-emerald-700 hover:bg-emerald-800 disabled:bg-slate-300 disabled:cursor-not-allowed shadow-sm transition flex items-center justify-center space-x-2 cursor-pointer"
                  >
                    {submitting ? (
                      <>
                        <svg
                          className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                          fill="none"
                          viewBox="0 0 24 24"
                        >
                          <circle
                            className="opacity-25"
                            cx="12"
                            cy="12"
                            r="10"
                            stroke="currentColor"
                            strokeWidth="4"
                          />
                          <path
                            className="opacity-75"
                            fill="currentColor"
                            d="M4 12a8 8 0 018-8v8H4z"
                          />
                        </svg>
                        <span>Evaluating Barrier Permeation & Optimizing Candidates...</span>
                      </>
                    ) : (
                      <>
                        <span>Generate Packaging Recommendations</span>
                        <svg
                          className="w-4 h-4 ml-1"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth="2"
                            d="M14 5l7 7m0 0l-7 7m7-7H3"
                          />
                        </svg>
                      </>
                    )}
                  </button>
                </div>
              </form>
            </div>

            {/* Right Column: Baseline Inspection Card (5 cols) */}
            <div className="lg:col-span-5 space-y-6">
              <div className="sticky top-24 space-y-6">
                <BaselinePreviewCard
                  commodity={commodityDetail}
                  loading={loadingDetail}
                />

                <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs space-y-3 text-xs text-slate-500">
                  <h4 className="font-bold text-slate-800 text-sm">Decision-Support Workflow</h4>
                  <p className="leading-relaxed">
                    1. Select commodity from the vetted knowledge catalog to inspect reference
                    physicochemical parameters.
                  </p>
                  <p className="leading-relaxed">
                    2. Configure temperature, humidity, shelf life, and transport stress profiles to
                    calculate water vapor & oxygen transmission limits.
                  </p>
                  <p className="leading-relaxed">
                    3. The recommendation engine evaluates candidate materials using ASTM D3985 / F1249
                    standards and multi-criteria utility weighting.
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};
