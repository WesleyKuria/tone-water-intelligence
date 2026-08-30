"use client";

import { motion, useInView } from "framer-motion";
import { useRef } from "react";
import Link from "next/link";
import ToneLogo from "@/components/ui/ToneLogo";
import { Droplet, CheckCircle2, TrendingUp, Sparkles, Building2 } from "lucide-react";

// ── Animation variants ────────────────────────────────────────────────────────

const EASE: [number, number, number, number] = [0.25, 0.46, 0.45, 0.94];

const fadeUpVariant = {
  hidden: { opacity: 0, y: 36 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.75, ease: EASE } },
};

const staggerContainer = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.13, delayChildren: 0.05 } },
};

function ScrollFade({
  children,
  className = "",
  delay = 0,
}: {
  children: React.ReactNode;
  className?: string;
  delay?: number;
}) {
  const ref = useRef<HTMLDivElement>(null);
  const inView = useInView(ref, { once: true, margin: "-80px" });
  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 36 }}
      animate={inView ? { opacity: 1, y: 0 } : { opacity: 0, y: 36 }}
      transition={{ duration: 0.75, ease: EASE, delay }}
      className={className}
    >
      {children}
    </motion.div>
  );
}

function ScrollStagger({
  children,
  className = "",
}: {
  children: React.ReactNode;
  className?: string;
}) {
  const ref = useRef<HTMLDivElement>(null);
  const inView = useInView(ref, { once: true, margin: "-80px" });
  return (
    <motion.div
      ref={ref}
      variants={staggerContainer}
      initial="hidden"
      animate={inView ? "visible" : "hidden"}
      className={className}
    >
      {children}
    </motion.div>
  );
}

// ── Data ──────────────────────────────────────────────────────────────────────

const funnelSteps = [
  {
    value: "129M",
    label: "Building footprints ingested",
    sub: "Microsoft USBuildingFootprints + Overture Maps — entire continental US",
  },
  {
    value: "~2M",
    label: "Commercial candidates",
    sub: "Filtered by NAICS codes, roof area >100,000 sq ft, non-residential classification",
  },
  {
    value: "50k+",
    label: "Fully scored buildings",
    sub: "After joining precipitation, utility rates, ESG risk, and regulatory layers",
  },
  {
    value: "11,577",
    label: "High-opportunity targets",
    sub: "Top-ranked across 37 states — surfaced on the interactive map",
  },
];

const dataSources = [
  {
    category: "Geometry",
    source: "Microsoft USBuildingFootprints",
    detail: "129M records — polygon area, classification, centroid",
  },
  {
    category: "Industrial signals",
    source: "EPA Facility Registry Service + NAICS",
    detail: "Flags cooling towers: non-potable water demand proxy",
  },
  {
    category: "Climate yield",
    source: "NOAA 30-Year Climatology Normals",
    detail: "Location-specific rainfall to calculate max harvestable gallons/yr",
  },
  {
    category: "Financials",
    source: "EFC Utility Dashboards + Municipal Open Data",
    detail: "Localized water/sewer rates for NPV, payback, ROI",
  },
  {
    category: "ESG & risk",
    source: "WRI Aqueduct Water Risk Atlas + SBTN/GRI",
    detail: "Drought stress index + corporate water-target compliance scores",
  },
  {
    category: "Policy",
    source: "TCEQ + State Tax Codes",
    detail: "Equipment exemptions factored into base and upside financial scenarios",
  },
];

const scoringDimensions = [
  {
    number: "01",
    title: "Physical Viability",
    detail: "Roof polygon area, geometry classification, structural signals from satellite + footprint data.",
  },
  {
    number: "02",
    title: "Financial Return",
    detail: "Three-scenario ROI model: base, conservative, upside. 10-year NPV, payback period, annualized savings.",
  },
  {
    number: "03",
    title: "Regulatory Incentives",
    detail: "State-level equipment tax exemptions, rebate programs, stormwater fee offset calculations.",
  },
  {
    number: "04",
    title: "ESG Alignment",
    detail: "SBTi water target compliance, GRI water reporting relevance, corporate sustainability mandate fit.",
  },
  {
    number: "05",
    title: "Climate Drought Risk",
    detail: "WRI Aqueduct water stress score + SBTN basin criticality — urgency multiplier on ROI.",
  },
];

// ── Page ──────────────────────────────────────────────────────────────────────

export default function PresentationPage() {
  return (
    <div
      className="bg-white text-[#1a1a1a] min-h-screen overflow-x-hidden"
      style={{ fontFamily: "var(--font-dm-sans), 'DM Sans', system-ui, sans-serif" }}
    >
      {/* ── Navbar ─────────────────────────────────────────────────────────── */}
      <motion.header
        initial={{ opacity: 0, y: -16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, ease: "easeOut" }}
        className="fixed top-0 left-0 right-0 z-50 flex items-center justify-between px-8 py-4 bg-white/90 backdrop-blur-sm border-b border-[#f0f0f0]"
      >
        <Link href="/" className="flex items-center gap-3">
          <ToneLogo size={36} />
          <span className="text-[26px] font-bold text-[#1a1a1a] tracking-tight">Tone</span>
        </Link>

        <Link
          href="/"
          className="group hidden md:inline-flex items-center justify-center gap-2 rounded-full bg-[#0F5F78] px-6 py-2.5 text-[16px] font-semibold text-white transition-colors duration-500 ease-out hover:bg-[#9FC7D6]"
        >
          <span>View Landing Page</span>
          <span className="transition-transform duration-500 ease-out group-hover:-translate-y-1 group-hover:translate-x-0.5">↗</span>
        </Link>
      </motion.header>

      {/* ── Hero / Cover ───────────────────────────────────────────────────── */}
      <section className="relative min-h-screen flex flex-col items-center justify-center pt-24 pb-16 overflow-hidden px-6">
        {/* Subtitle tag */}
        <motion.div
          initial={{ opacity: 0, y: -12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, ease: "easeOut", delay: 0.1 }}
          className="mb-8 inline-flex items-center gap-2 rounded-full border border-[#0F5F78]/25 bg-[#0F5F78]/6 px-6 py-2.5"
        >
          <span className="text-[18px] font-bold uppercase tracking-[0.15em] text-[#0F5F78]">
            💧 Water Intelligence & Reuse Engine
          </span>
        </motion.div>

        {/* Big project name */}
        <motion.div
          initial="hidden"
          animate="visible"
          variants={staggerContainer}
          className="relative z-10 text-center mx-auto max-w-[900px] mb-10"
        >
          <motion.div variants={fadeUpVariant} className="overflow-visible pb-2">
            <span
              className="block text-[96px] sm:text-[128px] md:text-[160px] lg:text-[192px] leading-[0.92] tracking-[-5px] text-[#1a1a1a]"
              style={{ fontFamily: "var(--font-crimson), 'Crimson Text', Georgia, serif" }}
            >
              Tone
            </span>
          </motion.div>
        </motion.div>

        {/* Info panel box */}
        <motion.div
          initial={{ opacity: 0, y: 28 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.75, ease: EASE, delay: 0.45 }}
          className="relative z-10 w-full max-w-3xl rounded-3xl border border-[#d4e8ef] bg-white/80 backdrop-blur-sm px-10 py-8 shadow-[0_8px_40px_rgba(15,95,120,0.10)]"
        >
          <p
            className="text-[26px] md:text-[30px] font-semibold text-[#0F5F78] mb-7 leading-snug tracking-[-0.3px]"
            style={{ fontFamily: "var(--font-crimson), 'Crimson Text', Georgia, serif" }}
          >
            Automated Commercial Water-Reuse Prospecting Engine
          </p>

          <div className="flex flex-col gap-4 text-[18px] md:text-[20px] text-[#444444] leading-snug">
            <div className="flex items-start gap-3">
              <Building2 className="mt-1 shrink-0 text-[#0F5F78]" size={20} />
              <span>Targeting 11,500+ commercial assets across 37 continental US states</span>
            </div>

            <div className="flex items-start gap-3">
              <TrendingUp className="mt-1 shrink-0 text-[#0F5F78]" size={20} />
              <span>Precision ROI, 10-year NPV modeling, and automated Gemini AI investment briefs</span>
            </div>

            <div className="flex items-start gap-3">
              <Droplet className="mt-1 shrink-0 text-[#0F5F78]" size={20} />
              <span>
                Project Lead:&nbsp;
                <span className="font-semibold text-[#1a1a1a]">Wesley Kuria</span>
                &nbsp;&middot;&nbsp;Tone Engineering Team
              </span>
            </div>
          </div>
        </motion.div>

        {/* Teal slab */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 1.0, delay: 0.7 }}
          className="absolute bottom-0 left-1/2 h-[22%] w-[96%] max-w-[1440px] -translate-x-1/2 rounded-t-[48px] bg-[#9FC7D6]/30"
        />

        {/* Scroll hint */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.8, delay: 1.2 }}
          className="absolute bottom-8 flex flex-col items-center gap-2 text-[#929292] z-10"
        >
          <span className="text-[16px] uppercase tracking-[0.18em]">Scroll</span>
          <motion.div animate={{ y: [0, 6, 0] }} transition={{ repeat: Infinity, duration: 1.6, ease: "easeInOut" }}>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <line x1="12" y1="5" x2="12" y2="19" />
              <polyline points="19 12 12 19 5 12" />
            </svg>
          </motion.div>
        </motion.div>
      </section>

      {/* ── Data Funnel ────────────────────────────────────────────────────── */}
      <section className="px-8 md:px-16 lg:px-24 py-24 md:py-32">
        <ScrollFade>
          <p className="text-[20px] uppercase tracking-[0.16em] text-[#929292] mb-8 font-semibold">
            The Data Pipeline
          </p>
        </ScrollFade>

        <ScrollFade delay={0.08}>
          <h2
            className="text-[52px] md:text-[68px] lg:text-[84px] leading-[1.0] tracking-[-2px] text-[#1a1a1a] mb-6 max-w-4xl"
            style={{ fontFamily: "var(--font-crimson), 'Crimson Text', Georgia, serif" }}
          >
            From 129M footprints to high-confidence targets.
          </h2>
        </ScrollFade>

        <ScrollFade delay={0.14}>
          <p className="text-[#6f6f6f] text-[20px] md:text-[22px] leading-relaxed max-w-3xl mb-20">
            A multi-stage geospatial pipeline eliminates false positives, matches cooling tower
            signatures, integrates climatology normals, and outputs actionable candidate profiles.
          </p>
        </ScrollFade>

        <ScrollStagger className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {funnelSteps.map((step, i) => (
            <motion.div
              key={i}
              variants={fadeUpVariant}
              className="rounded-3xl border border-[#e8e8e8] bg-[#fafafa] p-8 flex flex-col justify-between"
            >
              <div>
                <div
                  className="text-[52px] md:text-[60px] font-semibold text-[#1a1a1a] leading-none mb-3"
                  style={{ fontFamily: "var(--font-crimson), 'Crimson Text', Georgia, serif" }}
                >
                  {step.value}
                </div>
                <div className="text-[17px] font-semibold text-[#0F5F78] mb-2">{step.label}</div>
              </div>
              <p className="text-[14px] text-[#888888] leading-relaxed mt-4">{step.sub}</p>
            </motion.div>
          ))}
        </ScrollStagger>
      </section>

      {/* ── Scoring Architecture ────────────────────────────────────────────── */}
      <section className="px-8 md:px-16 lg:px-24 py-24 md:py-32 bg-[#f7fbfd]">
        <ScrollFade>
          <p className="text-[20px] uppercase tracking-[0.16em] text-[#929292] mb-8 font-semibold">
            Intelligence Model
          </p>
        </ScrollFade>

        <ScrollFade delay={0.08}>
          <h2
            className="text-[52px] md:text-[68px] lg:text-[84px] leading-[1.0] tracking-[-2px] text-[#1a1a1a] mb-16 max-w-4xl"
            style={{ fontFamily: "var(--font-crimson), 'Crimson Text', Georgia, serif" }}
          >
            Five scoring dimensions.
          </h2>
        </ScrollFade>

        <ScrollStagger className="grid gap-6 md:grid-cols-3 lg:grid-cols-5">
          {scoringDimensions.map((dim) => (
            <motion.div
              key={dim.number}
              variants={fadeUpVariant}
              className="rounded-3xl border border-[#d4e8ef] bg-white p-7 shadow-[0_4px_20px_rgba(15,95,120,0.06)]"
            >
              <span
                className="text-[42px] text-[#9FC7D6] font-light block mb-4"
                style={{ fontFamily: "var(--font-crimson), 'Crimson Text', Georgia, serif" }}
              >
                {dim.number}
              </span>
              <h3
                className="text-[22px] font-semibold text-[#1a1a1a] mb-3 leading-snug"
                style={{ fontFamily: "var(--font-crimson), 'Crimson Text', Georgia, serif" }}
              >
                {dim.title}
              </h3>
              <p className="text-[14px] text-[#6f6f6f] leading-relaxed">{dim.detail}</p>
            </motion.div>
          ))}
        </ScrollStagger>
      </section>

      {/* ── Innovation Highlights ───────────────────────────────────────────── */}
      <section className="px-8 py-24 md:px-16 md:py-32 lg:px-24">
        <ScrollFade>
          <p className="text-[20px] uppercase tracking-[0.16em] text-[#929292] mb-8 font-semibold">
            Key Advantages
          </p>
        </ScrollFade>

        <ScrollFade delay={0.1}>
          <h2
            className="mb-16 text-[52px] md:text-[68px] lg:text-[84px] leading-[1.0] tracking-[-2px] text-[#1a1a1a]"
            style={{ fontFamily: "var(--font-crimson), 'Crimson Text', Georgia, serif" }}
          >
            Engineered for Precision & Impact.
          </h2>
        </ScrollFade>

        <ScrollFade delay={0.15}>
          <div className="grid md:grid-cols-2 gap-8">
            {/* Feature 1 */}
            <div className="relative overflow-hidden rounded-3xl border border-[#d4e8ef] bg-gradient-to-br from-[#f0f9fc] via-[#e8f4f8] to-[#dceef5] px-10 py-12 shadow-[0_8px_48px_rgba(15,95,120,0.12)] flex flex-col justify-center">
              <div className="mb-6 flex h-16 w-16 items-center justify-center rounded-2xl bg-[#0F5F78] text-white">
                <Sparkles size={32} />
              </div>
              <h3
                className="text-[42px] leading-tight tracking-[-1px] text-[#0F5F78] mb-4"
                style={{ fontFamily: "var(--font-crimson), 'Crimson Text', Georgia, serif" }}
              >
                AI-Driven Investment Briefs
              </h3>
              <p className="text-[17px] text-[#4f7990] leading-relaxed mb-6">
                Automated generation of 7-section structured pitch briefs with localized utility rate schedules,
                engineering assumptions, and direct PDF generation.
              </p>
              <div className="flex items-center gap-2 text-teal-800 font-semibold text-sm">
                <CheckCircle2 size={18} className="text-teal-600" />
                <span>Instant ROI & NPV Financial Synthesis</span>
              </div>
            </div>

            {/* Feature 2 */}
            <div className="relative overflow-hidden rounded-3xl border border-[#e2e8f0] bg-slate-900 px-10 py-12 shadow-[0_8px_48px_rgba(15,23,42,0.15)] text-white flex flex-col justify-center">
              <div className="mb-6 flex h-16 w-16 items-center justify-center rounded-2xl bg-teal-500/20 text-teal-300 border border-teal-500/30">
                <TrendingUp size={32} />
              </div>
              <h3
                className="text-[42px] leading-tight tracking-[-1px] text-white mb-4"
                style={{ fontFamily: "var(--font-crimson), 'Crimson Text', Georgia, serif" }}
              >
                37-State Spatial Engine
              </h3>
              <p className="text-[17px] text-slate-300 leading-relaxed mb-6">
                Ingests 129M building geometries, EPA facility records, and NOAA 30-year precipitation normals
                to identify the most viable rooftop water-harvesting targets.
              </p>
              <div className="flex items-center gap-2 text-teal-300 font-semibold text-sm">
                <CheckCircle2 size={18} className="text-teal-400" />
                <span>Sub-millisecond Cached In-Memory Reads</span>
              </div>
            </div>
          </div>
        </ScrollFade>

        {/* CTA */}
        <ScrollFade delay={0.2} className="mt-16 text-center">
          <Link
            href="/map"
            className="group inline-flex items-center justify-center gap-2 rounded-full bg-[#0F5F78] px-12 py-5 text-[20px] font-semibold text-white transition-colors duration-500 ease-out hover:bg-[#9FC7D6]"
          >
            <span>Explore Tone Map & Dashboard</span>
            <span className="transition-transform duration-500 ease-out group-hover:-translate-y-1 group-hover:translate-x-0.5">↗</span>
          </Link>
        </ScrollFade>
      </section>

      {/* ── Footer ─────────────────────────────────────────────────────────── */}
      <footer className="px-8 md:px-16 lg:px-24 py-8 border-t border-[#e5e5e5]">
        <div className="flex items-center justify-between flex-wrap gap-4">
          <div className="flex items-center gap-3">
            <ToneLogo size={20} />
            <span className="text-[13px] text-[#929292]">© Tone. 2026</span>
          </div>
          <span className="text-[13px] text-[#929292]">Lead Architect: Wesley Kuria · All Rights Reserved</span>
        </div>
      </footer>
    </div>
  );
}
