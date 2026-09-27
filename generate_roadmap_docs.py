import os
import sys
from datetime import datetime

# -------------------------------------------------------------------------
# 1. GENERATE PROFESSIONAL PDF USING REPORTLAB
# -------------------------------------------------------------------------
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

PDF_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Aptimizer_Master_Product_Roadmap.pdf")
DOCX_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Aptimizer_Master_Product_Roadmap.docx")

# Color Palette
PRIMARY = colors.HexColor("#0F2942")     # Deep Civil Navy
BRAND = colors.HexColor("#1D4ED8")       # Vibrant Engineering Blue
BRAND_LIGHT = colors.HexColor("#EFF6FF") # Light Blue Tint
ACCENT = colors.HexColor("#D97706")      # Amber / Construction Gold
DARK = colors.HexColor("#0F172A")        # Slate 900
TEXT = colors.HexColor("#334155")        # Slate 700
MUTED = colors.HexColor("#64748B")       # Slate 500
LIGHT_BG = colors.HexColor("#F8FAFC")    # Slate 50
BORDER = colors.HexColor("#CBD5E1")      # Slate 300
SUCCESS_BG = colors.HexColor("#ECFDF5")  # Emerald 50
SUCCESS_TEXT = colors.HexColor("#065F46")# Emerald 800
WARN_BG = colors.HexColor("#FFFBEB")     # Amber 50
WARN_TEXT = colors.HexColor("#92400E")    # Amber 800

class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas for exact 'Page X of Y' page numbering and headers."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(MUTED)

        # Header (Pages 2+)
        if self._pageNumber > 1:
            self.drawString(20 * mm, 283 * mm, "Aptimizer Master Product Roadmap — Technical Audit & Engineering Execution Plan")
            self.setStrokeColor(BORDER)
            self.setLineWidth(0.5)
            self.line(20 * mm, 280 * mm, 190 * mm, 280 * mm)

        # Footer (All pages)
        self.setStrokeColor(BORDER)
        self.setLineWidth(0.5)
        self.line(20 * mm, 15 * mm, 190 * mm, 15 * mm)
        self.drawString(20 * mm, 10 * mm, "Confidential — Aptimizer Civil Engineering AI Operating System")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(190 * mm, 10 * mm, page_str)
        self.restoreState()


def generate_pdf():
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=A4,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=PRIMARY,
        alignment=0,
        spaceAfter=4,
    )
    subtitle_style = ParagraphStyle(
        "DocSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=MUTED,
        spaceAfter=12,
    )
    h1_style = ParagraphStyle(
        "Heading1_Custom",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=PRIMARY,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True,
    )
    h2_style = ParagraphStyle(
        "Heading2_Custom",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=9.5,
        leading=13,
        textColor=BRAND,
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True,
    )
    body_style = ParagraphStyle(
        "Body_Custom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.2,
        leading=11.5,
        textColor=TEXT,
        spaceAfter=3.5,
    )
    bullet_style = ParagraphStyle(
        "Bullet_Custom",
        parent=body_style,
        leftIndent=12,
        firstLineIndent=-7,
        spaceAfter=2,
    )
    callout_style = ParagraphStyle(
        "Callout_Text",
        parent=body_style,
        fontSize=8,
        leading=11.5,
        textColor=PRIMARY,
    )
    table_cell = ParagraphStyle(
        "TableCell",
        parent=body_style,
        fontSize=7.2,
        leading=9.5,
        spaceAfter=0,
    )
    table_cell_bold = ParagraphStyle(
        "TableCellBold",
        parent=table_cell,
        fontName="Helvetica-Bold",
        textColor=DARK,
    )
    table_header = ParagraphStyle(
        "TableHeader",
        parent=table_cell,
        fontName="Helvetica-Bold",
        textColor=colors.white,
        fontSize=7.5,
        leading=10,
    )

    def callout(text, bg=BRAND_LIGHT, border_color=BRAND):
        p = Paragraph(text, callout_style)
        t = Table([[p]], colWidths=[170 * mm])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), bg),
            ("BOX", (0,0), (-1,-1), 0.75, border_color),
            ("TOPPADDING", (0,0), (-1,-1), 5),
            ("BOTTOMPADDING", (0,0), (-1,-1), 5),
            ("LEFTPADDING", (0,0), (-1,-1), 8),
            ("RIGHTPADDING", (0,0), (-1,-1), 8),
        ]))
        return t

    story = []

    # Title Block
    story.append(Paragraph("Aptimizer: Master Product Roadmap & Technical Remediation Plan", title_style))
    story.append(Paragraph("From Conceptual Planning to Legally Defensible Civil Engineering AI OS | September 2026", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceAfter=8, spaceBefore=0))

    # Executive Overview
    story.append(Paragraph("Executive Context & Platform Audit", h1_style))
    story.append(Paragraph(
        "Aptimizer has established an impressive, unprecedented algorithmic core. Across Versions 1 to 3, the platform "
        "has built 324 catalogued capabilities spanning polygon setback derivations, multi-tower greedy and genetic layout packing, "
        "IS/NBC structural heuristics, CPM scheduling with congestion efficiency modeling, and an in-app AI assistant (APT) backed "
        "by a 74-clause Indian Standards RAG registry. However, to transition from an exploratory feasibility calculator into an "
        "indispensable, enterprise-grade software adopted by Tier-1 developers (DLF, Godrej, Prestige) and EPC giants (L&T, Shapoorji), "
        "Aptimizer must bridge critical industry gaps. This document details the <b>exact fixes for existing features</b> and the "
        "<b>multi-phase roadmap of what to build next</b>, articulated through the engineering lens of <i>What, How, and Why</i>.",
        body_style
    ))

    # Current Status Box
    status_summary = (
        "<b>Current Platform Status:</b> 420 Features Catalogued | 324 Built & Running | 28 Partially Built | 68 Planned<br/>"
        "<b>Primary Gaps:</b> CAD/BIM Interoperability (0% Built in V5), Structural Biaxial/Drift Realism, Statutory RERA Area Splits, "
        "Local Municipal DCR Presets, and 3D Earthwork Cut-and-Fill Site Grading."
    )
    story.append(callout(status_summary, bg=BRAND_LIGHT, border_color=BRAND))
    story.append(Spacer(1, 4 * mm))

    # -------------------------------------------------------------------------
    # PART 1: FIXING EXISTING FEATURES
    # -------------------------------------------------------------------------
    story.append(Paragraph("Part 1: Existing Features to Fix & Exact Remediation", h1_style))
    story.append(Paragraph(
        "Before expanding into autonomous systems, the following six core modules require immediate engineering elevation "
        "to ensure absolute technical and legal defensibility.",
        body_style
    ))

    # Fix 1
    story.append(Paragraph("1. Structural Column Biaxial Moments & High-Rise Foundation Selection", h2_style))
    story.append(Paragraph(
        "<b>WHAT is broken:</b> In <code>backend/engineering.py</code> (Module 1 & 3), column sizing relies solely on axial load capacity "
        "(IS 456 Cl. 39.3: <i>P<sub>u</sub> = 0.4 f<sub>ck</sub> A<sub>c</sub> + 0.67 f<sub>y</sub> A<sub>sc</sub></i>). In real multi-storey buildings (>15m), "
        "lateral wind and seismic shears create severe overturning moments, inducing biaxial bending (<i>M<sub>ux</sub>, M<sub>uy</sub></i>). Sizing on axial load alone "
        "severely undersizes perimeter/corner columns. Furthermore, Module 3 prescribes isolated pad footings regardless of height, which would suffer catastrophic "
        "differential settlement on tall towers.<br/>"
        "<b>HOW to fix it:</b><br/>"
        "• <i>Biaxial Interaction:</i> Implement the Bresler interaction formulation from IS 456 Cl. 39.6:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>(M<sub>ux</sub> / M<sub>ux1</sub>)<sup>&alpha;<sub>n</sub></sup> + (M<sub>uy</sub> / M<sub>uy1</sub>)<sup>&alpha;<sub>n</sub></sup> &le; 1.0</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;Approximate lateral moments from wind/seismic base shear distributed across the frame.<br/>"
        "• <i>Foundation Advisor:</i> Compute average contact pressure <i>q<sub>avg</sub> = &Sigma;P<sub>service</sub> / Footprint</i>. "
        "If <i>q<sub>avg</sub> &gt; SBC</i>, automatically reject isolated footings. Prescribe <b>RCC Raft/Mat Foundation (IS 2950)</b> for moderate loads, "
        "or <b>Bored Cast-in-Situ Piling (IS 2911)</b> when building height > 45m or on soft soil, outputting required pile count and diameter.<br/>"
        "<b>WHY:</b> Any chartered structural engineer will reject plans sized only for axial loads. Making sizing biaxially defensible establishes immediate professional credibility.",
        body_style
    ))
    story.append(Spacer(1, 2 * mm))

    # Fix 2
    story.append(Paragraph("2. Procedural Floor Plan Hierarchy & Core Pinning", h2_style))
    story.append(Paragraph(
        "<b>WHAT is broken:</b> In <code>backend/floorplan/</code>, room layouts are generated by slicing the perimeter footprint inward. "
        "In tall residential towers, physical architecture is strictly dictated by the <b>central vertical structural core</b> (shear walls, lifts, "
        "fire escape stairs, and MEP risers). Slicing rooms without a locked core produces unbuildable apartment layouts.<br/>"
        "<b>HOW to fix it:</b> Invert the generator hierarchy. Pin the core first: (1) Two fire-rated staircases (&ge; 1.5m tread per NBC Part 4 Cl. 4.3), "
        "(2) Passenger and stretcher fire lift shafts with smoke-stop lobbies, (3) Four dedicated vertical MEP shafts (electrical, PHE wet riser, stormwater, ventilation). "
        "Only once the core is frozen do apartment units expand outward into cruciform, linear, or L-shaped wings.<br/>"
        "<b>WHY:</b> Real MEP risers and structural shear cores must align vertically from foundation to terrace without offset. Locking the core guarantees structural viability.",
        body_style
    ))
    story.append(Spacer(1, 2 * mm))

    # Fix 3
    story.append(Paragraph("3. Statutory Area Accounting & RERA Carpet Schedule", h2_style))
    story.append(Paragraph(
        "<b>WHAT is broken:</b> <code>backend/engine.py</code> relies on legacy 'Super Built-up Area' loading factors (25%). Under the Indian Real Estate "
        "(Regulation and Development) Act 2016 (RERA), selling apartments on super built-up area is illegal; sales must occur strictly on <b>RERA Carpet Area</b>.<br/>"
        "<b>HOW to fix it:</b> Implement Section 2(k) of RERA 2016:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>RERA Carpet Area = Usable Internal Floor Area + Internal Partition Wall Thicknesses</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<i>(Explicitly excluding: External walls, service shafts, exclusive balconies/verandahs, and common areas).</i><br/>"
        "Provide a statutory RERA schedule table per unit type alongside sanction drawings.<br/>"
        "<b>WHY:</b> Real estate developers cannot launch projects or secure project finance without RERA-certified carpet area schedules.",
        body_style
    ))
    story.append(Spacer(1, 2 * mm))

    # Fix 4
    story.append(Paragraph("4. BOQ Substructure vs. Superstructure Split & CPWD DSR Mapping", h2_style))
    story.append(Paragraph(
        "<b>WHAT is broken:</b> <code>backend/takeoff.py</code> and <code>engine.py</code> aggregate concrete and steel into uniform bulk totals. "
        "In construction finance, substructure works (deep excavation, shoring, raft, basement waterproofing) carry completely different risk, rates, and cash flow curves "
        "than typical superstructure floors.<br/>"
        "<b>HOW to fix it:</b> Split BOQ into two distinct packages: <b>Package A: Substructure</b> (earthwork, retaining walls, foundation raft/piles, dewatering) and "
        "<b>Package B: Superstructure</b> (columns, shear walls, slabs, masonry, finishes). Map line items to standard 5-digit <b>CPWD Delhi Schedule of Rates (DSR)</b> codes.<br/>"
        "<b>WHY:</b> Lenders, quantity surveyors, and contractors bid substructure and superstructure separately. DSR mapping enables government and institutional adoption.",
        body_style
    ))
    story.append(Spacer(1, 2 * mm))

    # Fix 5
    story.append(Paragraph("5. Construction Programme Climate Windows & Tower Crane Cycles", h2_style))
    story.append(Paragraph(
        "<b>WHAT is broken:</b> In <code>backend/schedule.py</code>, CPM calculation assumes continuous output year-round and infinite vertical material hoisting. "
        "In India, monsoon months (June–September) severely disrupt excavation, external plastering, and waterproofing. Furthermore, high-rise floor cycle speed is physically "
        "governed by the <b>Tower Crane hook time</b>, not just crew size.<br/>"
        "<b>HOW to fix it:</b><br/>"
        "• <i>Monsoon Blackouts:</i> Introduce regional monsoon blackout calendars in coastal/monsoon zones with automatic activity shifting or 50% productivity derating.<br/>"
        "• <i>Crane Hook Cycle Limit:</i> Constrain the floor cycle: <i>T<sub>cycle</sub> = max(IS 456 Striking Days, Total Tonnage / Crane Hourly Hoist Rate)</i>.<br/>"
        "<b>WHY:</b> Real contractors will immediately identify an unconstrained monsoon or crane schedule as unrealistic, undermining confidence in the programme.",
        body_style
    ))
    story.append(Spacer(1, 2 * mm))

    # Fix 6
    story.append(Paragraph("6. Internal Road Geometry & Fire Tender Swept-Path Verification", h2_style))
    story.append(Paragraph(
        "<b>WHAT is broken:</b> <code>backend/siteplan/reserve.py</code> generates inward road networks, but corners are sharp 90-degree polygon vertices. "
        "Under NBC 2016 Part 4, fire tenders require a minimum <b>9.0m inside turning radius (12.0m outside turning radius)</b> clear of obstructions.<br/>"
        "<b>HOW to fix it:</b> Apply a fillet curve with minimum radius <i>R<sub>in</sub> &ge; 9.0m</i> at every road junction and driveway bend using Shapely geometry buffers. "
        "Flag non-compliant corners where fire engines would become trapped.<br/>"
        "<b>WHY:</b> Municipal Fire NOC (No Objection Certificate) is the #1 reason preliminary site sanction drawings are rejected by authorities.",
        body_style
    ))

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # PART 2: WHAT TO DO NEXT (THE ROADMAP)
    # -------------------------------------------------------------------------
    story.append(Paragraph("Part 2: What to Do Next — Multi-Phase Roadmap", h1_style))
    story.append(Paragraph(
        "The following four-phase execution roadmap prioritizes high-leverage commercial and technical breakthroughs, "
        "progressing systematically from immediate CAD/BIM interoperability to an autonomous civil engineering platform.",
        body_style
    ))

    # Phase Table
    phase_data = [
        [
            Paragraph("Phase", table_header),
            Paragraph("Timeline", table_header),
            Paragraph("Key Deliverables", table_header),
            Paragraph("AEC Software / Tools", table_header),
            Paragraph("Commercial Impact", table_header),
        ],
        [
            Paragraph("<b>Phase 1</b><br/>Interoperability Bridge", table_cell),
            Paragraph("Weeks 1–3", table_cell),
            Paragraph("• 1-Click Layered AutoCAD (.dxf)<br/>• OpenBIM IFC4 3D Export<br/>• ETABS (.s2k) / STAAD (.std) Export", table_cell),
            Paragraph("<code>ezdxf</code><br/><code>ifcopenshell</code><br/>CSI / Bentley format", table_cell),
            Paragraph("Eliminates the CAD silo; enables structural consultants & architects to adopt Aptimizer instantly.", table_cell),
        ],
        [
            Paragraph("<b>Phase 2</b><br/>Civil & Municipal Rigor", table_cell),
            Paragraph("Weeks 4–7", table_cell),
            Paragraph("• 3D Earthwork Cut-and-Fill Balancer<br/>• City DCR Engines (Mumbai, BLR, HYD)<br/>• PreDCR Sanction Layer Automation", table_cell),
            Paragraph("TIN / Grid Prismoidal<br/>Local Master Plans<br/>AutoDCR / PreDCR", table_cell),
            Paragraph("Saves millions in site earthworks; enables automated municipal building sanction submission.", table_cell),
        ],
        [
            Paragraph("<b>Phase 3</b><br/>Headless CAD Sheets", table_cell),
            Paragraph("Weeks 8–12", table_cell),
            Paragraph("• Headless FreeCAD TechDraw Worker<br/>• Automated A1/A0 Sanction Drawing Sheets<br/>• Spatial 3D Redlining & Approval Gates", table_cell),
            Paragraph("Headless FreeCAD<br/>Celery / Redis<br/>Three.js Pinning", table_cell),
            Paragraph("Replaces manual drafting of municipal submission sheets; enables enterprise team sign-offs.", table_cell),
        ],
        [
            Paragraph("<b>Phase 4</b><br/>Autonomous Civil OS (X)", table_cell),
            Paragraph("Weeks 13–18", table_cell),
            Paragraph("• Multi-Agent Engineering Swarm<br/>• Live TMT/Cement Price Tender Bundler<br/>• Drone Orthophoto vs CPM Verification", table_cell),
            Paragraph("Agent Swarms<br/>Wholesale Indices<br/>Photogrammetry", table_cell),
            Paragraph("Delivers the complete Aptimizer X vision: autonomous design optimization and real-time site monitoring.", table_cell),
        ],
    ]

    t_phase = Table(phase_data, colWidths=[28 * mm, 18 * mm, 52 * mm, 32 * mm, 40 * mm])
    t_phase.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), PRIMARY),
        ("GRID", (0,0), (-1,-1), 0.5, BORDER),
        ("TOPPADDING", (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("LEFTPADDING", (0,0), (-1,-1), 4),
        ("RIGHTPADDING", (0,0), (-1,-1), 4),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, LIGHT_BG]),
    ]))
    story.append(t_phase)
    story.append(Spacer(1, 4 * mm))

    # Detailed Phase Breakdowns
    story.append(Paragraph("Deep Dive: Phase 1 — The Interoperability Bridge (Weeks 1–3)", h2_style))
    story.append(Paragraph(
        "<b>Deliverable 1.1: 1-Click Layered AutoCAD Export (<code>ezdxf</code>)</b><br/>"
        "• <i>What:</i> Instant download of a production-ready <code>.dxf</code> drawing from any project state.<br/>"
        "• <i>How:</i> Implement <code>backend/cad_export.py</code> using <code>ezdxf</code>. Create dedicated layers: "
        "<code>A-SITE-BNDY</code> (property polygon), <code>A-SITE-STBK</code> (setback limits), <code>A-BLDG-FP</code> (tower footprints), "
        "<code>S-GRID</code> (column grid lines with bubble labels A, B, C / 1, 2, 3), <code>S-COLS</code> (hatched column rectangles), and "
        "<code>A-TEXT-DIMS</code> (linear dimensions and room carpet area tags).<br/>"
        "• <i>Why:</i> 100% of Indian architecture firms use AutoCAD. Giving them clean DXF files eliminates redrawing from scratch.<br/>"
        "<b>Deliverable 1.2: Certified OpenBIM IFC4 Export (<code>ifcopenshell</code>)</b><br/>"
        "• <i>What:</i> Certified 3D BIM export compatible with Revit, ArchiCAD, and Navisworks.<br/>"
        "• <i>How:</i> Use pure Python <code>ifcopenshell</code> to build <code>IfcProject &rarr; IfcSite &rarr; IfcBuildingStorey</code>. "
        "Extrude slabs as <code>IfcSlab</code> and columns as <code>IfcColumn</code>, attaching custom property sets (<i>Pset_CivilEngineering</i> with loads and concrete grades).<br/>"
        "• <i>Why:</i> Unlocks Version 5 (BIM Readiness) with zero desktop CAD dependencies.<br/>"
        "<b>Deliverable 1.3: ETABS / STAAD.Pro Analytical Script Export</b><br/>"
        "• <i>What:</i> Generate <code>.s2k</code> (ETABS) or <code>.std</code> (STAAD) text scripts containing nodes, frames, and load cases.<br/>"
        "• <i>Why:</i> Structural engineers spend 2–3 days setting up an analytical model. Aptimizer will generate it in 500 milliseconds.",
        body_style
    ))
    story.append(Spacer(1, 3 * mm))

    story.append(Paragraph("Deep Dive: Phase 2 — Civil & Municipal Sanction Engine (Weeks 4–7)", h2_style))
    story.append(Paragraph(
        "<b>Deliverable 2.1: 3D Earthwork Cut-and-Fill Balancer</b><br/>"
        "• <i>What:</i> Automatically calculate excavation vs fill volumes and optimize finished site formation levels.<br/>"
        "• <i>How:</i> Superimpose 3D terrain grid from GIS elevation data over building pads and internal roads. Calculate cut/fill using the prismoidal method: "
        "<i>&Delta;V = &Sigma; (Z<sub>existing</sub> - Z<sub>formation</sub>) &times; &Delta;x &Delta;y</i>. Compute the optimal datum level <i>Z<sub>0</sub></i> where "
        "<i>V<sub>cut</sub> &approx; V<sub>fill</sub> &times; 1.15</i> (soil bulking factor).<br/>"
        "• <i>Why:</i> Hauling excess soil off-site or importing fill costs lakhs of rupees. Zero-net earthwork balance is a massive cost-saver.<br/>"
        "<b>Deliverable 2.2: City DCR Presets & PreDCR Sanction Export</b><br/>"
        "• <i>What:</i> Pre-configured rules for Mumbai (DCPR 2034 Fungible FSI), Bengaluru (BBMP/BDA Master Plan), and Hyderabad (GO 168).<br/>"
        "• <i>How:</i> Provide an export mode formatting DXF layers with designated PreDCR polylines (<code>_BLDG_BOUNDARY</code>, <code>_NET_PLOT</code>, <code>_PROP_WORK</code>).<br/>"
        "• <i>Why:</i> Over 80% of municipal corporations in India use AutoDCR/PreDCR for automated building sanction.",
        body_style
    ))
    story.append(Spacer(1, 3 * mm))

    story.append(Paragraph("Deep Dive: Phase 3 — Headless FreeCAD & Drawing Sheet Automation (Weeks 8–12)", h2_style))
    story.append(Paragraph(
        "<b>Deliverable 3.1: Headless FreeCAD TechDraw Sanction Sheet Worker</b><br/>"
        "• <i>What:</i> Background generation of multi-page, formatted A1/A0 architectural drawing sheets.<br/>"
        "• <i>How:</i> Run headless FreeCAD inside an asynchronous Celery worker container. Using FreeCAD's TechDraw workbench, import the building geometry, "
        "slice horizontal floor plans at Z = 1.2m, generate vertical cross-sections, attach title blocks with developer name, project coordinates, and area tables, "
        "and render publication-grade PDF sheets.<br/>"
        "• <i>Why:</i> Offloads heavy drawing projection from the user's browser, automating days of manual drafting work.<br/>"
        "<b>Deliverable 3.2: Multi-Party 3D Spatial Redlining & Approval Gates</b><br/>"
        "• <i>What:</i> Enterprise collaboration workflow allowing stakeholders to pin comments directly onto 3D building elements and enforce statutory sign-offs.<br/>"
        "• <i>Why:</i> Fulfills the Version 4 Enterprise Collaboration promise.",
        body_style
    ))
    story.append(Spacer(1, 3 * mm))

    story.append(Paragraph("Deep Dive: Phase 4 — Aptimizer X: Autonomous Civil Engineering OS (Weeks 13–18)", h2_style))
    story.append(Paragraph(
        "<b>Deliverable 4.1: Multi-Agent Engineering Swarm</b><br/>"
        "• <i>What:</i> Replace the single-turn APT chat with an autonomous 4-agent background swarm: (1) <i>Structural Sentinel</i> (flags drift/slenderness), "
        "(2) <i>Sanction Watchdog</i> (monitors fire radii & setbacks), (3) <i>Commercial Guardian</i> (tracks cost/IRR deltas), and (4) <i>Carbon Officer</i>.<br/>"
        "<b>Deliverable 4.2: Dynamic Material Procurement & Tender Generator</b><br/>"
        "• <i>What:</i> Connect to real-time wholesale commodity price indices (TMT steel, cement) and auto-generate FIDIC / Indian Standard tender packages.<br/>"
        "<b>Deliverable 4.3: Drone Survey Photogrammetry vs. CPM As-Built Verification</b><br/>"
        "• <i>What:</i> Ingest site drone point clouds (<code>.las</code>) and compare completed slab heights against <code>backend/schedule.py</code> milestones.",
        body_style
    ))

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # PART 3: ARCHITECTURE & TECHNOLOGY RATIO (WHAT, HOW, WHY OF FREECAD)
    # -------------------------------------------------------------------------
    story.append(Paragraph("Part 3: Technology Strategy & The FreeCAD Question", h1_style))
    story.append(Paragraph(
        "A common technical proposal is: <i>'Can we fix all 3D features, floor plans, and CAD tools by embedding FreeCAD?'</i><br/>"
        "Here is the definitive architectural analysis of why a <b>hybrid decoupled architecture</b> is mandatory.",
        body_style
    ))

    tech_table_data = [
        [
            Paragraph("Component Layer", table_header),
            Paragraph("Recommended Technology", table_header),
            Paragraph("Why NOT Pure FreeCAD?", table_header),
            Paragraph("Core Benefit to Aptimizer", table_header),
        ],
        [
            Paragraph("<b>Interactive Client UI</b><br/>(3D Orbit, Floor Edit)", table_cell),
            Paragraph("React 19 + Three.js<br/>HTML5 Canvas / SVG", table_cell),
            Paragraph("FreeCAD is a C++/Qt desktop app. It cannot run responsively in a browser at 60fps.", table_cell),
            Paragraph("Instant in-browser rendering; zero install; smooth, modern web user experience.", table_cell),
        ],
        [
            Paragraph("<b>Instant 2D CAD Export</b><br/>(Drawings, Grids)", table_cell),
            Paragraph("Pure Python <code>ezdxf</code><br/>(In FastAPI Gateway)", table_cell),
            Paragraph("FreeCAD takes 2–3 seconds just to boot Python modules; <code>ezdxf</code> exports in &lt; 40ms.", table_cell),
            Paragraph("Blazing fast 1-click DXF export with zero container overhead.", table_cell),
        ],
        [
            Paragraph("<b>Certified OpenBIM</b><br/>(3D IFC Models)", table_cell),
            Paragraph("Pure Python <code>ifcopenshell</code><br/>(In FastAPI Gateway)", table_cell),
            Paragraph("FreeCAD's Arch workbench uses <code>ifcopenshell</code> under the hood anyway.", table_cell),
            Paragraph("Generates IFC4 building models directly in Python with full property sets.", table_cell),
        ],
        [
            Paragraph("<b>Complex Drawings & Boolean Solids</b>", table_cell),
            Paragraph("Headless FreeCAD Worker<br/>(Celery / Redis / Docker)", table_cell),
            Paragraph("FreeCAD is ideal here! It has Open CASCADE solid booleans and TechDraw projection.", table_cell),
            Paragraph("Leverages FreeCAD's true strength (A1/A0 sheets, terrain booleans) without slowing down the web app.", table_cell),
        ],
    ]

    t_tech = Table(tech_table_data, colWidths=[38 * mm, 38 * mm, 46 * mm, 48 * mm])
    t_tech.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), PRIMARY),
        ("GRID", (0,0), (-1,-1), 0.5, BORDER),
        ("TOPPADDING", (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("LEFTPADDING", (0,0), (-1,-1), 4),
        ("RIGHTPADDING", (0,0), (-1,-1), 4),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, LIGHT_BG]),
    ]))
    story.append(t_tech)
    story.append(Spacer(1, 5 * mm))

    # Strategic Summary Box
    summary_box = (
        "<b>Strategic Summary:</b><br/>"
        "1. <b>Immediately fix the 6 existing modules:</b> Column biaxial moments, raft/pile foundations, core-first floor plates, "
        "RERA carpet areas, substructure BOQ splits, and monsoon/crane scheduling limits.<br/>"
        "2. <b>Execute Phase 1 immediately:</b> Ship <code>ezdxf</code> 2D CAD and <code>ifcopenshell</code> IFC4 BIM export. This turns Aptimizer into an interoperable commercial platform overnight.<br/>"
        "3. <b>Deploy Headless FreeCAD as an asynchronous worker:</b> Use it strictly for heavy A1/A0 sanction drawing sheets and 3D terrain Boolean operations, keeping your frontend lightning-fast."
    )
    story.append(callout(summary_box, bg=SUCCESS_BG, border_color=SUCCESS_TEXT))

    # Build PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF generated successfully at: {PDF_PATH}")


# -------------------------------------------------------------------------
# 2. GENERATE EDITABLE WORD DOCUMENT (.DOCX) USING PYTHON-DOCX
# -------------------------------------------------------------------------
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_shading(cell, color_hex):
    shading_xml = f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>'
    cell._tc.get_or_add_tcPr().append(parse_xml(shading_xml))

def generate_docx():
    doc = Document()

    # Set Margins
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # Styles
    title_p = doc.add_paragraph()
    title_run = title_p.add_run("Aptimizer: Master Product Roadmap & Technical Remediation Plan")
    title_run.font.name = "Arial"
    title_run.font.size = Pt(20)
    title_run.font.bold = True
    title_run.font.color.rgb = RGBColor(15, 41, 66)

    sub_p = doc.add_paragraph()
    sub_run = sub_p.add_run("From Conceptual Planning to Legally Defensible Civil Engineering AI OS | September 2026")
    sub_run.font.name = "Arial"
    sub_run.font.size = Pt(10)
    sub_run.font.color.rgb = RGBColor(100, 116, 139)

    doc.add_paragraph("―" * 55)

    # Section 1
    h1 = doc.add_heading("1. Executive Context & Audit Summary", level=1)
    h1.runs[0].font.color.rgb = RGBColor(15, 41, 66)

    p1 = doc.add_paragraph(
        "Aptimizer has established an extraordinary algorithmic foundation across Versions 1 to 3, boasting 324 built features "
        "including polygon setback generation, greedy and genetic layout packing, IS/NBC structural checks, CPM scheduling with "
        "congestion curves, and an in-app AI assistant (APT) backed by a 74-clause IS/NBC RAG registry. However, to transition from a "
        "conceptual feasibility tool to an enterprise-grade civil engineering operating system used by Tier-1 developers and contractors, "
        "Aptimizer must overcome critical gaps in CAD/BIM interoperability, structural realism, and statutory compliance."
    )
    p1.style.font.size = Pt(10)

    # Section 2
    h2 = doc.add_heading("2. Existing Features to Fix & Technical Remediation", level=1)
    h2.runs[0].font.color.rgb = RGBColor(15, 41, 66)

    fixes = [
        ("1. Structural Column Biaxial Moments & High-Rise Foundations (backend/engineering.py)",
         "WHAT is broken: Column sizing relies solely on axial capacity (IS 456 Cl. 39.3), severely undersizing columns subjected to seismic/wind overturning moments. Module 3 prescribes isolated footings even for tall towers.\n"
         "HOW to fix it: Implement IS 456 Cl. 39.6 Bresler biaxial interaction curves [(Mux/Mux1)^an + (Muy/Muy1)^an <= 1.0]. Introduce an automated Foundation Advisor selecting RCC Raft Foundations (IS 2950) when contact pressure exceeds soil SBC, and Bored Cast-in-Situ Piles (IS 2911) for buildings >45m or on soft soil.\n"
         "WHY: Structural consultants will immediately reject plans without biaxial moment and realistic foundation checks."),

        ("2. Procedural Floor Plan Hierarchy & Core Pinning (backend/floorplan/)",
         "WHAT is broken: Room layouts are generated by slicing the perimeter footprint inward, producing unbuildable plans without pinned vertical circulation and MEP shafts.\n"
         "HOW to fix it: Invert the hierarchy. Pin the central structural core first (two 1.5m fire stairs per NBC Part 4, passenger/fire lifts, and 4 MEP risers). Grow residential wings outward from the frozen core.\n"
         "WHY: High-rise structural stability and MEP efficiency require continuous vertical riser alignment from foundation to terrace."),

        ("3. Statutory Area Accounting & RERA Carpet Schedule (backend/engine.py)",
         "WHAT is broken: Relies on legacy Super Built-Up area heuristics. Under the Indian RERA Act 2016, selling apartments on super built-up is illegal.\n"
         "HOW to fix it: Implement statutory Section 2(k) RERA Carpet Area (Internal Usable Area + Internal Partition Walls, strictly excluding exterior walls, service shafts, and balconies). Provide certified RERA schedules.\n"
         "WHY: Indian real estate developers cannot legally launch or finance projects without certified RERA carpet figures."),

        ("4. BOQ Substructure vs Superstructure Split & CPWD DSR Mapping (backend/takeoff.py)",
         "WHAT is broken: Concrete, steel, and earthwork are lumped as a project-wide uniform rate without distinguishing between foundation and typical floors.\n"
         "HOW to fix it: Split BOQ into Package A (Substructure: deep excavation, shoring, raft, waterproofing) and Package B (Superstructure: repetitive slabs, columns, finishes). Map items to 5-digit CPWD Delhi Schedule of Rates (DSR) codes.\n"
         "WHY: Banks and contractors bid substructure and superstructure separately. DSR mapping enables government/tender adoption."),

        ("5. Construction Programme Climate Windows & Tower Crane Cycles (backend/schedule.py)",
         "WHAT is broken: Schedule assumes uniform year-round productivity and infinite material hoist speed.\n"
         "HOW to fix it: Add regional Monsoon Calendar Blackouts (June–September) for excavation/external plastering. Constrain floor cycles by Tower Crane hook cycle times [Cycle = max(Striking, Tonnage/Crane Hoist Rate)].\n"
         "WHY: Any contractor will reject a schedule showing basement excavation in Mumbai or Bengaluru during peak July monsoons."),

        ("6. Internal Road Geometry & Fire Tender Swept-Path (backend/siteplan/reserve.py)",
         "WHAT is broken: Road network junctions are sharp 90-degree polygon vertices lacking fire tender clearance.\n"
         "HOW to fix it: Apply a fillet curve with minimum inside turning radius Rin >= 9.0m (12.0m outside) per NBC Part 4.\n"
         "WHY: Fire NOC is the single most common cause of municipal site plan rejection.")
    ]

    for title, body in fixes:
        hp = doc.add_paragraph()
        hr = hp.add_run(title)
        hr.font.bold = True
        hr.font.size = Pt(11)
        hr.font.color.rgb = RGBColor(29, 78, 216)
        bp = doc.add_paragraph(body)
        bp.style.font.size = Pt(9.5)

    # Section 3
    h3 = doc.add_heading("3. What to Do Next: Multi-Phase Product Roadmap", level=1)
    h3.runs[0].font.color.rgb = RGBColor(15, 41, 66)

    table = doc.add_table(rows=1, cols=4)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_cells = table.rows[0].cells
    headers = ["Phase & Timeline", "Key Deliverables", "Core Technology", "Strategic Impact"]
    for i, h in enumerate(headers):
        hdr_cells[i].text = h
        hdr_cells[i].paragraphs[0].runs[0].font.bold = True
        hdr_cells[i].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_shading(hdr_cells[i], "0F2942")

    phases = [
        ("Phase 1: Interoperability Bridge\n(Weeks 1–3)",
         "• 1-Click Layered AutoCAD (.dxf)\n• OpenBIM IFC4 3D Model Export\n• ETABS (.s2k) / STAAD (.std) Export",
         "ezdxf, ifcopenshell, CSI / Bentley parsers",
         "Eliminates CAD silo; allows architects & structural engineers to adopt Aptimizer immediately."),
        ("Phase 2: Civil & Municipal Rigor\n(Weeks 4–7)",
         "• 3D Earthwork Cut-and-Fill Balancer\n• City DCR Engines (Mumbai, BLR, HYD)\n• PreDCR Automated Sanction Export",
         "TIN / Grid Prismoidal, Local Master Plans, PreDCR",
         "Saves millions in earthwork hauling; unlocks automated municipal sanction approvals."),
        ("Phase 3: Headless CAD Sheets\n(Weeks 8–12)",
         "• Headless FreeCAD TechDraw Worker\n• Automated A1/A0 Sanction Drawing Sheets\n• 3D Spatial Redlining & Approval Gates",
         "Headless FreeCAD, Celery/Redis, Three.js",
         "Replaces manual drafting of submission sheets; enables multi-disciplinary enterprise sign-offs."),
        ("Phase 4: Autonomous Civil OS (X)\n(Weeks 13–18)",
         "• Multi-Agent Engineering Swarm\n• Live Commodity Price Tender Bundler\n• Drone Survey vs CPM As-Built Verification",
         "Agent Swarms, Wholesale Indices, Photogrammetry",
         "Delivers the complete Aptimizer X vision: autonomous engineering and real-time site monitoring.")
    ]

    for p_title, p_deliv, p_tech, p_impact in phases:
        row_cells = table.add_row().cells
        row_cells[0].text = p_title
        row_cells[1].text = p_deliv
        row_cells[2].text = p_tech
        row_cells[3].text = p_impact
        for cell in row_cells:
            cell.paragraphs[0].runs[0].font.size = Pt(8.5)
            set_cell_shading(cell, "F8FAFC")

    # Section 4
    h4 = doc.add_heading("4. The Technology Architecture: FreeCAD vs. Pure Python", level=1)
    h4.runs[0].font.color.rgb = RGBColor(15, 41, 66)

    p_arch = doc.add_paragraph(
        "Why FreeCAD cannot replace the interactive web application, but serves as an exceptional headless worker:\n\n"
        "1. Interactive Client (React 19 + Three.js): FreeCAD is a C++/Qt desktop app. It cannot deliver 60fps in-browser interactive editing. The web client must remain Three.js + Canvas2D.\n"
        "2. Fast 2D CAD (ezdxf): FreeCAD takes 2-3 seconds to boot; ezdxf exports clean layered AutoCAD files in <40ms inside FastAPI.\n"
        "3. OpenBIM (ifcopenshell): ifcopenshell generates certified IFC4 files directly in Python without C++ dependencies.\n"
        "4. Headless FreeCAD Worker: Headless FreeCAD is reserved for asynchronous Celery workers to run TechDraw projection sheets (A1/A0 drawing cuts) and 3D B-Rep Boolean terrain earthworks."
    )
    p_arch.style.font.size = Pt(9.5)

    doc.save(DOCX_PATH)
    print(f"DOCX generated successfully at: {DOCX_PATH}")

if __name__ == "__main__":
    generate_pdf()
    generate_docx()
