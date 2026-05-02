import os
import math
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import Color
from pypdf import PdfReader, PdfWriter
import io


class WatermarkService:
    POSITIONS = {
        'center': (0.5, 0.5),
        'top': (0.5, 0.85),
        'bottom': (0.5, 0.15),
        'top-left': (0.15, 0.85),
        'top-right': (0.85, 0.85),
        'bottom-left': (0.15, 0.15),
        'bottom-right': (0.85, 0.15),
    }

    def _create_watermark_pdf(self, page_width, page_height, text, position, opacity, font_size):
        packet = io.BytesIO()
        c = canvas.Canvas(packet, pagesize=(page_width, page_height))

        pos_key = position if position in self.POSITIONS else 'center'
        x_ratio, y_ratio = self.POSITIONS[pos_key]
        x = page_width * x_ratio
        y = page_height * y_ratio

        # Set opacity via color with alpha
        r, g, b = 0.5, 0.5, 0.5
        c.setFillColor(Color(r, g, b, alpha=opacity))
        c.setFont("Helvetica-Bold", font_size)

        # Rotate for diagonal watermark on center position
        c.saveState()
        if pos_key == 'center':
            c.translate(x, y)
            c.rotate(45)
            c.drawCentredString(0, 0, text)
        else:
            c.translate(x, y)
            c.drawCentredString(0, 0, text)

        c.restoreState()
        c.save()
        packet.seek(0)
        return packet

    def apply_watermark(self, pdf_path, text, position='center', opacity=0.3, font_size=48):
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        reader = PdfReader(pdf_path)
        writer = PdfWriter()

        for page in reader.pages:
            page_width = float(page.mediabox.width)
            page_height = float(page.mediabox.height)

            watermark_pdf_bytes = self._create_watermark_pdf(
                page_width, page_height, text, position, opacity, font_size
            )

            watermark_reader = PdfReader(watermark_pdf_bytes)
            watermark_page = watermark_reader.pages[0]

            page.merge_page(watermark_page)
            writer.add_page(page)

        temp_path = pdf_path + '.tmp'
        with open(temp_path, 'wb') as f:
            writer.write(f)

        os.replace(temp_path, pdf_path)
        return pdf_path
