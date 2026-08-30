"""
brief_html.py
Generates a self-contained HTML document for the investment brief in Kenyan context.
Used by the email endpoint to produce the PDF attachment.
"""

from __future__ import annotations
from models import BuildingRecord, ROIResponse, BriefResponse


def _kes(n: float) -> str:
    if n >= 1_000_000:
        return f"KSh {n / 1_000_000:.2f}M"
    if n >= 1_000:
        return f"KSh {round(n / 1_000)}K"
    return f"KSh {n:,.0f}"


def _liters(n: float) -> str:
    if n >= 1_000_000:
        return f"{n / 1_000_000:.2f}M L/yr"
    if n >= 1_000:
        return f"{round(n / 1_000)}K L/yr"
    return f"{n:,} L/yr"


def _esc(s: object) -> str:
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


ANGLE_LABELS = {
    "cost_savings":    "Tariff & Sewerage Savings",
    "resilience":      "Rationing Resilience & Bowser Disintermediation",
    "compliance":      "NEMA & 2024 Building Code Compliance",
    "esg_credibility": "SDG 6 Clean Water & Sustainability",
}


def _kpi_card(label: str, value: str, sub: str | None, highlight: bool) -> str:
    bg      = "#f0fdfa" if highlight else "#ffffff"
    border  = "#99f6e4" if highlight else "#e2e8f0"
    val_clr = "#0f766e" if highlight else "#0f172a"
    sub_clr = "#0d9488" if highlight else "#64748b"
    sub_html = f'<span style="font-size:10px;color:{sub_clr};">{_esc(sub)}</span>' if sub else ""
    return (
        f'<div style="background:{bg};border:1px solid {border};border-radius:12px;'
        f'padding:13px 15px;display:flex;flex-direction:column;gap:5px;break-inside:avoid;">'
        f'<span style="font-size:8.5px;font-weight:700;text-transform:uppercase;'
        f'letter-spacing:0.08em;color:#64748b;">{_esc(label)}</span>'
        f'<span style="font-size:19px;font-weight:900;color:{val_clr};line-height:1;'
        f'font-variant-numeric:tabular-nums;">{_esc(value)}</span>'
        f'{sub_html}</div>'
    )


def _savings_bar(label: str, kes: float, total: float) -> str:
    pct = round(kes / total * 100) if total > 0 else 0
    return (
        f'<div style="display:flex;align-items:center;gap:12px;margin-bottom:9px;">'
        f'<span style="font-size:12px;color:#64748b;width:155px;flex-shrink:0;">{_esc(label)}</span>'
        f'<div style="flex:1;height:5px;background:#f1f5f9;border-radius:9999px;overflow:hidden;">'
        f'<div style="width:{pct}%;height:100%;background:linear-gradient(to right,#2dd4bf,#14b8a6);'
        f'border-radius:9999px;"></div></div>'
        f'<span style="font-size:12px;font-weight:600;color:#334155;width:90px;text-align:right;'
        f'font-variant-numeric:tabular-nums;">{_kes(kes)}</span></div>'
    )


def _bullet(text: str, color: str) -> str:
    return (
        f'<li style="display:flex;align-items:flex-start;gap:10px;margin-bottom:8px;">'
        f'<span style="margin-top:7px;width:6px;height:6px;border-radius:50%;'
        f'background:{color};flex-shrink:0;display:inline-block;"></span>'
        f'<span style="font-size:12px;color:#334155;line-height:1.6;">{_esc(text)}</span></li>'
    )


def _step_card(order: str, action: str, owner: str, horizon: str) -> str:
    return (
        f'<div style="display:flex;align-items:flex-start;gap:11px;padding:11px 13px;'
        f'background:#f8fafc;border:1px solid #f1f5f9;border-radius:12px;margin-bottom:7px;break-inside:avoid;">'
        f'<div style="flex-shrink:0;width:24px;height:24px;border-radius:50%;background:#fff1f2;'
        f'border:1px solid #fecdd3;display:flex;align-items:center;justify-content:center;">'
        f'<span style="font-size:9px;font-weight:900;color:#e11d48;">{_esc(order)}</span></div>'
        f'<div><p style="font-size:12px;font-weight:600;color:#1e293b;margin:0 0 3px 0;">{_esc(action)}</p>'
        f'<span style="font-size:10px;color:#94a3b8;">{_esc(owner)}</span>'
        f'<span style="color:#cbd5e1;margin:0 4px;">·</span>'
        f'<span style="font-size:10px;font-weight:600;color:#fb7185;">{_esc(horizon)}</span>'
        f'</div></div>'
    )


def generate_brief_html(
    building: BuildingRecord,
    roi: ROIResponse,
    brief: BriefResponse,
    generated_at: str,
) -> str:
    """Return a complete standalone HTML document for the investment brief."""

    cv_pct      = brief.physical_suitability.cv_confidence_pct
    capex_low   = building.system_capex_range_kes[0] if building.system_capex_range_kes else round(roi.capex_mid_kes * 0.85)
    capex_high  = building.system_capex_range_kes[1] if building.system_capex_range_kes else round(roi.capex_mid_kes * 1.15)
    angle_label = ANGLE_LABELS.get(building.recommended_angle, building.recommended_angle)
    street_addr = building.address.split(",")[0]

    savings_breakdown = [
        ("Municipal Water Savings", roi.annual_water_savings_kes),
        ("Sewer Surcharge Relief",  roi.annual_sewer_savings_kes),
        ("Bowser/Tanker Avoidance",  roi.annual_bowser_avoidance_kes),
    ]
    if building.incentive_value_kes > 0:
        savings_breakdown.append(("Sustainability Rebate", building.incentive_value_kes / 10.0))
    total_savings = sum(v for _, v in savings_breakdown)

    kpis = [
        ("Harvestable Volume",  _liters(brief.physical_suitability.annual_capture_liters),
         f"{roi.harvestable_m3:,.0f} m³/yr yield", False),
        ("Annual Savings",      _kes(roi.total_annual_savings_kes),
         "NCWSC + Bowser offsets", False),
        ("Simple Payback",      f"{roi.simple_payback_yrs:.1f} yrs",
         "10-year asset life", False),
        ("10-yr NPV (10%)",     _kes(roi.npv_10yr_kes),
         "Discounted net value", False),
        ("Base ROI",            f"{roi.base_roi_pct:.1f}%",
         "10-year horizon", False),
        ("Confidence-Adj ROI",  f"{roi.confidence_adj_roi_pct:.1f}%",
         f"Discounted by {cv_pct}% CV confidence", True),
        ("CO₂ Offset",          f"{roi.co2_offset_kg:,} kg/yr",
         "Pumping grid abatement", False),
        ("CapEx Midpoint",      _kes(roi.capex_mid_kes),
         f"Range: {_kes(capex_low)} – {_kes(capex_high)}", False),
    ]
    kpi_html = "".join(_kpi_card(l, v, s, h) for l, v, s, h in kpis)
    bars_html = "".join(_savings_bar(l, v, total_savings) for l, v in savings_breakdown)

    opp_bullets = [
        f"{brief.physical_suitability.roof_area_sqm:,} m² roof captures approximately "
        f"{_liters(brief.physical_suitability.annual_capture_liters)} ({roi.harvestable_m3:,.0f} m³) under bimodal rainfall.",
        f"Annual combined savings of {_kes(roi.total_annual_savings_kes)} deliver a "
        f"{roi.simple_payback_yrs:.1f}-year simple payback, mitigating acute water rationing in {building.metro}.",
        (
            f"HVAC cooling tower consumption detected at {cv_pct}% CV confidence — "
            "highest-impact replacement for blowdown make-up water."
            if brief.physical_suitability.cooling_tower_detected
            else f"Roof geometry verified at {cv_pct}% CV confidence via satellite imagery."
        ),
        f"Avoids high-cost emergency water bowser deliveries (KSh {building.bowser_replacement_rate_per_m3_kes}/m³) during municipal outages."
    ]
    opp_html = "".join(_bullet(b, "#93c5fd") for b in opp_bullets)

    esg_bullets_data = [
        f"Supports SDG 6 (Clean Water and Sanitation) and Kenya Climate Change Act 2016 goals.",
        f"Direct carbon abatement of {roi.co2_offset_kg:,} kg CO₂e/year from reduced municipal pumping.",
        f"10-year discounted NPV of {_kes(roi.npv_10yr_kes)} at 10% rate shows robust financial returns."
    ]
    esg_html = "".join(_bullet(b, "#d8b4fe") for b in esg_bullets_data)

    steps = [
        ("1", "Conduct drone LIDAR roof survey & structural beam load verification", "Engineering Lead", "Week 1–2"),
        ("2", "Audit 12-month NCWSC utility bills and private water tanker delivery logs", "Facility Manager", "Week 1"),
        ("3", "Size modular underground storage tanks and dual-plumbing non-potable loop", "Hydraulic Engineer", "Week 2–3"),
        ("4", "File WRA (Water Resources Authority) registration & NEMA compliance check", "Compliance Officer", "Week 4"),
        ("5", "Procure filtration (KS EAS 12 standard) & automated IoT level monitors", "Procurement Lead", "Week 4–5"),
        ("6", "Commission system and train estate facilities team on seasonal valve switches", "Project Lead", "Week 6"),
    ]
    steps_html = "".join(_step_card(*s) for s in steps)

    closing = (
        f"This {building.building_type.replace('_', ' ')} in {building.metro} represents a "
        f"{'critical-urgency' if roi.simple_payback_yrs <= 3.5 else 'high-impact'} resilience project: "
        f"{_kes(roi.total_annual_savings_kes)}/yr in combined savings at a "
        f"{roi.simple_payback_yrs:.1f}-year payback."
    )

    disclaimer = (
        "This brief was generated by the Tone AI engine for commercial water reuse prospecting. "
        "Calculations reflect commercial water/sewer tariffs, stormwater fee schedules, and satellite CV confidence."
    )

    building_ref = building.building_id.upper()

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>Tone Investment Brief - {building_ref}</title>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 0; padding: 24px; color: #0f172a; background: #ffffff; }}
  .header {{ border-bottom: 2px solid #0f766e; padding-bottom: 16px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: flex-end; }}
  .grid-kpis {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 24px; }}
  .section {{ margin-bottom: 24px; }}
  .section-title {{ font-size: 14px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #0f766e; margin-bottom: 12px; }}
</style>
</head>
<body>
  <div class="header">
    <div>
      <h1 style="margin:0;font-size:22px;color:#0f766e;">TONE · INVESTMENT BRIEF</h1>
      <p style="margin:4px 0 0;font-size:14px;color:#64748b;">{_esc(building.address)} ({building_ref})</p>
    </div>
    <div style="text-align:right;">
      <span style="display:inline-block;padding:4px 10px;background:#f0fdfa;border:1px solid #99f6e4;border-radius:9999px;font-size:12px;font-weight:700;color:#0f766e;">
        {_esc(angle_label)}
      </span>
      <p style="margin:4px 0 0;font-size:11px;color:#94a3b8;">Generated {generated_at}</p>
    </div>
  </div>

  <div class="section">
    <div class="section-title">Executive Summary</div>
    <p style="font-size:13px;line-height:1.6;color:#334155;margin:0 0 16px;">{_esc(brief.why_this_building_now)}</p>
    <div class="grid-kpis">{kpi_html}</div>
  </div>

  <div class="section" style="display:flex;gap:24px;">
    <div style="flex:1;">
      <div class="section-title">Annual Savings Breakdown</div>
      {bars_html}
    </div>
    <div style="flex:1;">
      <div class="section-title">Physical & Climate Viability</div>
      <ul style="list-style:none;padding:0;margin:0;">{opp_html}</ul>
    </div>
  </div>

  <div class="section">
    <div class="section-title">6-Week Engineering & Deployment Action Plan</div>
    <div style="display:grid;grid-template-columns:repeat(2, 1fr);gap:10px;">{steps_html}</div>
  </div>

  <div class="section" style="border-top:1px solid #e2e8f0;padding-top:14px;">
    <div class="section-title">SDG 6 Clean Water & Climate Impact</div>
    <ul style="list-style:none;padding:0;margin:0;">{esg_html}</ul>
    <p style="font-size:12px;color:#475569;margin-top:12px;">{closing}</p>
    <p style="font-size:10px;color:#94a3b8;margin-top:12px;">{disclaimer}</p>
  </div>
</body>
</html>
"""
