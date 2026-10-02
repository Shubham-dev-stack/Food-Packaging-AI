"""Pydantic schemas for Commodity and related physiological entities."""

from pydantic import BaseModel, ConfigDict, Field

from backend.app.schemas.evidence import EvidenceSourceResponse


class CommodityPropertyResponse(BaseModel):
    """Physicochemical characteristics and critical baseline decay parameters."""

    model_config = ConfigDict(from_attributes=True)

    property_id: str
    commodity_id: str
    critical_water_activity_aw: float = Field(..., description="Critical water activity threshold")
    typical_moisture_pct: float = Field(
        ..., description="Baseline moisture percentage on wet basis"
    )
    oil_fat_content_pct: float = Field(..., description="Total lipid percentage")
    typical_ph: float = Field(..., description="Baseline pH")
    primary_spoilage_pathways: list[str] = Field(..., description="Documented spoilage pathways")
    is_light_sensitive: bool = Field(
        ..., description="Triggers opaque or metallized substrate requirement"
    )
    recommended_temp_min_c: float = Field(
        ..., description="Recommended minimum storage temperature (°C)"
    )
    recommended_temp_max_c: float = Field(
        ..., description="Recommended maximum storage temperature (°C)"
    )
    recommended_rh_min_pct: float = Field(
        ..., description="Recommended minimum storage relative humidity (%)"
    )
    recommended_rh_max_pct: float = Field(
        ..., description="Recommended maximum storage relative humidity (%)"
    )
    reference_id: str = Field(..., description="Evidence reference foreign key")
    evidence_source: EvidenceSourceResponse | None = Field(default=None)


class ProduceRespirationResponse(BaseModel):
    """Post-harvest biological respiration and gas exchange parameters for produce."""

    model_config = ConfigDict(from_attributes=True)

    respiration_id: str
    commodity_id: str
    reference_temp_c: float = Field(..., description="Reference measurement temperature (°C)")
    respiration_rate_co2: float = Field(..., description="Respiration rate in mg CO2/(kg*h)")
    respiration_class: str = Field(..., description="Qualitative respiration intensity class")
    q10_factor: float = Field(..., description="Empirical Q10 temperature sensitivity factor")
    critical_o2_extinction_pct: float = Field(
        ..., description="Lower oxygen extinction fermentation limit (%)"
    )
    max_tolerable_co2_pct: float = Field(
        ..., description="Upper tolerable carbon dioxide injury threshold (%)"
    )
    condensation_risk_level: str = Field(
        ..., description="Risk of liquid condensation formation inside package"
    )
    reference_id: str = Field(..., description="Evidence reference foreign key")
    evidence_source: EvidenceSourceResponse | None = Field(default=None)


class MAPConfigurationResponse(BaseModel):
    """Evidence-backed modified atmosphere packaging gas formulations."""

    model_config = ConfigDict(from_attributes=True)

    map_id: str
    commodity_id: str
    recommended_o2_min_pct: float = Field(..., description="Min recommended O2 (%)")
    recommended_o2_max_pct: float = Field(..., description="Max recommended O2 (%)")
    recommended_co2_min_pct: float = Field(..., description="Min recommended CO2 (%)")
    recommended_co2_max_pct: float = Field(..., description="Max recommended CO2 (%)")
    recommended_n2_pct: float | None = Field(default=None, description="Balance N2 (%)")
    target_storage_temp_c: float = Field(..., description="Target storage temperature (°C)")
    suitability_status: str = Field(..., description="Suitability status")
    application_notes: str | None = Field(default=None, description="Contextual technical guidance")
    reference_id: str = Field(..., description="Evidence reference foreign key")
    evidence_source: EvidenceSourceResponse | None = Field(default=None)


class CommodityBriefResponse(BaseModel):
    """Summary representation for commodity search and catalog listings."""

    model_config = ConfigDict(from_attributes=True)

    commodity_id: str
    common_name: str
    scientific_name: str | None = None
    category: str
    is_respiring: bool
    default_storage_mode: str
    description: str | None = None


class CommodityDetailResponse(CommodityBriefResponse):
    """Comprehensive commodity payload with linked properties, respiration, and MAP."""

    property: CommodityPropertyResponse | None = None
    respiration_data: list[ProduceRespirationResponse] = Field(default_factory=list)
    map_configuration: MAPConfigurationResponse | None = None
