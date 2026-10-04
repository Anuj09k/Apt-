"""
Builds Group 6: Scenario Comparison, Collaboration & Workflow, Engineering Decision Support, BIM, Digital Twin, AI OS, Intelligent Planning, GIS Urban
"""

import json

GROUP_6 = {
    "Scenario Comparison": {
        "Compare Layouts": (
            "Side-by-Side Floor Plans",
            "Visually displays two or more architectural masterplans side-by-side to compare tower positioning, road layout, and circulation."
        ),
        "Compare Costs": (
            "Multi-Scheme Cost Contrast",
            "Contrasts capital expenditures, material takeoff quantities, and per-square-foot rates across competing design schemes."
        ),
        "Compare Parking": (
            "Parking Yield Showdown",
            "Evaluates how different basement and podium parking layouts compare in car count, efficiency ratio, and ramp complexity."
        ),
        "Compare Sustainability": (
            "Green Score Benchmark",
            "Compares embodied carbon footprints, water circularity percentages, and potential green ratings across alternative concepts."
        ),
        "Compare ROI": (
            "Profitability Showdown",
            "Compares Internal Rate of Return (IRR), Net Present Value (NPV), and payback timelines across different developer schemes."
        ),
    },
    "Collaboration & Workflow": {
        "Multi-user Collaboration": (
            "Live Multi-Seat Workspace",
            "Enables multiple team members (architects, civil engineers, quantity surveyors) to work simultaneously within the same project."
        ),
        "Project Sharing": (
            "Secure Permission Sharing",
            "Allows project owners to grant read-only, commenting, or full editing privileges to external consultants and partners."
        ),
        "Team Roles": (
            "Disciplinary Access Tiers",
            "Assigns specialized interface views and editing permissions tailored to specific team roles (e.g. Lead Architect, Cost Estimator)."
        ),
        "Version Control": (
            "Milestone Version Keeper",
            "Maintains a clean historical record of major design milestones, preventing accidental overwrites and lost work."
        ),
        "Activity Logs": (
            "Audit Trail Tracker",
            "Records an immutable chronological log of who altered which parameters, ran calculations, or exported reports."
        ),
        "Task Assignment": (
            "Engineering Task Manager",
            "Allows project leads to assign specific design tasks (e.g. 'Resolve Rear Setback Violation') with deadlines to team members."
        ),
        "Approval Workflow": (
            "Multi-Gate Sign-Off Chain",
            "Implements a formal multi-stage sign-off process requiring Lead Architect and Structural Engineer approval before plan finalization."
        ),
        "Comments & Reviews": (
            "On-Plan Markup Notes",
            "Enables team members to pin sticky comment notes and threaded review questions directly onto specific rooms, columns, or drawings."
        ),
        "Workflow Automation": (
            "Smart Event Triggers",
            "Automatically triggers downstream actions (such as re-running BOQ takeoff or alerting the cost engineer) when layouts change."
        ),
    },
    "Engineering Decision Support": {
        "Construction Timeline": (
            "Phased Delivery Timeline",
            "Simulates the duration of each construction phase (excavation, substructure, super-structure, MEP, finishes) to guide commitments."
        ),
        "Labour Planning": (
            "Trade Workforce Scheduler",
            "Forecasts daily and monthly labor headcounts needed across different trades to prevent on-site workforce bottlenecks."
        ),
        "Equipment Planning": (
            "Heavy Machinery Logistics",
            "Schedules the deployment and mobilization timing of critical equipment like tower cranes, concrete batching plants, and hoists."
        ),
        "Utility Network Planning": (
            "Site Infrastructure Spine",
            "Coordinates external stormwater, sewage, electrical, and telecom duct paths to prevent underground utility collisions."
        ),
    },
    "BIM Readiness": {
        "IFC Export": (
            "Open BIM Standard Export",
            "Exports standardized IFC4 (Industry Foundation Classes) 3D building models containing complete architectural and structural metadata."
        ),
        "DWG Export": (
            "Industry Standard CAD Export",
            "Exports native DWG format drawings compatible with AutoCAD and standard professional drafting suites."
        ),
        "DXF Export": (
            "Universal Vector CAD File",
            "Exports clean layered DXF vector drawings with dedicated layers for walls, dimensions, doors, and furniture."
        ),
        "Revit Compatibility": (
            "Direct Revit Import Bridge",
            "Ensures exported BIM geometry maps seamlessly into Autodesk Revit families, floors, walls, and structural columns."
        ),
        "AutoCAD Compatibility": (
            "AutoCAD Layer Mapping",
            "Maintains standard line weights, text styles, and layer names for seamless drafting workflows in AutoCAD."
        ),
    },
    "Digital Twin Preparation": {
        "IoT Readiness": (
            "Smart Sensor Architecture",
            "Establishes a digital data model ready to map incoming real-time IoT sensor telemetry from the physical building."
        ),
        "Smart Sensor Integration": (
            "Telemetry Stream Connector",
            "Provides endpoints to connect structural strain gauges, temperature sensors, energy meters, and water flow meters."
        ),
        "Progress Tracking": (
            "Planned vs Actual Monitor",
            "Compares as-built construction site progress against the master schedule to instantly flag schedule slippages."
        ),
        "Quality Monitoring": (
            "Quality Assurance Gate",
            "Logs inspection checklists, concrete cube test results, and non-conformance reports against specific building members."
        ),
        "Safety Monitoring": (
            "Jobsite Safety Inspector",
            "Tracks on-site safety incidents, hazardous zones, and required protective equipment compliance across the active worksite."
        ),
        "Delay Prediction": (
            "Schedule Slip Early Warning",
            "Uses predictive analytics to flag potential upcoming project delays weeks before they impact the critical path."
        ),
        "Predictive Maintenance": (
            "Equipment Health Watchdog",
            "Analyzes operational telemetry to forecast when elevators, water pumps, and DG backup generators require servicing."
        ),
        "Facility Management": (
            "Post-Handover Asset Guide",
            "Organizes operational warranties, equipment serial numbers, and maintenance schedules for building facility managers."
        ),
    },
    "AI Operating System": {
        "AI Engineering Copilot": (
            "Always-On Engineering Partner",
            "An autonomous AI assistant embedded across all workflows that suggests optimizations, catches errors, and accelerates tasks."
        ),
        "AI Engineering Consultant": (
            "Advisory Knowledge Hub",
            "Provides deep technical counsel on complex zoning codes, foundation engineering, and structural framing strategies."
        ),
        "Engineering Knowledge Graph": (
            "Connected Civil Knowledge Web",
            "A comprehensive semantic graph linking building codes, material behaviors, structural principles, and cost databases."
        ),
        "Engineering Memory": (
            "Long-Term Project Recall",
            "Remembers past design choices, client preferences, and past engineering calculations across the entire project lifecycle."
        ),
        "Engineering Decision Log": (
            "Decision Rationale Archive",
            "Maintains a clear historical log of why specific architectural or structural decisions were approved and by whom."
        ),
        "Explainable AI": (
            "Transparent Logic Window",
            "Explains the exact mathematical formulas, engineering codes, and logical assumptions behind every AI-generated suggestion."
        ),
    },
    "Intelligent Planning": {
        "One-Click Project Generation": (
            "Instant Project Spawner",
            "Initializes a complete, turnkey development project with plot boundaries, preliminary towers, and financial models in seconds."
        ),
        "AI Layout Generator": (
            "Generative Floor Plan Engine",
            "Creates hundreds of compliant, ergonomically optimized floor plate variations automatically based on high-level constraints."
        ),
        "AI Township Planner": (
            "Large-Scale Masterplanner",
            "Coordinates multi-parcel mega developments, planning residential sectors, commercial high streets, schools, and central parks."
        ),
        "Mixed-Use Development Planning": (
            "Retail & Residential Integrator",
            "Harmonizes high-traffic retail shopping podiums with private residential towers above, separating security and logistics."
        ),
        "Apartment Capacity Prediction": (
            "Maximum Unit Yield Forecast",
            "Accurately estimates how many livable units of specific configurations can comfortably fit onto a given parcel of land."
        ),
        "Land Suitability Analysis": (
            "Site Feasibility Scorecard",
            "Ranks potential land purchases based on soil quality, flood susceptibility, road access, and statutory FSI potential."
        ),
        "Smart Building Recommendations": (
            "High-Performance Design Tips",
            "Recommends passive shading, high-efficiency glass, and energy-saving building configurations tailored to local climate."
        ),
    },
    "GIS & Urban Intelligence": {
        "City Growth Prediction": (
            "Urban Expansion Forecaster",
            "Analyzes historical demographic and satellite data to predict which urban corridors will experience the highest population growth."
        ),
        "Land Value Prediction": (
            "Property Price Forecaster",
            "Forecasts future land appreciation rates based on planned infrastructure investments and neighborhood transit connectivity."
        ),
        "Infrastructure Growth Prediction": (
            "Civic Grid Roadmap",
            "Tracks government masterplans for upcoming metro lines, highway expansions, water pipelines, and electrical grid upgrades."
        ),
        "Climate Analysis": (
            "Local Microclimate Profiler",
            "Evaluates seasonal rainfall, temperature extremes, humidity, and heat island effects specific to the project's exact location."
        ),
        "Disaster Risk Analysis": (
            "Natural Hazard Vulnerability Scan",
            "Assesses site exposure to regional earthquakes, cyclones, storm surges, and landslides to inform structural safety factors."
        ),
        "Earthquake Analysis": (
            "Seismic Zone Risk Assessor",
            "Identifies proximity to active tectonic fault lines and calculates required structural ductility and shear wall requirements."
        ),
        "Flood Analysis": (
            "Storm Runoff Inundation Map",
            "Simulates 100-year storm flood levels and local watershed drainage patterns to ensure buildings remain safely above floodlines."
        ),
        "Wind Analysis": (
            "Wind Tunnel Aerodynamic Scan",
            "Simulates high-velocity wind pressures on high-rise facades and pedestrian comfort zones around building podiums."
        ),
        "Noise & Pollution Analysis": (
            "Acoustic & Air Quality Shield",
            "Maps traffic noise corridors and industrial particulate levels to guide acoustic double-glazing and landscape green buffers."
        ),
    },
}

with open("plain_english_group6.json", "w", encoding="utf-8") as f:
    json.dump(GROUP_6, f, indent=2)
print("Group 6 saved.")
