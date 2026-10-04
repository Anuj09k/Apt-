"""
Aptimizer Complete Feature List (V1 to X+) PDF Generator
Produces an authentic, pixel-perfect 15-page PDF mirroring the exact ReportLab
styling, palette, typography, layout, and structure of the original document.

Incorporates all latest capabilities:
- 424 features total across 8 versions (417 built, 1 partial, 6 planned).
- Presentation-Grade 2D Architectural Floor Plan Engine (realistic furniture blocks, double-line poché walls, translucent dimension badges).
- Google Nano Banana AI 3D Architectural Render Engine (3D isometric cutaways, exterior facade concepts, luxury interior suites).
- Dedicated Architectural Deliverables (multi-page Floor Plans PDF drawings sheet, PNG export, multi-tower ZIP package).
- Enterprise Collaboration & Workflow Gating (5-stage approval gates, multidisciplinary task assignment, threaded reviews, automation rules).
- BIM & CAD Interoperability (georeferenced IFC4 model export with spatial hierarchy for Revit, DXF import with automated boundary extraction, layered DXF export for AutoCAD/BricsCAD/LibreCAD, DWG compatibility).
- AI Civil Engineering OS (AI Engineering Copilot, Consultant, Explainable AI, intelligent planning, GIS hazard analysis).
- X+ Generative Design items updated to Built & Running (Green).
"""

import os
import sys
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
pt = 1
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas
from pypdf import PdfReader

# -------------------------------------------------------------------------
# COLOR PALETTE (Exact RGB match to original PDF)
# -------------------------------------------------------------------------
PRIMARY = colors.Color(0.121569, 0.305882, 0.47451)        # #1F4E79 - Deep Civil Navy
SECTION_BLUE = colors.Color(0.180392, 0.458824, 0.713725)   # #2E75B6 - Category Header Blue
BUILT_GREEN = colors.Color(0.117647, 0.517647, 0.286275)    # #1E8449 - Built & Running
PARTIAL_ORANGE = colors.Color(0.784314, 0.498039, 0.039216) # #C87F0A - Partially Built
PLANNED_GREY = colors.Color(0.603922, 0.647059, 0.694118)   # #9AA5B1 - Planned
DARK_TEXT = colors.Color(0.101961, 0.101961, 0.101961)      # #1A1A1A - Dark Body Text
OBJ_TEXT = colors.Color(0.2, 0.2, 0.2)                       # #333333 - Objective Text
ROW_BG = colors.Color(0.933333, 0.952941, 0.972549)          # #EEF3F8 - Table Alternating Row
BORDER_COLOR = colors.Color(0.72549, 0.796078, 0.866667)    # #B9CBE0 - Table Grid Border
FOOTER_GREY = colors.Color(0.541176, 0.541176, 0.541176)    # #8A8A8A - Running Footer Text
LINE_GREY = colors.Color(0.8, 0.8, 0.8)                      # #CCCCCC - Divider Line

PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN = 20 * mm  # 56.6929 pt
USABLE_WIDTH = PAGE_WIDTH - 2 * MARGIN  # 481.8898 pt


class FeatureListCanvas(canvas.Canvas):
    """Custom canvas that renders the running footer on every page."""
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
            self.draw_footer()
            super().showPage()
        super().save()

    def draw_footer(self):
        self.saveState()
        self.setFont("Helvetica", 7.5)
        self.setFillColor(FOOTER_GREY)
        footer_str = f"Aptimizer Feature List  |  Page {self._pageNumber}"
        self.drawRightString(PAGE_WIDTH - MARGIN, 13 * mm, footer_str)
        self.restoreState()


def get_bullet_html(status):
    """Returns ZapfDingbats square symbol HTML."""
    if status == "built":
        color_hex = "#1E8449"
    elif status == "partial":
        color_hex = "#C87F0A"
    else:
        color_hex = "#9AA5B1"
    return f'<font name="ZapfDingbats" color="{color_hex}">n</font>'


def make_banner(title_text):
    """Generates the signature dark blue section banner matching original PDF."""
    style = ParagraphStyle(
        "BannerTitle",
        fontName="Helvetica-Bold",
        fontSize=14.5,
        leading=18,
        textColor=colors.white,
    )
    p = Paragraph(title_text, style)
    t = Table([[p]], colWidths=[USABLE_WIDTH])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), PRIMARY),
        ('TOPPADDING', (0, 0), (-1, -1), 9.4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 9.4),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    return t


def make_objective(obj_text):
    """Generates the Objective line."""
    style = ParagraphStyle(
        "ObjectiveStyle",
        fontName="Helvetica-Oblique",
        fontSize=9.5,
        leading=13.5,
        textColor=OBJ_TEXT,
        spaceAfter=5,
    )
    html = f'<b>Objective:</b> {obj_text}'
    return Paragraph(html, style)


def make_metrics(total, built, partial, planned):
    """Generates the metrics summary strip."""
    style = ParagraphStyle(
        "MetricsStyle",
        fontName="Helvetica",
        fontSize=9,
        leading=12.6,
        textColor=DARK_TEXT,
        spaceAfter=6,
    )
    b_bullet = get_bullet_html("built")
    p_bullet = get_bullet_html("partial")
    pl_bullet = get_bullet_html("planned")
    html = f'<b>{total}</b> features  |  {b_bullet} <b>{built}</b> built  |  {p_bullet} <b>{partial}</b> partial  |  {pl_bullet} <b>{planned}</b> planned'
    return Paragraph(html, style)


def make_section_header(title):
    """Generates a category section header."""
    style = ParagraphStyle(
        "SectionHeader",
        fontName="Helvetica-Bold",
        fontSize=11.5,
        leading=15,
        textColor=SECTION_BLUE,
        spaceBefore=6,
        spaceAfter=2,
    )
    return Paragraph(title, style)


def make_features_table(features):
    """Creates a 2-column table for a list of features."""
    feat_style = ParagraphStyle(
        "FeatItem",
        fontName="Helvetica",
        fontSize=9.2,
        leading=12.6,
        textColor=DARK_TEXT,
    )
    
    rows = []
    for i in range(0, len(features), 2):
        col1_item = features[i]
        b1 = get_bullet_html(col1_item["status"])
        p1 = Paragraph(f'{b1}&nbsp;&nbsp;{col1_item["name"]}', feat_style)
        
        if i + 1 < len(features):
            col2_item = features[i + 1]
            b2 = get_bullet_html(col2_item["status"])
            p2 = Paragraph(f'{b2}&nbsp;&nbsp;{col2_item["name"]}', feat_style)
        else:
            p2 = ""
        
        rows.append([p1, p2])
    
    col_w = USABLE_WIDTH / 2.0  # 240.9449 pt
    t = Table(rows, colWidths=[col_w, col_w])
    t.setStyle(TableStyle([
        ('TOPPADDING', (0, 0), (-1, -1), 1.2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1.2),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    return t


def build_page_1(story):
    """Page 1: Title, Subtitle, Divider, Consolidated Summary Table, Legend."""
    title_style = ParagraphStyle(
        "P1Title",
        fontName="Helvetica-Bold",
        fontSize=21,
        leading=26,
        textColor=PRIMARY,
        alignment=1,  # Center
        spaceAfter=8,
    )
    subtitle_style = ParagraphStyle(
        "P1Subtitle",
        fontName="Helvetica",
        fontSize=10.5,
        leading=15,
        textColor=colors.HexColor("#555555"),
        alignment=1,  # Center
        spaceAfter=15,
    )
    
    story.append(Spacer(1, 25 * pt))
    story.append(Paragraph("Aptimizer: Complete Feature List (V1 to X+)", title_style))
    story.append(Paragraph(
        "A consolidated feature index across all eight versions. 424 features total, of which 417 are built and 1 is partially built.",
        subtitle_style
    ))
    
    # Divider line
    story.append(HRFlowable(
        width="100%",
        thickness=0.6,
        color=LINE_GREY,
        spaceBefore=5,
        spaceAfter=22,
    ))
    
    # Consolidated Table
    table_data = [
        ["Version", "Focus", "Features", "Built", "Status"],
        ["Aptimizer V1", "Core Civil Engineering Planning Platform", "126", "126", "Complete"],
        ["Aptimizer V2", "GIS & Site Intelligence", "27", "25", "In progress"],
        ["Aptimizer V2.5", "Precision, Programme & Assurance", "116", "116", "Complete"],
        ["Aptimizer V3", "AI Engineering Platform", "55", "55", "Complete"],
        ["Aptimizer V4", "Enterprise Collaboration", "13", "13", "Complete"],
        ["Aptimizer V5", "BIM & Smart Construction", "13", "13", "Complete"],
        ["Aptimizer X", "AI Civil Engineering Operating System", "55", "55", "Complete"],
        ["Aptimizer X+", "Future Vision", "19", "14", "In progress"],
    ]
    
    col_widths = [85.04 * pt, 175.75 * pt, 53.86 * pt, 45.35 * pt, 70.87 * pt]  # 430.87 pt total
    t = Table(table_data, colWidths=col_widths, hAlign="CENTER")
    
    t_style = [
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8.6),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('TOPPADDING', (0, 0), (-1, 0), 6),
        ('ALIGN', (0, 0), (1, -1), 'LEFT'),
        ('ALIGN', (2, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.4, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, ROW_BG]),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8.6),
        ('TEXTCOLOR', (0, 1), (-1, -1), DARK_TEXT),
        ('TOPPADDING', (0, 1), (-1, -1), 5.5),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 5.5),
    ]
    t.setStyle(TableStyle(t_style))
    story.append(t)
    
    story.append(Spacer(1, 28 * pt))
    
    # Legend
    legend_style = ParagraphStyle(
        "LegendText",
        fontName="Helvetica",
        fontSize=9.2,
        leading=12.6,
        textColor=DARK_TEXT,
    )
    b_html = f'{get_bullet_html("built")}&nbsp;&nbsp;<b>Built and running</b>'
    p_html = f'{get_bullet_html("partial")}&nbsp;&nbsp;<b>Partially built</b>'
    pl_html = f'{get_bullet_html("planned")}&nbsp;&nbsp;<b>Planned</b>'
    
    leg_table = Table([[
        Paragraph(b_html, legend_style),
        Paragraph(p_html, legend_style),
        Paragraph(pl_html, legend_style)
    ]], colWidths=[160.63 * pt, 160.63 * pt, 160.63 * pt])
    leg_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(leg_table)
    story.append(PageBreak())


def build_page_2(story):
    """Page 2: Build Status: Where Aptimizer Stands Today."""
    story.append(make_banner("Build Status: Where Aptimizer Stands Today"))
    story.append(Spacer(1, 6 * pt))
    
    body_style = ParagraphStyle(
        "P2Body",
        fontName="Helvetica",
        fontSize=9.2,
        leading=13.0,
        textColor=colors.HexColor("#222222"),
        spaceAfter=5,
    )
    h2_style = ParagraphStyle(
        "P2H2",
        fontName="Helvetica-Bold",
        fontSize=11.5,
        leading=15,
        textColor=PRIMARY,
        spaceBefore=5,
        spaceAfter=3,
    )
    bullet_style = ParagraphStyle(
        "P2Bullet",
        fontName="Helvetica",
        fontSize=8.6,
        leading=11.5,
        textColor=colors.HexColor("#1A1A1A"),
        leftIndent=14,
        firstLineIndent=-14,
        spaceAfter=2.5,
    )
    
    story.append(Paragraph(
        "Aptimizer is built and running through <b>V5</b> and <b>Aptimizer X</b>, with active generative design, autonomous engineering, and smart city infrastructure in <b>X+</b>. V1, V2.5, V3, V4, V5, and X are functionally complete. X+ autonomous systems and generative design are operational. Long-range X+ XR/robotics and supplier negotiation capabilities remain planned.",
        body_style
    ))
    story.append(Paragraph(
        "The headline figure: <b>417 of 424 catalogued features are built</b>, with a further 1 partially built. Everything still outstanding sits in external live GIS integrations and the long-range XR/robotics and supplier negotiation roadmap.",
        body_style
    ))
    
    story.append(Paragraph("What was added since the previous feature list", h2_style))
    story.append(Paragraph(
        "The previous list catalogued 253 features across seven versions. This revision adds 171, with full completion of <b>V2.5</b>, <b>V4</b>, <b>V5</b>, and <b>Aptimizer X</b>, and advanced <b>X+</b> autonomous and generative capabilities. The largest additions are:",
        body_style
    ))
    
    additions = [
        ("Presentation-grade 2D architectural floor plan engine.", "Procedural furnished floor plate generation with realistic furniture blocks, structural wall poché (#0F172A), room dimension badges, and multi-format PDF/PNG/ZIP exports."),
        ("Google Nano Banana AI 3D architectural render engine.", "Real-time engineering prompt synthesis from live building geometry, generating photorealistic 3D isometric cutaways, exterior facade views, and luxury interior suites."),
        ("Site layout engine with genetic refinement.", "Multi-objective genetic algorithm (GA) off-grid search, setback envelopes, road reservation, and verified NBC Part 3 spacing clearance."),
        ("Enterprise collaboration & workflow gating (V4).", "5-stage approval gates with cryptographic audit certificates, multidisciplinary task assignment, threaded reviews, and event-driven automation rules."),
        ("BIM & Smart Construction Digital Twin (V5).", "Native AutoCAD R2018 DWG export, georeferenced IFC4 model export with spatial hierarchy (Revit Link IFC), layered DXF export, IoT sensor streaming with Arrhenius concrete maturity & stripping advisory, 4D BIM progress tracking with EVM (SPI/CPI), and BMS predictive maintenance."),
        ("Autonomous AI Engineering & Smart City (X+).", "Conversational design mutations, 5-agent multi-disciplinary review with consensus certificates, autonomous compliance audit, parametric BOQ takeoff, city-scale zoning, traffic simulation with fire-tender turning clearance, macro utility networks, and urban digital twin microclimate analysis."),
        ("AI Civil Engineering Operating System (X).", "Knowledge graph, memory timeline, decision log audit, what-if decision sandbox, CPWD benchmarks, live material pricing, forecasting, supplier intelligence, JIT calendar, inventory planning, tender documents, government approval dossier, urban growth, multi-hazard risk, green building scorecard, ESG, 30-yr LCC, and executive KPIs."),
        ("Generative design studio (X+).", "Generative facade archetype synthesis with solar metrics and Nano Banana prompts, central park landscape zoning, and automated parking bay layouts."),
        ("Programme, scheduling, and cash flow.", "Activity generation from quantities, full CPM passes, work calendars, prop removal safety rules, a target date solver, cash flow, NPV, and IRR."),
        ("Data reliability and code intelligence.", "Nine per-module data checks, freshness tracking, cross-module consistency, a 74-entry clause registry, and semantic IS/NBC clause verification."),
    ]
    
    for title, desc in additions:
        b = get_bullet_html("built")
        story.append(Paragraph(f"{b}&nbsp;&nbsp;<b>{title}</b> {desc}", bullet_style))
    
    story.append(Paragraph("What is not built", h2_style))
    
    not_built = [
        ("XR & Robotics and Supplier Negotiation in X+.", "AR/VR site walkthroughs, drone survey integration, robotics-assisted construction planning, and AI supplier negotiation."),
        ("Live External GIS Integrations in V2.", "Google Maps live API integration and full satellite imagery basemap tile streaming."),
    ]
    
    for title, desc in not_built:
        b = get_bullet_html("planned")
        desc_str = f" {desc}" if desc else ""
        story.append(Paragraph(f"{b}&nbsp;&nbsp;<b>{title}</b>{desc_str}", bullet_style))
    
    story.append(Spacer(1, 3 * pt))
    story.append(Paragraph(
        "Stated plainly: Aptimizer is a complete enterprise product through Aptimizer X, with full V2.5 precision engineering, complete V5 BIM & Digital Twin smart construction, fully operational Aptimizer X AI Civil Engineering OS, operational X+ autonomous engineering, smart city infrastructure, and generative design.",
        body_style
    ))
    story.append(PageBreak())



def build_page_3(story):
    """Page 3: How the Platform Is Used: Workflow Order."""
    story.append(make_banner("How the Platform Is Used: Workflow Order"))
    story.append(Spacer(1, 8 * pt))
    
    intro_style = ParagraphStyle(
        "P3Intro",
        fontName="Helvetica",
        fontSize=9.8,
        leading=14.5,
        textColor=colors.HexColor("#222222"),
        spaceAfter=10,
    )
    story.append(Paragraph(
        "The feature index that follows is ordered by version, because its job is to show what was built when and what comes next. The platform itself is not used in that order. A project moves through five stages, and each stage draws on features from several versions at once. This page maps one onto the other.",
        intro_style
    ))
    
    # Workflow table
    wf_data = [
        ["Stage", "Workspace Module", "Draws On", "Built"],
        ["1. Site", "Plot & Setbacks", "V1, V2.5", "Yes"],
        ["", "GIS & Smart City Infrastructure", "V2, X+", "Yes"],
        ["2. Design", "Autonomous Studio & Township", "X, X+", "Yes"],
        ["", "Apartment Planning", "V1, V2.5", "Yes"],
        ["", "Parking Layouts", "V1, X+", "Yes"],
        ["", "3D Visualisation", "V2.5", "Yes"],
        ["", "Floor Plans & 3D Deliverables", "V1, V2.5, X+", "Yes"],
        ["", "BIM, DWG & Digital Twin", "V5", "Yes"],
        ["3. Engineering", "Calculations & Multi-Agent Teams", "V1, X+", "Yes"],
        ["", "IS/NBC Compliance Audits", "V2.5, X+", "Yes"],
        ["4. Cost & Programme", "BOQ Takeoff & Quantities", "V1, V2.5, X+", "Yes"],
        ["", "Cost Estimation", "V1", "Yes"],
        ["", "Programme & 4D Progress", "V2.5, V5", "Yes"],
        ["", "Feasibility & ROI", "V2.5", "Yes"],
        ["5. Deliver", "Compliance", "V1, V2.5", "Yes"],
        ["", "Data Reliability", "V2.5", "Yes"],
        ["", "Reports", "V1", "Yes"],
        ["", "Versions & Team", "V1, V4", "Yes"],
    ]
    
    col_widths = [105 * pt, 185 * pt, 95 * pt, 45.87 * pt]  # 430.87 pt total
    t = Table(wf_data, colWidths=col_widths, hAlign="CENTER")
    
    t_style = [
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8.6),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 4.0),
        ('TOPPADDING', (0, 0), (-1, 0), 4.0),
        ('ALIGN', (0, 0), (1, -1), 'LEFT'),
        ('ALIGN', (2, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.4, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, ROW_BG]),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8.6),
        ('TEXTCOLOR', (0, 1), (-1, -1), DARK_TEXT),
        ('TOPPADDING', (0, 1), (-1, -1), 3.2),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 3.2),
        # Stage column bolding
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0, 1), (0, -1), PRIMARY),
    ]
    t.setStyle(TableStyle(t_style))
    story.append(t)
    
    story.append(Spacer(1, 6 * pt))
    
    h3_style = ParagraphStyle(
        "P3H3",
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=15,
        textColor=PRIMARY,
        spaceBefore=4,
        spaceAfter=3,
    )
    bullet_style = ParagraphStyle(
        "P3Bullet",
        fontName="Helvetica",
        fontSize=9.2,
        leading=12.8,
        textColor=colors.HexColor("#1A1A1A"),
        leftIndent=14,
        firstLineIndent=-14,
        spaceAfter=4,
    )
    
    story.append(Paragraph("Cutting across every stage", h3_style))
    story.append(Paragraph(
        "Two capabilities do not sit at a single point in the workflow, which is why they do not appear as a stage of their own.",
        intro_style
    ))
    
    b = get_bullet_html("built")
    story.append(Paragraph(
        f"{b}&nbsp;&nbsp;<b>AI assistance (V3).</b> APT, the optimisers and the AI advisors are reachable from every module, and each draws on the values that module has already computed. The assistant is context-aware by stage rather than being a separate destination.",
        bullet_style
    ))
    story.append(Paragraph(
        f"{b}&nbsp;&nbsp;<b>Data reliability (V2.5).</b> The checks run continuously against every module, but the report is placed in Deliver on purpose. The question it answers is whether the drawing set can be issued, and that is worth asking immediately before the report is generated, not while the design is still moving.",
        bullet_style
    ))
    
    story.append(Spacer(1, 4 * pt))
    note_style = ParagraphStyle(
        "P3Note",
        fontName="Helvetica",
        fontSize=8.8,
        leading=12.4,
        textColor=colors.HexColor("#333333"),
    )
    story.append(Paragraph(
        "<b>Reading order note:</b> a stage is only as trustworthy as the stage before it. Setbacks decide the buildable envelope, the envelope decides tower placement, placement decides areas, areas decide quantities, quantities decide cost and programme. An error at stage 1 propagates through all five, which is the reason the data reliability checks exist at all.",
        note_style
    ))
    story.append(PageBreak())


def build_feature_pages(story):
    """Builds Pages 4 through 15 from feature_data.py with exact typography."""
    from feature_data import PAGES_DATA
    
    # Page metadata (banners, objectives, metrics)
    page_meta = {
        4: {
            "banner": "Aptimizer V1: Core Civil Engineering Planning Platform",
            "objective": "Develop a platform for apartment planning, quantity estimation, cost estimation, and compliance calculations.",
            "metrics": (126, 126, 0, 0),
        },
        5: {
            # Continuation of V1
            "banner": None,
            "objective": None,
            "metrics": None,
        },
        6: {
            "banner": "Aptimizer V2: GIS & Site Intelligence",
            "objective": "Integrate maps, satellite imagery, and geospatial analysis.",
            "metrics": (27, 25, 1, 1),
        },
        7: {
            "banner": "Aptimizer V2.5: Precision, Programme & Assurance",
            "objective": "Make every number defensible: real development controls, a real site layout engine, a real programme, and a stated confidence in the data behind them.",
            "metrics": (116, 116, 0, 0),
        },
        8: {
            # Continuation of V2.5
            "banner": None,
            "objective": None,
            "metrics": None,
        },
        9: {
            "banner": "Aptimizer V3: AI Engineering Platform",
            "objective": "Introduce AI-driven planning and decision support.",
            "metrics": (55, 55, 0, 0),
        },
        10: {
            # Continuation of V3
            "banner": None,
            "objective": None,
            "metrics": None,
        },
        11: {
            "banner": "Aptimizer V4: Enterprise Collaboration",
            "objective": "Enable teamwork and enterprise workflows.",
            "metrics": (13, 13, 0, 0),
        },
        12: {
            "banner": "Aptimizer V5: BIM & Smart Construction",
            "objective": "Prepare for BIM, Digital Twin, and construction monitoring.",
            "metrics": (13, 13, 0, 0),
        },
        13: {
            "banner": "Aptimizer X: AI Civil Engineering Operating System",
            "objective": "A unified AI-powered platform for the entire project lifecycle.",
            "metrics": (55, 55, 0, 0),
        },
        14: {
            # Continuation of X
            "banner": None,
            "objective": None,
            "metrics": None,
        },
        15: {
            "banner": "Aptimizer X+: Future Vision",
            "objective": "A future roadmap beyond Aptimizer X.",
            "metrics": (19, 14, 0, 5),
        },
    }
    
    for p_num in range(4, 16):
        meta = page_meta[p_num]
        sects = PAGES_DATA.get(p_num) or PAGES_DATA.get(str(p_num))
        
        # Add banner / objective / metrics if version start page
        if meta["banner"]:
            story.append(make_banner(meta["banner"]))
            story.append(Spacer(1, 8 * pt))
            story.append(make_objective(meta["objective"]))
            story.append(Spacer(1, 2 * pt))
            tot, b, part, plan = meta["metrics"]
            story.append(make_metrics(tot, b, part, plan))
            story.append(Spacer(1, 4 * pt))
        
        # Add sections and their feature tables
        for s in sects:
            story.append(make_section_header(s["name"]))
            story.append(make_features_table(s["features"]))
            story.append(Spacer(1, 4 * pt))
        
        story.append(PageBreak())


def generate_pdf(output_path):
    """Main execution function to generate the feature list PDF."""
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=MARGIN,
    )
    
    story = []
    
    # Page 1: Cover & Consolidated Summary Table
    build_page_1(story)
    
    # Page 2: Build Status Narrative
    build_page_2(story)
    
    # Page 3: How the Platform Is Used (Workflow Order)
    build_page_3(story)
    
    # Pages 4 to 15: All Version Breakdowns
    build_feature_pages(story)
    
    doc.build(story, canvasmaker=FeatureListCanvas)
    print(f"Generated PDF: {output_path}")


if __name__ == "__main__":
    import shutil
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_pdf = os.path.join(current_dir, "Aptimizer_Feature_List_Updated.pdf")
    output_v2_pdf = os.path.join(current_dir, "Aptimizer_Feature_List_Updated_V2.pdf")
    
    generate_pdf(output_pdf)
    generate_pdf(output_v2_pdf)
    
    # PDF is generated directly in the Jules Apt project folder:
    # - output_pdf: Aptimizer_Feature_List_Updated.pdf
    # - output_v2_pdf: Aptimizer_Feature_List_Updated_V2.pdf

    # Verify page count with pypdf
    reader = PdfReader(output_pdf)
    print(f"VERIFICATION: Generated PDF has exactly {len(reader.pages)} pages.")
    assert len(reader.pages) == 15, f"Expected 15 pages, got {len(reader.pages)}"
    print("SUCCESS: 15-page structure verified!")
