# roi_engine.py
from dataclasses import dataclass
from models import BuildingRecord

COLLECTION_EFFICIENCY = 0.85
DISCHARGE_FRACTION = 0.75       # NCWSC charges 75% of water volume as sewer
CO2_KG_PER_M3 = 0.32            # Carbon offset for pumping & grid treatment in Kenya
DISCOUNT_RATE = 0.10            # 10% discount rate aligned with CBK commercial rates

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

def calc_npv(annual_savings_kes: float, capex_kes: float, years: int = 10) -> float:
    npv = -capex_kes
    for y in range(1, years + 1):
        npv += annual_savings_kes / ((1 + DISCOUNT_RATE) ** y)
    return npv

def calc_scenario(building: BuildingRecord, scenario: str = "base") -> dict:
    m = SCENARIO_MULTIPLIERS[scenario]
    capex_mid = sum(building.system_capex_range_kes) / 2

    harvestable_l = calc_harvestable_liters(
        building.roof_area_sqm,
        building.annual_rainfall_mm * m["rainfall"],
        efficiency=m["efficiency"],
    )
    harvestable_m3 = harvestable_l / 1000.0

    # 1. Municipal Water & Sewer Savings
    water_savings_kes = harvestable_m3 * building.water_rate_per_m3_kes
    sewer_savings_kes = harvestable_m3 * building.sewer_rate_per_m3_kes * DISCHARGE_FRACTION
    
    # 2. Water Bowser (Trucking) Avoidance during Rationing
    bowser_rate = building.bowser_replacement_rate_per_m3_kes or 750.0
    rationing_offset_fraction = 0.35
    bowser_avoidance_kes = (harvestable_m3 * rationing_offset_fraction) * (bowser_rate - building.water_rate_per_m3_kes)
    
    # 3. Sustainability Incentive / Rebate Amortization
    incentive_annual = building.incentive_value_kes / 10.0
    
    total_savings_kes = water_savings_kes + sewer_savings_kes + bowser_avoidance_kes + incentive_annual

    capex = capex_mid * m["capex"]
    payback = capex / total_savings_kes if total_savings_kes > 0 else 0.0
    npv = calc_npv(total_savings_kes, capex)
    base_roi = (((total_savings_kes * 10) - capex) / capex * 100) if capex > 0 else 0.0
    adj_roi = base_roi * building.cv_confidence_score
    co2_offset_kg = harvestable_m3 * CO2_KG_PER_M3

    return {
        "harvestable_liters":           int(harvestable_l),
        "harvestable_m3":               round(harvestable_m3, 1),
        "annual_water_savings_kes":     round(water_savings_kes, 2),
        "annual_sewer_savings_kes":     round(sewer_savings_kes, 2),
        "annual_bowser_avoidance_kes":  round(bowser_avoidance_kes, 2),
        "total_annual_savings_kes":     round(total_savings_kes, 2),
        "capex_mid_kes":                round(capex, 2),
        "simple_payback_yrs":           round(payback, 1),
        "npv_10yr_kes":                 round(npv, 2),
        "base_roi_pct":                 round(base_roi, 1),
        "confidence_adj_roi_pct":       round(adj_roi, 1),
        "co2_offset_kg":                int(co2_offset_kg),
        "cv_confidence_pct":            int(building.cv_confidence_score * 100),
    }
