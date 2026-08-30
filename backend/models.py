# models.py
from pydantic import BaseModel, Field, field_validator
from typing import Optional

_VALID_ANGLES = {"cost_savings", "resilience", "compliance", "esg_credibility"}

# ── Input from buildings.json ──────────────────────────────────────────────

class BuildingRecord(BaseModel):
    building_id: str
    address: str
    state: str = "Nairobi County"
    county: str = "Nairobi City County"
    metro: str = "Nairobi"
    building_type: str
    owner_tenant: Optional[str] = None

    lat: float = 0.0
    lng: float = 0.0

    # Metric physical dimensions
    roof_area_sqm: float = Field(default=1000.0)
    roof_area_sqft: Optional[float] = None  # Backward compatibility alias
    cooling_tower_present: bool = False
    cooling_tower_count: int = 0
    cv_confidence_score: float = Field(ge=0.0, le=1.0, default=0.85)

    imagery_url: Optional[str] = None
    imagery_date: Optional[str] = None
    imagery_source: Optional[str] = None

    # Nairobi localized climate and utility tariffs (NCWSC & Bowsers)
    annual_rainfall_mm: float = 950.0       # Nairobi bimodal rainfall average (~950mm)
    annual_rainfall_in: Optional[float] = None
    water_rate_per_m3_kes: float = 125.0    # NCWSC commercial water tariff per m³
    water_rate_per_kgal: Optional[float] = None
    sewer_rate_per_m3_kes: float = 93.75    # NCWSC sewer surcharge (75% of water tariff)
    sewer_rate_per_kgal: Optional[float] = None
    bowser_replacement_rate_per_m3_kes: float = 750.0  # Cost of private water tanker per m³
    
    stormwater_fee_active: bool = False
    stormwater_fee_kes_yr: float = 0.0
    incentive_value_kes: float = 0.0
    incentive_value_usd: Optional[float] = None
    system_capex_range_kes: tuple[float, float] = (3500000.0, 5500000.0)
    system_capex_range: Optional[tuple[float, float]] = None

    # ESG and Climate Risk
    sbti_committed: bool = False
    net_zero_pledge_yr: Optional[int] = None
    leed_certified: bool = False
    sdg6_aligned: bool = True
    water_risk_in_10k: bool = False
    sec_filing_snippet: Optional[str] = None
    drought_risk_index: float = 7.5

    urgency_score: int = Field(ge=1, le=10, default=8)
    urgency_drivers: list[str] = Field(default_factory=list)
    recommended_angle: str = "resilience"
    viability_score: float = 85.0

    # ── Validators: backward compat & normalise ────────────────────────────

    @field_validator("address", "metro", "state", "county", mode="before")
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
        return v if v in _VALID_ANGLES else "resilience"

    @field_validator("system_capex_range_kes", mode="before")
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
    harvestable_liters: int
    harvestable_m3: float
    annual_water_savings_kes: float
    annual_sewer_savings_kes: float
    annual_bowser_avoidance_kes: float
    total_annual_savings_kes: float
    capex_mid_kes: float
    simple_payback_yrs: float
    npv_10yr_kes: float
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
    building_type: str
    viability_score: float

class PhysicalSuitability(BaseModel):
    roof_area_sqm: int
    cooling_tower_detected: bool
    cv_confidence_pct: int
    annual_capture_liters: int
    annual_capture_m3: float

class FinancialSnapshot(BaseModel):
    total_annual_savings_kes: int
    simple_payback_yrs: float
    npv_10yr_kes: int
    confidence_adj_roi_pct: float
    incentive_flags: str

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
