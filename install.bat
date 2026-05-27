@echo off
REM Advanced 3D Expense Tracker - Streamlit Edition - Windows Installer
REM Developed by issu321
REM https://github.com/issu321/Advanced-CLI-Expense-Tracker

echo ╔══════════════════════════════════════════════════════════════╗
echo ║  ADVANCED 3D EXPENSE TRACKER - STREAMLIT EDITION           ║
echo ║  Windows Installer | Developed by issu321                  ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH.
    echo Please install Python 3.11+ from https://python.org
    pause
    exit /b 1
)

echo ✓ Python detected

if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

echo 🚀 Activating virtual environment...
call venv\Scripts\activate.bat

echo ⬆️  Upgrading pip...
python -m pip install --upgrade pip

echo 📥 Installing dependencies...
pip install -r requirements.txt

echo 🗄️  Initializing database...
python -c "import sqlite3; conn = sqlite3.connect('expense_data.db'); conn.close()"

echo.
echo ✅ Installation complete!
echo.
echo 🎉 Starting Advanced 3D Expense Tracker...
echo    Open your browser at: http://localhost:8501
echo.

streamlit run app.py

pause
