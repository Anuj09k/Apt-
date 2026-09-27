import { useRef, useState } from "react";
import { Link } from "react-router-dom";
import { motion, useMotionValueEvent, useReducedMotion, useScroll, useSpring } from "framer-motion";
import { ArrowRight, ArrowDown, ArrowUpRight, Menu, X, Check, Compass, Ruler, Layers, ShieldCheck, BookOpen, AlertTriangle } from "lucide-react";
import { Brand } from "../components/Brand";
import { ScrollScene } from "../components/ScrollScene";
import { useAuth } from "../context/AuthContext";
import { Reveal, RevealItem, Stagger } from "../components/landing/Reveal";
import ReactiveButton from "../components/landing/ReactiveButton";
import { ParameterDirectory } from "../components/landing/ParameterDirectory";
import { WORKSPACE_CATALOG, WORKSPACE_MODULES, PARAMETER_COUNT } from "../lib/workspaceCatalog";
import "./Landing.css";

const NAV = [["Workspace", "workspace"], ["Parameters", "parameters"], ["Pipeline", "pipeline"], ["Assurance", "intelligence"]];
const PIPELINE = [
  ["Boundary", "Validate the plot polygon and establish the site geometry."],
  ["Envelope", "Apply front, rear and side setbacks to the buildable area."],
  ["Circulation", "Reserve the fire-tender route and internal access roads."],
  ["Amenities", "Allocate the clubhouse, open space and shared facilities."],
  ["Tower placement", "Explore footprints, orientation, floor counts and unit yield."],
  ["Evaluation", "Check containment, spacing and supported project constraints."],
];
const CODES = [
  ["Structural loads", "IS 875 Parts 1–3"], ["Seismic actions", "IS 1893 (Part 1)"],
  ["Concrete structures", "IS 456"], ["Foundation references", "IS 6403 / IS 1904"],
  ["Concrete mix design", "IS 10262"], ["Water demand", "IS 1172"],
  ["Fire & life safety", "NBC 2016 Part 4"], ["Accessibility", "NBC Part 3 / RPwD"],
  ["Green assessment", "GRIHA / IGBC"],
];

export default function Landing() {
  const { user } = useAuth();
  const hero = useRef(null);
  const reduced = useReducedMotion();
  const [menu, setMenu] = useState(false);
  const [solid, setSolid] = useState(false);
  const { scrollYProgress, scrollY } = useScroll();
  const progress = useSpring(scrollYProgress, { stiffness: 180, damping: 32 });
  // The ref must be measured in its owning component, after its DOM has committed.
  const { scrollYProgress: heroProgress } = useScroll({ target: hero, offset: ["start 64px", "end end"] });
  const sceneProgress = useSpring(heroProgress, { stiffness: 260, damping: 24, mass: 0.25, restDelta: 0.0001 });
  useMotionValueEvent(scrollY, "change", value => setSolid(previous => previous === (value > 20) ? previous : value > 20));
  const href = user ? "/projects" : "/register";
  const cta = user ? "Open workspace" : "Start a project";

  return <div className="landing-page" data-testid="landing-page">
    <a href="#workspace" className="landing-skip" data-testid="landing-skip-content">Skip to workspace overview</a>
    <motion.div aria-hidden="true" className="fixed inset-x-0 top-0 z-50 h-0.5 origin-left bg-blue-600" style={{ scaleX: reduced ? scrollYProgress : progress }} data-testid="landing-scroll-progress" />
    <header className={`landing-nav ${solid ? "landing-nav-solid" : ""}`} data-testid="landing-nav">
      <div className="landing-container flex h-16 items-center justify-between gap-3">
        <Link to="/" aria-label="Aptimizer home" data-testid="landing-nav-brand"><Brand testid="landing-nav-brand-lockup" markClass="h-8 w-auto" wordClass="text-lg" /></Link>
        <nav className="hidden items-center gap-7 lg:flex" aria-label="Main navigation">{NAV.map(([name, id]) => <a key={id} href={`#${id}`} data-testid={`landing-nav-${id}`} className="landing-nav-link">{name}</a>)}</nav>
        <div className="flex items-center gap-2">
          {!user && <Link to="/login" className="landing-nav-link hidden sm:block mr-3" data-testid="landing-nav-sign-in">Sign in</Link>}
          <ReactiveButton as={Link} to={href} size="sm" icon={<ArrowUpRight size={15} />} className="!px-3" data-testid="landing-nav-primary-cta">{cta}</ReactiveButton>
          <button className="p-2 lg:hidden text-slate-600" aria-label={menu ? "Close navigation" : "Open navigation"} aria-expanded={menu} aria-controls="landing-mobile-nav" onClick={() => setMenu(!menu)} data-testid="landing-menu-toggle">{menu ? <X size={20} /> : <Menu size={20} />}</button>
        </div>
      </div>
      {menu && <nav id="landing-mobile-nav" className="landing-container grid gap-1 border-t py-4 lg:hidden" aria-label="Mobile navigation" data-testid="landing-mobile-nav">{[...NAV, ...(!user ? [["Sign in", "/login"]] : [])].map(([name, id]) => <a key={id} href={id.startsWith("/") ? id : `#${id}`} onClick={() => setMenu(false)} data-testid={`landing-mobile-${id.replace("/", "")}`} className="py-2 text-sm text-slate-700">{name}</a>)}</nav>}
    </header>

    <main>
      <section ref={hero} className={`landing-hero ${reduced ? "landing-hero-static" : ""}`} data-testid="landing-hero">
        <div className="landing-stage">
          <ScrollScene progress={sceneProgress} className="landing-scene-media" />
          <div className="landing-hero-heading landing-container">
            <p className="landing-eyebrow">Aptimizer / Built for Indian engineering</p>
            <h1 data-testid="landing-heading">From the first line.<br /><span>To the bigger picture.</span></h1>
          </div>
          <div className="landing-hero-bottom landing-container">
            <p className="max-w-xs text-xs leading-relaxed text-slate-700">Site. Structure. Cost. One connected project.</p>
            <a href="#workspace" data-testid="landing-explore" className="flex items-center gap-3 text-xs font-medium text-slate-800">Explore Aptimizer <ArrowDown size={16} /></a>
          </div>
        </div>
      </section>

      <section id="workspace" className="landing-section landing-overview scroll-mt-16" data-testid="landing-workspace">
        <div className="landing-container">
          <div className="grid items-end gap-10 lg:grid-cols-[1.2fr_1fr]">
            <Reveal><p className="landing-eyebrow">01 / The connected workspace</p><h2 className="landing-display">Plan with context.<br /><span className="text-blue-600">Build with confidence.</span></h2></Reveal>
            <Reveal delay={0.06}><p className="text-sm leading-relaxed text-slate-600">Carry a project from its site boundary through apartment planning, preliminary engineering, quantities, programme and feasibility. A shared project model keeps the work connected.</p>
              <ReactiveButton as={Link} to={href} icon={<ArrowRight size={16} />} className="mt-6" data-testid="landing-hero-primary-cta">{cta}</ReactiveButton></Reveal>
          </div>
          <div className="landing-statline" data-testid="landing-metrics">
            {[[WORKSPACE_MODULES.length, "workspace modules"], [PARAMETER_COUNT, "parameter groups"], [6, "layout stages"], ["INR", "project costing"]].map(([value, label], i) => <div key={label} data-testid={`landing-metric-${i}`}><strong>{value}</strong><span>{label}</span></div>)}
          </div>
          <Stagger className="grid gap-7 sm:grid-cols-2 lg:grid-cols-5" step={0.04}>
            {WORKSPACE_CATALOG.map((g, i) => <RevealItem key={g.id} className="min-w-0" data-testid={`landing-workspace-group-${g.id}`}>
              <div className="flex items-center justify-between border-t border-slate-300 pt-4"><g.icon size={19} className="text-blue-600" /><span className="font-mono text-[10px] text-slate-400">0{i + 1}</span></div>
              <h3 className="mt-4 text-sm font-semibold">{g.label}</h3>
              <ul className="mt-3 space-y-2">{g.modules.map(m => <li key={m.id} className="text-xs leading-relaxed text-slate-500">{m.name}</li>)}</ul>
            </RevealItem>)}
          </Stagger>
        </div>
      </section>

      <ParameterDirectory />

      <section id="pipeline" className="landing-section landing-pipeline scroll-mt-16" data-testid="landing-pipeline">
        <div className="landing-container"><Reveal><p className="landing-eyebrow">03 / The layout pipeline</p><h2 className="landing-title">From boundary to a considered scheme.</h2></Reveal>
          <Stagger className="mt-10 grid gap-x-12 gap-y-8 sm:grid-cols-2 lg:grid-cols-3" step={0.05}>{PIPELINE.map(([name, body], i) => <RevealItem key={name} data-testid={`landing-pipeline-step-${i}`}>
            <div className="border-t border-slate-300 pt-5"><span className="font-mono text-xs text-blue-600">0{i + 1}</span><h3 className="mt-4 text-base font-semibold">{name}</h3><p className="mt-2 max-w-xs text-sm leading-relaxed text-slate-600">{body}</p></div>
          </RevealItem>)}</Stagger>
        </div>
      </section>

      <section id="modules" className="landing-section bg-white scroll-mt-16" data-testid="landing-modules">
        <div className="landing-container grid gap-10 lg:grid-cols-[0.8fr_1.2fr]">
          <Reveal><p className="landing-eyebrow">04 / Engineering references</p><h2 className="landing-title">A reference behind the check.</h2><p className="mt-4 max-w-sm text-sm leading-relaxed text-slate-600">Supported checks reference Indian standards and local controls. Confirm the applicable edition, amendments and project-specific requirements with your engineer.</p><BookOpen className="mt-8 text-blue-600" size={30} /></Reveal>
          <div>{CODES.map(([name, code], i) => <div key={name} data-testid={`landing-code-${i}`} className="flex flex-wrap items-baseline justify-between gap-x-4 gap-y-1 border-b border-slate-200 py-3.5"><span className="text-sm text-slate-700">{name}</span><span className="font-mono text-xs text-blue-700">{code}</span></div>)}</div>
        </div>
      </section>

      <section id="intelligence" className="landing-section landing-assurance scroll-mt-16" data-testid="landing-intelligence">
        <div className="landing-container">
          <Reveal><p className="landing-eyebrow">05 / Engineering, with accountability</p><h2 className="landing-title">Know the basis. Not just the number.</h2></Reveal>
          <div className="mt-10 grid gap-12 lg:grid-cols-[1fr_0.85fr]">
            <div className="space-y-7">{[
              [Compass, "Inputs stay visible", "Site geometry, material properties, rates and project controls remain distinct from computed outputs."],
              [Ruler, "Arithmetic you can follow", "Area and FAR derivations show their inputs and formulas. Core calculations preserve precision before display formatting."],
              [Layers, "Estimates are identified", "Default rates, empirical service-core areas, soil references and forecasts are assumptions—not field measurements."],
              [ShieldCheck, "Review is part of the workflow", "Stale calculations and save conflicts are surfaced. AI explanations depend on configured services; they do not replace engineering approval."],
            ].map(([Icon, title, text], i) => <div key={title} className="flex gap-4" data-testid={`landing-assurance-${i}`}><Icon size={19} className="mt-1 shrink-0 text-blue-600" /><div><h3 className="text-sm font-semibold">{title}</h3><p className="mt-2 text-sm leading-relaxed text-slate-600">{text}</p></div></div>)}</div>
            <div>
              <div className="rounded-md border border-slate-300 bg-white" data-testid="landing-calculation-example"><div className="flex flex-wrap items-center justify-between gap-2 border-b px-5 py-4"><span className="text-sm font-medium">Permitted built-up area</span><span className="font-mono text-[10px] text-slate-500">ILLUSTRATIVE EXAMPLE</span></div>
                <dl className="px-5 py-2">{[["Plot area", "4,000.00 m²"], ["Configured FAR", "2.50"], ["Basis", "Plot area × FAR"]].map(([label, value]) => <div key={label} className="flex flex-wrap justify-between gap-2 py-3 text-sm"><dt className="text-slate-500">{label}</dt><dd className="font-mono text-xs">{value}</dd></div>)}</dl>
                <div className="flex items-center justify-between gap-3 border-t bg-blue-50 px-5 py-5"><span className="flex items-center gap-2 text-xs text-blue-800"><Check size={15} /> Result</span><strong className="font-mono text-xl text-blue-700" data-testid="landing-example-result">10,000.00 m²</strong></div>
              </div>
              <p className="mt-5 flex items-start gap-2 text-xs leading-relaxed text-slate-600" data-testid="landing-engineering-disclaimer"><AlertTriangle size={16} className="mt-0.5 shrink-0 text-amber-600" />Preliminary planning and decision support. Not a certified structural solver, survey, or statutory approval. Qualified review is required before construction.</p>
            </div>
          </div>
        </div>
      </section>
      <section className="landing-section bg-[#11231f] text-white" data-testid="landing-cta"><div className="landing-container flex flex-wrap items-center justify-between gap-8"><div><p className="font-mono text-xs text-emerald-300">YOUR NEXT PROJECT</p><h2 className="mt-4 text-lg font-semibold">Start with the site. Keep the whole picture.</h2></div><ReactiveButton as={Link} to={href} size="lg" icon={<ArrowUpRight size={18} />} data-testid="landing-cta-primary">{cta}</ReactiveButton></div></section>
    </main>
    <footer className="border-t bg-white py-8" data-testid="landing-footer"><div className="landing-container flex flex-wrap items-center justify-between gap-6"><Brand testid="landing-footer-brand-lockup" markClass="h-7 w-auto" wordClass="text-base" /><p className="text-xs text-slate-500">Civil engineering & real-estate planning · Indian codes · INR</p><a href="#parameters" className="landing-nav-link" data-testid="landing-footer-parameters">Parameter directory <ArrowUpRight className="inline ml-1" size={13} /></a></div></footer>
  </div>;
}