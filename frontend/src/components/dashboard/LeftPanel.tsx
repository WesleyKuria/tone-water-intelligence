"use client";
import React from "react";
import { ChevronLeft, Globe, Droplets, Factory, Building, ShieldCheck } from "lucide-react";
import { SelectionState } from "./ProspectingDashboard";
import FilterPanel from "../filters/FilterPanel";

type LeftPanelProps = {
  selection: SelectionState;
  setSelection: React.Dispatch<React.SetStateAction<SelectionState>>;
};

const VIEW_LABELS: Record<SelectionState["mapMode"], string> = {
  national: "Pan-African View",
  state:    "Regional Hub View",
  metro:    "Metropolitan View",
  building: "Asset Detail View",
};

const COUNTRIES = [
  { code: "ALL", label: "All Africa", flag: "🌍" },
  { code: "KE",  label: "Kenya",      flag: "🇰🇪" },
  { code: "ZA",  label: "South Africa", flag: "🇿🇦" },
  { code: "NG",  label: "Nigeria",    flag: "🇳🇬" },
  { code: "RW",  label: "Rwanda",     flag: "🇷🇼" },
];

const USE_CASES = [
  { key: "ALL", label: "All Use Cases", icon: Globe },
  { key: "industrial_tanker_offset", label: "Tanker & Rationing Offset", icon: Factory },
  { key: "cooling_tower_makeup", label: "Cooling Tower Make-Up", icon: Droplets },
  { key: "horticulture_agro", label: "Agri-Processing & Cold Chain", icon: ShieldCheck },
  { key: "logistics_warehousing", label: "Logistics & Warehouses", icon: Building },
  { key: "green_sez", label: "Eco-Industrial SEZs", icon: ShieldCheck },
];

export default function LeftPanel({ selection, setSelection }: LeftPanelProps) {
  const goNational = () => setSelection(prev => ({ ...prev, mapMode: "national", selectedState: null, selectedMetro: null, selectedBuildingId: null }));
  const goState    = () => setSelection(prev => ({ ...prev, mapMode: "state",    selectedMetro: null, selectedBuildingId: null }));
  const goMetro    = () => setSelection(prev => ({ ...prev, mapMode: "metro",    selectedBuildingId: null }));

  const parentAction =
    selection.mapMode === "building" ? goMetro :
    selection.mapMode === "metro"    ? goState  :
    selection.mapMode === "state"    ? goNational : null;

  return (
    <div className="flex flex-col h-full overflow-y-auto scrollbar-dark"
      style={{ background: "rgba(255,255,255,0.04)", backdropFilter: "blur(24px)" }}>

      {/* Logo */}
      <div className="px-5 py-4 border-b border-white/[0.08]">
        <div className="flex items-center gap-2.5">
          <img src="/assets/Hand Holding Water Droplet.png" alt="Tone" className="w-12 h-12 object-contain shrink-0" />
          <div className="min-w-0">
            <h1 className="text-base font-black tracking-tight bg-gradient-to-r from-blue-300 via-cyan-300 to-teal-300 bg-clip-text text-transparent leading-tight">Tone 💧</h1>
            <p className="text-[11px] text-slate-400 font-medium leading-tight">Pan-African Water Intelligence</p>
          </div>
        </div>
      </div>

      {/* Country / Hub Selector */}
      <div className="px-4 py-3.5 border-b border-white/[0.06]">
        <p className="text-[10px] uppercase tracking-widest text-slate-500 mb-2 font-bold flex items-center justify-between">
          <span>Target Market</span>
          <span className="text-[9px] text-cyan-400 font-mono">Active Data</span>
        </p>
        <div className="grid grid-cols-2 gap-1.5">
          {COUNTRIES.map(c => {
            const isSelected = selection.selectedCountry === c.code;
            return (
              <button
                key={c.code}
                onClick={() => setSelection(prev => ({
                  ...prev,
                  selectedCountry: c.code,
                  selectedState: null,
                  selectedMetro: null,
                  selectedBuildingId: null,
                  mapMode: "national"
                }))}
                className={`flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-xs font-semibold transition-all duration-150 border text-left ${
                  isSelected
                    ? "bg-blue-600/30 text-cyan-200 border-cyan-400/40 shadow-sm shadow-cyan-500/10"
                    : "bg-white/[0.03] text-slate-400 hover:text-slate-200 border-white/[0.06] hover:bg-white/[0.07]"
                }`}
              >
                <span>{c.flag}</span>
                <span className="truncate">{c.label}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Use-Case Selector */}
      <div className="px-4 py-3 border-b border-white/[0.06]">
        <p className="text-[10px] uppercase tracking-widest text-slate-500 mb-2 font-bold">Use Case Priority</p>
        <div className="space-y-1">
          {USE_CASES.map(uc => {
            const isSelected = selection.selectedUseCase === uc.key;
            const Icon = uc.icon;
            return (
              <button
                key={uc.key}
                onClick={() => setSelection(prev => ({
                  ...prev,
                  selectedUseCase: uc.key,
                  selectedBuildingId: null
                }))}
                className={`w-full text-left text-xs px-2.5 py-1.5 rounded-lg transition-all duration-150 font-medium flex items-center gap-2 border ${
                  isSelected
                    ? "bg-cyan-500/20 text-cyan-200 border-cyan-400/40 shadow-sm shadow-cyan-500/10"
                    : "text-slate-400 hover:text-slate-200 border-transparent hover:bg-white/[0.05]"
                }`}
              >
                <Icon size={13} className={isSelected ? "text-cyan-300 shrink-0" : "text-slate-500 shrink-0"} />
                <span className="truncate">{uc.label}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Scope navigation */}
      <div className="px-4 py-3 border-b border-white/[0.06]">
        <p className="text-[10px] uppercase tracking-widest text-slate-500 mb-2 font-semibold">Scope</p>
        <div className="space-y-1">
          <button
            onClick={goNational}
            className={`w-full text-left text-xs px-2.5 py-1.5 rounded-lg transition-all duration-150 font-medium border ${
              selection.mapMode === "national"
                ? "bg-blue-500/20 text-blue-300 border-blue-500/30"
                : "text-slate-400 hover:text-slate-200 border-transparent hover:bg-white/[0.05]"
            }`}
          >
            {VIEW_LABELS.national}
          </button>

          {selection.selectedState && (
            <button
              onClick={goState}
              className={`w-full text-left text-xs px-2.5 py-1.5 rounded-lg transition-all duration-150 font-medium flex items-center gap-1.5 border ${
                selection.mapMode === "state"
                  ? "bg-blue-500/20 text-blue-300 border-blue-500/30"
                  : "text-slate-400 hover:text-slate-200 border-transparent hover:bg-white/[0.05]"
              }`}
            >
              <ChevronLeft size={11} className="text-slate-500 shrink-0" />
              <span className="truncate">Hub: {selection.selectedState}</span>
            </button>
          )}

          {selection.selectedMetro && (
            <button
              onClick={goMetro}
              className={`w-full text-left text-xs px-2.5 py-1.5 rounded-lg transition-all duration-150 font-medium flex items-center gap-1.5 border ${
                selection.mapMode === "metro"
                  ? "bg-blue-500/20 text-blue-300 border-blue-500/30"
                : "text-slate-400 hover:text-slate-200 border-transparent hover:bg-white/[0.05]"
              }`}
            >
              <ChevronLeft size={11} className="text-slate-500 shrink-0" />
              <span className="truncate">Metro: {selection.selectedMetro}</span>
            </button>
          )}
        </div>
      </div>

      {/* Filters */}
      <div className="px-4 py-3 flex-1 overflow-y-auto scrollbar-dark">
        <p className="text-[10px] uppercase tracking-widest text-slate-500 mb-2.5 font-semibold">Asset Criteria</p>
        <FilterPanel selection={selection} setSelection={setSelection} />
      </div>
    </div>
  );
}

