"""
Builds Group 2: Utility Planning, Quantity Estimation, BOQ, Cost Estimation, Compliance Engine, Reports
"""

import json

GROUP_2 = {
    "Utility Planning": {
        "Water Demand": (
            "Daily Thirst Meter",
            "Calculates total daily domestic and flushing water requirements in liters based on resident population and NBC standards."
        ),
        "Underground Tank": (
            "Sub-Basement Reservoir",
            "Sizes the primary subterranean water storage sump to hold a multi-day emergency municipal water reserve."
        ),
        "Overhead Tank": (
            "Rooftop Water Tower",
            "Calculates required rooftop storage tanks for gravity-fed pressurized domestic and fire suppression water distribution."
        ),
        "STP Planning": (
            "On-Site Water Recycler",
            "Sizes the Sewage Treatment Plant to purify blackwater and greywater into reusable flushing and landscaping water."
        ),
        "WTP Planning": (
            "Pure Drinking Filter",
            "Plans Water Treatment Plants to filter raw borewell or municipal supply to potable drinking standards."
        ),
        "Rainwater Harvesting": (
            "Storm Catchment System",
            "Designs filtration pits and recharge aquifers to capture 100% of rainwater runoff from building rooftops and paved ground."
        ),
        "Electrical Room": (
            "Power Substation Vault",
            "Sizes and positions high-voltage transformer, DG backup generator, and electrical breaker panel rooms safely on the site."
        ),
        "Pump Room": (
            "Water Pressure Engine",
            "Allocates space for hydropneumatic booster pumps, fire pumps, and plumbing manifolds to maintain constant water pressure."
        ),
    },
    "Quantity Estimation": {
        "Concrete": (
            "Liquid Stone Volume",
            "Calculates total cubic meters of ready-mix concrete required for foundations, columns, beams, and slabs."
        ),
        "Cement": (
            "Binding Powder Bag Count",
            "Translates concrete, mortar, and plaster volumes into exact 50kg cement bag counts needed on site."
        ),
        "Steel": (
            "Rebar Tonnage Tally",
            "Computes total metric tonnes of reinforced steel rebars (TMT) required across all structural members."
        ),
        "Bricks/Blocks": (
            "Wall Block Counter",
            "Estimates the precise number of clay bricks or AAC lightweight blocks needed to build internal and external walls."
        ),
        "Sand": (
            "Fine Aggregate Supply",
            "Measures river sand or manufactured M-sand volumes needed for structural concrete and smooth wall plaster."
        ),
        "Aggregate": (
            "Crushed Stone Quarry Order",
            "Estimates 10mm and 20mm coarse gravel quantities required for heavy concrete batching."
        ),
        "Tiles": (
            "Floor & Wall Tile Area",
            "Calculates total square meters of vitrified, ceramic, and anti-skid floor and wall tiles with cut wastage factors."
        ),
        "Paint": (
            "Wall Color Liter Order",
            "Calculates liters of primer, putty, interior emulsion, and weather-proof exterior paint needed for all surfaces."
        ),
        "Doors": (
            "Doorway Inventory",
            "Counts and catalogs all main entrance teak doors, bedroom flush doors, and water-resistant bathroom doors."
        ),
        "Windows": (
            "Glazing & Frame Tally",
            "Catalogs all UPVC and aluminium sliding windows, glass ventilators, and balcony French doors."
        ),
        "Plumbing": (
            "Pipe & Drainage Network",
            "Estimates running meters of CPVC water lines, UPVC drain lines, soil stacks, and sanitary ware fixtures."
        ),
        "Electrical": (
            "Conduit & Wire Spool Tally",
            "Calculates total meters of electrical wiring, conduits, light fixtures, switchboards, and distribution boards."
        ),
        "Waterproofing": (
            "Leak-Proof Shield",
            "Quantifies chemical membrane barriers applied over podiums, basements, terrace roofs, and sunken bathrooms."
        ),
        "Finishing Materials": (
            "Surface Beauty Pack",
            "Measures skirtings, granite kitchen countertops, staircase nosings, and false ceiling panels."
        ),
    },
    "BOQ": {
        "Automatic Bill of Quantities": (
            "Instant Itemized Cost Sheet",
            "Generates a complete, standardized Bill of Quantities linking every material, labor task, and machinery cost code."
        ),
        "Material Summary": (
            "Master Supply List",
            "Consolidates raw material quantities into an executive procurement summary ready for supplier bidding."
        ),
        "Labour Summary": (
            "Workforce Man-Hour Ledger",
            "Projects the total person-days required for masons, bar-benders, carpenters, plumbers, and electricians."
        ),
        "Equipment Summary": (
            "Heavy Machinery Roster",
            "Schedules tower cranes, concrete boom placers, earth excavators, and passenger hoists needed on site."
        ),
        "BOQ PDF Export": (
            "Official Tender Dossier",
            "Exports an audit-ready, formatted BOQ document ready for contractor tendering, client sign-off, or bank loan dossiers."
        ),
        "BOQ Excel Export": (
            "Procurement Spreadsheet",
            "Exports editable Excel spreadsheets complete with formulas, rate items, and contractor pricing columns."
        ),
        "Structure-Derived Quantity Take-off": (
            "Physics-Backed Take-off",
            "Derives quantities directly from structural member dimensions rather than generic rule-of-thumb estimates."
        ),
        "Column & Beam Section Sizing": (
            "Skeletal Sizing Engine",
            "Calculates preliminary column and beam cross-sections to ensure architectural designs are structurally realistic."
        ),
        "Mix Proportion Derivation": (
            "Recipe Ratio Formula",
            "Determines water-cement-aggregate design mix ratios (e.g., M25, M30, M40) for various structural elements."
        ),
        "Take-off Sanity Checks": (
            "Error-Proof Anomaly Filter",
            "Cross-examines estimated material quantities against industry benchmarks to immediately flag erroneous spikes."
        ),
    },
    "Cost Estimation": {
        "Material Cost": (
            "Raw Supply Expense",
            "Calculates total financial outlay for cement, steel, bricks, finishes, and fixtures based on current market rates."
        ),
        "Labour Cost": (
            "Workforce Payroll Estimate",
            "Calculates total skilled and unskilled contractor payroll expenses across every construction trade."
        ),
        "Equipment Cost": (
            "Machinery Hire Expense",
            "Forecasts total leasing, fuel, and maintenance costs for heavy construction machinery and tooling."
        ),
        "Construction Cost": (
            "Direct Hard Costs",
            "Aggregates all direct physical building costs (materials + labor + equipment) into a single baseline construction budget."
        ),
        "Cost per Flat": (
            "Per-Apartment Price Tag",
            "Divides total tower construction cost by the number of units to reveal the exact build cost per apartment."
        ),
        "Cost per sq m": (
            "Area Unit Rate",
            "Normalizes total expenditure against built-up area to evaluate commercial competitiveness against city market benchmarks."
        ),
        "Budget Summary": (
            "Financial Health Dashboard",
            "An executive single-page financial overview contrasting planned budgets, cost breakdowns, and gross profit margins."
        ),
        "Wastage Allowance": (
            "Scrap & Spoilage Buffer",
            "Factors in realistic 3-5% on-site material cutting losses and breakages into the procurement budget."
        ),
        "Preliminaries": (
            "Site Setup & Logistics Budget",
            "Accounts for job-site trailers, temporary water/power, security staff, access fencing, and project insurance."
        ),
        "Overhead & Profit": (
            "Contractor Margin Allowance",
            "Calculates general contractor head-office overheads and reasonable profit margins (typically 10-15%)."
        ),
        "Contingency": (
            "Rainy Day Reserve Fund",
            "Sets aside an essential 5-10% financial reserve to safeguard against unforeseen subsoil conditions or site emergencies."
        ),
        "Escalation": (
            "Inflation Shock Absorber",
            "Models projected steel, cement, and fuel price inflation across multi-year construction timelines."
        ),
        "GST": (
            "Statutory Tax Tally",
            "Calculates applicable Goods & Services Tax (GST) brackets across materials, labour contracts, and professional fees."
        ),
    },
    "Compliance Engine": {
        "FAR Validation": (
            "Floor Area Limit Check",
            "Verifies that the total proposed building area does not exceed municipal Floor Area Ratio limits."
        ),
        "FSI Validation": (
            "FSI Cap Gatekeeper",
            "Ensures full compliance with local zonal Floor Space Index laws, preventing illegal unauthorized overbuilding."
        ),
        "Stair Width": (
            "Emergency Egress Width Check",
            "Ensures staircases meet statutory minimum widths (e.g. 1.5m to 2.0m) to prevent human crush during rapid evacuations."
        ),
        "Corridor Width": (
            "Hallway Clearance Check",
            "Guarantees internal circulation passages meet mandatory clear widths for wheelchairs and fire rescue stretchers."
        ),
        "Lift Compliance": (
            "Elevator Safety Mandate",
            "Ensures elevator counts, car capacities, and fire-fighting lifts meet National Building Code requirements."
        ),
        "Fire Exit Checks": (
            "Fire Life-Safety Audit",
            "Validates that the distance from any apartment front door to the nearest fire exit stair does not exceed legal limits (e.g. 30m)."
        ),
        "Accessibility Checks": (
            "Universal Access Shield",
            "Validates wheelchair ramps, grab rails, door clearances, and barrier-free paths for disabled and elderly residents."
        ),
        "Setback Validation": (
            "Property Line Boundary Check",
            "Confirms front, rear, and side setback buffers are clear of permanent structures for fire tender circulation."
        ),
        "Height vs Road Width Rule": (
            "Street-to-Sky Limit",
            "Restricts maximum building height according to adjoining road width to ensure neighborhood sunlight and emergency access."
        ),
        "Open Space vs Height Rule": (
            "Tower Clearance Buffer",
            "Increases mandatory perimeter open grounds as the building grows taller to satisfy fire-tender reach bylaws."
        ),
        "Clause-Referenced Results": (
            "By-Law Citation Anchor",
            "Tags every compliance rule check with the exact municipal by-law, NBC chapter, or IS code clause number."
        ),
        "Compliance Margin Warnings": (
            "Early Breach Warning",
            "Alerts designers when dimensions fall within 5% of legal limits so design tweaks don't trigger permit rejection."
        ),
    },
    "Reports": {
        "BOQ Report": (
            "Official Quantities Document",
            "Generates a polished, print-ready Bill of Quantities report ready for contractor bidding and bank valuation."
        ),
        "Cost Report": (
            "Financial Feasibility Book",
            "Produces a comprehensive cost breakdown report itemizing capital expenditure across all civil trades."
        ),
        "Quantity Report": (
            "Material Tonnage Report",
            "Summarizes all raw material volumes and tonnages needed across the full lifecycle of the project."
        ),
        "Parking Report": (
            "Vehicle Allocation Dossier",
            "Summarizes provided versus statutory required car, two-wheeler, and EV charging parking spaces."
        ),
        "Compliance Report": (
            "Municipal Sanction Docket",
            "Produces a clean compliance certificate listing every tested by-law with green pass / red fail statuses."
        ),
        "Executive Summary": (
            "One-Page Leadership Brief",
            "A concise, high-impact summary of project dimensions, financial metrics, and statutory compliance for C-suite leaders."
        ),
        "PDF Export": (
            "Universal Document Export",
            "Compiles presentation-grade PDF reports with custom headers, company branding, and page numbering."
        ),
        "Per-Tower Report Sections": (
            "Wing-by-Wing Breakdown",
            "Breaks down complex multi-tower developments into individual tower data sheets for targeted construction phasing."
        ),
        "Excel Workbook Export": (
            "Data Spreadsheet Bundle",
            "Exports multi-tab Excel workbooks containing live formulas, raw takeoff numbers, and financial tables."
        ),
        "Tower Floor Plans PDF Report": (
            "Architectural Drawing Sheet",
            "Generates high-resolution multi-page 2D architectural drawing sheets complete with room tags and dimensions."
        ),
        "Floor Plan Image & ZIP Export": (
            "Graphic Asset Package",
            "Bundles high-resolution PNG/SVG floor plans and marketing brochures into a single downloadable ZIP archive."
        ),
    },
}

with open("plain_english_group2.json", "w", encoding="utf-8") as f:
    json.dump(GROUP_2, f, indent=2)
print("Group 2 saved.")
