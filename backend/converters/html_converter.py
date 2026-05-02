import os
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors

from converters.base_converter import BaseConverter


class HtmlConverter(BaseConverter):

    TAG_PATTERNS = [
        (re.compile(r'<h1[^>]*>(.*?)</h1>', re.IGNORECASE | re.DOTALL), 'h1'),
        (re.compile(r'<h2[^>]*>(.*?)</h2>', re.IGNORECASE | re.DOTALL), 'h2'),
        (re.compile(r'<h3[^>]*>(.*?)</h3>', re.IGNORECASE | re.DOTALL), 'h3'),
        (re.compile(r'<h[456][^>]*>(.*?)</h[456]>', re.IGNORECASE | re.DOTALL), 'h4'),
        (re.compile(r'<p[^>]*>(.*?)</p>', re.IGNORECASE | re.DOTALL), 'p'),
        (re.compile(r'<li[^>]*>(.*?)</li>', re.IGNORECASE | re.DOTALL), 'li'),
    ]

    def convert(self, input_path, output_path):
        html_content = self._read_file(input_path)
        filename = os.path.basename(input_path)

        doc = self._make_doc(output_path)
        styles = self._build_styles()
        story = []

        story.append(Paragraph(f"File: {filename}", styles['title']))
        story.append(Paragraph("Language: HTML", styles['subtitle']))
        story.append(Spacer(1, 6))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#f97316')))
        story.append(Spacer(1, 8))

        story.extend(self._parse_html(html_content, styles))

        doc.build(story)

    def _strip_tags(self, text):
        clean = re.sub(r'<[^>]+>', '', text)
        clean = clean.replace('&nbsp;', ' ').replace('&amp;', '&')
        clean = clean.replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"')
        return clean.strip()

    def _parse_html(self, html, styles):
        elements = []

        # Remove script and style blocks
        html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
        html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)

        # Extract title tag
        title_match = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
        if title_match:
            title_text = self._strip_tags(title_match.group(1))
            if title_text:
                elements.append(Paragraph(title_text, styles['page_title']))
                elements.append(Spacer(1, 8))

        # Track positions to parse in order
        all_matches = []
        for pattern, tag_type in self.TAG_PATTERNS:
            for m in pattern.finditer(html):
                all_matches.append((m.start(), tag_type, self._strip_tags(m.group(1))))

        all_matches.sort(key=lambda x: x[0])

        for _, tag_type, text in all_matches:
            if not text:
                continue
            style = styles.get(tag_type, styles['p'])
            elements.append(Paragraph(text, style))
            elements.append(Spacer(1, 4))

        # If no structured content found, render as source
        if not all_matches:
            lines = html.split('\n')
            for i, line in enumerate(lines, 1):
                safe = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                leading = len(line) - len(line.lstrip(' '))
                safe = '\u00a0' * leading + safe.lstrip(' ')
                elements.append(Paragraph(
                    f'<font color="#6b7280" size="7">{i:4d}</font>  '
                    f'<font face="Courier" size="8.5">{safe}</font>',
                    styles['code_line']
                ))

        return elements

    def _build_styles(self):
        return {
            'title': ParagraphStyle('title', fontName='Helvetica-Bold', fontSize=13,
                                    textColor=colors.HexColor('#1e293b'), spaceAfter=2),
            'subtitle': ParagraphStyle('subtitle', fontName='Helvetica', fontSize=9,
                                       textColor=colors.HexColor('#64748b'), spaceAfter=4),
            'page_title': ParagraphStyle('page_title', fontName='Helvetica-Bold', fontSize=16,
                                         textColor=colors.HexColor('#0f172a'), spaceAfter=6),
            'h1': ParagraphStyle('h1', fontName='Helvetica-Bold', fontSize=14,
                                 textColor=colors.HexColor('#1d4ed8'), spaceAfter=6, spaceBefore=8),
            'h2': ParagraphStyle('h2', fontName='Helvetica-Bold', fontSize=12,
                                 textColor=colors.HexColor('#1d4ed8'), spaceAfter=5, spaceBefore=6),
            'h3': ParagraphStyle('h3', fontName='Helvetica-Bold', fontSize=11,
                                 textColor=colors.HexColor('#374151'), spaceAfter=4, spaceBefore=4),
            'h4': ParagraphStyle('h4', fontName='Helvetica-BoldOblique', fontSize=10,
                                 textColor=colors.HexColor('#374151'), spaceAfter=3),
            'p': ParagraphStyle('p', fontName='Helvetica', fontSize=10,
                                textColor=colors.HexColor('#374151'), spaceAfter=4, leading=14),
            'li': ParagraphStyle('li', fontName='Helvetica', fontSize=10,
                                 textColor=colors.HexColor('#374151'), leftIndent=15,
                                 spaceAfter=3, leading=13),
            'code_line': ParagraphStyle('code_line', fontName='Courier', fontSize=8.5,
                                        leading=13, textColor=colors.HexColor('#1e293b'),
                                        backColor=colors.HexColor('#fff7ed'), wordWrap='CJK'),
        }
