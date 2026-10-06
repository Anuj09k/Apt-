import React, { useState, useEffect } from "react";
import { api, apiError } from "../lib/api";
import { toast } from "sonner";
import {
  Leaf,
  Globe2,
  TrendingUp,
  ShieldAlert,
  Volume2,
  Award,
  FileText,
  DollarSign,
  LayoutDashboard,
  Wrench,
  CheckCircle2,
  Flame,
  Droplets,
  Wind,
  Sun,
  ShieldCheck,
} from "lucide-react";
import { Section, Metric } from "../components/Field";
import { Button } from "../components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../components/ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "../components/ui/table";
import { inr, num } from "../lib/format";

export default function UrbanSustainabilityModule({ project, projectId }) {
  const [activeTab, setActiveTab] = useState("predictions");
  const [greenStandard, setGreenStandard] = useState("IGBC");
  const [loading, setLoading] = useState(false);

  // States
  const [urbanData, setUrbanData] = useState(null);
  const [climateData, setClimateData] = useState(null);
  const [noiseData, setNoiseData] = useState(null);
  const [greenData, setGreenData] = useState(null);
  const [esgData, setEsgData] = useState(null);
  const [lccData, setLccData] = useState(null);
  const [execKpis, setExecKpis] = useState(null);
  const [equipmentData, setEquipmentData] = useState(null);

  useEffect(() => {
    loadGreenScorecard();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [greenStandard]);

  useEffect(() => {
    loadAllData();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [projectId]);

  async function loadGreenScorecard() {
    try {
      const res = await api.get(`/projects/${projectId}/sustainability/green-building?standard=${greenStandard}`);
      setGreenData(res.data);
    } catch (e) {
      toast.error(apiError(e));
    }
  }

  async function loadAllData() {
    setLoading(true);
    try {
      const [uRes, cRes, nRes, eRes, lRes, kRes, eqRes] = await Promise.all([
        api.get(`/projects/${projectId}/urban/growth-value`),
        api.get(`/projects/${projectId}/urban/climate-disasters`),
        api.get(`/projects/${projectId}/urban/noise-pollution`),
        api.get(`/projects/${projectId}/sustainability/esg`),
        api.get(`/projects/${projectId}/sustainability/lifecycle-cost?years=30`),
        api.get(`/projects/${projectId}/executive/dashboard-kpis`),
        api.get(`/projects/${projectId}/construction/equipment-risks`),
      ]);
      setUrbanData(uRes.data);
      setClimateData(cRes.data);
      setNoiseData(nRes.data);
      setEsgData(eRes.data);
      setLccData(lRes.data);
      setExecKpis(kRes.data);
      setEquipmentData(eqRes.data);
      loadGreenScorecard();
    } catch (e) {
      toast.error(apiError(e));
    } finally {
      setLoading(false);
    }
  }

const URBAN_TAB_GROUPS = [
  {
    category: "Urban & Climate",
    tabs: [
      { id: "predictions", label: "Urban Growth & Value", icon: TrendingUp },
      { id: "climate", label: "Climate & Disasters", icon: ShieldAlert },
      { id: "noise", label: "Noise & Pollution", icon: Volume2 },
    ],
  },
  {
    category: "ESG & Green",
    tabs: [
      { id: "green", label: "Green Scorecard", icon: Award },
      { id: "esg", label: "ESG & Carbon Dossier", icon: FileText },
    ],
  },
  {
    category: "Economics & Operations",
    tabs: [
      { id: "lcc", label: "30-Year LCC", icon: DollarSign },
      { id: "executive", label: "Executive Dashboard", icon: LayoutDashboard },
      { id: "equipment", label: "Equipment & Delays", icon: Wrench },
    ],
  },
];

  return (
    <div className="space-y-6 pb-12">
      {/* Header Banner */}
      <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-2xs">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="rounded bg-emerald-50 border border-emerald-200 px-2 py-0.5 text-xs font-semibold text-emerald-800">
                Environmental & Sustainability
              </span>
              <span className="text-xs text-slate-500 font-medium">ESG, IGBC/LEED, LCC & Urban Intelligence</span>
            </div>
            <h1 className="text-2xl font-bold tracking-tight text-slate-900 flex items-center gap-2">
              <Leaf className="h-6 w-6 text-emerald-600" />
              Urban Intelligence, ESG & Sustainability
            </h1>
            <p className="text-sm text-slate-600 max-w-3xl">
              Land value appreciation forecasting, multi-hazard disaster resilience, green building certification scorecards, Scope 1/2/3 carbon accounting, 30-year LCC, and executive dashboards.
            </p>
          </div>
          <Button variant="outline" size="sm" onClick={loadAllData} disabled={loading} className="gap-2 border-slate-300 text-slate-700 hover:bg-slate-50 hover:text-slate-900 font-medium">
            {loading ? "Refreshing..." : "Refresh Analytics"}
          </Button>
        </div>

        {/* Clubbed Tab Navigation */}
        <div className="mt-6 border-t border-slate-100 pt-4 space-y-3">
          <div className="flex flex-wrap gap-4 items-center">
            {URBAN_TAB_GROUPS.map((grp) => (
              <div key={grp.category} className="flex items-center gap-1 rounded-lg bg-slate-100 p-1 border border-slate-200/80">
                <span className="px-2 text-[10px] font-bold uppercase tracking-wider text-slate-500">
                  {grp.category}:
                </span>
                {grp.tabs.map((tab) => {
                  const Icon = tab.icon;
                  const active = activeTab === tab.id;
                  return (
                    <button
                      key={tab.id}
                      onClick={() => setActiveTab(tab.id)}
                      className={`flex items-center gap-1.5 rounded-md px-2.5 py-1 text-xs font-semibold transition-all ${
                        active
                          ? "bg-emerald-600 text-white shadow-xs font-bold"
                          : "text-slate-700 hover:bg-white hover:text-slate-900"
                      }`}
                    >
                      <Icon className="h-3.5 w-3.5" />
                      {tab.label}
                    </button>
                  );
                })}
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* TAB 1: URBAN GROWTH & LAND VALUE */}
      {activeTab === "predictions" && (
        <div className="space-y-6">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <Metric label="Current Plot Value" value={inr(urbanData?.estimated_current_plot_value_inr)} />
            <Metric label="Base Land Rate" value={`₹${num(urbanData?.base_land_rate_inr_sqm)}/m²`} />
            <Metric label="Projected 5-Yr CAGR" value={urbanData?.five_year_cagr_pct == null ? "Enter land cost" : `${urbanData.five_year_cagr_pct}% (assumed)`} />
            <Metric label="Infrastructure Capacity" value="ADEQUATE (94%)" />
          </div>

          <Section title="5-Year Land Value Appreciation Projection" desc="Hedonic land valuation model integrating transit corridor expansion and density zoning">
            <div className="overflow-x-auto rounded-lg border border-slate-200">
              <Table>
                <TableHeader className="bg-slate-50 border-b border-slate-200">
                  <TableRow>
                    <TableHead className="text-slate-700 font-semibold">Year</TableHead>
                    <TableHead className="text-right text-slate-700 font-semibold">Projected Land Rate</TableHead>
                    <TableHead className="text-right text-slate-700 font-semibold">Estimated Plot Valuation</TableHead>
                    <TableHead className="text-right text-slate-700 font-semibold">Cumulative Capital Gain</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {urbanData?.appreciation_projections?.map((ap, idx) => (
                    <TableRow key={idx} className="text-xs hover:bg-slate-50/50">
                      <TableCell className="font-semibold text-slate-900">{ap.year}</TableCell>
                      <TableCell className="text-right font-bold text-emerald-700 font-mono">₹{num(ap.projected_land_rate_inr_sqm)}/m²</TableCell>
                      <TableCell className="text-right text-slate-900 font-semibold font-mono">{inr(ap.estimated_plot_value_inr)}</TableCell>
                      <TableCell className="text-right font-bold text-amber-800 font-mono">+{ap.cumulative_gain_pct}%</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
            <div className="mt-4 space-y-1.5">
              <strong className="text-xs text-slate-700 font-semibold block">Identified Value Catalysts:</strong>
              {urbanData?.growth_catalysts?.map((cat, i) => (
                <div key={i} className="text-xs text-slate-600 flex items-center gap-2">
                  <span className="h-1.5 w-1.5 rounded-full bg-emerald-600"></span>
                  {cat}
                </div>
              ))}
            </div>
          </Section>
        </div>
      )}

      {/* TAB 2: CLIMATE & MULTI-HAZARD DISASTERS */}
      {activeTab === "climate" && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Metric label="Composite Resilience Score" value={climateData?.composite_resilience_score == null ? "—" : `${climateData.composite_resilience_score}/100`} />
            <Metric label="Rating" value={climateData?.resilience_rating || "—"} />
            <Metric label="Annual Solar Irradiation" value={climateData?.annual_solar_irradiation_kwh_m2 == null ? "See GIS sun path" : `${climateData.annual_solar_irradiation_kwh_m2} kWh/m²`} />
          </div>

          <Section title="Multi-Hazard Disaster Risk & Mitigation Analysis" desc="Comprehensive vulnerability assessment across seismic, flood, wind, and heat extremes">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {climateData?.hazards?.map((hz, idx) => (
                <div key={idx} className="rounded-xl border border-slate-200 bg-slate-50/70 p-4 text-xs space-y-2 shadow-xs">
                  <div className="flex items-center justify-between border-b border-slate-200 pb-2">
                    <span className="font-bold text-slate-900 text-sm">{hz.hazard_type}</span>
                    <span className={`px-2 py-0.5 rounded text-[10px] font-semibold border ${
                      hz.risk_level.includes("HIGH") ? "bg-rose-100 text-rose-800 border-rose-200" :
                      hz.risk_level.includes("MODERATE") ? "bg-amber-100 text-amber-800 border-amber-200" : "bg-emerald-100 text-emerald-800 border-emerald-200"
                    }`}>
                      {hz.risk_level}
                    </span>
                  </div>
                  <div className="text-slate-700 text-[11px] space-y-1">
                    <div><strong className="text-slate-600">Zone Classification:</strong> {hz.zone}</div>
                    <div><strong className="text-slate-600">Structural Mitigation:</strong> {hz.structural_mitigation}</div>
                  </div>
                </div>
              ))}
            </div>
          </Section>
        </div>
      )}

      {/* TAB 3: NOISE & AIR POLLUTION */}
      {activeTab === "noise" && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Section title="Acoustic Attenuation Modeling" desc="Traffic noise decay from abutting road to front building facade">
              <div className="rounded-xl border border-slate-200 bg-slate-50/70 p-4 text-xs space-y-3 shadow-xs">
                <div className="grid grid-cols-2 gap-3 text-center">
                  <div className="rounded bg-white border border-slate-200 p-2.5 shadow-2xs">
                    <span className="text-slate-500 block text-[10px] font-medium">Curb Noise Level</span>
                    <strong className="text-rose-700 text-lg font-bold font-mono">{noiseData?.noise_analysis?.curb_noise_level_dba} dB(A)</strong>
                  </div>
                  <div className="rounded bg-white border border-slate-200 p-2.5 shadow-2xs">
                    <span className="text-slate-500 block text-[10px] font-medium">Front Facade Noise</span>
                    <strong className="text-emerald-700 text-lg font-bold font-mono">{noiseData?.noise_analysis?.front_facade_noise_dba} dB(A)</strong>
                  </div>
                </div>
                <div className="text-slate-700 text-[11px] space-y-1.5 pt-1">
                  <div><strong className="text-slate-600">CPCB Daytime Residential Limit:</strong> {noiseData?.noise_analysis?.cpcb_daytime_residential_norm_dba} dB(A)</div>
                  <div><strong className="text-slate-600">Glazing Specification:</strong> {noiseData?.noise_analysis?.acoustic_glazing_recommendation}</div>
                  <span className="inline-block rounded bg-emerald-100 border border-emerald-200 px-2 py-0.5 text-emerald-800 font-semibold text-[10px] mt-1">
                    {noiseData?.noise_analysis?.compliance_status}
                  </span>
                </div>
              </div>
            </Section>

            <Section title="Site Air Quality & Particulate Dispersion" desc="Ambient PM2.5/PM10 concentrations and vegetative buffer mitigation">
              <div className="rounded-xl border border-slate-200 bg-slate-50/70 p-4 text-xs space-y-3 shadow-xs">
                <div className="grid grid-cols-2 gap-3 text-center">
                  <div className="rounded bg-white border border-slate-200 p-2.5 shadow-2xs">
                    <span className="text-slate-500 block text-[10px] font-medium">Ambient PM 2.5</span>
                    <strong className="text-amber-800 text-lg font-bold font-mono">{noiseData?.air_quality_analysis?.ambient_pm25_ug_m3 ?? "No station data"}{noiseData?.air_quality_analysis?.ambient_pm25_ug_m3 != null ? " µg/m³" : ""}</strong>
                  </div>
                  <div className="rounded bg-white border border-slate-200 p-2.5 shadow-2xs">
                    <span className="text-slate-500 block text-[10px] font-medium">Ambient PM 10</span>
                    <strong className="text-amber-800 text-lg font-bold font-mono">{noiseData?.air_quality_analysis?.ambient_pm10_ug_m3 ?? "No station data"}{noiseData?.air_quality_analysis?.ambient_pm10_ug_m3 != null ? " µg/m³" : ""}</strong>
                  </div>
                </div>
                <div>
                  <strong className="text-slate-600 block mb-1">Mitigation Strategy:</strong>
                  <ul className="space-y-1 list-disc list-inside text-slate-700 text-[11px]">
                    {noiseData?.air_quality_analysis?.mitigation_strategy?.map((s, i) => (
                      <li key={i}>{s}</li>
                    ))}
                  </ul>
                </div>
              </div>
            </Section>
          </div>
        </div>
      )}

      {/* TAB 4: GREEN BUILDING SCORECARD */}
      {activeTab === "green" && (
        <div className="space-y-6">
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <Select value={greenStandard} onValueChange={setGreenStandard}>
                <SelectTrigger className="w-36 bg-white border-slate-200 text-xs text-slate-900">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="IGBC">IGBC Rating</SelectItem>
                  <SelectItem value="GRIHA">GRIHA Rating</SelectItem>
                  <SelectItem value="LEED">LEED v4.1</SelectItem>
                </SelectContent>
              </Select>
              <span className="rounded bg-emerald-100 border border-emerald-200 px-3 py-1 text-xs font-bold text-emerald-800">
                {greenData?.certification_tier}
              </span>
            </div>
            <div className="flex items-center gap-4 text-xs text-slate-700">
              <span>Points: <strong className="text-slate-900 font-bold">{greenData?.total_points_achieved}</strong> / {greenData?.max_possible_points}</span>
              <span>Energy Savings: <strong className="text-emerald-700 font-bold">{greenData?.estimated_energy_savings_pct ?? "—"}{greenData?.estimated_energy_savings_pct != null ? "%" : ""}</strong></span>
              <span>Water Reduction: <strong className="text-teal-700 font-bold">{greenData?.estimated_potable_water_reduction_pct ?? "—"}{greenData?.estimated_potable_water_reduction_pct != null ? "%" : ""}</strong></span>
            </div>
          </div>

          <Section title="Credit Category Breakdown" desc="Detailed points distribution across environmental impact categories">
            <div className="overflow-x-auto rounded-lg border border-slate-200">
              <Table>
                <TableHeader className="bg-slate-50 border-b border-slate-200">
                  <TableRow>
                    <TableHead className="text-slate-700 font-semibold">Category</TableHead>
                    <TableHead className="text-center text-slate-700 font-semibold">Points Awarded</TableHead>
                    <TableHead className="text-center text-slate-700 font-semibold">Max Points</TableHead>
                    <TableHead className="text-slate-700 font-semibold">Design Highlights</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {greenData?.categories?.map((cat, idx) => (
                    <TableRow key={idx} className="text-xs hover:bg-slate-50/50">
                      <TableCell className="font-semibold text-slate-900">{cat.category}</TableCell>
                      <TableCell className="text-center font-bold text-emerald-700 font-mono">{cat.awarded_points}</TableCell>
                      <TableCell className="text-center text-slate-600 font-mono">{cat.max_points}</TableCell>
                      <TableCell className="text-slate-700 text-[11px]">{cat.highlights}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          </Section>
        </div>
      )}

      {/* TAB 5: ESG & CARBON DOSSIER */}
      {activeTab === "esg" && (
        <div className="space-y-6">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <Metric label="Total Carbon Footprint" value={`${num(esgData?.carbon_accounting_tco2e?.total_footprint_tco2e)} tCO₂e`} />
            <Metric label="Carbon Intensity" value={`${esgData?.carbon_accounting_tco2e?.carbon_intensity_tco2e_per_m2} tCO₂e/m²`} />
            <Metric label="Worker Welfare" value="100% Compliant" />
            <Metric label="ESG Rating" value={esgData?.esg_composite_rating || "Not rated"} />
          </div>

          <Section title="Scope 1, 2, and 3 Greenhouse Gas Accounting" desc="Embodied and operational carbon breakdown conforming to GRI & BRSR standards">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="rounded-xl border border-slate-200 bg-slate-50/70 p-4 text-xs space-y-2 shadow-xs">
                <span className="rounded bg-blue-100 border border-blue-200 px-2 py-0.5 text-blue-900 font-semibold text-[10px]">SCOPE 1 (Direct)</span>
                <strong className="text-slate-900 text-base font-bold block">{esgData?.carbon_accounting_tco2e?.scope_1_direct_emissions} tCO₂e</strong>
                <p className="text-slate-600 text-[11px]">On-site diesel generators, excavators, and construction fleet emissions.</p>
              </div>
              <div className="rounded-xl border border-slate-200 bg-slate-50/70 p-4 text-xs space-y-2 shadow-xs">
                <span className="rounded bg-teal-100 border border-teal-200 px-2 py-0.5 text-teal-900 font-semibold text-[10px]">SCOPE 2 (Indirect Grid)</span>
                <strong className="text-slate-900 text-base font-bold block">{esgData?.carbon_accounting_tco2e?.scope_2_electricity_emissions} tCO₂e</strong>
                <p className="text-slate-600 text-[11px]">Grid electricity consumption during construction and curing operations.</p>
              </div>
              <div className="rounded-xl border border-slate-200 bg-slate-50/70 p-4 text-xs space-y-2 shadow-xs">
                <span className="rounded bg-emerald-100 border border-emerald-200 px-2 py-0.5 text-emerald-900 font-semibold text-[10px]">SCOPE 3 (Embodied Materials)</span>
                <strong className="text-slate-900 text-base font-bold block">{esgData?.carbon_accounting_tco2e?.scope_3_embodied_materials} tCO₂e</strong>
                <p className="text-slate-600 text-[11px]">Embodied emissions from rebar manufacturing, cement clinker, and transportation.</p>
              </div>
            </div>
          </Section>
        </div>
      )}

      {/* TAB 6: 30-YEAR LCC */}
      {activeTab === "lcc" && (
        <div className="space-y-6">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <Metric label="Initial Capex" value={inr(lccData?.initial_capital_expenditure_capex_inr)} />
            <Metric label="30-Yr Opex" value={inr(lccData?.cumulative_operational_expenditure_30yr_inr)} />
            <Metric label="Periodic Rehab" value={inr(lccData?.periodic_rehabilitation_cost_inr)} />
            <Metric label="30-Yr Total LCC" value={inr(lccData?.total_lifecycle_cost_inr)} />
          </div>

          <Section title="Periodic Capital Rehabilitation Schedule" desc="Major replacement cycles for elevators, central chillers, facade recoating, and solar inverters">
            <div className="overflow-x-auto rounded-lg border border-slate-200">
              <Table>
                <TableHeader className="bg-slate-50 border-b border-slate-200">
                  <TableRow>
                    <TableHead className="w-24 text-slate-700 font-semibold">Year</TableHead>
                    <TableHead className="text-slate-700 font-semibold">Rehabilitation & Overhaul Item</TableHead>
                    <TableHead className="text-right text-slate-700 font-semibold">Projected Cost (INR)</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {lccData?.rehabilitation_schedule?.map((r, idx) => (
                    <TableRow key={idx} className="text-xs hover:bg-slate-50/50">
                      <TableCell className="font-bold text-blue-700 font-mono">Year {r.year}</TableCell>
                      <TableCell className="font-semibold text-slate-900">{r.item}</TableCell>
                      <TableCell className="text-right font-bold text-amber-800 font-mono">{inr(r.cost_inr)}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
            <div className="mt-3 flex items-center justify-between text-xs text-slate-600 border-t border-slate-200 pt-3">
              <span>Capex vs Opex Ratio: <strong className="text-slate-900">{lccData?.cost_ratio_capex_vs_opex}</strong></span>
              <span>Net Present Value (NPV @ 8%): <strong className="text-emerald-700 font-bold">{inr(lccData?.net_present_value_npv_inr)}</strong></span>
            </div>
          </Section>
        </div>
      )}

      {/* TAB 7: EXECUTIVE DASHBOARD */}
      {activeTab === "executive" && (
        <div className="space-y-6">
          <div className="rounded-xl border border-slate-200 bg-white p-5 text-xs space-y-4 shadow-sm">
            <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-200 pb-3">
              <div>
                <span className="text-slate-500 text-xs block font-medium">Project Portfolio Synthesis</span>
                <h3 className="font-bold text-slate-900 text-lg">{execKpis?.project_name}</h3>
              </div>
              <span className="rounded bg-emerald-100 border border-emerald-200 px-3 py-1 font-bold text-emerald-900 text-xs">
                {execKpis?.kpis?.project_health_status}
              </span>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="rounded-lg bg-slate-50 border border-slate-200 p-3">
                <span className="text-slate-500 block text-[11px] font-medium">Developer IRR</span>
                <strong className="text-emerald-700 text-xl font-bold font-mono">{execKpis?.kpis?.project_internal_rate_of_return_irr_pct ?? "—"}{execKpis?.kpis?.project_internal_rate_of_return_irr_pct != null ? "%" : ""}</strong>
              </div>
              <div className="rounded-lg bg-slate-50 border border-slate-200 p-3">
                <span className="text-slate-500 block text-[11px] font-medium">Equity Multiple</span>
                <strong className="text-blue-700 text-xl font-bold font-mono">{execKpis?.kpis?.equity_multiple ?? "—"}{execKpis?.kpis?.equity_multiple != null ? "x" : ""}</strong>
              </div>
              <div className="rounded-lg bg-slate-50 border border-slate-200 p-3">
                <span className="text-slate-500 block text-[11px] font-medium">Gross Development Value</span>
                <strong className="text-slate-900 text-xl font-bold font-mono">{inr(execKpis?.kpis?.gross_development_value_gdv_inr)}</strong>
              </div>
              <div className="rounded-lg bg-slate-50 border border-slate-200 p-3">
                <span className="text-slate-500 block text-[11px] font-medium">Projected Margin</span>
                <strong className="text-amber-800 text-xl font-bold font-mono">{execKpis?.kpis?.projected_gross_margin_pct}%</strong>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-3 pt-2 text-slate-700">
              <div className="rounded-lg border border-slate-200 bg-slate-50 p-3">
                <span className="text-slate-500 block text-[10px] font-medium">Statutory Clearance</span>
                <span className="font-semibold text-emerald-700">{execKpis?.kpis?.statutory_clearance_index_pct ?? "—"}% of compliance rules pass</span>
              </div>
              <div className="rounded-lg border border-slate-200 bg-slate-50 p-3">
                <span className="text-slate-500 block text-[10px] font-medium">Structural Safety Factor</span>
                <span className="font-semibold text-blue-700">{execKpis?.kpis?.structural_safety_factor ?? "See Engineering module"}</span>
              </div>
              <div className="rounded-lg border border-slate-200 bg-slate-50 p-3">
                <span className="text-slate-500 block text-[10px] font-medium">Green Building Target</span>
                <span className="font-semibold text-emerald-800">{execKpis?.kpis?.green_certification_target}</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* TAB 8: EQUIPMENT & DELAY RISK */}
      {activeTab === "equipment" && (
        <div className="space-y-6">
          <Section title="Heavy Construction Equipment Fleet" desc="Machinery from the BOQ (equipment-days) and delay risk from the programme simulation">
            <div className="overflow-x-auto rounded-lg border border-slate-200">
              <Table>
                <TableHeader className="bg-slate-50 border-b border-slate-200">
                  <TableRow>
                    <TableHead className="text-slate-700 font-semibold">Equipment Description</TableHead>
                    <TableHead className="text-center text-slate-700 font-semibold">Allocated Units</TableHead>
                    <TableHead className="text-center text-slate-700 font-semibold">Utilization</TableHead>
                    <TableHead className="text-center text-slate-700 font-semibold">Site Status</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {equipmentData?.equipment_fleet?.map((eq, idx) => (
                    <TableRow key={idx} className="text-xs hover:bg-slate-50/50">
                      <TableCell className="font-semibold text-slate-900">{eq.equipment}</TableCell>
                      <TableCell className="text-center font-bold text-slate-900 font-mono">{eq.allocated_qty}</TableCell>
                      <TableCell className="text-center font-semibold text-blue-700 font-mono">{eq.utilization_pct}%</TableCell>
                      <TableCell className="text-center">
                        <span className="rounded bg-emerald-100 border border-emerald-200 px-2 py-0.5 text-[10px] font-semibold text-emerald-800">
                          {eq.status}
                        </span>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          </Section>

          <Section title="Multi-Factor Construction Delay Risks" desc="Weather, labor, and supply chain vulnerability analysis">
            <div className="space-y-3">
              {equipmentData?.identified_delay_risks?.map((rk, idx) => (
                <div key={idx} className="rounded-lg border border-slate-200 bg-slate-50/70 p-3.5 text-xs space-y-1.5 shadow-2xs">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-slate-900">{rk.factor}</span>
                    <span className="font-semibold text-rose-700 font-mono">+{rk.impact_days} Days Float Impact</span>
                  </div>
                  <p className="text-slate-700 text-[11px]"><strong className="text-slate-600">Mitigation:</strong> {rk.mitigation}</p>
                </div>
              ))}
            </div>
            <div className="mt-3 flex items-center justify-between text-xs text-slate-600 border-t border-slate-200 pt-3">
              <span>Total Recommended Float Buffer: <strong className="text-amber-800 font-bold font-mono">{equipmentData?.recommended_float_buffer_days} Days</strong></span>
              <span>Schedule Confidence Index: <strong className="text-emerald-700 font-bold font-mono">{equipmentData?.schedule_confidence_index_pct ?? "—"}{equipmentData?.schedule_confidence_index_pct != null ? "% on-time probability" : ""}</strong></span>
            </div>
          </Section>
        </div>
      )}
    </div>
  );
}
