import React from "react";
import { SelectionState } from "./ProspectingDashboard";
import StateSummaryPanel from "../panels/StateSummaryPanel";
import MetroSummaryPanel from "../panels/MetroSummaryPanel";
import BuildingListPanel from "../panels/BuildingListPanel";
import BuildingProfilePanel from "../panels/BuildingProfilePanel";
import { BuildingCandidate } from "@/types/building";
import { StateScore } from "@/types/state";
import { RoiResult } from "@/types/roi";
import { BriefResult } from "@/types/brief";
import RoiPreviewPanel from "../panels/RoiPreviewPanel";
import BriefPreviewPanel from "../panels/BriefPreviewPanel";

type RightPanelProps = {
  selection: SelectionState;
  setSelection: React.Dispatch<React.SetStateAction<SelectionState>>;
  buildings: BuildingCandidate[];
  filteredBuildings: BuildingCandidate[];
  stateScores: StateScore[];
  roiResult: RoiResult | null;
  isCalculatingRoi: boolean;
  roiError: string | null;
  onCalculateRoi: (building: BuildingCandidate) => void;
  briefResult: BriefResult | null;
  isGeneratingBrief: boolean;
  briefError: string | null;
  onGenerateBrief: (building: BuildingCandidate) => void;
};

export default function RightPanel(props: RightPanelProps) {
  const { selection, setSelection } = props;

  const panelStyle = { background: "rgba(255,255,255,0.04)", backdropFilter: "blur(24px)" };

  if (selection.mapMode === "national") {
    const sorted = [...props.filteredBuildings].sort((a, b) => b.viability_score - a.viability_score);
    return (
      <div className="flex flex-col h-full overflow-y-auto scrollbar-dark p-5 space-y-4" style={panelStyle}>
        <div className="pb-3 border-b border-white/[0.08]">
          <div className="flex items-center justify-between">
            <h2 className="text-sm font-bold text-slate-200">Commercial Target Assets</h2>
            <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-blue-500/20 text-blue-300 border border-blue-500/30">
              {sorted.length} Assets
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Ranked by AI viability score & water harvesting potential.
          </p>
        </div>

        <div className="space-y-2">
          {sorted.map((b) => (
            <button
              key={b.building_id}
              onClick={() => setSelection(prev => ({ ...prev, mapMode: "building", selectedBuildingId: b.building_id, selectedMetro: b.metro, selectedState: b.state }))}
              className="w-full text-left p-3.5 rounded-xl border border-white/[0.08] hover:border-blue-400/40 transition-all duration-200 hover:shadow-lg group"
              style={{ background: "rgba(255,255,255,0.04)" }}
            >
              <div className="flex items-start justify-between gap-2 mb-1.5">
                <span className="text-sm font-bold text-slate-100 group-hover:text-blue-300 transition-colors truncate">
                  {b.address.split(",")[0]}
                </span>
                <span className="text-sm font-black text-emerald-400 shrink-0 px-2 py-0.5 rounded bg-emerald-500/10 border border-emerald-500/20">
                  {b.viability_score}
                </span>
              </div>
              <p className="text-xs text-slate-400 mb-2 truncate">
                {b.metro} · {b.building_type.replace(/_/g, " ")}
              </p>
              <div className="flex items-center justify-between text-[11px] text-slate-400">
                <span>Roof: {b.roof_area_sqm?.toLocaleString() ?? Math.round((b.roof_area_sqft ?? 0) * 0.0929).toLocaleString()} m²</span>
                <span className="text-blue-300 font-medium">View Analysis →</span>
              </div>
            </button>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full overflow-y-auto scrollbar-dark" style={panelStyle}>
      {selection.mapMode === "state" && (
        <div className="p-5 space-y-4">
          <StateSummaryPanel selection={selection} stateScores={props.stateScores} />
          <MetroSummaryPanel selection={selection} setSelection={setSelection} stateScores={props.stateScores} />
        </div>
      )}

      {selection.mapMode === "metro" && (
        <div className="p-5 h-full flex flex-col">
          <BuildingListPanel
            selection={selection}
            setSelection={setSelection}
            filteredBuildings={props.filteredBuildings}
          />
        </div>
      )}

      {selection.mapMode === "building" && (
        <div className="flex flex-col h-full">
          <BuildingProfilePanel
            selection={selection}
            filteredBuildings={props.filteredBuildings}
            isCalculatingRoi={props.isCalculatingRoi}
            onCalculateRoi={props.onCalculateRoi}
            isGeneratingBrief={props.isGeneratingBrief}
            onGenerateBrief={props.onGenerateBrief}
          />
          {(props.roiResult || props.isCalculatingRoi || props.roiError) && (
            <div className="px-4 pb-4">
              <RoiPreviewPanel
                roiResult={props.roiResult}
                loading={props.isCalculatingRoi}
                error={props.roiError}
              />
            </div>
          )}
          {(props.briefResult || props.isGeneratingBrief || props.briefError) && (
            <div className="px-4 pb-4">
              <BriefPreviewPanel
                briefResult={props.briefResult}
                loading={props.isGeneratingBrief}
                error={props.briefError}
              />
            </div>
          )}
        </div>
      )}
    </div>
  );
}
