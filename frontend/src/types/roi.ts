// Legacy type used by map panel (RoiPreviewPanel) — do not remove
export type RoiResult = {
  annual_harvestable_gal?: number;
  harvestable_liters?: number;
  harvestable_m3?: number;
  annual_water_savings_usd?: number;
  annual_sewer_savings_usd?: number;
  total_annual_savings_local?: number;
  capex_range?: [number, number];
  payback_yrs: number;
  npv_10yr_usd?: number;
  npv_10yr_local?: number;
  base_roi_percent: number;
  confidence_adj_roi_percent: number;
  currency?: string;
  currency_symbol?: string;
  water_autonomy_days?: number;
};

// Backend POST /roi response — mirrors models.py ROIResponse exactly
export type ROIResponse = {
  building_id: string;
  scenario: string;
  currency?: string;
  currency_symbol?: string;
  usd_exchange_rate?: number;

  harvestable_liters?: number;
  harvestable_m3?: number;
  harvestable_gal?: number;
  water_autonomy_days?: number;

  // Local currency
  annual_water_savings_local?: number;
  annual_sewer_savings_local?: number;
  annual_bowser_avoidance_local?: number;
  total_annual_savings_local?: number;
  capex_mid_local?: number;
  npv_10yr_local?: number;

  // USD
  annual_water_savings_usd?: number;
  annual_sewer_savings_usd?: number;
  stormwater_fee_avoidance_usd?: number;
  total_annual_savings_usd?: number;
  capex_mid_usd?: number;
  simple_payback_yrs: number;
  npv_10yr_usd?: number;

  // Backward compatibility
  annual_water_savings_kes?: number;
  annual_sewer_savings_kes?: number;
  annual_bowser_avoidance_kes?: number;
  total_annual_savings_kes?: number;
  capex_mid_kes?: number;
  npv_10yr_kes?: number;

  base_roi_pct: number;
  confidence_adj_roi_pct: number;
  co2_offset_kg?: number;
  co2_offset_lbs?: number;
  cv_confidence_pct: number;
};

// Building fields returned by GET /buildings/{id} (full BuildingRecord)
export type BuildingInfo = {
  building_id: string;
  address: string;
  country_code?: string;
  country_name?: string;
  metro: string;
  city?: string;
  state: string;
  county?: string;
  building_type: string;
  use_case_category?: string;
  use_case_title?: string;
  owner_tenant?: string;
  viability_score: number;
  recommended_angle: "cost_savings" | "resilience" | "compliance" | "esg_credibility";
  
  // Physical
  lat?: number;
  lng?: number;
  roof_area_sqm?: number;
  roof_area_sqft?: number;
  cooling_tower_present?: boolean;
  cooling_tower_count?: number;
  cv_confidence_score: number;
  imagery_url?: string;
  imagery_date?: string;
  imagery_source?: string;

  // Climate
  annual_rainfall_mm?: number;
  annual_rainfall_in?: number;
  drought_risk_index?: number;

  // Currency & Utility
  currency?: string;
  currency_symbol?: string;
  usd_exchange_rate?: number;
  utility_provider?: string;
  water_rate_per_m3_local?: number;
  sewer_rate_per_m3_local?: number;
  bowser_replacement_rate_per_m3_local?: number;
  daily_water_demand_m3?: number;
  rationing_days_per_month?: number;
  water_autonomy_days?: number;

  // Financial
  incentive_value_local?: number;
  incentive_value_usd?: number;
  system_capex_range_local?: [number, number];
  system_capex_range?: [number, number];
  urgency_score?: number;

  // ESG
  sbti_committed?: boolean;
  net_zero_pledge_yr?: number;
  leed_certified?: boolean;
  edge_certified?: boolean;
  sdg6_aligned?: boolean;
  sec_filing_snippet?: string;
  regulatory_framework?: string;
};

// Backend POST /brief response — mirrors models.py BriefResponse exactly
export type BriefAPIResponse = {
  prospect_summary: {
    address: string;
    metro_state: string;
    country_name?: string;
    use_case_title?: string;
    building_type: string;
    viability_score: number;
  };
  physical_suitability: {
    roof_area_sqm?: number;
    roof_area_sqft?: number;
    cooling_tower_detected: boolean;
    cv_confidence_pct: number;
    annual_capture_liters?: number;
    annual_capture_m3?: number;
    annual_capture_gal?: number;
    water_autonomy_days?: number;
  };
  financial_snapshot: {
    currency?: string;
    currency_symbol?: string;
    total_annual_savings_local?: number;
    total_annual_savings_usd?: number;
    simple_payback_yrs: number;
    npv_10yr_local?: number;
    npv_10yr_usd?: number;
    confidence_adj_roi_pct: number;
    incentive_flags: string;
    total_annual_savings_kes?: number;
    npv_10yr_kes?: number;
  };
  why_this_building_now: string;
  recommended_sales_angle: string;
  confidence_caveats: {
    cv_confidence_pct: number;
    key_assumptions: string;
    next_validation_step: string;
  };
  six_week_action_plan?: string[];
};

