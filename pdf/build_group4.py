"""
Builds Group 4: Development Finance, Data Reliability & Assurance, IS & NBC Code Intelligence, Engineering Modules, 3D & Visualisation
"""

import json

GROUP_4 = {
    "Development Finance": {
        "Saleable Area Derivation": (
            "Market Revenue Multiplier",
            "Calculates the exact total billable square footage of residential, commercial, and parking spaces to be sold to buyers."
        ),
        "Revenue Model": (
            "Total Inflow Forecast",
            "Projects total gross sales revenue based on market price per square foot across all units and amenities."
        ),
        "S-Curve Cost Spread": (
            "Capital Burn S-Curve",
            "Models gradual cash expenditure starting slow during foundation, peaking at superstructure, and tapering at finishes."
        ),
        "Monthly Cash Flow": (
            "Monthly Inflow vs Outflow",
            "Balances monthly customer milestone collections against contractor invoice payments to prevent liquidity shortages."
        ),
        "NPV": (
            "Net Present Value",
            "Discounts all future multi-year cash inflows and outflows to today's rupee value to evaluate true project profitability."
        ),
        "IRR": (
            "Internal Rate of Return",
            "Computes the annual percentage yield of the real estate investment to evaluate if it beats bank financing hurdle rates."
        ),
        "Break-even Point": (
            "Cost Recovery Milestone",
            "Identifies the exact sales milestone (e.g. 58% of units sold) where total revenue fully covers all land and construction debt."
        ),
        "Preliminaries per Month": (
            "Monthly Site Overhead",
            "Models fixed monthly site management overheads such as security, crane rentals, supervisor salaries, and site utilities."
        ),
        "Finance Configuration": (
            "Loan & Interest Setup",
            "Lets developers configure bank construction loan interest rates, equity-to-debt ratios, and sales absorption velocity."
        ),
    },
    "Data Reliability & Assurance": {
        "Plot Data Check": (
            "Land Data Health Check",
            "Verifies that plot boundary coordinates, survey lines, and edge classifications are mathematically closed and sound."
        ),
        "Development Controls Check": (
            "Zoning Parameters Check",
            "Ensures FSI, ground coverage, and setback parameters entered into the project match official municipal master plans."
        ),
        "Tower Data Check": (
            "Tower Architecture Check",
            "Verifies that tower heights, floor-to-floor clearances, and core dimensions are realistic and structurally feasible."
        ),
        "Site Layout Check": (
            "Masterplan Integrity Check",
            "Validates that all towers, roads, amenities, and parking structures sit entirely within the legal plot boundary."
        ),
        "GIS Data Check": (
            "Geospatial Precision Check",
            "Confirms satellite imagery, road width overlays, and contour data align with millimeter ground truth."
        ),
        "Parking Check": (
            "Parking Quota Check",
            "Audits parking designs to ensure car counts, turning radii, and ramp slopes meet statutory building code minimums."
        ),
        "Engineering Check": (
            "Structural & MEP Sanity Check",
            "Ensures column spans, water tank capacities, and lift counts satisfy mechanical and civil engineering safety norms."
        ),
        "Finance Check": (
            "Financial Logic Audit",
            "Checks that financial cash flows, escalation buffers, and profit models do not contain circular or missing formulas."
        ),
        "Programme Check": (
            "Timeline Logic Audit",
            "Verifies that construction task predecessors, curing delays, and milestone dependencies are realistically sequenced."
        ),
        "Data Freshness Tracking": (
            "Data Timestamp Tracker",
            "Monitors when input assumptions were last updated, flagging stale cost rates or outdated municipal bylaw data."
        ),
        "Cross-Module Consistency Checks": (
            "Ecosystem Sync Guard",
            "Ensures that changing a dimension in architectural planning instantly synchronizes with BOQ quantities and finance."
        ),
        "Compliance Margin Reporting": (
            "Safety Buffer Gauge",
            "Reports how much headroom exists between actual project measurements and statutory maximum/minimum limits."
        ),
        "Module Warning Rollup": (
            "Central Alert Aggregator",
            "Collects all warnings, code breaches, and data anomalies across all 47 modules into a single consolidated dashboard."
        ),
        "Overall Trust Score": (
            "Project Reliability Index",
            "Gives the entire development a single confidence score (0-100%) indicating how complete, verified, and bank-ready the project is."
        ),
        "Data Health Report Export": (
            "Assurance Audit Certificate",
            "Generates a formal data verification document proving to investors and lenders that all calculations are fully validated."
        ),
    },
    "IS & NBC Code Intelligence": {
        "Central Code Constant Registry": (
            "Master Engineering Constants",
            "A standardized repository of standard civil constants (steel density, concrete strength, live loads, fire ratings)."
        ),
        "74-Entry Clause Registry": (
            "Bylaw Clause Database",
            "A structured digital index of 74 foundational clauses from the National Building Code (NBC) and Indian Standards (IS)."
        ),
        "Clause Text Corpus Ingestion": (
            "Legal Code Digitizer",
            "Ingests and parses dense government building codes, development control regulations, and technical standards."
        ),
        "Clause Chunking & Indexing": (
            "Smart Code Indexer",
            "Breaks dense legal clauses into bite-sized, searchable concepts tagged with building height, occupancy, and zone."
        ),
        "Semantic Clause Retrieval (RAG)": (
            "AI Code Search Engine",
            "Uses semantic Retrieval-Augmented Generation to instantly find the exact relevant building code clause for any design question."
        ),
        "Code Search Endpoint": (
            "Bylaw Search Bar",
            "An API endpoint allowing users to search across NBC 2016, IS 456, IS 1893, and local municipal bylaws using natural language."
        ),
        "Code Question Answering": (
            "AI Building Code Consultant",
            "Answers complex architectural compliance questions with clear plain-English interpretations grounded in statutory text."
        ),
        "Citation Extraction": (
            "Legal Clause Tagger",
            "Extracts and references the exact section, table, and clause numbers (e.g. NBC 2016 Part 4 Table 7) supporting any rule."
        ),
        "Citation Verification Against Registry": (
            "Hallucination Shield",
            "Cross-references every generated citation against the certified legal registry to ensure AI never invents fake bylaws."
        ),
        "Cited Extracts in Answers": (
            "Verbatim Legal Proof",
            "Displays verbatim excerpts of the actual statutory code directly inside AI answers for complete legal transparency."
        ),
    },
    "Engineering Modules (IS/NBC)": {
        "Structural Load Estimator (IS 875)": (
            "Gravity Load Calculator",
            "Computes dead weight of walls, slabs, and finishes alongside live human occupancy loads per IS 875 Part 1 & 2."
        ),
        "Wind Force Coefficients (IS 875-3)": (
            "Wind Pressure Profiler",
            "Calculates design wind speeds and aerodynamic gust pressures on high-rise facades according to IS 875 Part 3."
        ),
        "Seismic Zone & Base Shear (IS 1893)": (
            "Earthquake Safety Force",
            "Determines regional earthquake zone factor (II to V) and computes total base shear force the building must resist per IS 1893."
        ),
        "Foundation Advisor (IS 6403/1904)": (
            "Subsoil Footing Guide",
            "Recommends shallow isolated footings, raft foundations, or deep bored piles based on soil safe bearing capacity."
        ),
        "Concrete Mix Design (IS 10262)": (
            "Concrete Recipe Engineer",
            "Designs optimal water-cement ratios and aggregate gradations for specified target compressive strengths per IS 10262."
        ),
        "Water Infrastructure (IS 1172)": (
            "Plumbing Supply Standard",
            "Determines required daily domestic water flow rates, pipe sizes, and storage capacities per IS 1172 standards."
        ),
        "Storm Water & RWH (IS 3764)": (
            "Rain Runoff & Drainage Design",
            "Sizes perimeter stormwater drains, catch basins, and percolation recharge pits per IS 3764 and local bylaws."
        ),
        "Parking Compliance (NBC/SP:21)": (
            "Vehicle Code Validator",
            "Validates parking bay dimensions (2.5m x 5.0m), driveways, and turning circles against NBC and SP:21 handbook rules."
        ),
        "Fire Safety Compliance (NBC Part 4)": (
            "Fire Life-Safety Guardian",
            "Checks compartmentation, fire hydrant positions, sprinkler coverage, and fire-escape doors against NBC 2016 Part 4."
        ),
        "Accessibility Compliance (NBC Part 3)": (
            "Barrier-Free Standard",
            "Ensures wheelchair ramp slopes (1:12), tactile paving, and disabled washroom dimensions comply with NBC Part 3."
        ),
        "Green Building Preliminary Rating": (
            "Eco-Certification Scorecard",
            "Evaluates energy efficiency, water recycling, and material sustainability to estimate IGBC or GRIHA green star ratings."
        ),
        "Column Grid Optimizer": (
            "Structural Column Sizer",
            "Suggests efficient, regular column grid spacings (e.g. 6m x 6m or 7.5m x 7.5m) that align parking below with flats above."
        ),
        "Embodied Carbon": (
            "Material Carbon Footprint",
            "Calculates total metric tonnes of carbon emissions embedded in the manufacturing and transport of cement, steel, and bricks."
        ),
        "Plantation Plan": (
            "Oxygen & Greenery Planner",
            "Calculates required tree counts per plot area, recommending native shade and oxygen-generating species."
        ),
    },
    "3D & Visualisation": {
        "3D Site Model": (
            "Interactive Digital Campus",
            "Renders a full 3D interactive model of the site complete with buildings, terrain contours, and roads in real time."
        ),
        "Tower Massing": (
            "Building Volume Blocks",
            "Displays simple 3D geometric volumetric masses of towers to visualize skyline impact, shadows, and bulk proportions."
        ),
        "Road & Plot Rendering": (
            "Site Surface Visualizer",
            "Renders textured internal asphalt driveways, pedestrian sidewalks, and perimeter fencing in the 3D viewer."
        ),
        "Amenity & Clubhouse Rendering": (
            "Lifestyle Amenities Visualizer",
            "Renders community recreation centers, swimming pools, tennis courts, and children's play areas in 3D."
        ),
        "Central Park & Landscape": (
            "Green Oasis Visualizer",
            "Displays central green lawns, botanical gardens, shade trees, and outdoor seating plazas in lush 3D visuals."
        ),
        "Floor Plate Viewer": (
            "Floor-by-Floor 3D Slicer",
            "Allows users to peel open any storey of a tower to inspect the interior unit arrangement, corridors, and core."
        ),
        "Site Diagrams": (
            "Masterplan Graphic Diagrams",
            "Generates color-coded thematic maps showing circulation flows, security zones, and service delivery pathways."
        ),
        "Blueprint View": (
            "Classic Blue-White Plan",
            "Toggles 2D views into a high-contrast architectural blueprint style with crisp vector lines and dimension annotations."
        ),
        "Live Metrics Strip": (
            "Real-Time HUD Gauge",
            "A persistent heads-up display showing live FSI, unit counts, budget totals, and compliance status as you edit."
        ),
        "Command Palette": (
            "Instant Keyboard Navigator",
            "A fast keyboard-driven search popup (Ctrl+K) to jump to any tool, tower, report, or calculation instantly."
        ),
        "Presentation-Grade Furnished 2D Blueprint Engine": (
            "Architectural Brochure Plan",
            "Renders presentation-ready floor plans furnished with realistic sofas, dining sets, kitchen counters, and beds."
        ),
        "Structural Wall Poché & Dimension Badges": (
            "Pro-Grade Drafting Style",
            "Fills load-bearing walls with solid architectural hatch poché and displays crisp, translucent dimension badges."
        ),
    },
}

with open("plain_english_group4.json", "w", encoding="utf-8") as f:
    json.dump(GROUP_4, f, indent=2)
print("Group 4 saved.")
