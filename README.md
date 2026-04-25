# Multi-Format to PDF Converter System

A universal file-to-PDF converter that allows users to convert various file formats into a standardized PDF document.

## Supported Conversions

- `.py` → `.pdf`
- `.ipynb` → `.pdf`
- `.c` → `.pdf`
- `.html` → `.pdf`

## Features

- **File Upload**: Upload `.py`, `.ipynb`, `.c`, `.html` files with automatic file type detection
- **Conversion Engine**: Convert files into structured PDF format while maintaining layout and formatting
- **Syntax Highlighting**: Highlight code for `.py` and `.c` files to improve readability
- **Preview System**: Preview PDF before downloading
- **Download**: Export final PDF file

## Project Structure

```
multi-to-pdf/
│
├── frontend/
│   ├── upload.html
│   └── preview.html
│
├── backend/
│   ├── app.py
│   │
│   ├── converters/
│   │   ├── py_to_pdf.py
│   │   ├── ipynb_to_pdf.py
│   │   ├── c_to_pdf.py
│   │   └── html_to_pdf.py
│   │
│   ├── services/
│   │   ├── syntax_highlighter.py
│   │   └── pdf_generator.py
│   │
│   └── utils/
│       └── file_handler.py
│
├── uploads/
├── outputs/
│
├── requirements.txt
└── README.md
```

## Technologies Used

- **Backend**: Python (Flask)
- **PDF Generation**: ReportLab, WeasyPrint
- **Conversion**: nbconvert, Pygments, pdfkit / wkhtmltopdf
- **Frontend**: HTML, CSS, JavaScript

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install wkhtmltopdf (for HTML to PDF conversion):
   - Download from: https://wkhtmltopdf.org/downloads.html
   - Add to system PATH

3. Run the Flask application:
```bash
python backend/app.py
```

4. Open your browser and navigate to `http://localhost:5000`

## Usage

1. Open the upload page in your browser
2. Select or drag-and-drop your file
3. Click "Convert to PDF"
4. Preview the generated PDF
5. Download the PDF file

## Example Use Cases

- Convert Python code → PDF for assignment submission
- Convert Jupyter Notebook → PDF report
- Convert C program → printable document
- Convert HTML webpage → PDF for sharing

## Future Enhancements

- Batch file conversion
- Drag-and-drop interface
- AI-based code formatting
- Cloud storage integration
- Watermark & password-protected PDFs
