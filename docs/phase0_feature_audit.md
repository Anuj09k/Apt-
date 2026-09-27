# Phase 0 audit — feature claims vs what the code actually does today

Source of truth for this audit: the backend modules under `backend/` plus the routes
registered in `server.py` and their tests under `tests/`. The feature list at
`structured_features.json` / `feature_data.py` is what it is auditing.

Current JSON claim: **424 features, 417 built, 1 partial, 6 planned.**

This doc records the honest status of the highest-claim "upper layer" modules — the ones
where the feature-list label is most likely to be ahead of the code.

---

## How to read the table

- **Real and tested** — there is a real computation, it is wired behind a route, and the
  module's own test file exercises it (42 tests, 9.44s, green, across the six audited modules).
- **Real but placeholder-ish** — the function exists and returns a shaped response, but the
  numbers are illustrative defaults rather than something derived from a live feed or a real
  external system.
- **Skeleton / mostly label** — a module or endpoint exists, but the feature is largely a
  structured demo response; the backend does not actually do the claimed thing in any depth.
- **Only-claimed** — the feature list marks it built, but there is no matching backend
  computation of the kind the label implies.

---

## Audited modules

### BIM & CAD interoperability (`backend/bim.py`)

Status in feature list: built (IFC export, DWG export, DXF export, Revit compatibility, AutoCAD compatibility).

Real backend today:

- DXF import — `inspect_dxf()` and `import_boundary()` read a DXF, inventory layers, and extract
  the largest closed ring on a chosen layer as the plot boundary, with a real `ezdxf.recover`
  reader and a sketched auditor report. Coordinates are projected onto the same local frame the
  layout engine uses.
- DXF export — `export_siteplan_dxf()` writes a layered R2018 ASCII drawing (boundary, tower
  footprints with labels, parking bays).
- DWG export — `export_siteplan_dwg()` currently returns the same bytes as the DXF export. The
  function exists and is wired, but it is not a separate DWG writer today.
- IFC4 export — `export_ifc4()` builds a real georeferenced IFC4 model via `ifcopenshell`:
  IfcProject, IfcSite with RefLatitude/RefLongitude, one IfcBuilding per tower, an
  IfcBuildingStorey per floor with a slab mass, boundary as IfcGeographicElement.
- Pre-download summaries — `dxf_summary()` and `ifc_summary()` give the "what you are about to
  download" card.

Verdict:

- **Real and tested** for DXF in, DXF out, and IFC4 out. This is the strongest of the six modules
  audited.
- **Real but placeholder-ish** for DWG: the endpoint exists and returns bytes, but today it is the
  DXF stream, not a native DWG writer. The "DWG compatibility" claim is therefore more "we export
  a DXF that a DWG-capable reader can open" than "we write DWG".
- **Real and tested** for Revit compatibility in the IFC sense — Revit can Link IFC and the model
  carries the georeferencing and spatial hierarchy the claim implies. That is a fair "compatibility"
  claim if scoped to IFC Link, less fair if it implies native RVT round-tripping.

 reclassification suggestion:

- IFC export → keep built.
- DXF export → keep built.
- DXF import → keep built.
- DWG export → reclassify to "partial" unless a real DWG writer is added, and scope the label to
  "DXF/DWG-compatible ASCII export", not "native DWG".
- Revit/AutoCAD compatibility → keep built only if scoped explicitly to "opens in Revit via IFC Link
  and in any DXF reader", not as full native interchange.

---

### Digital Twin & Smart Construction (`backend/digital_twin.py`)

Status in feature list: built (IoT readiness, smart sensor integration, progress tracking, quality
monitoring, safety monitoring, delay prediction, predictive maintenance, facility management).

Real backend today: six functions, all returning shaped responses, all tested.

- IoT readiness — `iot_registry()` returns a fixed 5-device inventory with types, models, battery,
  status, telemetry param, gateway status, polling interval. It is a sample registry, not a device
  inventory that comes from the project or from real devices.
- Smart sensor telemetry — `sensor_telemetry()` returns hardcoded current values: concrete maturity
  with an Arrhenius-flavoured strength estimate and a formwork-stripping advisory, environmental
  telemetry, structural health telemetry. The maturity/strength logic is a single illustrative
  calculation, not a real time series.
- 4D progress tracking — `track_progress_4d()` returns EVM numbers (PV/EV/AC, SPI, CPI) and a
  floor-by-floor status table. The EVM numbers are illustrative constants; the floor status is a
  deterministic pattern from floor count.
- Quality & safety — `quality_safety_audit()` returns hardcoded cube tests, defects, and safety
  stats, plus a safety risk index string.
- Delay prediction — `predict_delays()` returns a Monte-Carlo-flavoured answer with a fixed
  baseline/predicted date, on-time probability, 1000 iterations claim, and three risk factors.
  There is no actual simulation; the numbers are a single canned scenario.
- Facility management — `facility_management()` returns a fixed 4-asset register with operating
  hours, health score, vibration, next service due, preventive maintenance calendar.

Verdict:

- **Real but placeholder-ish throughout.** Every function returns a well-shaped, plausible,
  nicely-cited answer, but none of them is derived from real sensor telemetry, a real schedule
  baseline, a real asset register, or a real Monte-Carlo run. The module is a credible demo surface,
  not an operational digital twin.
- The "delay prediction" label is the furthest from the code: `predict_delays()` says "Monte Carlo"
  and "1000 iterations" but is a single canned return. That is the clearest over-claim in the module.
- The "smart sensor integration" label is fair only if scoped to "simulated telemetry shape with an
  Arrhenius maturity advisory", not to actual sensor integration.

reclassification suggestion:

- IoT readiness → partial (device schema + sample inventory, no real device/project integration).
- Smart sensor integration → partial (illustrative telemetry + one maturity calculation; not live
  sensors).
- 4D progress tracking → partial (EVM shape + floor status pattern; not tied to a real baseline or
  actuals).
- Quality & safety monitoring → partial (sample cube tests/defects/safety stats).
- Delay prediction → partial at best, and rename/refine away from the "Monte Carlo 1000 iterations"
  framing unless a real simulation is added.
- Predictive maintenance & facility management → partial (sample asset register + maintenance
  calendar; not a live BMS or degradation model).

---

### AI Civil Engineering Operating System (`backend/ai_os.py`)

Status in feature list: built (AI Engineering Copilot, AI Engineering Consultant, Engineering
Knowledge Graph, Engineering Memory, Engineering Decision Log, Explainable AI). The feature list
also puts "Explainable AI" here; the code does not have a separate explainable-AI engine — the
"explainability" is the shaped rationale/confidence fields in memory and decision log.

Real backend today:

- Knowledge graph — `build_knowledge_graph()` returns a fixed 13-node, 12-edge semantic graph
  (standards, project parameters, structural/spatial components) with a small metrics block. It is
  generated from constants, lightly informed by project tower/floor/area/dev-controls values for the
  labels. It is a knowledge graph in shape, not one built from the project's real computed state.
- Engineering memory — `get_engineering_memory()` returns four fixed episodic memory entries with
  timestamps, domains, rationales, and confidence scores. Again, shape is right; content is canned.
- Decision log — `audit_decision_log()` returns four fixed decisions with an SHA-256 audit hash over
  id+decision. The hash is real, the decisions are not.
- Decision sandbox / what-if simulator — `simulate_decision_sandbox()` is the most real function in
  the module: it takes overrides (floors, concrete grade, slab type, footprint scale), recomputes
  built-up, FAR, cost, quantities, carbon, and deltas against a baseline. This one actually computes
  something from inputs.
- Engineering benchmarking — `compare_benchmarks()` returns four benchmark comparisons with CPWD and
  industry p75 numbers. The project values are illustrative constants derived from tower/floor count,
  not from the project's real quantities or cost model.

Verdict:

- **Real and tested** for the decision sandbox — that one genuinely computes deltas from overrides.
- **Real but placeholder-ish** for knowledge graph, memory, decision log, and benchmarks: the
  structures are right and the tests pass, but the content is illustrative rather than derived from a
  real project state, real decisions, or a real benchmark source.
- "AI Engineering Copilot / Consultant / Explainable AI" are not separate runtime engines in this
  module — they are feature-list labels for the knowledge graph + memory + decision log + sandbox
  shape. That is a fair marketing stacking, but not five separate built engines.

reclassification suggestion:

- Engineering Knowledge Graph → partial (real graph shape, canned content, lightly project-aware).
- Engineering Memory → partial (real episodic shape, canned episodes).
- Engineering Decision Log → partial (real audit hash + decision shape, canned decisions).
- Explainable AI → partial at best; rename/refine to "decision rationale + confidence fields" rather
  than a separate explainability engine.
- Decision Sandbox / What-If Simulator → keep built; it computes.
- AI Engineering Copilot / Consultant → these are better treated as the APT layer + the sandbox, not
  as separate built engines in ai_os.py. Consider moving the label to "partial" until there is a
  real copilot/consultant flow that is more than a shaped demo.

---

### Smart City Platform (`backend/smart_city.py`)

Status in feature list: built (city-scale planning, traffic simulation, utility network optimisation,
urban digital twin, infrastructure demand forecasting).

Real backend today: five functions, all tested.

- City-scale planning — `city_scale_plan()` returns a land-use distribution, density guidelines, and
  urban-fabric metrics from project tower/area/params. The land-use split is a fixed percentage model;
  the "proposed density" uses tower count and a fixed 48 units/tower assumption.
- Traffic simulation — `simulate_traffic()` computes trip generation from units via ITE-flavoured
  rates, road capacity from lane count, a volume/capacity ratio, an LOS grade, delay and queue
  estimates, and a fire-tender turning check. This is the most computational of the five — it is a
  real parametric model, but it is a simple one, and the inputs (units per floor, road width) come
  from the project or from defaults.
- Utility network optimisation — `optimize_utility_network()` starts a real stormwater computation
  (Rational formula Q = C*I*A/360) and then continues into water network, sewerage, and electrical
  figures. The file was truncated in this audit at the water-network block, so the sewerage/electrical
  tail is inferred from the function signature and the test coverage rather than read verbatim.
- Urban digital twin — `urban_digital_twin()` returns spatial context, sun-path microclimate, and an
  Urban Heat Island index shape.
- Infrastructure demand forecasting — `forecast_infrastructure_demand()` returns multi-year civic
  demand projections for water, power, waste, and social infrastructure.

Verdict:

- **Real and tested** for the traffic simulation's parametric core (trip generation, capacity, LOS,
  fire-tender check). This is a real, if simple, model.
- **Real but placeholder-ish** for city-scale planning, utility network, urban twin, and infra demand:
  well-shaped, plausible, test-covered, but largely a fixed-model demo rather than a real city-scale
  analysis tied to a real urban dataset.
- "Smart City Platform" is a big label for five functions that are, at present, a credible parametric
 demo plus a few canned layers.

reclassification suggestion:

- City-scale planning → partial (real percentage model, fixed assumptions).
- Traffic simulation → keep built for the parametric LOS/turning model, but scope the claim to
  "parametric trip generation + LOS + fire-tender clearance", not a full traffic simulation.
- Utility network optimisation → partial (real Rational-formula stormwater head, rest illustrative).
- Urban digital twin → partial (spatial + microclimate shape, not a real urban twin).
- Infrastructure demand forecasting → partial (parametric projections, not a real forecast feed).

---

### Smart Procurement & Ecosystem (`backend/procurement_market.py`)

Status in feature list: built (live material prices, material price forecasting, supplier
intelligence, procurement calendar, inventory planning, engineering/plugin/API marketplace, tender
document generator, government approval assistant, educational mode).

Real backend today: nine functions, all tested.

- Live material prices — `get_live_material_prices()` returns a fixed per-metro price table in
  `METRO_PRICES`, plus a trend/volatility decoration and a "last updated" timestamp. This is a
  price table, not a live feed.
- Material price forecasting — `forecast_material_prices()` returns a 12-month seasonal+inflation
  projection series with bounds and a confidence decay. It is a real little model on top of a base
  price, but the base price is the same fixed table.
- Supplier intelligence — `get_supplier_intelligence()` returns five fixed Tier-1 suppliers with
  ratings, OTD, lead time, credit terms, certifications.
- Procurement calendar — `get_procurement_calendar()` returns a fixed set of JIT milestones aligned
  to CPM activity ids, scaled a little by floor count.
- Inventory planning — `calculate_inventory_plan()` computes EOQ-style reorder points and safety
  stock from a fixed per-m² consumption model and a project built-up estimate.
- Marketplace catalog — `get_marketplace_catalog()` returns fixed plugins and API descriptions and a
  developer portal URL.
- Tender document generator — `generate_tender_documents()` returns a NIT-style tender package header
  and section list from project name and built-up.
- Government approval assistant — `generate_government_approval_dossier()` exists (tested) and returns
  a dossier shape; this audit did not read its body in full, but it is in the same "shaped demo"
  family as the rest.
- Educational mode — `get_educational_mode_guide()` exists (tested) and returns a guide shape for a
  topic.

Verdict:

- **Real but placeholder-ish throughout.** Every function is a real, test-covered, well-shaped
  endpoint, but the "live" in "live material prices" is the clearest over-claim: there is no live
  price feed, just a fixed table with a "last updated" stamp and trend decorations. The marketplace,
  tender generator, government dossier, and educational mode are real endpoints that return real
  shapes, but they are generator/demo surfaces, not an actual marketplace, an actual live tender
  pack tied to a real BOQ, or a real approval submission pipeline.

reclassification suggestion:

- Live material prices → partial (real per-metro table, not a live feed). If the word "live" stays,
  scope it to "indexed price table updated manually", not "live market data".
- Material price forecasting → keep built as a parametric forecaster on top of the price table, but
  scope it honestly as a simple seasonal+inflation projection, not a commodity forecast.
- Supplier intelligence → partial (fixed supplier list; not live vendor intelligence).
- Procurement calendar → partial (fixed milestone shape, scaled by floors; not synced to a real CPM
  baseline).
- Inventory planning → partial (real EOQ-style math on fixed consumption assumptions).
- Marketplace, tender generator, government approval assistant, educational mode → partial each: real
  generator/demo endpoints, not an actual marketplace / live tender pack / live approval pipeline.

---

### Autonomous AI Engineering & Intelligent Planning (`backend/autonomous_planning.py`)

Status in feature list: built (conversational project design, multi-agent engineering teams,
autonomous compliance checking, autonomous BOQ & costing, AI township planner, mixed-use planning),
with AI negotiation with suppliers marked planned.

Real backend today: six functions, all tested.

- One-click generation — `one_click_generate()` is a real generator: it builds a plot, dev controls,
  towers, unit mix, parking, metrics, and a generation log from high-level params. This is the most
  real function in the module — it actually synthesizes a scheme shape.
- Conversational design — `conversational_design()` parses a handful of natural-language mutation
  patterns (floor changes, unit-mix share changes, EV slot adds, basement adds, setback changes) and
  applies them as atomic updates to a project shape. It is a real parser+applier for a small mutation
  vocabulary, with a fallback "no pattern matched" path.
- Multi-agent review — `multi_agent_review()` returns a 5-agent audit (architect, structural, MEP,
  QS/cost, compliance/safety) with scores, verdicts, findings, recommendations, and a consensus
  certificate hash. The agents are real in shape and they do look at the project's FAR, height, units,
  built-up, setbacks — but the verdicts, scores, and recommendations are generated from rules and
  canned text, not from a real multi-agent runtime.
- Autonomous compliance audit — `autonomous_compliance_audit()` runs a real set of NBC-flavoured
  checks (FAR, ground coverage, height-vs-road-width, front/rear setbacks, fire egress) with
  permissible/achieved/margin/remediation fields, computed from project values and
  `siteplan.devcontrols.setback_minimums()`. This is a real compliance checker in shape and in
  computation, though it is a small, fixed check set.
- Autonomous BOQ & costing — `autonomous_boq_engine()` computes a parametric takeoff (concrete, steel,
  shuttering, masonry, flooring, plaster, paint) from built-up with rates and amounts, then adds MEP,
  preliminaries, contingency, and a benchmark variance. This is a real parametric BOQ/cost model.
- Township & mixed-use planner — `township_mixed_use_plan()` returns a zoning distribution, sector
  breakdown, master-plan metrics, and circulation strategy from params/plot. It is a real zoning model
  on fixed percentage assumptions.

Verdict:

- **Real and tested** for one-click generation, conversational design (within its small mutation
  vocabulary), autonomous compliance audit (the check computation), and autonomous BOQ/costing (the
  parametric takeoff). These are the strongest parts of the module.
- **Real but placeholder-ish** for multi-agent review and township/mixed-use planning: real structures,
  real project-awareness, but canned agent verdicts/scores and fixed zoning percentages.
- "Autonomous compliance checking" is fairly earned for the check computation; "autonomous BOQ & costing"
  is fairly earned for the parametric takeoff; "conversational project design" is fairly earned for the
  parser/applier, with the caveat that the vocabulary is small.

reclassification suggestion:

- One-click project generation → keep built.
- Conversational project design → keep built within its current mutation vocabulary; note the vocab is
  small.
- Autonomous compliance checking → keep built for the current check set; scope to the rules it
  actually checks.
- Autonomous BOQ & costing → keep built for the parametric takeoff/cost model; scope to "parametric",
  since the rates are fixed assumptions.
- Multi-agent engineering teams → partial (real 5-agent shape and project-awareness, canned verdicts/
  scores/recommendations; not a real multi-agent runtime).
- AI township planner / mixed-use planning → partial for the same reason: real zoning model, fixed
  percentage assumptions, no real master-plan dataset.

---

## Summary table

| Module | Feature-list label | Honest status today | Note |
|---|---|---|---|
| bim.py | IFC/DWG/DXF export, Revit/AutoCAD compatibility | Mostly built; DWG is really DXF | DXF in/out + IFC4 out are real and tested; DWG endpoint returns DXF bytes |
| digital_twin.py | IoT, sensors, progress, quality, safety, delay prediction, predictive maintenance, facility mgmt | Real-but-placeholder across the board | Every function is a well-shaped demo; delay prediction still claims "Monte Carlo 1000 iterations" with no simulation |
| ai_os.py | AI copilot, consultant, knowledge graph, memory, decision log, explainable AI | Sandbox built; rest placeholder-ish | Decision sandbox computes; graph/memory/log/benchmarks are shaped canned content |
| smart_city.py | City-scale planning, traffic simulation, utility optimisation, urban twin, infra demand forecasting | Traffic core built; rest placeholder-ish | Trip gen/LOS/fire-tender is a real parametric model; the rest is a fixed-model demo |
| procurement_market.py | Live prices, forecasting, supplier intelligence, procurement calendar, inventory, marketplace, tender generator, govt dossier, educational mode | Real endpoints, placeholder content; "live" is the clearest over-claim | Price table is fixed, not live; marketplace is a catalog demo, not a marketplace |
| autonomous_planning.py | Conversational design, multi-agent teams, autonomous compliance, autonomous BOQ/costing, township/mixed-use planner | Strong core; multi-agent + township partial | One-click gen, conversational parser, compliance checks, parametric BOQ are real; multi-agent verdicts and zoning % are canned |

---

## What this means for the 417-built number

The six modules above carry a large chunk of the upper-layer "built" count. None of them is empty —
every one has real endpoints and passing tests — but several of the labels stacked on top of them are
ahead of the code:

- "Live material prices", "Monte Carlo delay prediction", "native DWG", "AI copilot/consultant as
  separate built engines", and "actual marketplace / live tender pack / live approval pipeline" are the
  clearest over-claims.
- The honest read is closer to: **a lot of well-engineered demo surfaces that are real in shape and
  partially real in computation**, not 417 fully shipped, production-hardened features.

Recommended single-source-of-truth action: keep `structured_features.json` / `feature_data.py` as the
index, but make its status labels match the table above, and stop regenerating decorative PDFs from the
unchanged claim count until the labels do.

---

Audited by: Phase 0 auto-run.
Test gate used: `cd backend && pytest tests/bim_test.py tests/digital_twin_test.py tests/ai_os_test.py tests/autonomous_planning_test.py tests/procurement_market_test.py tests/smart_city_test.py -q` — 42 passed, 9.44s.
