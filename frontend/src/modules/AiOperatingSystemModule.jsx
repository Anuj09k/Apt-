import React, { useState, useEffect } from "react";
import { api, apiError } from "../lib/api";
import { toast } from "sonner";
import {
  BrainCircuit,
  Database,
  History,
  GitFork,
  CheckCircle2,
  Sliders,
  Award,
  Layers,
  FileCheck,
  Building,
  TrendingUp,
  Scale,
} from "lucide-react";
import { Section, Metric } from "../components/Field";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../components/ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "../components/ui/table";
import { inr, num } from "../lib/format";

export default function AiOperatingSystemModule({ project, projectId }) {
  const [activeTab, setActiveTab] = useState("graph");
  const [loading, setLoading] = useState(false);

  // States
  const [graphData, setGraphData] = useState(null);
  const [memoryData, setMemoryData] = useState(null);
  const [decisionLog, setDecisionLog] = useState(null);
  const [benchmarks, setBenchmarks] = useState(null);

  // Decision Sandbox states
  const [sandboxFloors, setSandboxFloors] = useState(14);
  const [sandboxConcrete, setSandboxConcrete] = useState("M35");
  const [sandboxSlab, setSandboxSlab] = useState("PT Flat Slab");
  const [sandboxScale, setSandboxScale] = useState(1.0);
  const [sandboxResult, setSandboxResult] = useState(null);
  const [simulating, setSimulating] = useState(false);

  useEffect(() => {
    loadAllData();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [projectId]);

  async function loadAllData() {
    setLoading(true);
    try {
      const [gRes, mRes, dRes, bRes] = await Promise.all([
        api.get(`/projects/${projectId}/ai-os/knowledge-graph`),
        api.get(`/projects/${projectId}/ai-os/memory`),
        api.get(`/projects/${projectId}/ai-os/decision-log`),
        api.get(`/projects/${projectId}/ai-os/benchmarks`),
      ]);
      setGraphData(gRes.data);
      setMemoryData(mRes.data);
      setDecisionLog(dRes.data);
      setBenchmarks(bRes.data);
      // Run initial sandbox
      runSandboxSimulation();
    } catch (e) {
      toast.error(apiError(e));
    } finally {
      setLoading(false);
    }
  }

  async function runSandboxSimulation() {
    setSimulating(true);
    try {
      const res = await api.post(`/projects/${projectId}/ai-os/sandbox`, {
        floors: Number(sandboxFloors),
        concrete_grade: sandboxConcrete,
        slab_type: sandboxSlab,
        footprint_scale: Number(sandboxScale),
      });
      setSandboxResult(res.data);
    } catch (e) {
      toast.error(apiError(e));
    } finally {
      setSimulating(false);
    }
  }

  return (
    <div className="space-y-6 pb-12">
      {/* Header Banner */}
      <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-2xs">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="rounded bg-blue-50 border border-blue-200 px-2 py-0.5 text-xs font-semibold text-blue-700">
                Core Engineering OS
              </span>
              <span className="text-xs text-slate-500 font-medium">IS & NBC Code Intelligence</span>
            </div>
            <h1 className="text-2xl font-bold tracking-tight text-slate-900 flex items-center gap-2">
              <BrainCircuit className="h-6 w-6 text-blue-600" />
              AI Civil Engineering Operating System
            </h1>
            <p className="text-sm text-slate-600 max-w-3xl">
              Semantic engineering knowledge graph, persistent design memory, hash-chained decision log, and engine-backed what-if sandbox.
            </p>
          </div>
          <Button variant="outline" size="sm" onClick={loadAllData} disabled={loading} className="gap-2 border-slate-300 text-slate-700 hover:bg-slate-50 hover:text-slate-900 font-medium">
            {loading ? "Refreshing..." : "Refresh Intelligence"}
          </Button>
        </div>

        {/* Tab Navigation */}
        <div className="mt-6 flex flex-wrap gap-2 border-t border-slate-100 pt-4">
          {[
            { id: "graph", label: "Knowledge Graph", icon: GitFork },
            { id: "memory", label: "Engineering Memory", icon: History },
            { id: "log", label: "Decision Audit Log", icon: FileCheck },
            { id: "sandbox", label: "Decision Sandbox", icon: Sliders },
            { id: "benchmarks", label: "CPWD Benchmarks", icon: Scale },
          ].map((tab) => {
            const Icon = tab.icon;
            const active = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 rounded-lg px-3.5 py-2 text-xs font-semibold transition-all ${
                  active
                    ? "bg-blue-600 text-white shadow-xs"
                    : "bg-slate-100 text-slate-700 hover:bg-slate-200 hover:text-slate-900 border border-slate-200/60"
                }`}
              >
                <Icon className="h-4 w-4" />
                {tab.label}
              </button>
            );
          })}
        </div>
      </div>

      {/* TAB 1: KNOWLEDGE GRAPH */}
      {activeTab === "graph" && (
        <div className="space-y-6">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <Metric label="Graph Nodes" value={graphData?.metrics?.total_nodes ?? "—"} />
            <Metric label="Semantic Links" value={graphData?.metrics?.total_relationships ?? "—"} />
            <Metric label="Governing Standards" value={graphData?.metrics?.governing_standards_count ?? "—"} />
            <Metric label="Graph Density" value={graphData?.metrics?.graph_density ?? "—"} />
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Section title="Active Semantic Nodes" desc="Regulatory clauses, geometric constraints, and structural members">
              <div className="space-y-2 max-h-96 overflow-y-auto pr-1">
                {graphData?.nodes?.map((n) => (
                  <div key={n.id} className="flex items-center justify-between rounded-lg border border-slate-200 bg-slate-50/70 p-3 text-xs shadow-2xs">
                    <div className="flex items-center gap-2.5">
                      <span className={`px-2 py-0.5 rounded font-mono text-[10px] font-semibold border ${
                        n.type === "standard" ? "bg-amber-100 text-amber-900 border-amber-200" :
                        n.type === "parameter" ? "bg-blue-100 text-blue-900 border-blue-200" : "bg-emerald-100 text-emerald-900 border-emerald-200"
                      }`}>
                        {n.type.toUpperCase()}
                      </span>
                      <span className="font-semibold text-slate-900">{n.label}</span>
                    </div>
                    <span className="text-slate-600 font-medium">{n.category}</span>
                  </div>
                ))}
              </div>
            </Section>

            <Section title="Ontological Relationships" desc="Governing, sizing, and constraint interdependencies">
              <div className="space-y-2 max-h-96 overflow-y-auto pr-1">
                {graphData?.edges?.map((e, idx) => (
                  <div key={idx} className="flex items-center justify-between rounded-lg border border-slate-200 bg-slate-50/70 p-3 text-xs shadow-2xs">
                    <div className="flex items-center gap-2">
                      <span className="font-mono font-medium text-slate-800">{e.source}</span>
                      <span className="rounded bg-blue-50 border border-blue-200 px-1.5 py-0.5 text-[10px] text-blue-800 font-mono font-semibold">
                        --[{e.relation}]--&gt;
                      </span>
                      <span className="font-mono font-medium text-slate-800">{e.target}</span>
                    </div>
                    <span className="text-[10px] text-slate-500 font-medium">Weight: {e.weight}</span>
                  </div>
                ))}
              </div>
            </Section>
          </div>
        </div>
      )}

      {/* TAB 2: ENGINEERING MEMORY */}
      {activeTab === "memory" && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Metric label="Episodes Logged" value={memoryData?.total_episodes ?? 0} />
            <Metric label="Source" value="Project activity log" />
            <Metric label="Dominant Domain" value={memoryData?.memory_summary?.dominant_domain || "—"} />
          </div>

          <Section title="Episodic Engineering Memory" desc="What changed on this project, when and by whom - read from its activity log">
            <div className="space-y-4">
              {memoryData?.episodes?.length === 0 && (
                <div className="py-6 text-center text-xs text-muted-foreground">No recorded activity on this project yet.</div>
              )}
              {memoryData?.episodes?.map((ep) => (
                <div key={ep.id} className="rounded-lg border border-slate-200 bg-slate-50/70 p-4 text-xs space-y-2 shadow-xs">
                  <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-200 pb-2">
                    <div className="flex items-center gap-2">
                      <span className="font-mono font-bold text-blue-700">{ep.id}</span>
                      <span className="rounded bg-blue-100 border border-blue-200 px-2 py-0.5 text-[11px] font-semibold text-blue-800">{ep.domain}</span>
                      <span className="text-sm font-semibold text-slate-900">{ep.title}</span>
                    </div>
                    <div className="flex items-center gap-3 text-slate-600 text-[11px]">
                      <span>Author: <strong className="text-slate-900">{ep.author}</strong></span>
                      <span>{ep.timestamp ? new Date(ep.timestamp).toLocaleString() : ""}</span>
                    </div>
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3 pt-1 text-slate-800">
                    <div>
                      <strong className="text-slate-600 block mb-0.5">Design Context:</strong>
                      <p>{ep.context}</p>
                    </div>
                    <div>
                      <strong className="text-slate-600 block mb-0.5">Engineering Rationale:</strong>
                      <p className="text-emerald-900 font-medium bg-emerald-50/70 p-2.5 rounded border border-emerald-200">{ep.rationale}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </Section>
        </div>
      )}

      {/* TAB 3: DECISION AUDIT LOG */}
      {activeTab === "log" && (
        <div className="space-y-6">
          <div className="flex items-center justify-between rounded-lg border border-emerald-200 bg-emerald-50/80 p-4 text-xs shadow-xs">
            <div className="flex items-center gap-3">
              <CheckCircle2 className="h-5 w-5 text-emerald-700" />
              <div>
                <div className="font-semibold text-emerald-950 text-sm">Hash-Chained Decision Log</div>
                <div className="font-mono text-emerald-800 text-[11px]">{decisionLog?.audit_hash || "No entries yet"}</div>
              </div>
            </div>
            <span className="rounded bg-emerald-100 border border-emerald-200 px-2.5 py-1 font-semibold text-emerald-900 text-xs">
              {`${decisionLog?.total_decisions ?? 0} recorded entries`}
            </span>
          </div>

          <Section title="Recorded Decisions" desc="Each entry's hash covers the one before it, so any later edit to the history breaks the chain">
            <div className="overflow-x-auto rounded-lg border border-slate-200">
              <Table>
                <TableHeader className="bg-slate-50 border-b border-slate-200">
                  <TableRow>
                    <TableHead className="w-28 text-slate-700 font-semibold">Ref ID</TableHead>
                    <TableHead className="w-36 text-slate-700 font-semibold">Category</TableHead>
                    <TableHead className="text-slate-700 font-semibold">Decision</TableHead>
                    <TableHead className="text-slate-700 font-semibold">Detail</TableHead>
                    <TableHead className="w-40 text-slate-700 font-semibold">By</TableHead>
                    <TableHead className="w-28 text-right text-slate-700 font-semibold">Entry Hash</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {decisionLog?.decisions?.map((dec) => (
                    <TableRow key={dec.id} className="text-xs hover:bg-slate-50/50">
                      <TableCell className="font-mono font-semibold text-blue-700">{dec.id}</TableCell>
                      <TableCell className="font-medium text-slate-700">{dec.category}</TableCell>
                      <TableCell className="font-semibold text-slate-900">{dec.decision}</TableCell>
                      <TableCell className="text-slate-700">{dec.justification}</TableCell>
                      <TableCell className="text-slate-600">{dec.agent_signoff}</TableCell>
                      <TableCell className="text-right font-mono text-[10px] text-slate-600">{dec.entry_hash}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          </Section>
        </div>
      )}

      {/* TAB 4: DECISION SANDBOX */}
      {activeTab === "sandbox" && (
        <div className="space-y-6">
          <Section title="What-If Decision Simulator" desc="Adjust structural and spatial parameters to evaluate instant cost, FAR, and carbon deltas">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 rounded-xl border border-slate-200 bg-slate-50/70 p-4 text-xs">
              <div>
                <label className="text-slate-700 font-medium block mb-1">Storeys / Floors: {sandboxFloors}</label>
                <Input
                  type="number"
                  min="4"
                  max="40"
                  value={sandboxFloors}
                  onChange={(e) => setSandboxFloors(e.target.value)}
                  className="bg-white border-slate-200"
                />
              </div>
              <div>
                <label className="text-slate-700 font-medium block mb-1">Concrete Grade</label>
                <Select value={sandboxConcrete} onValueChange={setSandboxConcrete}>
                  <SelectTrigger className="bg-white border-slate-200"><SelectValue /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="M30">M30 (Standard Frame)</SelectItem>
                    <SelectItem value="M35">M35 (High-Rise Standard)</SelectItem>
                    <SelectItem value="M40">M40 (Slim Column Core)</SelectItem>
                    <SelectItem value="M50">M50 (Ultra High-Strength)</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div>
                <label className="text-slate-700 font-medium block mb-1">Floor Slab System</label>
                <Select value={sandboxSlab} onValueChange={setSandboxSlab}>
                  <SelectTrigger className="bg-white border-slate-200"><SelectValue /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="PT Flat Slab">Post-Tensioned Flat Slab</SelectItem>
                    <SelectItem value="RCC Beam-Slab">Conventional RCC Beam-Slab</SelectItem>
                    <SelectItem value="Precast Hollow-Core">Precast Hollow-Core Planks</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div>
                <label className="text-slate-700 font-medium block mb-1">Footprint Scale: {sandboxScale}x</label>
                <Input
                  type="number"
                  step="0.05"
                  min="0.7"
                  max="1.5"
                  value={sandboxScale}
                  onChange={(e) => setSandboxScale(e.target.value)}
                  className="bg-white border-slate-200"
                />
              </div>
            </div>
            <div className="mt-3 flex justify-end">
              <Button size="sm" onClick={runSandboxSimulation} disabled={simulating} className="bg-blue-600 hover:bg-blue-700 text-white">
                {simulating ? "Calculating Deltas..." : "Run What-If Simulation"}
              </Button>
            </div>
          </Section>

          {sandboxResult && (
            <div className="space-y-4">
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <Metric label="Simulated Built-Up" value={`${num(sandboxResult.simulation?.builtup_sqm)} m²`} />
                <Metric label="Achieved FAR" value={sandboxResult.simulation?.achieved_far} />
                <Metric label="Simulated Cost" value={inr(sandboxResult.simulation?.estimated_cost_inr)} />
                <Metric label="Embodied Carbon" value={`${num(sandboxResult.simulation?.quantities?.embodied_carbon_tonnes)} tCO₂e`} />
              </div>

              <div className="rounded-xl border border-slate-200 bg-white p-4 text-xs shadow-xs">
                <h4 className="font-semibold text-slate-900 mb-3 flex items-center justify-between">
                  <span>Delta vs. Baseline Scheme</span>
                  <span className={`px-2 py-0.5 rounded font-mono text-[10px] font-semibold border ${
                    sandboxResult.deltas?.verdict === "FEASIBLE" ? "bg-emerald-100 text-emerald-800 border-emerald-200" : "bg-rose-100 text-rose-800 border-rose-200"
                  }`}>
                    {sandboxResult.deltas?.verdict}
                  </span>
                </h4>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-slate-700">
                  <div className="rounded-lg bg-slate-50 border border-slate-200 p-3">
                    <span className="text-slate-500 block text-[11px]">Area Variance:</span>
                    <strong className="text-slate-900 text-base font-bold">
                      {sandboxResult.deltas?.builtup_area_sqm >= 0 ? "+" : ""}{num(sandboxResult.deltas?.builtup_area_sqm)} m²
                    </strong>
                  </div>
                  <div className="rounded-lg bg-slate-50 border border-slate-200 p-3">
                    <span className="text-slate-500 block text-[11px]">Cost Variance:</span>
                    <strong className={`text-base font-bold ${sandboxResult.deltas?.cost_inr > 0 ? "text-amber-800" : "text-emerald-700"}`}>
                      {sandboxResult.deltas?.cost_inr >= 0 ? "+" : ""}{inr(sandboxResult.deltas?.cost_inr)} ({sandboxResult.deltas?.cost_pct}%)
                    </strong>
                  </div>
                  <div className="rounded-lg bg-slate-50 border border-slate-200 p-3">
                    <span className="text-slate-500 block text-[11px]">Material Takeoff:</span>
                    <span className="block text-slate-900 font-medium">
                      Concrete: {num(sandboxResult.simulation?.quantities?.concrete_m3)} m³ | Steel: {num(sandboxResult.simulation?.quantities?.steel_reinforcement_mt)} MT
                    </span>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* TAB 5: CPWD BENCHMARKS */}
      {activeTab === "benchmarks" && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Metric label="Efficiency Score" value={benchmarks?.overall_efficiency_score == null ? "—" : `${benchmarks.overall_efficiency_score}%`} />
            <Metric label="Metrics Evaluated" value={benchmarks?.total_metrics_evaluated ?? 0} />
          </div>

          <Section title="Benchmarking against Typical Ranges" desc={benchmarks?.summary || "This project's take-off, circulation and cost against typical Indian residential ranges"}>
            <div className="overflow-x-auto rounded-lg border border-slate-200">
              <Table>
                <TableHeader className="bg-slate-50 border-b border-slate-200">
                  <TableRow>
                    <TableHead className="text-slate-700 font-semibold">Engineering Metric</TableHead>
                    <TableHead className="text-slate-700 font-semibold">Unit</TableHead>
                    <TableHead className="text-right text-slate-700 font-semibold">Project Value</TableHead>
                    <TableHead className="text-right text-slate-700 font-semibold">Typical Low</TableHead>
                    <TableHead className="text-right text-slate-700 font-semibold">Typical High</TableHead>
                    <TableHead className="text-center text-slate-700 font-semibold">Outside Range</TableHead>
                    <TableHead className="text-center text-slate-700 font-semibold">Status</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {benchmarks?.benchmarks?.map((b, idx) => (
                    <TableRow key={idx} className="text-xs hover:bg-slate-50/50">
                      <TableCell className="font-semibold text-slate-900">{b.metric}</TableCell>
                      <TableCell className="text-slate-600 font-mono">{b.unit}</TableCell>
                      <TableCell className="text-right font-bold font-mono text-blue-700">{b.project_value}</TableCell>
                      <TableCell className="text-right text-slate-700 font-mono">{b.cpwd_benchmark ?? "—"}</TableCell>
                      <TableCell className="text-right text-slate-600 font-mono">{b.industry_p75 ?? "—"}</TableCell>
                      <TableCell className={`text-center font-semibold font-mono ${!b.variance_pct ? "text-emerald-700" : "text-amber-800"}`}>
                        {b.variance_pct == null ? "—" : b.variance_pct > 0 ? `+${b.variance_pct}%` : `${b.variance_pct}%`}
                      </TableCell>
                      <TableCell className="text-center">
                        <span className={`rounded border px-2 py-0.5 text-[10px] font-semibold ${
                          b.status === "WITHIN RANGE" || b.status === "BELOW BENCHMARK"
                            ? "bg-emerald-100 border-emerald-200 text-emerald-800"
                            : "bg-amber-100 border-amber-200 text-amber-800"}`}>
                          {b.status}
                        </span>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
            <p className="mt-3 text-xs text-slate-600 italic">{benchmarks?.summary}</p>
          </Section>
        </div>
      )}
    </div>
  );
}
