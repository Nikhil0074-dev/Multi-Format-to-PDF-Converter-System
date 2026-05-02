@echo off
echo Multi-Format PDF Converter - Backend Startup
echo =============================================

cd /d "%~dp0backend"

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python 3.8 or higher from https://www.python.org
    pause
    exit /b 1
)

echo Installing dependencies...
pip install flask flask-cors pypdf reportlab pygments werkzeug --quiet

echo.
echo Starting Flask server on http://localhost:5000
echo Open frontend\index.html in your browser once the server starts.
echo Press Ctrl+C to stop the server.
echo.

python app.py
pause
