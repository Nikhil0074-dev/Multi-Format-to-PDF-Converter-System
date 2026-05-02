import os
import json
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors

from converters.base_converter import BaseConverter


class IpynbConverter(BaseConverter):

    def convert(self, input_path, output_path):
        raw = self._read_file(input_path)
        try:
            notebook = json.loads(raw)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid notebook JSON: {e}")

        filename = os.path.basename(input_path)
        doc = self._make_doc(output_path)
        styles = self._build_styles()
        story = []

        story.append(Paragraph(f"Notebook: {filename}", styles['nb_title']))
        kernel = notebook.get('metadata', {}).get('kernelspec', {}).get('display_name', 'Unknown')
        story.append(Paragraph(f"Kernel: {kernel}", styles['subtitle']))
        story.append(Spacer(1, 6))
        story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#7c3aed')))
        story.append(Spacer(1, 10))

        cells = notebook.get('cells', [])
        for cell_index, cell in enumerate(cells, 1):
            cell_type = cell.get('cell_type', 'unknown')
            source_lines = cell.get('source', [])
            source = ''.join(source_lines) if isinstance(source_lines, list) else source_lines

            if cell_type == 'markdown':
                story.append(Paragraph(f"[Markdown Cell {cell_index}]", styles['cell_label_md']))
                story.extend(self._render_markdown(source, styles))

            elif cell_type == 'code':
                story.append(Paragraph(f"[Code Cell {cell_index}]", styles['cell_label_code']))
                story.extend(self._render_code(source, styles))

                outputs = cell.get('outputs', [])
                if outputs:
                    story.append(Paragraph("Output:", styles['output_label']))
                    story.extend(self._render_outputs(outputs, styles))

            story.append(Spacer(1, 8))

        doc.build(story)

    def _render_markdown(self, source, styles):
        elements = []
        for line in source.split('\n'):
            stripped = line.strip()
            if not stripped:
                elements.append(Spacer(1, 3))
                continue
            safe = stripped.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            if stripped.startswith('### '):
                elements.append(Paragraph(safe[4:], styles['md_h3']))
            elif stripped.startswith('## '):
                elements.append(Paragraph(safe[3:], styles['md_h2']))
            elif stripped.startswith('# '):
                elements.append(Paragraph(safe[2:], styles['md_h1']))
            elif stripped.startswith('- ') or stripped.startswith('* '):
                elements.append(Paragraph('\u2022 ' + safe[2:], styles['md_li']))
            else:
                elements.append(Paragraph(safe, styles['md_p']))
        return elements

    def _render_code(self, source, styles):
        elements = []
        for i, line in enumerate(source.split('\n'), 1):
            safe = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            leading = len(line) - len(line.lstrip(' '))
            safe = '\u00a0' * leading + safe.lstrip(' ')
            elements.append(Paragraph(
                f'<font color="#7c3aed" size="7">{i:3d}</font>  '
                f'<font face="Courier" size="8.5" color="#1e293b">{safe}</font>',
                styles['code_line']
            ))
        return elements

    def _render_outputs(self, outputs, styles):
        elements = []
        for output in outputs:
            output_type = output.get('output_type', '')
            if output_type in ('stream', 'display_data', 'execute_result'):
                text_data = output.get('text', output.get('data', {}).get('text/plain', []))
                if isinstance(text_data, list):
                    text_data = ''.join(text_data)
                for line in text_data.split('\n'):
                    safe = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                    elements.append(Paragraph(
                        f'<font face="Courier" size="8" color="#374151">{safe}</font>',
                        styles['output_text']
                    ))
            elif output_type == 'error':
                ename = output.get('ename', 'Error')
                evalue = output.get('evalue', '')
                elements.append(Paragraph(
                    f'<font color="#dc2626">{ename}: {evalue}</font>',
                    styles['output_text']
                ))
        return elements

    def _build_styles(self):
        return {
            'nb_title': ParagraphStyle('nb_title', fontName='Helvetica-Bold', fontSize=14,
                                       textColor=colors.HexColor('#1e293b'), spaceAfter=2),
            'subtitle': ParagraphStyle('subtitle', fontName='Helvetica', fontSize=9,
                                       textColor=colors.HexColor('#64748b'), spaceAfter=4),
            'cell_label_code': ParagraphStyle('cell_label_code', fontName='Helvetica-Bold', fontSize=8,
                                              textColor=colors.HexColor('#7c3aed'), spaceAfter=2,
                                              spaceBefore=6),
            'cell_label_md': ParagraphStyle('cell_label_md', fontName='Helvetica-Bold', fontSize=8,
                                            textColor=colors.HexColor('#0ea5e9'), spaceAfter=2,
                                            spaceBefore=6),
            'output_label': ParagraphStyle('output_label', fontName='Helvetica-BoldOblique', fontSize=8,
                                           textColor=colors.HexColor('#64748b'), spaceBefore=3, spaceAfter=2),
            'code_line': ParagraphStyle('code_line', fontName='Courier', fontSize=8.5, leading=13,
                                        backColor=colors.HexColor('#faf5ff'), wordWrap='CJK'),
            'output_text': ParagraphStyle('output_text', fontName='Courier', fontSize=8.5, leading=13,
                                          backColor=colors.HexColor('#f0f9ff'), wordWrap='CJK'),
            'md_h1': ParagraphStyle('md_h1', fontName='Helvetica-Bold', fontSize=14,
                                    textColor=colors.HexColor('#1d4ed8'), spaceAfter=5, spaceBefore=6),
            'md_h2': ParagraphStyle('md_h2', fontName='Helvetica-Bold', fontSize=12,
                                    textColor=colors.HexColor('#1d4ed8'), spaceAfter=4, spaceBefore=4),
            'md_h3': ParagraphStyle('md_h3', fontName='Helvetica-Bold', fontSize=11,
                                    textColor=colors.HexColor('#374151'), spaceAfter=3),
            'md_p': ParagraphStyle('md_p', fontName='Helvetica', fontSize=10, leading=14,
                                   textColor=colors.HexColor('#374151'), spaceAfter=3),
            'md_li': ParagraphStyle('md_li', fontName='Helvetica', fontSize=10, leading=13,
                                    leftIndent=12, textColor=colors.HexColor('#374151'), spaceAfter=2),
        }
