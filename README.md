### Multi-Format PDF Converter

==========================

A professional file-to-PDF conversion system with batch processing,
drag-and-drop interface, and watermarking.


SUPPORTED FILE FORMATS
-----------------------
  .py       Python source files (with line numbers)
  .ipynb    Jupyter Notebooks (cells + outputs)
  .c / .cpp C and C++ source files
  .html     HTML files (rendered structure)
  .txt      Plain text files
  .java     Java source files
  .js       JavaScript files
  .css      CSS stylesheets


REQUIREMENTS
------------
  Python 3.8+
  pip


INSTALLATION
------------

1. Install Python dependencies:

    pip install flask flask-cors pypdf reportlab pygments werkzeug

   Or using requirements.txt:

    pip install -r requirements.txt


RUNNING THE APPLICATION
-----------------------

Step 1 - Start the Flask backend:

    cd backend
    python app.py

    The server will start at: http://localhost:5000
    You should see: Running on http://127.0.0.1:5000

Step 2 - Open the frontend:

    Open frontend/index.html in any modern web browser.
    Double-click the file or drag it into a browser window.


USAGE
-----

1. The status indicator in the top-right shows "Server Online" when the
   backend is connected.

2. Drag files into the drop zone, or click to browse and select files.
   Multiple files can be added at once.

3. (Optional) Enable and configure the watermark in the right panel:
   - Enter watermark text (e.g. "CONFIDENTIAL", "DRAFT")
   - Choose position: center, top, bottom, corners
   - Adjust opacity and font size with sliders

4. Click "Convert N Files" to start batch conversion.
   Each file shows its status: Pending, Converting, Done, or Error.

5. Download individual PDFs from the Results panel on the right,
   or click "Download ZIP" to get all converted files in one archive.


PROJECT STRUCTURE
-----------------

  multi-pdf-converter/
  |
  +-- frontend/
  |   +-- index.html              Single-page app (HTML + React)
  |
  +-- backend/
  |   +-- app.py                  Flask API server
  |   +-- converters/
  |   |   +-- base_converter.py   Base class for all converters
  |   |   +-- py_converter.py     Python to PDF
  |   |   +-- ipynb_converter.py  Jupyter Notebook to PDF
  |   |   +-- c_converter.py      C/C++ to PDF
  |   |   +-- html_converter.py   HTML to PDF
  |   |   +-- text_converter.py   Text/generic code to PDF
  |   +-- services/
  |   |   +-- batch_processor.py  Manages multi-file conversion
  |   |   +-- watermark.py        Watermark overlay engine
  |   +-- utils/
  |       +-- file_handler.py     File system utilities
  |
  +-- uploads/                    Uploaded files (auto-created)
  +-- outputs/                    Converted PDFs (auto-created)
  +-- temp/                       Temporary files for ZIP (auto-created)
  +-- requirements.txt
  +-- README.md


API ENDPOINTS
-------------

  GET  /api/health             Check server status
  POST /api/upload             Upload one or more files
  POST /api/convert            Convert uploaded files to PDF
  GET  /api/download/<name>    Download a single PDF
  POST /api/download-zip       Download multiple PDFs as ZIP
  POST /api/cleanup            Delete uploaded/output files by ID


WATERMARK OPTIONS
-----------------

  Text     : Any string (e.g. "CONFIDENTIAL", "DRAFT", "SUBMITTED")
  Position : center, top, bottom, top-left, top-right, bottom-left, bottom-right
  Opacity  : 5% to 90% (lower = lighter)
  Font Size: 20 to 96pt


TROUBLESHOOTING
---------------

  "Server Offline" shown in UI:
    - Make sure you ran "python app.py" in the backend folder
    - Check that port 5000 is not in use by another application
    - Look for error messages in the terminal where Flask is running

  File conversion fails:
    - Check the error message shown in the file item
    - Ensure the file is valid and not corrupted
    - Check terminal output for Python stack traces

  ZIP download does not start:
    - Some browsers block automatic downloads; check the downloads bar
    - Ensure at least one file was converted successfully

  Port 5000 already in use:
    - Change the port in backend/app.py:  app.run(port=5001)
    - Update the API constant in frontend/index.html to match:
        const API = 'http://localhost:5001/api';


NOTES
-----

  - Files are stored in uploads/ and outputs/ during the session.
    You can safely delete these folders to free up space.
  - The maximum upload size is 50 MB per request.
  - The frontend connects to http://localhost:5000 by default.
    If you change the backend port, update the API constant at the
    top of frontend/index.html accordingly.
