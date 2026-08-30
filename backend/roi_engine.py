# roi_engine.py
from dataclasses import dataclass
from models import BuildingRecord

COLLECTION_EFFICIENCY = 0.85
CO2_KG_PER_M3 = 0.32  # Carbon offset for pumping & grid treatment

# Country-specific commercial discount rates
COUNTRY_DISCOUNT_RATES = {
    "KE": 0.10,  # Central Bank of Kenya commercial benchmark
    "ZA": 0.09,  # South African Reserve Bank benchmark
    "NG": 0.14,  # Central Bank of Nigeria benchmark
    "RW": 0.10,  # National Bank of Rwanda benchmark
    "GH": 0.16,  # Bank of Ghana benchmark
    "US": 0.06,  # US commercial benchmark
}

SCENARIO_MULTIPLIERS = {
    "conservative": {"rainfall": 0.80, "efficiency": 0.80, "capex": 1.15},
    "base":         {"rainfall": 1.00, "efficiency": 0.85, "capex": 1.00},
    "upside":       {"rainfall": 1.20, "efficiency": 0.90, "capex": 0.90},
}

def calc_harvestable_liters(
    roof_area_sqm: float,
    annual_rainfall_mm: float,
    efficiency: float = COLLECTION_EFFICIENCY,
) -> float:
    """1 mm of rainfall on 1 m² roof = 1 Liter of water."""
    return roof_area_sqm * annual_rainfall_mm * efficiency

def calc_npv(annual_savings: float, capex: float, discount_rate: float = 0.10, years: int = 10) -> float:
    npv = -capex
    for y in range(1, years + 1):
        npv += annual_savings / ((1 + discount_rate) ** y)
    return npv

def calc_scenario(building: BuildingRecord, scenario: str = "base") -> dict:
    m = SCENARIO_MULTIPLIERS.get(scenario, SCENARIO_MULTIPLIERS["base"])
    
    # Retrieve local Capex range
    capex_range = building.system_capex_range_local or building.system_capex_range_kes or (3500000.0, 5500000.0)
    capex_mid = sum(capex_range) / 2.0

    harvestable_l = calc_harvestable_liters(
        building.roof_area_sqm,
        building.annual_rainfall_mm * m["rainfall"],
        efficiency=m["efficiency"],
    )
    harvestable_m3 = harvestable_l / 1000.0

    # Tariffs
    water_rate = building.water_rate_per_m3_local or building.water_rate_per_m3_kes or 125.0
    sewer_rate = building.sewer_rate_per_m3_local or building.sewer_rate_per_m3_kes or 93.75
    discharge_fraction = building.sewer_discharge_fraction or 0.75

    # 1. Municipal Water & Sewer Savings in local currency
    water_savings = harvestable_m3 * water_rate
    sewer_savings = harvestable_m3 * sewer_rate * discharge_fraction
    
    # 2. Alternative Water / Tanker Bowser / Diesel Borehole Avoidance
    bowser_rate = (
        building.bowser_replacement_rate_per_m3_local
        or building.bowser_replacement_rate_per_m3_kes
        or 750.0
    )
    # Estimate fraction of water that would otherwise be trucked in during supply cuts / dry spells
    rationing_offset_fraction = min(0.50, (building.rationing_days_per_month / 30.0) * 0.90) if building.rationing_days_per_month > 0 else 0.35
    bowser_avoidance = (harvestable_m3 * rationing_offset_fraction) * max(0.0, bowser_rate - water_rate)
    
    # 3. Sustainability Incentive / Rebate Amortization
    incentive_val = building.incentive_value_local or building.incentive_value_kes or 0.0
    incentive_annual = incentive_val / 10.0
    
    total_savings_local = water_savings + sewer_savings + bowser_avoidance + incentive_annual

    capex_adjusted = capex_mid * m["capex"]
    payback = capex_adjusted / total_savings_local if total_savings_local > 0 else 0.0
    
    # Country-specific discount rate
    discount_rate = COUNTRY_DISCOUNT_RATES.get(building.country_code, 0.10)
    npv_local = calc_npv(total_savings_local, capex_adjusted, discount_rate=discount_rate)
    
    base_roi = (((total_savings_local * 10) - capex_adjusted) / capex_adjusted * 100) if capex_adjusted > 0 else 0.0
    adj_roi = base_roi * building.cv_confidence_score
    co2_offset_kg = harvestable_m3 * CO2_KG_PER_M3

    # USD Normalization
    usd_rate = building.usd_exchange_rate if building.usd_exchange_rate > 0 else 130.0
    total_savings_usd = total_savings_local / usd_rate
    capex_mid_usd = capex_adjusted / usd_rate
    npv_10yr_usd = npv_local / usd_rate

    # Water Autonomy Days (how many operating days the captured water supports)
    daily_demand = building.daily_water_demand_m3 if building.daily_water_demand_m3 > 0 else 15.0
    autonomy_days = int(harvestable_m3 / daily_demand) if daily_demand > 0 else 30

    return {
        "building_id":                  building.building_id,
        "scenario":                     scenario,
        "currency":                     building.currency,
        "currency_symbol":              building.currency_symbol,
        "usd_exchange_rate":            usd_rate,
        "harvestable_liters":           int(harvestable_l),
        "harvestable_m3":               round(harvestable_m3, 1),
        "water_autonomy_days":          autonomy_days,

        # Local Currency
        "annual_water_savings_local":    round(water_savings, 2),
        "annual_sewer_savings_local":    round(sewer_savings, 2),
        "annual_bowser_avoidance_local": round(bowser_avoidance, 2),
        "total_annual_savings_local":    round(total_savings_local, 2),
        "capex_mid_local":               round(capex_adjusted, 2),
        "npv_10yr_local":                round(npv_local, 2),

        # USD Normalised
        "total_annual_savings_usd":      round(total_savings_usd, 2),
        "capex_mid_usd":                 round(capex_mid_usd, 2),
        "npv_10yr_usd":                  round(npv_10yr_usd, 2),

        # Backward compatibility
        "annual_water_savings_kes":     round(water_savings, 2),
        "annual_sewer_savings_kes":     round(sewer_savings, 2),
        "annual_bowser_avoidance_kes":  round(bowser_avoidance, 2),
        "total_annual_savings_kes":     round(total_savings_local, 2),
        "capex_mid_kes":                round(capex_adjusted, 2),
        "npv_10yr_kes":                 round(npv_local, 2),

        "simple_payback_yrs":           round(payback, 1),
        "base_roi_pct":                 round(base_roi, 1),
        "confidence_adj_roi_pct":       round(adj_roi, 1),
        "co2_offset_kg":                int(co2_offset_kg),
        "cv_confidence_pct":            int(building.cv_confidence_score * 100),
    }

