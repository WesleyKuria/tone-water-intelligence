# rag_corpus.py

CORPUS = [
    {
        "source": "Kenya Water Act 2016 (Sections 36 & 40) - Water Resources Authority (WRA)",
        "tags": ["Nairobi", "compliance", "permitting", "WRA", "resilience"],
        "text": (
            "The Water Act 2016 empowers WRA to regulate commercial water abstraction and storage. "
            "Commercial rainwater harvesting systems exceeding 50,000 liters are encouraged to reduce "
            "reliance on stressed aquifers and municipal supply lines. Stored surface runoff requires appropriate "
            "spillway design and first-flush diversion mechanisms to prevent urban flash flooding."
        ),
    },
    {
        "source": "NEMA Environmental Management and Co-ordination (Water Quality) Regulations 2006",
        "tags": ["NEMA", "compliance", "sanitation", "water_quality"],
        "text": (
            "Third Schedule standards stipulate effluent discharge and non-potable re-use specifications. "
            "Harvested rainwater used for toilet flushing, HVAC cooling towers, and landscape irrigation "
            "must comply with basic turbidity (<5 NTU), suspended solids, and total coliform thresholds. "
            "A standard first-flush diverter and multi-barrier filtration system comply with NEMA audit expectations."
        ),
    },
    {
        "source": "Kenya National Building Code 2024 (Section 64 & Green Building Standards)",
        "tags": ["compliance", "engineering", "Nairobi", "roof"],
        "text": (
            "Mandatory rainwater harvesting provisions apply to commercial, institutional, and high-density "
            "residential developments with roof surfaces exceeding 200 m². Mandates gutters sized for 50-year "
            "storm intensities (Nairobi peak 100mm/hr) and separate plumbing loops for non-potable water supply."
        ),
    },
    {
        "source": "NCWSC Nairobi Water Distribution & Rationing Policy 2023-2027",
        "tags": ["resilience", "cost_savings", "Nairobi", "drought"],
        "text": (
            "Nairobi faces a 300,000 m³/day supply deficit against 810,000 m³/day demand. Commercial zones "
            "(Industrial Area, Upper Hill, Westlands, Madaraka) experience 2 to 4 rationing days weekly. Relying on "
            "private water bowsers costs between KSh 600 - 900 per m³ compared to standard KSh 120/m³ municipal "
            "tariffs. Decentralized rooftop storage provides 14 to 30 days of strategic water buffering."
        ),
    },
    {
        "source": "Kenya Standard KS EAS 12:2018 & KS 05-459 (Rainwater Quality Guidelines)",
        "tags": ["water_quality", "sanitation", "cooling_tower", "KS"],
        "text": (
            "Specifies microbiological and chemical thresholds for non-potable commercial applications. "
            "When integrating rainwater into HVAC cooling towers or institutional laundry, dual media "
            "sand filtration, UV sterilization, and anti-scaling conditioning are required to prevent Legionella "
            "and corrosion."
        ),
    },
    {
        "source": "Strathmore Sustainability Framework & Kenya Climate Change Act 2016",
        "tags": ["ESG", "esg_credibility", "SDG6", "education"],
        "text": (
            "Aligns with Kenya National Climate Change Action Plan (NCCAP III) and SDG 6 (Clean Water and "
            "Sanitation). Institutional rainwater capture provides demonstrable ESG metric credits, reduces "
            "embodied carbon in municipal water transmission, and qualifies for Green Building Society certification."
        ),
    }
]
