import { useMemo, useState } from "react";
import { Search, X, ArrowUpRight } from "lucide-react";
import { WORKSPACE_CATALOG, WORKSPACE_MODULES, PARAMETER_COUNT } from "../../lib/workspaceCatalog";
import { Input } from "../ui/input";
import { Button } from "../ui/button";

export const ParameterDirectory = () => {
  const [query, setQuery] = useState("");
  const [group, setGroup] = useState("all");
  const [kind, setKind] = useState("all");
  const results = useMemo(() => WORKSPACE_CATALOG.filter(g => group === "all" || g.id === group).flatMap(g => g.modules.map(m => ({ ...m, group: g.label, parameters: m.parameters.filter(p =>
    (kind === "all" || p.kind === kind) && `${m.name} ${p.name} ${p.unit} ${p.basis}`.toLowerCase().includes(query.trim().toLowerCase())
  ) })).filter(m => m.parameters.length)), [query, group, kind]);
  const count = results.reduce((n, m) => n + m.parameters.length, 0);
  const reset = () => { setQuery(""); setGroup("all"); setKind("all"); };
  return <section id="parameters" className="landing-section bg-white scroll-mt-20" data-testid="landing-parameters">
    <div className="landing-container">
      <div className="flex flex-wrap items-end justify-between gap-6">
        <div><p className="landing-eyebrow">02 / Inside the workspace</p>
          <h2 className="landing-title">The parameters behind the project.</h2>
          <p className="mt-3 max-w-2xl text-sm leading-relaxed text-slate-600">{WORKSPACE_MODULES.length} connected modules. Inputs, calculated values and estimates—clearly distinguished.</p></div>
        <span className="font-mono text-xs text-slate-500" data-testid="parameter-directory-total">{PARAMETER_COUNT} parameter groups</span>
      </div>
      <div className="mt-8 grid gap-3 sm:grid-cols-[1fr_180px]">
        <div className="relative"><Search className="absolute left-3 top-3 h-4 w-4 text-slate-400" />
          <Input aria-label="Search parameters" data-testid="parameter-search" placeholder="Search parameters, units or codes…" value={query} onChange={e => setQuery(e.target.value)} className="h-11 pl-10 pr-10 bg-slate-50" />
          {query && <button onClick={() => setQuery("")} aria-label="Clear search" data-testid="parameter-search-clear" className="absolute right-2 top-2 p-1.5 text-slate-500 hover:text-blue-700"><X size={16} /></button>}
        </div>
        <select value={kind} onChange={e => setKind(e.target.value)} aria-label="Parameter type" data-testid="parameter-type-filter" className="h-11 rounded-md border bg-white px-3 text-sm focus:ring-2 focus:ring-blue-600">
          <option value="all">All parameter types</option>{["Input", "Calculated", "Estimate"].map(t => <option key={t}>{t}</option>)}
        </select>
      </div>
      <div className="mt-4 flex flex-wrap gap-2" aria-label="Module groups">
        {[{ id: "all", label: "All modules" }, ...WORKSPACE_CATALOG].map(g => <button key={g.id} onClick={() => setGroup(g.id)} aria-pressed={group === g.id} data-testid={`parameter-group-${g.id}`}
          className={`rounded-md border px-3 py-2 text-xs font-medium transition-colors ${group === g.id ? "border-blue-600 bg-blue-600 text-white" : "border-slate-200 text-slate-600 hover:border-blue-400 hover:text-blue-700"}`}>{g.label}</button>)}
      </div>
      <div className="my-6 flex flex-wrap items-center justify-between gap-2 border-b pb-4">
        <p aria-live="polite" className="font-mono text-xs text-slate-500" data-testid="parameter-result-count">{count} parameter groups · {results.length} modules</p>
        {(query || group !== "all" || kind !== "all") && <Button variant="ghost" size="sm" onClick={reset} data-testid="parameter-reset">Reset filters <X size={14} className="ml-2" /></Button>}
      </div>
      {results.length ? <div className="grid gap-x-12 gap-y-8 md:grid-cols-2 xl:grid-cols-3">
        {results.map(m => <article key={m.id} className="min-w-0 border-b pb-6" data-testid={`parameter-module-${m.id}`}>
          <div className="flex items-start gap-3"><m.icon size={19} className="mt-0.5 shrink-0 text-blue-600" /><div><h3 className="text-sm font-semibold text-slate-900">{m.name}</h3><p className="mt-1 text-xs leading-relaxed text-slate-500">{m.note}</p></div></div>
          <ul className="mt-4 space-y-2">{m.parameters.map(p => <li key={p.name}>
            <details className="parameter-detail" data-testid={`parameter-detail-${m.id}-${p.name.toLowerCase().replace(/[^a-z0-9]+/g, "-")}`}>
              <summary className="flex cursor-pointer items-start justify-between gap-3 rounded-sm py-2 text-sm focus-visible:outline-blue-600" data-testid={`parameter-toggle-${m.id}-${p.name.toLowerCase().replace(/[^a-z0-9]+/g, "-")}`}>
                <span className="min-w-0">{p.name}<span className="mt-1 block font-mono text-[10px] text-slate-500">{p.unit}</span></span>
                <span className={`mt-0.5 shrink-0 rounded-sm px-1.5 py-0.5 text-[9px] font-medium ${p.kind === "Input" ? "bg-blue-50 text-blue-700" : p.kind === "Calculated" ? "bg-emerald-50 text-emerald-800" : "bg-amber-50 text-amber-800"}`}>{p.kind}</span>
              </summary><p className="border-l-2 border-blue-200 pl-3 pb-2 text-xs leading-relaxed text-slate-600">{p.basis}</p>
            </details>
          </li>)}</ul>
        </article>)}
      </div> : <div className="py-14 text-center" data-testid="parameter-empty-state"><Search className="mx-auto text-slate-300" size={28} /><h3 className="mt-4 text-sm font-medium">No matching parameters</h3><Button variant="link" onClick={reset} data-testid="parameter-empty-reset">Show all parameters <ArrowUpRight size={14} className="ml-1" /></Button></div>}
      <p className="mt-8 text-xs leading-relaxed text-slate-500" data-testid="parameter-directory-disclaimer">A curated index of the current workspace. Reference data, generated concepts and estimates require project-specific verification.</p>
    </div>
  </section>;
};