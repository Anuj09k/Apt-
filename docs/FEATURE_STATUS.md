# Feature status corrections (2026-10-07 audit)

The feature list PDF marks 417 of 424 features "built". After the audit fixes, this is what
each disputed feature actually does, so the next PDF can state it accurately.

## Now computed from the project (were fixed sample values before)

| Feature | Source of the numbers now |
|---|---|
| Delay Prediction | Seeded Monte Carlo over the project's CPM programme (P50/P80/P90, driving activities) |
| 4D Progress / EVM | PV from the cost-loaded programme; EV/AC/SPI/CPI only when progress and actual cost are recorded in `site_data` |
| Engineering Benchmarking | The project's take-off, circulation and cost against typical ranges (no unsourced "CPWD" figures) |
| Autonomous BOQ & Costing | The BOQ module's own bill |
| Multi-Agent Engineering Teams | Engine, Engineering and Compliance results; verdicts follow from checks |
| Autonomous Compliance Checking | The engine's compliance rules plus setback and height-to-road checks |
| One-Click Project Generation | Towers now carry engine fields; metrics come from the engine |
| Procurement Calendar, Inventory Planning | Programme activities and take-off quantities |
| Tender Document Generator | BOQ total and programme duration |
| Government Approval Assistant | Readiness checked against the project's data and documents |
| Engineering Memory, Decision Log | The project's activity log, hash-chained |
| Decision Sandbox | Re-runs the engine on a modified copy of the project |
| Utility Network Optimisation, Infrastructure Demand Forecasting | Utilities module, external network design, project occupancy |
| Green Building Planner / Scorecard | Engineering module's GRIHA / IGBC checklist |
| ESG Reporting, Lifecycle Cost, Executive Dashboards | Engineering carbon, BOQ, Finance and Compliance results |
| Equipment Scheduling | BOQ quantities and programme duration |
| Approval certificates | HMAC-SHA256 signed; `GET /projects/{id}/approvals/{aid}/verify` |

## Still sample or reference data, now labelled as such

| Feature | Status to show |
|---|---|
| IoT Readiness, Smart Sensor Integration, Quality & Safety Monitoring, Predictive Maintenance, Facility Management | Partial: computes from `site_data` records; shows labelled sample data until records or sensors are connected (no ingestion pipeline yet) |
| Live Material Prices | Partial: maintained reference price table, not a live feed |
| Material Price Forecasting | Partial: seasonal + inflation model, not a market forecast |
| Supplier Intelligence | Partial: vendor register; anonymous sample rows until vendors are entered |
| Engineering / Plugin / API Marketplace | Partial: catalogue of real exports; STAAD/ETABS and P6 exchange are planned |
| Urban Digital Twin microclimate, Land Value Prediction, City Growth Prediction | Partial: indicative; needs land cost / external datasets |
| DWG Export | Built when the ODA File Converter is installed on the server; otherwise DXF is served (AutoCAD opens DXF) |

## Corrected figures

- Clause registry: 66 curated entries (the PDF says 74), plus whatever code corpus is indexed.
