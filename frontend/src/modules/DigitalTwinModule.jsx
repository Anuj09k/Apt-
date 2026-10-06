import { useEffect, useState } from "react";
import { toast } from "sonner";
import {
  Activity,
  Cpu,
  Clock,
  ShieldCheck,
  Wrench,
  AlertTriangle,
  CheckCircle2,
  RefreshCw,
  Layers,
  BarChart3,
  Thermometer,
} from "lucide-react";
import { api, apiError } from "../lib/api";
import { Section, Metric } from "../components/Field";
import { Button } from "../components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "../components/ui/table";
import { num } from "../lib/format";

export default function DigitalTwinModule({ project, projectId }) {
  const [summary, setSummary] = useState(null);
  const [sensors, setSensors] = useState(null);
  const [delays, setDelays] = useState(null);
  const [loading, setLoading] = useState(false);

  const loadData = async () => {
    if (!projectId) return;
    setLoading(true);
    try {
      const [sumRes, senRes, delRes] = await Promise.all([
        api.get(`/projects/${projectId}/digital-twin/summary`),
        api.get(`/projects/${projectId}/digital-twin/sensors`),
        api.get(`/projects/${projectId}/digital-twin/delays`),
      ]);
      setSummary(sumRes.data);
      setSensors(senRes.data);
      setDelays(delRes.data);
    } catch (e) {
      toast.error(apiError(e.response?.data?.detail));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [projectId]);

  const prog = summary?.progress_4d;
  const qs = summary?.quality_safety;
  const fm = summary?.facility_management;
  const liveConc = sensors?.live_telemetry?.concrete_curing_maturity;
  // Blocks without site records return labelled sample data; say so on screen.
  const sampleBlocks = [
    sensors?.registry?.data_source === "sample" && "device registry",
    liveConc?.data_source === "sample" && "concrete maturity",
    qs?.data_source === "sample" && "quality & safety",
    fm?.data_source === "sample" && "facility management",
  ].filter(Boolean);
  const show = (v, suffix = "") => (v === null || v === undefined ? "—" : `${v}${suffix}`);

  return (
    <div className="space-y-6">
      {/* HEADER */}
      <div className="rounded-xl border border-slate-800 bg-gradient-to-r from-slate-900 via-slate-900 to-purple-950/80 p-6 shadow-md text-white">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-purple-600 text-white shadow-lg shadow-purple-500/30">
              <Activity className="h-6 w-6" />
            </div>
            <div>
              <h1 className="text-xl font-bold tracking-tight text-white">Digital Twin & Smart Construction</h1>
              <p className="text-xs text-slate-300">
                IoT sensor telemetry, concrete maturity tracking, 4D BIM progress (EVM), quality cube tests, and predictive facility maintenance
              </p>
            </div>
          </div>
          <Button onClick={loadData} disabled={loading} size="sm" className="bg-slate-800 hover:bg-slate-700 text-white border-slate-700">
            {loading ? <RefreshCw className="mr-1.5 h-3.5 w-3.5 animate-spin" /> : <RefreshCw className="mr-1.5 h-3.5 w-3.5" />}
            Refresh Telemetry
          </Button>
        </div>
      </div>

      {sampleBlocks.length > 0 && (
        <div className="flex items-start gap-2 rounded-lg border border-amber-300 bg-amber-50 p-3 text-xs text-amber-900">
          <AlertTriangle className="h-4 w-4 shrink-0 mt-0.5 text-amber-600" />
          <span>
            <strong>Sample data shown for: {sampleBlocks.join(", ")}.</strong> No site records or sensors are connected
            to this project, so these panels are illustrative only and must not be used for site decisions.
            Progress and delay figures are computed from this project's own programme.
          </span>
        </div>
      )}

      {/* METRICS STRIP */}
      {prog && (
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-4 md:grid-cols-5">
          <Metric label="Completion" value={show(prog.project_completion_pct, "%")} hint={prog.completion_basis} />
          <Metric label="Schedule Perf (SPI)" value={show(prog.earned_value_metrics?.schedule_performance_index_spi)} hint={prog.schedule_status} />
          <Metric label="Cost Perf (CPI)" value={show(prog.earned_value_metrics?.cost_performance_index_cpi)} hint="Needs recorded actual cost" />
          <Metric label="Quality Index" value={show(qs?.quality_index_score, "/100")} hint="Share of cube results passed" />
          <Metric label="Safety Man-Hours" value={qs?.safety?.safe_man_hours_worked == null ? "—" : num(qs.safety.safe_man_hours_worked)} hint={`LTIs: ${show(qs?.safety?.lost_time_injuries_lti)}`} />
        </div>
      )}

      {/* 1. IOT SENSOR TELEMETRY & CONCRETE MATURITY */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <Section
          title="IoT Sensors & Device Registry"
          description="Live status of on-site telemetry gateways and environmental monitors"
        >
          <div className="space-y-2">
            {sensors?.registry?.devices?.map((d) => (
              <div key={d.id} className="flex items-center justify-between rounded border border-slate-200 bg-slate-50/70 p-2.5 text-xs shadow-2xs">
                <div>
                  <div className="font-bold text-slate-900 flex items-center gap-2">
                    <Cpu className="h-3.5 w-3.5 text-purple-600" />
                    {d.id} — {d.type}
                  </div>
                  <div className="text-[11px] text-slate-500">{d.location} • {d.model}</div>
                </div>
                <div className="text-right">
                  <span className={`rounded border px-1.5 py-0.5 text-[10px] font-semibold uppercase ${
                    d.status === "online" ? "bg-emerald-100 border-emerald-200 text-emerald-800" : "bg-amber-100 border-amber-200 text-amber-800"
                  }`}>
                    {d.status}{d.battery_pct != null ? ` (${d.battery_pct}%)` : ""}
                  </span>
                  <div className="mt-0.5 text-[10px] text-slate-500 font-mono">{d.telemetry_param}</div>
                </div>
              </div>
            ))}
          </div>
        </Section>

        {/* CONCRETE MATURITY CARD */}
        <Section
          title="Smart Concrete Maturity Tracker"
          description="ASTM C1074 maturity (Nurse-Saul and Arrhenius) checked against IS 456 Cl. 11.3 minimum stripping times"
        >
          {liveConc ? (
            <div className="rounded-lg border border-purple-200 bg-purple-50/60 p-4 text-xs space-y-3">
              <div className="flex items-center justify-between border-b border-purple-200 pb-2">
                <span className="font-bold text-purple-950 flex items-center gap-1.5">
                  <Thermometer className="h-4 w-4 text-purple-700" /> Core Temperature: {liveConc.current_core_temp_celsius}°C
                </span>
                <span className="text-purple-800 font-medium">Ambient: {liveConc.ambient_temp_celsius}°C</span>
              </div>

              <div className="grid grid-cols-2 gap-3 text-slate-700">
                <div>Curing Age: <strong className="text-slate-900">{liveConc.curing_age_hours} hrs</strong></div>
                <div>Equivalent Age: <strong className="text-slate-900">{liveConc.equivalent_age_maturity_index} °C-hrs</strong></div>
                <div>Est. Compressive Strength: <strong className="text-slate-900 text-sm font-bold">{show(liveConc.estimated_compressive_strength_mpa, " MPa")}</strong></div>
                <div>Grade: <strong className="text-slate-900">M{liveConc.target_strength_mpa}</strong></div>
              </div>

              <div className={`rounded bg-white p-2.5 font-semibold border shadow-2xs ${
                liveConc.strip_ok ? "text-emerald-800 border-emerald-200" : "text-amber-800 border-amber-300"
              }`}>
                {liveConc.strip_ok ? "✓ " : "⚠ "}{liveConc.formwork_stripping_advisory}
              </div>
            </div>
          ) : (
            <div className="py-6 text-center text-xs text-muted-foreground">Loading concrete telemetry...</div>
          )}
        </Section>
      </div>

      {/* 2. 4D PROGRESS TRACKING & SCHEDULE DELAYS */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <Section
          title="4D BIM Progress Tracking"
          description="Floor-by-floor status from the CPM programme (recorded progress where entered)"
        >
          <div className="max-h-64 overflow-y-auto space-y-1.5 pr-1">
            {prog?.floor_4d_breakdown?.map((f) => (
              <div key={f.floor} className="flex items-center justify-between rounded bg-slate-50 border border-slate-200 px-3 py-2 text-xs">
                <span className="font-medium text-slate-900">{f.floor}</span>
                <div className="flex items-center gap-3">
                  <span
                    className={`rounded px-1.5 py-0.5 text-[10px] font-bold uppercase border ${
                      f.status === "completed"
                        ? "bg-emerald-100 border-emerald-200 text-emerald-800"
                        : f.status === "in_progress"
                        ? "bg-blue-100 border-blue-200 text-blue-800"
                        : f.status === "formwork_rebar"
                        ? "bg-amber-100 border-amber-200 text-amber-800"
                        : "bg-slate-100 border-slate-200 text-slate-600"
                    }`}
                  >
                    {f.status.replace("_", " ")} ({f.completion_pct}%)
                  </span>
                  <span className="text-[11px] text-slate-500 font-mono">{f.planned_date || f.actual_date}</span>
                </div>
              </div>
            ))}
          </div>
        </Section>

        {/* DELAYS & MONTE CARLO */}
        <Section
          title="Schedule Delay Risk Simulation"
          description={delays?.method || "Monte Carlo forecast over this project's programme"}
        >
          {delays && (
            <div className="space-y-3 text-xs">
              <div className="flex items-center justify-between rounded bg-slate-50 border border-slate-200 p-3 text-slate-700">
                <div>Baseline: <strong className="text-slate-900">{delays.baseline_completion_date}</strong></div>
                <div>Predicted (P50): <strong className="text-slate-900 font-bold">{delays.predicted_completion_date}</strong></div>
                <div>P80: <strong className="text-slate-900">{delays.p80_completion_date}</strong></div>
                <div>On-Time Probability: <strong className="text-slate-900 text-sm font-bold">{delays.on_time_probability_pct}%</strong></div>
              </div>

              <div className="border border-slate-200 rounded p-3 bg-white shadow-2xs">
                <div className="font-semibold text-slate-900 mb-2">Activities driving the delay:</div>
                <ul className="space-y-1.5 text-slate-700">
                  {delays.risk_factors_analyzed?.map((r, i) => (
                    <li key={i} className="flex items-start gap-1.5">
                      <AlertTriangle className="h-3.5 w-3.5 text-amber-600 shrink-0 mt-0.5" />
                      <span>
                        <strong className="text-slate-900">{r.factor}</strong> (drives completion in {r.probability_pct}% of runs, +{r.impact_days}d when it does): {r.mitigation}
                      </span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          )}
        </Section>
      </div>

      {/* 3. QUALITY CUBE TESTS & PREDICTIVE FACILITY MANAGEMENT */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <Section
          title="Quality Assurance & Concrete Cube Tests"
          description="IS 456 7-day and 28-day compressive strength batch logs"
        >
          <div className="overflow-x-auto rounded-lg border border-slate-200">
            <Table>
              <TableHeader className="bg-slate-50 border-b border-slate-200">
                <TableRow>
                  <TableHead className="text-slate-700 font-semibold">Batch ID / Member</TableHead>
                  <TableHead className="text-slate-700 font-semibold">Grade</TableHead>
                  <TableHead className="text-right text-slate-700 font-semibold">7-Day</TableHead>
                  <TableHead className="text-right text-slate-700 font-semibold">28-Day</TableHead>
                  <TableHead className="text-slate-700 font-semibold">Status</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {qs?.cube_tests?.map((b) => (
                  <TableRow key={b.batch_id} className="text-xs hover:bg-slate-50/50">
                    <TableCell className="font-medium text-xs text-slate-900">
                      <div>{b.batch_id}</div>
                      <div className="text-[10px] text-slate-500">{b.member}</div>
                    </TableCell>
                    <TableCell className="text-xs text-slate-700 font-medium">{b.grade}</TableCell>
                    <TableCell className="text-right text-xs font-mono text-slate-900">{b.test_7d_mpa} MPa</TableCell>
                    <TableCell className="text-right text-xs font-mono text-slate-900">{b.test_28d_mpa} {typeof b.test_28d_mpa === 'number' ? 'MPa' : ''}</TableCell>
                    <TableCell>
                      <span className="rounded bg-emerald-100 border border-emerald-200 px-1.5 py-0.5 text-[10px] font-bold text-emerald-800">
                        {b.status}
                      </span>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        </Section>

        {/* FACILITY MANAGEMENT */}
        <Section
          title="Predictive Facility Management & BMS"
          description="Equipment operating hours, vibration thresholds, and preventive maintenance calendar"
        >
          <div className="space-y-2">
            {fm?.assets?.map((a) => (
              <div key={a.tag} className="flex items-center justify-between rounded border border-slate-200 bg-slate-50/70 p-2.5 text-xs shadow-2xs">
                <div>
                  <div className="font-bold text-slate-900">{a.name}</div>
                  <div className="text-[11px] text-slate-500">{a.location} • {num(a.operating_hours)} hrs runtime</div>
                </div>
                <div className="text-right">
                  <span className={`rounded border px-1.5 py-0.5 text-[10px] font-semibold ${
                    a.status === 'Optimal' ? 'bg-emerald-100 border-emerald-200 text-emerald-800' : 'bg-amber-100 border-amber-200 text-amber-800'
                  }`}>
                    {a.status} ({a.health_score_pct}%)
                  </span>
                  <div className="text-[10px] text-slate-500 mt-0.5 font-mono">Due: {show(a.next_service_due)}</div>
                </div>
              </div>
            ))}
          </div>
        </Section>
      </div>
    </div>
  );
}
