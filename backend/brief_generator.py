# brief_generator.py
import os
import json
import logging
from pathlib import Path

from dotenv import load_dotenv
from pydantic import ValidationError

from models import BuildingRecord, BriefResponse, ROIResponse
from models import ProspectSummary, PhysicalSuitability, FinancialSnapshot, ConfidenceCaveats
from rag_retrieval import retrieve_context

load_dotenv()

logger = logging.getLogger(__name__)

MODEL = "gemini-2.5-flash"

# ── Feature flags ─────────────────────────────────────────────────────────────
USE_GEMINI = os.environ.get("USE_GEMINI", "true").lower() != "false"

# Session-level circuit breaker: flipped to True on quota/rate errors
_gemini_disabled = False

# ── Brief cache (in-memory, keyed by building_id) ─────────────────────────────
_brief_cache: dict[str, BriefResponse] = {}

# Persist cache to disk
_CACHE_FILE = Path(__file__).parent / "data" / "brief_cache.json"


def _load_disk_cache():
    if _CACHE_FILE.exists():
        try:
            raw = json.loads(_CACHE_FILE.read_text(encoding="utf-8"))
            for bid, data in raw.items():
                _brief_cache[bid] = BriefResponse.model_validate(data)
            logger.info("Loaded %d cached briefs from disk.", len(_brief_cache))
        except Exception as e:
            logger.warning("Could not load brief cache: %s", e)


def _save_disk_cache(building_id: str, brief: BriefResponse):
    try:
        existing = {}
        if _CACHE_FILE.exists():
            existing = json.loads(_CACHE_FILE.read_text(encoding="utf-8"))
        existing[building_id] = brief.model_dump()
        _CACHE_FILE.write_text(json.dumps(existing, indent=2), encoding="utf-8")
    except Exception as e:
        logger.warning("Could not persist brief cache: %s", e)


_load_disk_cache()

# ── Gemini client (lazy) ──────────────────────────────────────────────────────
_client = None


def _get_client():
    global _client
    if _client is None:
        from google import genai
        key = os.environ.get("GOOGLE_API_KEY")
        if not key:
            raise RuntimeError("GOOGLE_API_KEY not set — add it to backend/.env")
        _client = genai.Client(api_key=key)
    return _client


# ── Prompt builder ────────────────────────────────────────────────────────────

def build_prompt(building: BuildingRecord, roi: ROIResponse, context: str) -> str:
    return f"""You are an elite Water Infrastructure & Sustainability Engineer writing a decision-grade
investment brief for a commercial/institutional rainwater harvesting opportunity in Nairobi, Kenya.
Fill every field with specific, numbers-driven content in Kenyan Shillings (KShs) and metric units (Liters/m³).

## Candidate Building Profile
- Building: {building.address} ({building.building_type})
- Location: {building.metro}, {building.county}
- Roof Surface Area: {building.roof_area_sqm:,.0f} m²
- Cooling Tower Detected: {building.cooling_tower_present} (Satellite Confidence: {building.cv_confidence_score * 100:.0f}%)
- Annual Local Rainfall: {building.annual_rainfall_mm} mm/yr (Bimodal Nairobi pattern)

## ROI & Resilience Model ({roi.scenario} scenario)
- Harvestable Volume:             {roi.harvestable_liters:,} Liters/year ({roi.harvestable_m3:,.1f} m³/year)
- Annual Municipal Water Savings: KSh {roi.annual_water_savings_kes:,.0f}
- Annual Sewer Surcharge Relief:  KSh {roi.annual_sewer_savings_kes:,.0f}
- Water Bowser (Trucking) Avoided: KSh {roi.annual_bowser_avoidance_kes:,.0f}
- Total Annual Savings:           KSh {roi.total_annual_savings_kes:,.0f}
- Estimated System Capex (Mid):   KSh {roi.capex_mid_kes:,.0f}
- Simple Payback Period:          {roi.simple_payback_yrs} Years
- 10-Year Discounted NPV (10%):   KSh {roi.npv_10yr_kes:,.0f}
- Confidence-Adjusted ROI:        {roi.confidence_adj_roi_pct}% (Base ROI × {roi.cv_confidence_pct}% CV confidence)
- Carbon Abatement:               {roi.co2_offset_kg:,} kg CO₂e/year

## Grounded Kenyan Regulatory & Market Context
{context}

## Instructions
**why_this_building_now** — Write 2–3 sharp sentences combining NCWSC supply gaps, water trucking costs, roof capture capacity, and SDG 6 impact.
**recommended_sales_angle** — State the customized value proposition ({building.recommended_angle}).
**confidence_caveats** — Provide:
- cv_confidence_pct reflecting satellite detection certainty.
- key_assumptions: 2–3 load-bearing assumptions (e.g. 950mm bimodal rainfall, KSh 125/m³ tariff).
- next_validation_step: single highest-value action (e.g. on-site roof inspection and NCWSC billing audit).
**six_week_action_plan** — Provide 6 weekly bullet points detailing drone LIDAR scan, storage tank sizing, dual plumbing integration, WRA permitting, and commissioning.

Return a complete, sales-ready brief conforming to the schema.
"""


# ── Template fallback ─────────────────────────────────────────────────────────

def _fmtkes(n: float) -> str:
    if n >= 1_000_000: return f"KSh {n/1_000_000:.2f}M"
    if n >= 1_000:     return f"KSh {n/1_000:.0f}K"
    return f"KSh {n:,.0f}"


def generate_template_brief(building: BuildingRecord, roi: ROIResponse) -> BriefResponse:
    cv_pct    = roi.cv_confidence_pct
    btype     = building.building_type.replace("_", " ").title()
    city      = building.metro
    savings   = _fmtkes(roi.total_annual_savings_kes)
    payback   = f"{roi.simple_payback_yrs:.1f}"
    npv       = _fmtkes(roi.npv_10yr_kes)
    harvest_l = f"{roi.harvestable_liters:,}"
    harvest_m3 = f"{roi.harvestable_m3:,.1f}"

    angle_map = {
        "cost_savings":    "Utility Tariff & Sewerage Surcharge Reduction",
        "resilience":      "Water Rationing Resilience & Bowser Disintermediation",
        "compliance":      "NEMA Water Quality & 2024 Building Code Mandate Compliance",
        "esg_credibility": "Strathmore Sustainability & SDG 6 Clean Water Leadership",
    }
    sales_angle = angle_map.get(building.recommended_angle, "Rainwater Resilience & Cost Optimization")

    drivers = building.urgency_drivers or [
        f"NCWSC rationing cycles in {building.metro}",
        f"Large {btype} roof surface suitable for high-volume collection",
        "Rising private water bowser costs during supply cuts",
    ]

    why_now = (
        f"{btype} in {city} presents a {savings}/year savings and risk mitigation opportunity with a "
        f"{payback}-year simple payback at prevailing NCWSC commercial rates and tanker prices. "
        f"The {building.roof_area_sqm:,.0f} m² roof can harvest {harvest_l} Liters/year ({harvest_m3} m³/yr) "
        f"at {cv_pct}% CV satellite confidence, yielding a 10-year NPV of {npv}. "
        f"{drivers[0]} creates urgent justification for immediate system deployment."
    )

    incentive_note = (
        f"KSh {building.incentive_value_kes:,.0f} sustainability rebate/grant applicable"
        if building.incentive_value_kes > 0
        else "Direct utility bill and bowser displacement ROI model"
    )

    action_plan = [
        "Week 1: Drone roof LIDAR survey & gutter flow rate verification.",
        "Week 2: Water consumption audit & NCWSC 12-month billing baseline analysis.",
        "Week 3: Storage tank sizing (modular underground/surface) & first-flush filtration engineering.",
        "Week 4: Dual-plumbing schematic design for toilet flushing and non-potable loop integration.",
        "Week 5: WRA (Water Resources Authority) registration & NEMA EIA checklist sign-off.",
        "Week 6: System installation, IoT flow sensor calibration, and facility team commissioning."
    ]

    return BriefResponse(
        prospect_summary=ProspectSummary(
            address=building.address or f"{btype} · {city}",
            metro_state=f"{building.metro}, {building.county}",
            building_type=btype,
            viability_score=building.viability_score,
        ),
        physical_suitability=PhysicalSuitability(
            roof_area_sqm=int(building.roof_area_sqm),
            cooling_tower_detected=building.cooling_tower_present,
            cv_confidence_pct=cv_pct,
            annual_capture_liters=roi.harvestable_liters,
            annual_capture_m3=roi.harvestable_m3,
        ),
        financial_snapshot=FinancialSnapshot(
            total_annual_savings_kes=int(roi.total_annual_savings_kes),
            simple_payback_yrs=roi.simple_payback_yrs,
            npv_10yr_kes=int(roi.npv_10yr_kes),
            confidence_adj_roi_pct=roi.confidence_adj_roi_pct,
            incentive_flags=incentive_note,
        ),
        why_this_building_now=why_now,
        recommended_sales_angle=sales_angle,
        confidence_caveats=ConfidenceCaveats(
            cv_confidence_pct=cv_pct,
            key_assumptions=(
                f"1. Nairobi annual rainfall average of {building.annual_rainfall_mm}mm (KMD bimodal data). "
                f"2. 85% collection efficiency on commercial roof structure. "
                f"3. NCWSC commercial tariff at KSh {building.water_rate_per_m3_kes:.2f}/m³ and bowser rate at KSh {building.bowser_replacement_rate_per_m3_kes:.2f}/m³."
            ),
            next_validation_step=(
                "Conduct structural load inspection of roof beams and verify 12-month NCWSC utility receipts "
                f"{'along with HVAC cooling tower blowdown meter logs' if building.cooling_tower_present else ''}."
            ),
        ),
        six_week_action_plan=action_plan,
    )


# ── Gemini generator ──────────────────────────────────────────────────────────

def _call_gemini(building: BuildingRecord, roi: ROIResponse) -> BriefResponse:
    from google.genai import types

    context = retrieve_context(building)
    prompt  = build_prompt(building, roi, context)

    response = _get_client().models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=BriefResponse,
        ),
    )
    return BriefResponse.model_validate_json(response.text)


# ── Public entry point ────────────────────────────────────────────────────────

def generate_brief(building: BuildingRecord, roi: ROIResponse) -> BriefResponse:
    global _gemini_disabled

    bid = building.building_id

    # 1. Cache hit
    if bid in _brief_cache:
        logger.info("Brief cache hit for %s", bid)
        return _brief_cache[bid]

    # 2. Gemini path
    if USE_GEMINI and not _gemini_disabled:
        try:
            brief = _call_gemini(building, roi)
            logger.info("Gemini brief generated for %s", bid)
        except Exception as e:
            err = str(e)
            if "429" in err or "quota" in err.lower() or "RESOURCE_EXHAUSTED" in err:
                logger.warning("Gemini quota hit — disabling for this session. Falling back to template.")
                _gemini_disabled = True
            else:
                logger.warning("Gemini failed (%s) — falling back to template.", err)
            brief = generate_template_brief(building, roi)
    else:
        reason = "USE_GEMINI=false" if not USE_GEMINI else "quota circuit breaker active"
        logger.info("Using template brief for %s (%s)", bid, reason)
        brief = generate_template_brief(building, roi)

    # 3. Cache and return
    _brief_cache[bid] = brief
    _save_disk_cache(bid, brief)
    return brief
