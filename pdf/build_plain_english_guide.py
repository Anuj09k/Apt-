import json
import os
import sys
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

# Colors
PRIMARY = colors.Color(0.121569, 0.305882, 0.47451)        # #1F4E79 - Deep Civil Navy
SECTION_BLUE = colors.Color(0.180392, 0.458824, 0.713725)   # #2E75B6 - Category Blue
BUILT_GREEN = colors.Color(0.117647, 0.517647, 0.286275)    # #1E8449 - Built Green
DARK_TEXT = colors.Color(0.10, 0.10, 0.10)
MUTED_TEXT = colors.Color(0.35, 0.35, 0.35)
ROW_BG = colors.Color(0.95, 0.965, 0.98)
BORDER_COLOR = colors.Color(0.82, 0.86, 0.90)
FOOTER_GREY = colors.Color(0.50, 0.50, 0.50)

PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN = 14 * mm
USABLE_WIDTH = PAGE_WIDTH - 2 * MARGIN

class NumberedCanvas(canvas.Canvas):
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

    def draw_decorations(self, total_pages):
        self.saveState()
        # Header (Pages 2+)
        if self._pageNumber > 1:
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(PRIMARY)
            self.drawString(MARGIN, PAGE_HEIGHT - 9 * mm, "APTIMIZER  |  COMPLETE BUILT FEATURES GUIDE")
            self.setFont("Helvetica", 8)
            self.setFillColor(MUTED_TEXT)
            self.drawRightString(PAGE_WIDTH - MARGIN, PAGE_HEIGHT - 9 * mm, "Plain-English Meaning & Memory Anchors")
            self.setStrokeColor(BORDER_COLOR)
            self.setLineWidth(0.5)
            self.line(MARGIN, PAGE_HEIGHT - 11 * mm, PAGE_WIDTH - MARGIN, PAGE_HEIGHT - 11 * mm)

        # Footer (All pages)
        self.setFont("Helvetica", 7.5)
        self.setFillColor(FOOTER_GREY)
        self.drawString(MARGIN, 9 * mm, "Aptimizer Civil AI & Architectural Design Platform  •  All 417 Verified Built Features")
        self.drawRightString(PAGE_WIDTH - MARGIN, 9 * mm, f"Page {self._pageNumber} of {total_pages}")
        self.setStrokeColor(BORDER_COLOR)
        self.setLineWidth(0.5)
        self.line(MARGIN, 12 * mm, PAGE_WIDTH - MARGIN, 12 * mm)
        self.restoreState()

print("Base setup complete.")
