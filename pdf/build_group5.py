"""
Builds Group 5: AI Suite (Planner, Civil, Structural, QS, Cost, Sustainability, Business, Rec Engine, APT)
"""

import json

GROUP_5 = {
    "AI Planner": {
        "Automatic Layout Generation": (
            "Instant Masterplan Generator",
            "Generates dozens of complete, optimized site and floor layout options with a single click based on plot geometry and zoning rules."
        ),
        "Smart Tower Placement": (
            "Intelligent Tower Siting",
            "Positions towers algorithmically on the plot to maximize natural sunlight, wind flow, privacy, and views while respecting setbacks."
        ),
        "Apartment Mix Optimisation": (
            "Ideal Unit Mix Solver",
            "Optimizes the ratio of 1BHK, 2BHK, 3BHK, and 4BHK units to maximize developer revenue while matching local market buyer demand."
        ),
        "Floor Optimisation": (
            "Zero-Waste Floor Stacker",
            "Refines floor plate geometry to eliminate dark, unventilated pockets, dead-end corridors, and wasted circulation area."
        ),
        "Open Space Optimisation": (
            "Green Space Maximizer",
            "Arranges buildings to consolidate mandatory open ground into usable, high-value central parks and recreational zones."
        ),
    },
    "AI Civil Engineer": {
        "Civil Design Suggestions": (
            "Virtual Senior Engineer",
            "Offers proactive engineering recommendations on drainage slopes, road grades, retaining walls, and retaining structures."
        ),
        "FAR Optimisation": (
            "Floor Area Maximizer",
            "Calculates the exact building massing and floor counts needed to utilize 100% of legally permissible Floor Area Ratio."
        ),
        "FSI Optimisation": (
            "Legal Floor Yield Booster",
            "Unlocks maximum allowable built-up area by strategically combining base FSI, paid premium FSI, and TDR incentive schemes."
        ),
        "Utility Optimisation": (
            "Smart Infrastructure Routing",
            "Optimizes underground pipe networks, water tanks, and electrical substations to minimize piping runs and pumping energy."
        ),
        "Parking Optimisation": (
            "Smart Vehicle Bay Sizer",
            "Maximizes the number of standard, EV, and visitor parking bays accommodated within tight basement and surface footprints."
        ),
    },
    "AI Structural Advisor": {
        "Column Grid Suggestions": (
            "Optimal Column Spacing",
            "Suggests efficient, uniform column grid layouts (e.g., 6m x 6m or 7.5m x 7.5m) that align parking bays below with apartment walls above."
        ),
        "Beam Layout Suggestions": (
            "Skeletal Beam Network",
            "Proposes sensible primary and secondary beam layouts to safely support floor slabs without excessive ceiling depths."
        ),
        "Foundation Recommendations": (
            "Subsoil Footing Advisor",
            "Evaluates soil bearing capacity and building loads to recommend the most cost-effective foundation (isolated, raft, or pile)."
        ),
        "Structural Risk Warnings": (
            "Structural Hazard Detector",
            "Flags potential structural vulnerabilities such as floating columns, soft storeys, excessive cantilevers, or torsional irregularity."
        ),
    },
    "AI Quantity Surveyor": {
        "Quantity Optimisation": (
            "Material Volume Trimmer",
            "Refines structural and architectural dimensions to reduce unnecessary concrete, steel, and masonry bulk without compromising safety."
        ),
        "Waste Reduction": (
            "Zero-Scrap Strategy",
            "Analyzes standard material manufacturing dimensions to minimize on-site cutting losses and scrap material generation."
        ),
        "Steel Cutting Optimisation": (
            "Rebar Bar-Bending Solver",
            "Calculates optimal bar-bending schedules (BBS) to cut standard 12-meter rebar lengths with minimal leftover offcut scrap."
        ),
        "Tile Waste Optimisation": (
            "Tile Pattern Calculator",
            "Simulates tile layout grids across floor rooms to minimize edge cuts, broken tiles, and aesthetic joint misalignment."
        ),
        "BOQ Optimisation": (
            "Cost-Efficient Item Schedule",
            "Streamlines Bill of Quantities items and work descriptions to prevent duplicate contractor billings and scope creep."
        ),
    },
    "AI Cost Engineer": {
        "Cost Prediction": (
            "Early Project Price Tag",
            "Forecasts overall project construction cost within minutes of initial concept design using historical regional cost benchmarks."
        ),
        "Budget Optimisation": (
            "Target Budget Balancer",
            "Rebalances material specifications and finishes across high-visibility versus back-of-house areas to keep the project strictly within budget."
        ),
        "Cost Comparison": (
            "Scenario Expense Benchmarker",
            "Compares capital expenditure across different design iterations, structural systems, or finishing grades side by side."
        ),
        "Cost Saving Suggestions": (
            "Value Engineering Ideas",
            "Suggests practical value engineering alternatives (e.g. fly-ash bricks, optimized slab thicknesses) that lower costs without hurting quality."
        ),
        "Grade Sweep Analysis": (
            "Finish Specification Sweep",
            "Simulates how shifting between affordable, standard, and luxury specification tiers impacts total cost and profit margins."
        ),
    },
    "AI Sustainability": {
        "Green Building Score": (
            "Eco-Rating Predictor",
            "Pre-evaluates the project against IGBC, GRIHA, and LEED certification criteria, predicting the likely star rating or plaque."
        ),
        "Carbon Footprint": (
            "Embodied & Operational Carbon Meter",
            "Measures total carbon emissions generated during material manufacturing, transport, and 50-year building operations."
        ),
        "Solar Potential": (
            "Rooftop Clean Power Calculator",
            "Simulates annual solar irradiance on building rooftops to calculate feasible solar photovoltaic energy output."
        ),
        "Water Efficiency": (
            "Water Recycling Balance",
            "Models daily water circularity by combining low-flow plumbing fixtures, rainwater harvesting, and STP greywater reuse."
        ),
        "Tree Plantation Suggestions": (
            "Native Urban Forest Planner",
            "Recommends native tree and shrub species that maximize shade, air purification, and biodiversity while requiring minimal irrigation."
        ),
    },
    "AI Business Consultant": {
        "ROI Analysis": (
            "Return on Investment Calculator",
            "Projects the percentage return on invested equity across the entire project lifecycle to demonstrate bankability to investors."
        ),
        "Profit Forecast": (
            "Bottom-Line Profit Projection",
            "Forecasts net developer profit after subtracting land cost, approval fees, construction expenditure, financing interest, and marketing."
        ),
        "Project Feasibility": (
            "Go / No-Go Decision Engine",
            "Evaluates market absorption rates, regulatory constraints, and financial viability to give an objective verdict on land acquisition."
        ),
        "Break-even Analysis": (
            "Debt-Free Sales Target",
            "Identifies the exact sales milestone (in units and rupees) where total cash inflows completely cover all project expenditures."
        ),
    },
    "AI Recommendation Engine": {
        "Design Improvements": (
            "Aesthetic & Functional Tips",
            "Suggests subtle architectural tweaks to enhance room proportions, cross-ventilation, natural daylighting, and aesthetic balance."
        ),
        "Engineering Suggestions": (
            "Smart Structural Tweaks",
            "Identifies opportunities to streamline plumbing shafts, simplify structural spans, and standardize window opening sizes."
        ),
        "Cost Optimisation": (
            "Commercial Sweet Spot",
            "Pinpoints where small architectural changes can yield major structural savings without sacrificing livability."
        ),
        "Material Recommendations": (
            "Best-Fit Material Selector",
            "Recommends durable, eco-friendly, locally sourced building materials tailored to the specific microclimate and budget tier."
        ),
    },
    "APT: In-App AI Assistant": {
        "Project Q&A;": (
            "Conversational Civil Co-Pilot",
            "An interactive chat assistant that answers any question about the project's areas, costs, bylaws, and engineering metrics in plain English."
        ),
        "Civil Engineering Guidance": (
            "On-Demand Engineering Expert",
            "Explains complex civil engineering principles, formula derivations, and design codes in simple, accessible language."
        ),
        "Report Explanation": (
            "Report Translator",
            "Translates dense engineering reports, BOQs, and financial schedules into clear executive summaries for non-technical stakeholders."
        ),
        "Scenario Comparison": (
            "Design Trade-off Explainer",
            "Narrates the pros, cons, and financial differences between alternative architectural schemes in everyday terms."
        ),
        "Streaming Responses": (
            "Instant Thought Streaming",
            "Streams conversational answers token-by-token in real time, eliminating frustrating loading delays during design discussions."
        ),
        "Module-Aware Opening Questions": (
            "Contextual Conversation Starter",
            "Suggests smart, relevant follow-up questions tailored to whichever module (parking, structural, finance) the user is currently viewing."
        ),
        "Project State Context Builder": (
            "Live Project Memory",
            "Feeds current real-time project dimensions, costs, and compliance numbers into the AI prompt so answers are always grounded in fact."
        ),
        "Context & Analysis Caching": (
            "High-Speed Memory Cache",
            "Caches complex analytical calculations so the assistant can answer follow-up questions in milliseconds without re-computing."
        ),
        "Query Classification": (
            "Smart Intent Router",
            "Directs user questions to the appropriate specialized internal engine (e.g. structural, municipal bylaw, or financial)."
        ),
        "Capability Questions": (
            "Feature Discovery Guide",
            "Answers questions about what Aptimizer can do, guiding new users step-by-step through advanced platform tools."
        ),
        "Chat Threads & History": (
            "Design Discussion Archive",
            "Saves organized chat histories and design deliberation threads so teams can revisit previous design rationales anytime."
        ),
        "Citation Verification": (
            "Bylaw Grounding Verifier",
            "Verifies that every bylaw clause cited by the assistant exists in the official NBC/IS database before showing it to the user."
        ),
        "Provider Fallback & Retry": (
            "Zero-Downtime AI Engine",
            "Automatically switches between backup AI foundation models if primary cloud services experience latency or temporary outages."
        ),
    },
}

with open("plain_english_group5.json", "w", encoding="utf-8") as f:
    json.dump(GROUP_5, f, indent=2)
print("Group 5 saved.")
