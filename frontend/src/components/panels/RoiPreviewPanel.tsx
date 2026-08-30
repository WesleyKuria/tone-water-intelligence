import React from 'react';
import { RoiResult } from '@/types/roi';

type Props = {
  roiResult: RoiResult | null;
  loading: boolean;
  error: string | null;
};

export default function RoiPreviewPanel({ roiResult, loading, error }: Props) {
  if (error) {
    return (
      <div className="p-4 rounded-xl border border-red-500/30 text-red-400 text-xs"
        style={{ background: "rgba(239,68,68,0.08)" }}>
        {error}
      </div>
    );
  }

  if (loading) {
    return (
      <div className="p-4 rounded-xl border border-blue-500/30 text-center flex flex-col items-center gap-2"
        style={{ background: "rgba(59,130,246,0.08)" }}>
        <div className="animate-spin w-4 h-4 border-2 border-blue-400 border-t-transparent rounded-full" />
        <span className="font-semibold text-blue-300 text-xs">Calculating comprehensive ROI & Savings...</span>
      </div>
    );
  }

  if (!roiResult) return null;

  const sym = roiResult.currency_symbol || "$";
  const waterSav = roiResult.annual_water_savings_usd ?? 0;
  const sewerSav = roiResult.annual_sewer_savings_usd ?? 0;
  const totLocal = roiResult.total_annual_savings_local;
  const npv = roiResult.npv_10yr_local ?? roiResult.npv_10yr_usd ?? 0;

  return (
    <div className="rounded-xl border border-white/[0.08] overflow-hidden"
      style={{ background: "rgba(255,255,255,0.05)" }}>
      <div className="p-3 border-b border-white/[0.06] font-semibold text-slate-300 text-xs flex items-center justify-between">
        <span>ROI & Financial Analysis</span>
        {roiResult.water_autonomy_days && (
          <span className="text-[10px] text-cyan-300 font-mono">⚡ {roiResult.water_autonomy_days}d Autonomy</span>
        )}
      </div>
      <div className="p-3 grid grid-cols-2 gap-y-3 gap-x-4">
        <div>
          <div className="text-[10px] uppercase font-bold text-slate-500 mb-0.5 tracking-widest">
            {totLocal ? "Total Savings" : "Water Savings"}
          </div>
          <div className="font-semibold text-emerald-400 text-sm">
            {totLocal ? `${sym} ${totLocal.toLocaleString()}` : `$${waterSav.toLocaleString()}`} <span className="text-[11px] text-slate-500 font-normal">/ yr</span>
          </div>
        </div>
        <div>
          <div className="text-[10px] uppercase font-bold text-slate-500 mb-0.5 tracking-widest">Sewer / Tanker</div>
          <div className="font-semibold text-teal-400 text-sm">
            ${sewerSav.toLocaleString()} <span className="text-[11px] text-slate-500 font-normal">/ yr</span>
          </div>
        </div>
        <div>
          <div className="text-[10px] uppercase font-bold text-slate-500 mb-0.5 tracking-widest">Payback Period</div>
          <div className="font-semibold text-slate-200 text-sm">{roiResult.payback_yrs} <span className="text-[11px] text-slate-500 font-normal">yrs</span></div>
        </div>
        <div>
          <div className="text-[10px] uppercase font-bold text-slate-500 mb-0.5 tracking-widest">10-Yr NPV</div>
          <div className="font-semibold text-slate-200 text-sm">{sym} {npv.toLocaleString()}</div>
        </div>
      </div>
      <div className="px-3 pb-3">
        <div className="rounded-xl p-2 flex justify-between items-center text-xs border border-white/[0.06]"
          style={{ background: "rgba(255,255,255,0.04)" }}>
          <span className="font-semibold text-slate-400">Base ROI</span>
          <span className="font-bold text-slate-200">{roiResult.base_roi_percent}%</span>
        </div>
      </div>
    </div>
  );
}

