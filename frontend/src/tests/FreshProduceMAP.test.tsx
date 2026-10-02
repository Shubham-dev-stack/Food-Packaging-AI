import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { FreshProduceDashboard } from '../components/recommendation/fresh-produce/FreshProduceDashboard';
import type { CommodityDetailResponse, TargetSpecificationsResponse } from '../types/api';

const mockRespiringCommodity: CommodityDetailResponse = {
  commodity_id: 'COMM_BROCCOLI',
  common_name: 'Fresh Broccoli Florets',
  scientific_name: 'Brassica oleracea var. italica',
  category: 'vegetable',
  is_respiring: true,
  default_storage_mode: 'chilled',
  description: 'Fresh horticultural floral heads with high respiration.',
  property: {
    property_id: 'PROP_BROCCOLI',
    commodity_id: 'COMM_BROCCOLI',
    typical_moisture_pct: 90.0,
    critical_water_activity_aw: 0.98,
    oil_fat_content_pct: 0.4,
    typical_ph: 6.5,
    primary_spoilage_pathways: ['senescence_fermentation', 'moisture_loss'],
    is_light_sensitive: false,
    recommended_temp_min_c: 0.0,
    recommended_temp_max_c: 4.0,
    recommended_rh_min_pct: 95.0,
    recommended_rh_max_pct: 98.0,
    reference_id: 'REF_USDA_HB66_2016',
  },
  respiration_data: [
    {
      respiration_id: 'RESP_BROCCOLI_5C',
      commodity_id: 'COMM_BROCCOLI',
      reference_temp_c: 5.0,
      respiration_rate_co2: 65.0,
      respiration_class: 'extremely_high',
      q10_factor: 2.2,
      critical_o2_extinction_pct: 1.0,
      max_tolerable_co2_pct: 15.0,
      condensation_risk_level: 'high',
      reference_id: 'REF_KADER_2002',
    },
  ],
  map_configuration: {
    map_id: 'MAP_BROCCOLI',
    commodity_id: 'COMM_BROCCOLI',
    recommended_o2_min_pct: 1.0,
    recommended_o2_max_pct: 2.0,
    recommended_co2_min_pct: 5.0,
    recommended_co2_max_pct: 10.0,
    recommended_n2_pct: 88.0,
    target_storage_temp_c: 4.0,
    suitability_status: 'suitable',
    application_notes: 'Delays sepal yellowing; requires perforated film to avoid sulfur odors.',
    reference_id: 'REF_KADER_2002',
  },
};

const mockNonRespiringCommodity: CommodityDetailResponse = {
  commodity_id: 'COMM_POTATO_CHIPS',
  common_name: 'Fried Potato Chips',
  scientific_name: 'Solanum tuberosum',
  category: 'snack_fried',
  is_respiring: false,
  default_storage_mode: 'ambient',
  description: 'Crispy fried snack.',
  property: null,
  respiration_data: [],
  map_configuration: null,
};

const mockTargetSpecs: TargetSpecificationsResponse = {
  max_recommended_wvtr: 40.0,
  max_recommended_otr: 6850.0,
  recommended_thickness_um: 35.0,
  sealability_required: 'excellent',
  is_light_barrier_required: false,
  is_microperforation_required: true,
  target_wvtr_rationale: 'Moderate-to-high water vapor transmission to prevent condensation.',
  target_otr_rationale: 'Equilibrium O2 demand: OTR >= 6850.0 cm3/(m2*day*atm).',
  thickness_rationale: 'Gauge balanced for breathable web stability (30-40 um).',
};

describe('Phase 7: Fresh Produce & Modified Atmosphere Packaging (MAP)', () => {
  it('1. renders fresh produce dashboard for respiring commodities', () => {
    const { container } = render(
      <FreshProduceDashboard
        commodityDetail={mockRespiringCommodity}
        targetSpecs={mockTargetSpecs}
        storageTempC={4.0}
      />
    );

    expect(
      screen.getByText(/Fresh Produce Respiration & Atmosphere Management/i)
    ).toBeDefined();
    expect(screen.getByText(/Respiring Crop Active/i)).toBeDefined();
    expect(container.querySelector('section')).not.toBeNull();
  });

  it('2. does NOT render fresh produce dashboard for non-respiring commodities', () => {
    const { container } = render(
      <FreshProduceDashboard
        commodityDetail={mockNonRespiringCommodity}
        targetSpecs={mockTargetSpecs}
        storageTempC={23.0}
      />
    );

    expect(
      screen.queryByText(/Fresh Produce Respiration & Atmosphere Management/i)
    ).toBeNull();
    expect(container.firstChild).toBeNull();
  });

  it('3. renders baseline and Q10 temperature-scaled respiration kinetics', () => {
    render(
      <FreshProduceDashboard
        commodityDetail={mockRespiringCommodity}
        targetSpecs={mockTargetSpecs}
        storageTempC={4.0}
      />
    );

    expect(screen.getByText(/Post-Harvest Respiration Kinetics/i)).toBeDefined();
    expect(screen.getByText(/65/i)).toBeDefined();
    expect(screen.getByText(/Q₁₀ = 2\.2/i)).toBeDefined();
    expect(screen.getByText(/Extremely High/i)).toBeDefined();
    expect(screen.getByText(/1% O₂ \(Hypoxia threshold\)/i)).toBeDefined();
  });

  it('4. renders MAP gas targets when supported by evidence', () => {
    render(
      <FreshProduceDashboard
        commodityDetail={mockRespiringCommodity}
        targetSpecs={mockTargetSpecs}
        storageTempC={4.0}
      />
    );

    expect(
      screen.getByText(/Modified Atmosphere Packaging \(MAP\) Headspace Targets/i)
    ).toBeDefined();
    expect(screen.getByText(/MAP Recommended/i)).toBeDefined();
    expect(screen.getByText(/1% – 2%/i)).toBeDefined(); // O2 window
    expect(screen.getByText(/5% – 10%/i)).toBeDefined(); // CO2 window
    expect(screen.getByText(/~88%/i)).toBeDefined(); // N2 balance
  });

  it('5. renders ventilated-only advisory when commodity is unsuitable for gas flush', () => {
    const ventilatedCommodity: CommodityDetailResponse = {
      ...mockRespiringCommodity,
      map_configuration: {
        ...mockRespiringCommodity.map_configuration!,
        suitability_status: 'ventilated_only',
      },
    };

    render(
      <FreshProduceDashboard
        commodityDetail={ventilatedCommodity}
        targetSpecs={mockTargetSpecs}
        storageTempC={4.0}
      />
    );

    expect(screen.getByText(/Ventilated Only \(No Gas Flush\)/i)).toBeDefined();
    expect(screen.getByText(/Advisory: Gas Packaging Prohibited/i)).toBeDefined();
  });

  it('6. handles missing MAP configuration gracefully with Research Required state', () => {
    const unconfiguredProduce: CommodityDetailResponse = {
      ...mockRespiringCommodity,
      map_configuration: null,
    };

    render(
      <FreshProduceDashboard
        commodityDetail={unconfiguredProduce}
        targetSpecs={mockTargetSpecs}
        storageTempC={4.0}
      />
    );

    expect(screen.getByText(/Research Required/i)).toBeDefined();
    expect(
      screen.getByText(/Commodity-specific MAP gas composition tolerances are not registered/i)
    ).toBeDefined();
  });

  it('7. renders micro-perforation and breathability guidance when required', () => {
    render(
      <FreshProduceDashboard
        commodityDetail={mockRespiringCommodity}
        targetSpecs={mockTargetSpecs}
        storageTempC={4.0}
      />
    );

    expect(
      screen.getByText(/Package Gas Exchange & Breathability Evaluation/i)
    ).toBeDefined();
    expect(
      screen.getByText(/Ventilation \/ Micro-perforation Required/i)
    ).toBeDefined();
    expect(
      screen.getByText(/Equilibrium O2 demand: OTR >= 6850\.0 cm3\/\(m2\*day\*atm\)\./i)
    ).toBeDefined();
  });

  it('8. handles temperature abuse warnings for sub-freezing storage', () => {
    render(
      <FreshProduceDashboard
        commodityDetail={mockRespiringCommodity}
        targetSpecs={mockTargetSpecs}
        storageTempC={-5.0}
      />
    );

    expect(
      screen.getByText(/Storage temperature \(-5°C\) is below freezing/i)
    ).toBeDefined();
  });
});
