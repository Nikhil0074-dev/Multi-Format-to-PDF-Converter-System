import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors

from converters.base_converter import BaseConverter

LANG_MAP = {
    'txt': 'Plain Text',
    'java': 'Java',
    'js': 'JavaScript',
    'css': 'CSS',
    'ts': 'TypeScript',
    'rb': 'Ruby',
    'go': 'Go',
    'rs': 'Rust',
    'sh': 'Shell Script',
    'md': 'Markdown',
    'xml': 'XML',
    'json': 'JSON',
    'yaml': 'YAML',
    'yml': 'YAML',
    'sql': 'SQL',
}

ACCENT_MAP = {
    'java': '#f59e0b',
    'js': '#eab308',
    'css': '#0ea5e9',
    'ts': '#3b82f6',
    'rb': '#ef4444',
    'go': '#06b6d4',
    'rs': '#f97316',
    'sh': '#10b981',
    'sql': '#8b5cf6',
    'json': '#64748b',
    'xml': '#64748b',
    'yaml': '#64748b',
    'yml': '#64748b',
    'md': '#6366f1',
}


class TextConverter(BaseConverter):

    def convert(self, input_path, output_path):
        source = self._read_file(input_path)
        filename = os.path.basename(input_path)
        ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else 'txt'
        lang = LANG_MAP.get(ext, ext.upper())
        accent = ACCENT_MAP.get(ext, '#64748b')

        doc = self._make_doc(output_path)
        styles = self._build_styles(accent)
        story = []

        story.append(Paragraph(f"File: {filename}", styles['title']))
        story.append(Paragraph(f"Language: {lang}", styles['subtitle']))
        story.append(Spacer(1, 6))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor(accent)))
        story.append(Spacer(1, 6))

        lines = source.split('\n')
        for i, line in enumerate(lines, 1):
            safe = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            leading = len(line) - len(line.lstrip(' '))
            safe = '\u00a0' * leading + safe.lstrip(' ')
            story.append(Paragraph(
                f'<font color="#9ca3af" size="7">{i:4d}</font>  '
                f'<font face="Courier" size="8.5" color="#1e293b">{safe}</font>',
                styles['code_line']
            ))

        doc.build(story)

    def _build_styles(self, accent):
        return {
            'title': ParagraphStyle('title', fontName='Helvetica-Bold', fontSize=13,
                                    textColor=colors.HexColor('#1e293b'), spaceAfter=2),
            'subtitle': ParagraphStyle('subtitle', fontName='Helvetica', fontSize=9,
                                       textColor=colors.HexColor('#64748b'), spaceAfter=4),
            'code_line': ParagraphStyle('code_line', fontName='Courier', fontSize=8.5,
                                        leading=13, backColor=colors.HexColor('#f8fafc'),
                                        wordWrap='CJK'),
        }
