import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT


class BaseConverter:
    PAGE_WIDTH, PAGE_HEIGHT = A4
    MARGIN = 15 * mm

    def convert(self, input_path, output_path):
        raise NotImplementedError("Subclasses must implement convert()")

    def _make_doc(self, output_path):
        return SimpleDocTemplate(
            output_path,
            pagesize=A4,
            leftMargin=self.MARGIN,
            rightMargin=self.MARGIN,
            topMargin=self.MARGIN,
            bottomMargin=self.MARGIN
        )

    def _read_file(self, path):
        encodings = ['utf-8', 'latin-1', 'cp1252', 'ascii']
        for enc in encodings:
            try:
                with open(path, 'r', encoding=enc) as f:
                    return f.read()
            except (UnicodeDecodeError, UnicodeError):
                continue
        raise ValueError(f"Cannot read file with supported encodings: {path}")
