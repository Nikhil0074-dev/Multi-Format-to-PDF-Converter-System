#!/bin/bash
echo "Multi-Format PDF Converter - Backend Startup"
echo "============================================="

# Move to script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/backend"

# Check Python
if ! command -v python3 &>/dev/null; then
    if ! command -v python &>/dev/null; then
        echo "ERROR: Python is not installed."
        echo "Install it with: sudo apt install python3   (Ubuntu/Debian)"
        echo "                 brew install python3       (macOS)"
        exit 1
    fi
    PY=python
else
    PY=python3
fi

echo "Using: $($PY --version)"

# Install deps
echo "Installing dependencies..."
$PY -m pip install flask flask-cors pypdf reportlab pygments werkzeug --quiet

echo ""
echo "Starting Flask server on http://localhost:5000"
echo "Open frontend/index.html in your browser once the server is ready."
echo "Press Ctrl+C to stop."
echo ""

$PY app.py
