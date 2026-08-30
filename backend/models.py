# models.py
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Any

_VALID_ANGLES = {"cost_savings", "resilience", "compliance", "esg_credibility"}
_VALID_USE_CASES = {
    "industrial_tanker_offset",
    "cooling_tower_makeup",
    "horticulture_agro",
    "logistics_warehousing",
    "commercial_cre",
    "green_sez",
    "data_center"
}

# ── Input from buildings.json ──────────────────────────────────────────────

class BuildingRecord(BaseModel):
    building_id: str
    address: str
    country_code: str = "KE"             # KE | ZA | NG | RW | GH
    country_name: str = "Kenya"
    state: str = "Nairobi County"        # County, Province, or State
    county: str = "Nairobi City County"
    metro: str = "Nairobi"
    city: Optional[str] = "Nairobi"
    building_type: str
    use_case_category: str = "commercial_cre"
    use_case_title: str = "Commercial Rooftop Reuse"
    owner_tenant: Optional[str] = None

    lat: float = 0.0
    lng: float = 0.0

    # Metric physical dimensions
    roof_area_sqm: float = Field(default=1000.0)
    roof_area_sqft: Optional[float] = None
    roof_geometry: Optional[dict[str, Any]] = None
    cooling_tower_present: bool = False
    cooling_tower_count: int = 0
    cv_confidence_score: float = Field(ge=0.0, le=1.0, default=0.85)

    imagery_url: Optional[str] = None
    imagery_date: Optional[str] = None
    imagery_source: Optional[str] = None

    # Climate & Precipitation
    annual_rainfall_mm: float = 950.0
    annual_rainfall_in: Optional[float] = None
    drought_risk_index: float = 7.5
    flood_risk_index: Optional[float] = 4.0
    water_stress_tier: str = "High"

    # Multi-currency & Utility tariffs
    currency: str = "KES"                # KES | ZAR | NGN | RWF | USD
    currency_symbol: str = "KSh"         # KSh | R | ₦ | FRw | $
    usd_exchange_rate: float = 130.0     # Local units per 1 USD
    utility_provider: str = "Nairobi City Water & Sewerage Co (NCWSC)"

    # Tariffs in local currency per m³
    water_rate_per_m3_local: float = 125.0
    sewer_rate_per_m3_local: float = 93.75
    sewer_discharge_fraction: float = 0.75
    bowser_replacement_rate_per_m3_local: float = 750.0  # Private water tanker or borehole diesel cost / m³

    # Backward compatibility aliases
    water_rate_per_m3_kes: Optional[float] = None
    sewer_rate_per_m3_kes: Optional[float] = None
    bowser_replacement_rate_per_m3_kes: Optional[float] = None
    water_rate_per_kgal: Optional[float] = None
    sewer_rate_per_kgal: Optional[float] = None

    # Operational Water Resilience Metrics
    daily_water_demand_m3: float = 15.0
    rationing_days_per_month: int = 10
    water_autonomy_days: int = 35

    # Financials in local currency
    stormwater_fee_active: bool = False
    stormwater_fee_local_yr: float = 0.0
    stormwater_fee_kes_yr: Optional[float] = None
    incentive_value_local: float = 0.0
    incentive_value_kes: Optional[float] = None
    incentive_value_usd: Optional[float] = None
    system_capex_range_local: tuple[float, float] = (3500000.0, 5500000.0)
    system_capex_range_kes: Optional[tuple[float, float]] = None
    system_capex_range: Optional[tuple[float, float]] = None

    # ESG and Compliance
    sbti_committed: bool = False
    net_zero_pledge_yr: Optional[int] = None
    leed_certified: bool = False
    edge_certified: bool = False
    sdg6_aligned: bool = True
    water_risk_in_10k: bool = False
    sec_filing_snippet: Optional[str] = None
    regulatory_framework: Optional[str] = "WARMA & NEMA Kenya Water Standards"

    urgency_score: int = Field(ge=1, le=10, default=8)
    urgency_drivers: list[str] = Field(default_factory=list)
    recommended_angle: str = "resilience"
    viability_score: float = 85.0

    # ── Validators: backward compat & normalise ────────────────────────────

    @field_validator("address", "metro", "state", "county", "country_code", "currency", mode="before")
    @classmethod
    def coerce_str(cls, v: object) -> str:
        if v is None:
            return ""
        if isinstance(v, float) and v != v:
            return ""
        return str(v)

    @field_validator("cv_confidence_score", mode="before")
    @classmethod
    def clamp_cv_score(cls, v: object) -> float:
        return max(0.0, min(1.0, float(v)))

    @field_validator("urgency_score", mode="before")
    @classmethod
    def clamp_urgency(cls, v: object) -> int:
        return max(1, min(10, int(v)))

    @field_validator("recommended_angle", mode="before")
    @classmethod
    def normalise_angle(cls, v: object) -> str:
        return str(v) if str(v) in _VALID_ANGLES else "resilience"

    @field_validator("system_capex_range_local", mode="before")
    @classmethod
    def order_capex_range(cls, v: object) -> tuple[float, float]:
        if isinstance(v, (list, tuple)) and len(v) == 2:
            low, high = float(v[0]), float(v[1])
            return (low, high) if low <= high else (high, low)
        return (3500000.0, 5500000.0)

# ── ROI request / response ─────────────────────────────────────────────────

class ROIRequest(BaseModel):
    building_id: str
    scenario: str = "base"  # conservative | base | upside

class ROIResponse(BaseModel):
    building_id: str
    scenario: str
    currency: str = "KES"
    currency_symbol: str = "KSh"
    usd_exchange_rate: float = 130.0

    harvestable_liters: int
    harvestable_m3: float
    water_autonomy_days: int

    # Local Currency Financials
    annual_water_savings_local: float
    annual_sewer_savings_local: float
    annual_bowser_avoidance_local: float
    total_annual_savings_local: float
    capex_mid_local: float
    npv_10yr_local: float

    # USD Normalised Financials
    total_annual_savings_usd: float
    capex_mid_usd: float
    npv_10yr_usd: float

    # Backward compatibility fields
    annual_water_savings_kes: Optional[float] = None
    annual_sewer_savings_kes: Optional[float] = None
    annual_bowser_avoidance_kes: Optional[float] = None
    total_annual_savings_kes: Optional[float] = None
    capex_mid_kes: Optional[float] = None
    npv_10yr_kes: Optional[float] = None

    simple_payback_yrs: float
    base_roi_pct: float
    confidence_adj_roi_pct: float
    co2_offset_kg: int
    cv_confidence_pct: int

# ── Brief request / response ───────────────────────────────────────────────

class BriefRequest(BaseModel):
    building_id: str

class ProspectSummary(BaseModel):
    address: str
    metro_state: str
    country_name: str = "Kenya"
    use_case_title: str = "Commercial Rooftop Reuse"
    building_type: str
    viability_score: float

class PhysicalSuitability(BaseModel):
    roof_area_sqm: int
    cooling_tower_detected: bool
    cv_confidence_pct: int
    annual_capture_liters: int
    annual_capture_m3: float
    water_autonomy_days: int = 30

class FinancialSnapshot(BaseModel):
    currency: str = "KES"
    currency_symbol: str = "KSh"
    total_annual_savings_local: int
    total_annual_savings_usd: int
    simple_payback_yrs: float
    npv_10yr_local: int
    npv_10yr_usd: int
    confidence_adj_roi_pct: float
    incentive_flags: str
    total_annual_savings_kes: Optional[int] = None
    npv_10yr_kes: Optional[int] = None

class ConfidenceCaveats(BaseModel):
    cv_confidence_pct: int
    key_assumptions: str
    next_validation_step: str

class BriefResponse(BaseModel):
    prospect_summary: ProspectSummary
    physical_suitability: PhysicalSuitability
    financial_snapshot: FinancialSnapshot
    why_this_building_now: str
    recommended_sales_angle: str
    confidence_caveats: ConfidenceCaveats
    six_week_action_plan: list[str] = Field(default_factory=list)

