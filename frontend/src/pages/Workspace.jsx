import { lazy, Suspense, useCallback, useEffect, useMemo, useRef, useState } from "react";
import { useParams } from "react-router-dom";
import { toast } from "sonner";
import { Sparkles } from "lucide-react";
import { api, apiError } from "../lib/api";
import { TopBar } from "../components/TopBar";
import { MetricsStrip } from "../components/MetricsStrip";
import { CommandPalette } from "../components/CommandPalette";
import AptPanel from "../components/AptPanel";
import { ProjectNav } from "../components/ProjectNav";
import ErrorBoundary from "../components/ErrorBoundary";
import SiteModule from "../modules/SiteModule";
import { WORKSPACE_CATALOG } from "../lib/workspaceCatalog";
import { CalculationNotice } from "../components/CalculationNotice";
import { Button } from "../components/ui/button";

// Loaded on demand.
const GisModule = lazy(() => import("../modules/GisModule"));
const ThreeDModule = lazy(() => import("../modules/ThreeDModule"));
const EngineeringModule = lazy(() => import("../modules/EngineeringModule"));
const PlanningModule = lazy(() => import("../modules/PlanningModule"));
const CalculationsModule = lazy(() => import("../modules/CalculationsModule"));
const ParkingModule = lazy(() => import("../modules/ParkingModule"));
const BoqModule = lazy(() => import("../modules/BoqModule"));
const CostModule = lazy(() => import("../modules/CostModule"));
const ProgrammeModule = lazy(() => import("../modules/ProgrammeModule"));
const FinanceModule = lazy(() => import("../modules/FinanceModule"));
const ComplianceModule = lazy(() => import("../modules/ComplianceModule"));
const ReportsModule = lazy(() => import("../modules/ReportsModule"));
const DataHealthModule = lazy(() => import("../modules/DataHealthModule"));
const CollaborationModule = lazy(() => import("../modules/CollaborationModule"));
const GenerativeStudioModule = lazy(() => import("../modules/GenerativeStudioModule"));
const BimModule = lazy(() => import("../modules/BimModule"));
const AutonomousStudioModule = lazy(() => import("../modules/AutonomousStudioModule"));
const TownshipModule = lazy(() => import("../modules/TownshipModule"));
const DigitalTwinModule = lazy(() => import("../modules/DigitalTwinModule"));
const ProcurementMarketModule = lazy(() => import("../modules/ProcurementMarketModule"));
const UrbanSustainabilityModule = lazy(() => import("../modules/UrbanSustainabilityModule"));

const COMPONENTS = {
  plot: SiteModule, gis: GisModule, township: TownshipModule,
  "autonomous-studio": AutonomousStudioModule, planning: PlanningModule, parking: ParkingModule,
  studio: GenerativeStudioModule, "3d": ThreeDModule, calculations: CalculationsModule,
  engineering: EngineeringModule, bim: BimModule, "digital-twin": DigitalTwinModule,
  boq: BoqModule, cost: CostModule, procurement: ProcurementMarketModule,
  programme: ProgrammeModule, finance: FinanceModule, compliance: ComplianceModule,
  "urban-sustainability": UrbanSustainabilityModule, "data-health": DataHealthModule,
  reports: ReportsModule, collaboration: CollaborationModule,
};
const GROUPS = WORKSPACE_CATALOG.map(g => [g.id, g.label, g.modules.map(m => [m.id, m.name, m.icon, COMPONENTS[m.id]])]);

const MODULES = GROUPS.flatMap(([, , items]) => items);

// Holds the panel's height while a chunk arrives, so the surrounding chrome does not jump
// and settle. Deliberately quiet: on a warm cache this is on screen for a few frames, and
// a spinner that announces itself is worse than one nobody notices.
function ModuleLoading() {
  return (
    <div className="flex items-center justify-center py-24 text-sm text-muted-foreground"
         data-testid="module-loading">
      Loading module...
    </div>
  );
}
const GROUP_OF = Object.fromEntries(
  GROUPS.flatMap(([g, , items]) => items.map((m) => [m[0], g])));
const GROUP_LABEL = Object.fromEntries(GROUPS.map(([g, label]) => [g, label]));

const EDITABLE = [
  "name", "client", "location", "plot_reference", "status", "plot", "towers", "parking", "config",
  "quantity_ratios", "rates", "labour_rates", "equipment_rates", "utility_config", "compliance_rules",
  "engineering", "finance", "solar", "cost_adders", "wastage_pct",
  // The programme config holds the user's per-task edits; without it a reload silently
  // discards them and the table quietly reverts to the generated plan.
  "schedule",
  // Setbacks live under dev_controls and are the one value the envelope is built from.
  // Without this every setback edit was discarded on reload.
  "dev_controls",
  // Shared, society-wide amenity areas are edited through update() like everything else
  // here. Leaving them out meant the clubhouse and pool areas a user typed were dropped
  // the moment the page reloaded, while still counting toward area until then.
  "society_amenities",
  // The packed site layout. Both the site map and the 3D view write it through update()
  // and both read it back expecting it to persist; it never did, so every session paid
  // to regenerate it and the staleness stamp it carries had nothing to compare against.
  "site_layout",
];

export default function Workspace() {
  const { projectId } = useParams();
  const [project, setProject] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [accessRole, setAccessRole] = useState("viewer");
  const [active, setActive] = useState("plot");
  const [saveState, setSaveState] = useState("saved");
  // "fresh" | "recomputing" | "stale" — whether the figures on screen were computed from
  // the project as it stands. `analysedAt` is when they last were.
  const [analysisState, setAnalysisState] = useState("recomputing");
  const [analysedAt, setAnalysedAt] = useState(null);
  const [duration, setDuration] = useState(null);
  const dirty = useRef(0);   // edit generation, not a boolean -- see saveNow
  const savedSnapshot = useRef(null);
  const saving = useRef(false);
  const saveBlocked = useRef(false);
  const [saveMessage, setSaveMessage] = useState("");
  const [loadError, setLoadError] = useState("");
  const [analysisError, setAnalysisError] = useState("");

  useEffect(() => {
    api
      .get(`/projects/${projectId}`)
      .then(({ data }) => {
        savedSnapshot.current = data;
        setAccessRole(data.access_role);
        setProject(data);
      })
      .catch((e) => setLoadError(apiError(e.response?.data?.detail)));
  }, [projectId]);

  // Live recalculation.
  //
  // A failure here used to end in `.catch(() => {})`. When /analyse failed — a backend
  // restart, a network blip, a document the engine throws on — `analysis` kept its previous
  // value, so FAR, built-up area, cost, the compliance score and the whole metrics rail
  // carried on showing figures computed from an older version of the project with nothing
  // on screen to say so. Silence is the worst outcome for a number someone signs off on.
  //
  // So a failure is recorded, retried with the same backoff the autosave uses, and shown.
  const analyseRetries = useRef(0);
  const analyseTimer = useRef(null);

  useEffect(() => {
    if (!project) return;
    let cancelled = false;
    const controller = new AbortController();
    setAnalysisState((prev) => (prev === "stale" ? "stale" : "recomputing"));

    const run = () => {
      api
        .post("/analyse", { project }, { signal: controller.signal })
        .then(({ data }) => {
          if (cancelled) return;
          analyseRetries.current = 0;
          setAnalysis(data);
          setAnalysedAt(new Date());
          setAnalysisState("fresh");
          setAnalysisError("");
        })
        .catch((e) => {
          if (cancelled) return;
          setAnalysisState("stale");
          setAnalysisError(apiError(e.response?.data?.detail));
          if (e.response?.status === 422) return;
          const wait = Math.min(2000 * 2 ** analyseRetries.current, 30000);
          analyseRetries.current += 1;
          analyseTimer.current = setTimeout(run, wait);
        });
    };

    analyseTimer.current = setTimeout(run, 250);
    return () => {
      cancelled = true;
      controller.abort();
      clearTimeout(analyseTimer.current);
    };
  }, [project]);

  // Autosave.
  //
  // Three things it has to get right, and the original got none of them:
  //
  //  1. A FAILED SAVE MUST RETRY. It used to toast an error and stop. The next attempt
  //     only came if the user happened to edit again, so a save that failed while they
  //     were finishing up lost the work silently.
  //  2. AN EDIT DURING A SAVE MUST NOT BE MARKED CLEAN. The flag was cleared after the
  //     request returned, so anything typed while it was in flight was recorded as
  //     already saved and then never sent.
  //  3. LEAVING THE PAGE MUST FLUSH. There is a debounce window where recent edits exist
  //     only in memory; closing the tab inside it threw them away.
  const saveTimer = useRef(null);
  const retries = useRef(0);
  const latest = useRef(project);
  useEffect(() => {
    latest.current = project;
  }, [project]);

  const saveNow = useCallback(async () => {
    const snapshot = latest.current;
    if (!snapshot || !dirty.current || saving.current || saveBlocked.current) return;
    saving.current = true;
    // Claim the current edit generation. Anything the user types after this line bumps it
    // again, so the save cannot mark those edits clean.
    const generation = dirty.current;
    setSaveState("saving");
    const updates = {};
    EDITABLE.forEach((k) => {
      if (snapshot[k] !== undefined && JSON.stringify(snapshot[k]) !== JSON.stringify(savedSnapshot.current?.[k])) updates[k] = snapshot[k];
    });
    if (!Object.keys(updates).length) {
      dirty.current = 0;
      saving.current = false;
      setSaveState("saved");
      return;
    }
    try {
      // The revision this edit started from. The server writes only if the document is
      // still at it, so a save can no longer replace a whole subtree — the tower list, the
      // plot — that someone else changed while this tab was editing.
      const { data } = await api.put(`/projects/${projectId}`, { updates, rev: snapshot.rev });
      retries.current = 0;
      savedSnapshot.current = { ...snapshot, rev: data.rev };
      latest.current = { ...latest.current, rev: data.rev };
      setSaveMessage("");
      if (data && data.rev !== undefined) setProject((prev) => ({ ...prev, rev: data.rev }));
      if (dirty.current === generation) {
        dirty.current = false;
        setSaveState("saved");
      } else {
        setSaveState("saving");        // more arrived while this was in flight
      }
    } catch (e) {
      // Never automatically overlay the stale local document onto someone else's edit.
      if (e.response?.status === 409) {
        saveBlocked.current = true;
        setSaveState("conflict");
        setSaveMessage("The server has a newer revision. Your local edits have NOT overwritten it. Export your draft, then load the server version and reapply the intended changes.");
        clearTimeout(saveTimer.current);
        return;
      }
      setSaveState("error");
      setSaveMessage(apiError(e.response?.data?.detail));
      if ([400, 403, 422].includes(e.response?.status)) return;
      // Back off and keep trying rather than dropping the work on the floor.
      const wait = Math.min(2000 * 2 ** retries.current, 30000);
      retries.current += 1;
      if (retries.current === 1) toast.error(apiError(e.response?.data?.detail));
      saveTimer.current = setTimeout(saveNow, wait);
    } finally {
      saving.current = false;
    }
  }, [projectId]);

  useEffect(() => {
    if (!project || !dirty.current || saveBlocked.current) return;
    setSaveState("saving");
    clearTimeout(saveTimer.current);
    saveTimer.current = setTimeout(saveNow, 900);
    return () => clearTimeout(saveTimer.current);
  }, [project, saveNow]);

  // Flush on the way out: closing the tab, switching away, or navigating.
  useEffect(() => {
    const flush = () => {
      if (!dirty.current) return;
      clearTimeout(saveTimer.current);
      saveNow();
    };
    const onHide = () => { if (document.visibilityState === "hidden") flush(); };
    const onBeforeUnload = (e) => {
      if (!dirty.current) return;
      flush();
      e.preventDefault();
      e.returnValue = "";        // prompts only while a save is genuinely outstanding
    };
    document.addEventListener("visibilitychange", onHide);
    window.addEventListener("beforeunload", onBeforeUnload);
    return () => {
      document.removeEventListener("visibilitychange", onHide);
      window.removeEventListener("beforeunload", onBeforeUnload);
      flush();
    };
  }, [saveNow]);

  // Headline build duration for the metrics strip. Uses the summary form of the
  // programme endpoint, which skips float verification and the 120-activity payload --
  // the completion date does not depend on either, and this runs on every recalculation.
  useEffect(() => {
    if (!project) return;
    let cancelled = false;
    const t = setTimeout(() => {
      // The project's own schedule config, so the headline cost reflects the programme the
      // user actually set -- target date, added tasks and all -- not a default one.
      api.post("/schedule", { project, summary: true, config: project.schedule || {} })
        .then(({ data }) => { if (!cancelled) setDuration(data.ok ? data : null); })
        .catch(() => { if (!cancelled) setDuration(null); });
    }, 600);   // debounce: the project mutates on every keystroke while editing
    return () => { cancelled = true; clearTimeout(t); };
  }, [project]);

  const update = useCallback((mutator) => {
    // A counter, not a boolean: the save compares the value it started with against the
    // value at the end, which is how an edit made mid-request stays dirty.
    dirty.current = (dirty.current || 0) + 1;
    setProject((prev) => {
      const copy = structuredClone(prev);
      mutator(copy);
      return copy;
    });
  }, []);

  const exportDraft = () => {
    const url = URL.createObjectURL(new Blob([JSON.stringify(latest.current, null, 2)], { type: "application/json" }));
    const link = document.createElement("a"); link.href = url; link.download = "aptimizer-unsaved-draft.json"; link.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  };
  const reloadServer = async () => {
    if (!window.confirm("Replace local edits with the server version? Export your draft first if you need to keep them.")) return;
    try {
      const { data } = await api.get(`/projects/${projectId}`);
      dirty.current = 0; saveBlocked.current = false; savedSnapshot.current = data; latest.current = data;
      setProject(data); setSaveState("saved"); setSaveMessage("");
    } catch (e) { toast.error(apiError(e.response?.data?.detail)); }
  };

  const readOnly = accessRole === "viewer";
  const Current = useMemo(() => (MODULES.find((m) => m[0] === active) || MODULES[0])?.[3], [active]);

  const [paletteOpen, setPaletteOpen] = useState(false);
  const [aptOpen, setAptOpen] = useState(false);

  useEffect(() => {
    const onKey = (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        setPaletteOpen((v) => !v);
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  if (!project)
    return (
      <div className="min-h-screen bg-slate-50">
        <TopBar />
        <div className="p-10 text-sm text-slate-500" data-testid="workspace-loading">
          {loadError ? <div role="alert" data-testid="workspace-load-error">{loadError}<Button className="ml-4" onClick={() => window.location.reload()} data-testid="workspace-load-retry">Retry</Button></div> : "Loading project…"}
        </div>
      </div>
    );

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col overflow-x-hidden">
      <TopBar>
        <div className="flex items-center gap-3 min-w-0">
          <div className="min-w-0">
            <div className="text-sm font-semibold tracking-tight truncate" data-testid="workspace-project-name">
              {project.name}
            </div>
            <div className="text-[11px] text-slate-500 truncate">
              {project.client || "—"} · {project.location || "—"} · {project.plot_reference || "—"}
            </div>
          </div>
          <span
            className={`text-[10px] font-mono uppercase px-1.5 py-0.5 rounded-sm ${
              saveState === "saved"
                ? "bg-emerald-50 text-emerald-700"
                : saveState === "saving"
                ? "bg-amber-50 text-amber-700"
                : "bg-red-50 text-red-700"
            }`}
            data-testid="save-indicator"
            title={saveState === "error"
              ? "Not saved. Check the error below."
              : saveState === "conflict" ? "Saving paused — a newer revision exists."
              : saveState === "saving" ? "Saving…" : "All changes saved"}
          >
            {saveState === "error" ? "not saved" : saveState}
          </span>
          <span className="text-[10px] font-mono uppercase px-1.5 py-0.5 rounded-sm bg-slate-100" data-testid="access-role-badge">
            {accessRole}
          </span>
        </div>
      </TopBar>

      <ProjectNav
        groups={GROUPS}
        active={active}
        onPick={setActive}
        onOpenPalette={() => setPaletteOpen(true)}
      />

      {saveMessage && <div role="alert" className="border-b border-red-200 bg-red-50 px-4 py-3 text-sm text-red-900" data-testid="workspace-save-warning">
        <p>{saveMessage}</p><div className="mt-2 flex flex-wrap gap-2"><Button size="sm" variant="outline" onClick={exportDraft} data-testid="workspace-export-draft">Export local draft</Button>
        {saveState === "conflict" && <Button size="sm" variant="outline" onClick={reloadServer} data-testid="workspace-load-server">Load server version</Button>}</div>
      </div>}
      {analysisState !== "fresh" && <div role="status" className={`border-b px-4 py-2 text-xs ${analysisState === "stale" ? "bg-amber-50 text-amber-900" : "bg-blue-50 text-blue-800"}`} data-testid="workspace-analysis-status">
        {analysisState === "stale" ? `Results are out of date. ${analysisError || "Recalculation failed."} Correct invalid inputs before relying on these figures.` : "Recalculating… displayed results may reflect earlier inputs."}
      </div>}

      <div className="flex flex-1 min-h-0">
        <aside
          className="w-56 shrink-0 bg-white border-r border-slate-200 hidden md:block"
          data-testid="metrics-panel"
        >
          <MetricsStrip analysis={analysis} duration={duration} vertical
                        state={analysisState} at={analysedAt} />
        </aside>

        <main className="flex-1 min-w-0 p-4 md:p-6 space-y-4" data-testid={`module-panel-${active}`}>
          <CalculationNotice basis={analysis?.calculation_basis} onReview={() => setActive("data-health")} />
          {Current && (
            <ErrorBoundary compact key={active} title={`Error in ${active} module`}>
              <Suspense fallback={<ModuleLoading />}>
                <Current
                  project={project}
                  analysis={analysis}
                  update={update}
                  readOnly={readOnly}
                  projectId={projectId}
                  setProject={setProject}
                  goToModule={setActive}
                />
              </Suspense>
            </ErrorBoundary>
          )}
        </main>
      </div>

      {/* Apt sits on the workspace chrome rather than in a tab: "why is this number what
          it is" gets asked from whichever tab is showing the number. Floating bottom-right
          because that is where an assistant is looked for, and nothing can compress it. */}
      {!aptOpen && (
        <button
          onClick={() => setAptOpen(true)}
          title="Ask Apt about this project"
          data-testid="apt-trigger"
          className="fixed bottom-5 right-5 z-40 flex items-center gap-2 rounded-full bg-[#F4C2C2] hover:bg-[#EBACAC] text-[#6B2233] shadow-lg shadow-[#F4C2C2]/50 pl-3.5 pr-4 py-2.5 text-sm font-medium transition-colors"
        >
          <Sparkles className="h-4 w-4" />
          Ask Apt
        </button>
      )}

      <AptPanel open={aptOpen} onOpenChange={setAptOpen} projectId={projectId} module={active} />

      <CommandPalette
        open={paletteOpen}
        onClose={() => setPaletteOpen(false)}
        modules={MODULES}
        groupLabel={(key) => GROUP_LABEL[GROUP_OF[key]] || ""}
        onPick={setActive}
        active={active}
      />
    </div>
  );
}
