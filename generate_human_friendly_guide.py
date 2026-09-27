"""
Aptimizer Built Features Plain-English Guide PDF Generator
Creates an authentic, executive-ready, human-understandable guide to all 417 built features.
"""

import os
import sys
import json
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

# -------------------------------------------------------------------------
# PALETTE
# -------------------------------------------------------------------------
PRIMARY = colors.Color(0.121569, 0.305882, 0.47451)        # #1F4E79 - Deep Civil Navy
SECONDARY = colors.Color(0.180392, 0.458824, 0.713725)      # #2E75B6 - Category Header Blue
ACCENT_GREEN = colors.Color(0.117647, 0.517647, 0.286275)   # #1E8449 - Built & Running
DARK_TEXT = colors.Color(0.10, 0.10, 0.10)                  # #1A1A1A - Dark Body Text
MUTED_TEXT = colors.Color(0.35, 0.35, 0.35)                 # #595959 - Muted Text
ROW_BG = colors.Color(0.95, 0.965, 0.98)                    # #F2F6FA - Soft Alternating Row
BORDER_COLOR = colors.Color(0.82, 0.86, 0.90)               # #D1DCE6 - Table Grid Border
FOOTER_GREY = colors.Color(0.50, 0.50, 0.50)

PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN = 15 * mm
USABLE_WIDTH = PAGE_WIDTH - 2 * MARGIN

class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas for dynamic total page count."""
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
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        self.saveState()
        # Top banner on page 2+
        if self._pageNumber > 1:
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(PRIMARY)
            self.drawString(MARGIN, PAGE_HEIGHT - 10 * mm, "APTIMIZER  |  COMPLETE BUILT FEATURES GUIDE")
            self.setFont("Helvetica", 8)
            self.setFillColor(MUTED_TEXT)
            self.drawRightString(PAGE_WIDTH - MARGIN, PAGE_HEIGHT - 10 * mm, "In Plain English for Everyone")
            self.setStrokeColor(BORDER_COLOR)
            self.setLineWidth(0.5)
            self.line(MARGIN, PAGE_HEIGHT - 12 * mm, PAGE_WIDTH - MARGIN, PAGE_HEIGHT - 12 * mm)

        # Footer
        self.setFont("Helvetica", 7.5)
        self.setFillColor(FOOTER_GREY)
        self.drawString(MARGIN, 10 * mm, "Aptimizer Civil AI Platform  •  All 417 Verified Built Features")
        page_str = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(PAGE_WIDTH - MARGIN, 10 * mm, page_str)
        self.setStrokeColor(BORDER_COLOR)
        self.setLineWidth(0.5)
        self.line(MARGIN, 13 * mm, PAGE_WIDTH - MARGIN, 13 * mm)
        self.restoreState()

print("Canvas defined.")
