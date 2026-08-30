# rag_corpus.py

CORPUS = [
    # ── Kenya ──────────────────────────────────────────────────────────────────
    {
        "source": "Kenya Water Act 2016 (Sections 36 & 40) - Water Resources Authority (WRA)",
        "tags": ["Nairobi", "KE", "Kenya", "compliance", "permitting", "WRA", "resilience"],
        "text": (
            "The Water Act 2016 empowers WRA to regulate commercial water abstraction and storage. "
            "Commercial rainwater harvesting systems exceeding 50,000 liters are encouraged to reduce "
            "reliance on stressed aquifers and municipal supply lines. Stored surface runoff requires appropriate "
            "spillway design and first-flush diversion mechanisms to prevent urban flash flooding."
        ),
    },
    {
        "source": "NEMA Environmental Management and Co-ordination (Water Quality) Regulations 2006",
        "tags": ["NEMA", "KE", "Kenya", "compliance", "sanitation", "water_quality"],
        "text": (
            "Third Schedule standards stipulate effluent discharge and non-potable re-use specifications. "
            "Harvested rainwater used for toilet flushing, HVAC cooling towers, and landscape irrigation "
            "must comply with basic turbidity (<5 NTU), suspended solids, and total coliform thresholds. "
            "A standard first-flush diverter and multi-barrier filtration system comply with NEMA audit expectations."
        ),
    },
    {
        "source": "NCWSC Nairobi Water Distribution & Rationing Policy 2023-2027",
        "tags": ["resilience", "cost_savings", "Nairobi", "KE", "Kenya", "drought"],
        "text": (
            "Nairobi faces a 300,000 m³/day supply deficit against 810,000 m³/day demand. Commercial zones "
            "(Industrial Area, Athi River, Upper Hill, Westlands) experience 2 to 4 rationing days weekly. Relying on "
            "private water bowsers costs between KSh 600 - 900 per m³ compared to standard KSh 125/m³ municipal "
            "tariffs. Decentralized rooftop storage provides 14 to 45 days of strategic water buffering."
        ),
    },
    {
        "source": "Kenya Standard KS EAS 12:2018 & KS 05-459 (Rainwater Quality Guidelines)",
        "tags": ["water_quality", "sanitation", "cooling_tower", "KE", "Kenya", "KS"],
        "text": (
            "Specifies microbiological and chemical thresholds for non-potable commercial applications. "
            "When integrating rainwater into HVAC cooling towers or institutional laundry, dual media "
            "sand filtration, UV sterilization, and anti-scaling conditioning are required to prevent Legionella "
            "and corrosion."
        ),
    },
    {
        "source": "Kenya National Climate Change Action Plan (NCCAP III) & SDG 6 Alignment",
        "tags": ["ESG", "esg_credibility", "SDG6", "KE", "Kenya", "education"],
        "text": (
            "Aligns with Kenya National Climate Change Action Plan (NCCAP III) and SDG 6 (Clean Water and "
            "Sanitation). Institutional and commercial rainwater capture provides demonstrable ESG metric credits, "
            "reduces embodied carbon in municipal water transmission, and qualifies for Green Building Society certification."
        ),
    },

    # ── South Africa ───────────────────────────────────────────────────────────
    {
        "source": "City of Cape Town Water By-law (Amended 2018/2020) - Alternative Water Systems",
        "tags": ["Cape Town", "ZA", "South Africa", "compliance", "by-law", "resilience"],
        "text": (
            "Mandates that all commercial and industrial developments install water-saving devices and encourages "
            "rainwater harvesting systems connected to non-potable plumbing lines. System must have an approved "
            "backflow prevention device (reduced pressure zone unit) to prevent contamination of the municipal potable grid. "
            "Offsets punitive Level 2–4 stepped industrial water tariffs."
        ),
    },
    {
        "source": "South Africa National Water Act (Act 36 of 1998) & King IV ESG Guidelines",
        "tags": ["ZA", "South Africa", "Johannesburg", "ESG", "esg_credibility", "compliance"],
        "text": (
            "Under the National Water Act and JSE Sustainability Disclosure guidance (King IV), commercial "
            "property owners and industrial manufacturers are evaluated on water stewardship and catchment resilience. "
            "Decentralized stormwater retention and onsite reuse reduce municipal drainage overload and secure "
            "uninterrupted industrial operations during load-shedding-induced water pumping failures."
        ),
    },

    # ── Nigeria ────────────────────────────────────────────────────────────────
    {
        "source": "Lagos State Water Regulatory Commission (LASWARCO) & Ground Water Conservation Directive",
        "tags": ["Lagos", "NG", "Nigeria", "compliance", "resilience", "cost_savings"],
        "text": (
            "Due to municipal water coverage gaps in industrial estates (Ikeja, Agbara, Lekki FTZ), over 90% of industrial "
            "facilities rely on deep boreholes and costly diesel-powered treatment plants. Lagos experiences over 1,600 mm "
            "of annual precipitation. Harvesting rooftop runoff reduces diesel pumping expenses, halts saline aquifer "
            "intrusion, and lowers reverse osmosis membrane replacement overhead."
        ),
    },
    {
        "source": "Manufacturers Association of Nigeria (MAN) Energy & Water Security Whitepaper",
        "tags": ["Lagos", "NG", "Nigeria", "cost_savings", "resilience", "industrial"],
        "text": (
            "Industrial self-generated water costs in Nigeria average ₦1,800 to ₦2,500 per m³ when factoring in "
            "diesel generator pumping, chemical coagulation, and filtration. Rooftop rainwater capture offers high-purity, "
            "near-zero TDS raw water that cuts operational treatment costs by up to 65% for FMCG and manufacturing plants."
        ),
    },

    # ── Rwanda & Regional SEZs ─────────────────────────────────────────────────
    {
        "source": "Rwanda Environment Management Authority (REMA) & Kigali SEZ Green Guidelines",
        "tags": ["Kigali", "RW", "Rwanda", "compliance", "ESG", "green_sez", "resilience"],
        "text": (
            "Kigali Special Economic Zone (KSEZ) master planning requires all industrial warehouses and manufacturing "
            "units to integrate rainwater retention tanks to prevent downstream Nyabugogo basin flooding. Rainwater capture "
            "qualifies for preferential IFC EDGE Green Building debt financing and reduces WASAC utility bills."
        ),
    }
]

