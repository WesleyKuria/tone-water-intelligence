export type BuildingCandidate = {
  building_id: string;
  address: string;
  country_code?: string;
  country_name?: string;
  lat: number;
  lng: number;
  metro: string;
  city?: string;
  state: string;
  county?: string;
  building_type: string;
  use_case_category?: "industrial_tanker_offset" | "cooling_tower_makeup" | "horticulture_agro" | "logistics_warehousing" | "commercial_cre" | "green_sez" | "data_center" | string;
  use_case_title?: string;
  owner_tenant?: string;

  // Physical & Geometry
  roof_area_sqm?: number;
  roof_area_sqft?: number;
  roof_geometry?: GeoJSON.Geometry;
  cooling_tower_present: boolean;
  cooling_tower_count: number;
  cv_confidence_score: number;
  imagery_date?: string;
  imagery_source?: string;
  imagery_url?: string;

  // Climate & Risk
  annual_rainfall_mm?: number;
  annual_rainfall_in?: number;
  harvestable_gal_yr?: number;
  drought_risk_index: number;
  flood_risk_index?: number;
  water_restriction_active?: boolean;
  water_stress_tier?: string;

  // Multi-Currency & Tariffs
  currency?: string;
  currency_symbol?: string;
  usd_exchange_rate?: number;
  utility_provider?: string;
  water_rate_per_m3_local?: number;
  sewer_rate_per_m3_local?: number;
  bowser_replacement_rate_per_m3_local?: number;
  water_rate_per_kgal?: number;
  sewer_rate_per_kgal?: number;

  // Operational Water Resilience
  daily_water_demand_m3?: number;
  rationing_days_per_month?: number;
  water_autonomy_days?: number;

  // Financials
  annual_water_savings_usd?: number;
  annual_sewer_savings_usd?: number;
  incentive_value_local?: number;
  incentive_value_usd?: number;
  system_capex_range_local?: [number, number];
  system_capex_range?: [number, number];
  simple_payback_yrs: number;
  npv_10yr_usd?: number;
  confidence_adj_roi_pct: number;

  stormwater_fee_active?: boolean;
  stormwater_fee_local_yr?: number;
  stormwater_fee_usd_yr?: number;
  state_incentive_type?: string;
  permit_pathway?: string;
  regulatory_urgency?: number;
  regulatory_framework?: string;

  // ESG & Certification
  sbti_committed?: boolean;
  net_zero_pledge_yr?: number;
  leed_certified?: boolean;
  edge_certified?: boolean;
  sdg6_aligned?: boolean;
  esg_score_proxy?: number;
  water_risk_in_10k?: boolean;
  sec_filing_snippet?: string;

  urgency_score: number;
  urgency_drivers: string[];
  recommended_angle: "cost_savings" | "resilience" | "compliance" | "esg_credibility";
  viability_score: number;
};

