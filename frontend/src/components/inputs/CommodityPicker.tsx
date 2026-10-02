import React from 'react';
import type { CommodityBriefResponse } from '../../types/api';

interface CommodityPickerProps {
  commodities: CommodityBriefResponse[];
  selectedCommodityId: string;
  loading: boolean;
  error: string | null;
  onSelectCommodity: (id: string) => void;
  onRetry: () => void;
}

export const CommodityPicker: React.FC<CommodityPickerProps> = ({
  commodities,
  selectedCommodityId,
  loading,
  error,
  onSelectCommodity,
  onRetry,
}) => {
  if (loading) {
    return (
      <div className="p-4 bg-slate-50 border border-slate-200 rounded-xl flex items-center space-x-3 text-slate-600 text-sm">
        <div className="w-4 h-4 border-2 border-emerald-600 border-t-transparent rounded-full animate-spin" />
        <span>Loading food commodities from knowledge base...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 bg-rose-50 border border-rose-200 rounded-xl space-y-2 text-rose-800 text-sm">
        <p className="font-semibold">Failed to load commodities</p>
        <p className="text-xs">{error}</p>
        <button
          type="button"
          onClick={onRetry}
          className="mt-2 text-xs font-semibold px-3 py-1.5 bg-rose-600 text-white rounded-lg hover:bg-rose-700 transition"
        >
          Retry Loading
        </button>
      </div>
    );
  }

  if (commodities.length === 0) {
    return (
      <div className="p-4 bg-slate-50 border border-slate-200 rounded-xl text-slate-600 text-sm">
        No commodities registered in the catalog.
      </div>
    );
  }

  return (
    <div className="space-y-2">
      <label htmlFor="commodity-select" className="block text-xs font-semibold text-slate-700">
        Select Food Commodity <span className="text-rose-500 font-bold">*</span>
      </label>
      <select
        id="commodity-select"
        value={selectedCommodityId}
        onChange={(e) => onSelectCommodity(e.target.value)}
        className="w-full px-3.5 py-2.5 bg-white border border-slate-300 rounded-xl text-sm font-medium text-slate-900 shadow-xs focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition"
      >
        <option value="" disabled>
          -- Choose a Food Commodity --
        </option>
        {commodities.map((item) => (
          <option key={item.commodity_id} value={item.commodity_id}>
            {item.common_name} ({item.category.replace('_', ' ')})
            {item.is_respiring ? ' • Respiring Crop' : ''}
          </option>
        ))}
      </select>
    </div>
  );
};
