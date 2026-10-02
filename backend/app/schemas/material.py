"""Pydantic schemas for PackagingMaterial and barrier properties."""

from pydantic import BaseModel, ConfigDict, Field

from backend.app.schemas.evidence import EvidenceSourceResponse


class PackagingBarrierPropertyResponse(BaseModel):
    """Standardized barrier and mechanical specifications measured under ASTM/ISO standards."""

    model_config = ConfigDict(from_attributes=True)

    barrier_id: str
    material_id: str
    nominal_thickness_um: float = Field(..., description="Film thickness in micrometers")
    nominal_thickness_mil: float | None = Field(default=None, description="Film thickness in mils")
    otr_value: float = Field(..., description="Oxygen transmission rate in cm3/(m2*day*atm)")
    otr_test_temp_c: float = Field(..., description="OTR test measurement temperature (°C)")
    otr_test_rh_pct: float = Field(..., description="OTR test measurement relative humidity (%)")
    wvtr_value: float = Field(..., description="Water vapor transmission rate in g/(m2*day)")
    wvtr_test_temp_c: float = Field(..., description="WVTR test measurement temperature (°C)")
    wvtr_test_rh_pct: float = Field(..., description="WVTR test measurement relative humidity (%)")
    co2_tr_value: float | None = Field(
        default=None, description="CO2 transmission rate in cm3/(m2*day*atm)"
    )
    tensile_strength_md_mpa: float = Field(
        ..., description="Machine-direction tensile strength (MPa)"
    )
    elongation_at_break_pct: float = Field(..., description="Elongation at break (%)")
    puncture_resistance_n: float = Field(
        ..., description="Puncture resistance under ASTM F1306 (N)"
    )
    is_breathable: bool
    is_microperforated: bool
    microperforation_density_per_m2: int | None = None
    test_standard_otr: str
    test_standard_wvtr: str
    reference_id: str


class SustainabilityMetricResponse(BaseModel):
    """LCA and circularity metrics for environmental impact assessment."""

    model_config = ConfigDict(from_attributes=True)

    sustainability_id: str
    material_id: str
    carbon_footprint_kgco2e_per_kg: float = Field(
        ..., description="Cradle-to-gate GHG intensity (kg CO2-eq/kg)"
    )
    circularity_tier: str = Field(..., description="Qualitative circularity classification")
    is_mono_material: bool = Field(..., description="Whether material is mono-material")
    epr_category_india: str | None = Field(
        default=None, description="Category under India Plastic Waste Management Rules"
    )
    reference_id: str


class CostIndexResponse(BaseModel):
    """Relative economic indices benchmarking packaging cost against monolayer LDPE."""

    model_config = ConfigDict(from_attributes=True)

    cost_id: str
    material_id: str
    relative_cost_multiplier: float = Field(
        ..., description="Cost multiplier indexed against monolayer LDPE (= 1.0)"
    )
    conversion_complexity: str = Field(..., description="Manufacturing converting complexity")
    reference_id: str


class PackagingMaterialResponse(BaseModel):
    """Packaging material catalog item with full physical and ecological profile."""

    model_config = ConfigDict(from_attributes=True)

    material_id: str
    name: str
    trade_code: str
    material_family: str
    structure_type: str
    density_g_cm3: float
    is_biodegradable: bool
    recyclability_category: str
    food_contact_compliant: bool
    sealability_rating: str
    seal_initiation_temp_c: float | None = None
    reference_id: str
    evidence_source: EvidenceSourceResponse | None = None
    barrier_properties: list[PackagingBarrierPropertyResponse] = Field(default_factory=list)
    sustainability_metric: SustainabilityMetricResponse | None = None
    cost_index: CostIndexResponse | None = None
