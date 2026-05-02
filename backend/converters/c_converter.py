import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors

from converters.base_converter import BaseConverter


class CConverter(BaseConverter):

    def convert(self, input_path, output_path):
        source_code = self._read_file(input_path)
        filename = os.path.basename(input_path)
        ext = filename.rsplit('.', 1)[-1].upper()
        lang_label = {'C': 'C', 'CPP': 'C++', 'H': 'C Header'}.get(ext, ext)

        doc = self._make_doc(output_path)
        styles = self._build_styles()
        story = []

        story.append(Paragraph(f"File: {filename}", styles['title']))
        story.append(Paragraph(f"Language: {lang_label}", styles['subtitle']))
        story.append(Spacer(1, 6))

        story.append(Table(
            [['']],
            colWidths=[A4[0] - 30 * mm],
            style=TableStyle([
                ('LINEBELOW', (0, 0), (-1, -1), 1, colors.HexColor('#16a34a')),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ])
        ))

        lines = source_code.split('\n')
        for i, line in enumerate(lines, 1):
            safe_line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            leading_spaces = len(line) - len(line.lstrip(' '))
            safe_line = '\u00a0' * leading_spaces + safe_line.lstrip(' ')

            line_para = Paragraph(
                f'<font color="#6b7280" size="7">{i:4d}</font>  '
                f'<font face="Courier" size="8.5" color="#1e293b">{safe_line}</font>',
                styles['code_line']
            )
            story.append(line_para)

        doc.build(story)

    def _build_styles(self):
        return {
            'title': ParagraphStyle(
                'title',
                fontName='Helvetica-Bold',
                fontSize=13,
                textColor=colors.HexColor('#1e293b'),
                spaceAfter=2,
            ),
            'subtitle': ParagraphStyle(
                'subtitle',
                fontName='Helvetica',
                fontSize=9,
                textColor=colors.HexColor('#64748b'),
                spaceAfter=4,
            ),
            'code_line': ParagraphStyle(
                'code_line',
                fontName='Courier',
                fontSize=8.5,
                leading=13,
                textColor=colors.HexColor('#1e293b'),
                backColor=colors.HexColor('#f0fdf4'),
                wordWrap='CJK',
            ),
        }
