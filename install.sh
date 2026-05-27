#!/bin/bash

# ============================================================
#  ADVANCED 3D EXPENSE TRACKER - STREAMLIT EDITION
#  Linux Installer | Developed by issu321
#  https://github.com/issu321/Advanced-CLI-Expense-Tracker
# ============================================================

set -e

# =========================
# COLORS
# =========================
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

clear

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║      💎 ADVANCED 3D EXPENSE TRACKER INSTALLER 💎            ║"
echo "║                                                              ║"
echo "║             STREAMLIT EDITION - LINUX SETUP                 ║"
echo "║                                                              ║"
echo "║                  Developed by issu321                       ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

echo -e "${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "📊 Interactive 3D Expense Analytics"
echo -e "💰 Budget & Savings Management"
echo -e "📈 Real-Time Financial Insights"
echo -e "🌐 Streamlit Powered Dashboard"
echo -e "${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# ============================================================
# VENV CONFIRMATION
# ============================================================

echo -e "${YELLOW}[IMPORTANT NOTICE]${NC}"
echo ""
echo "Python Virtual Environment (venv) is REQUIRED."
echo ""
echo "Before continuing:"
echo " • Create a Python virtual environment"
echo " • Activate the venv"
echo ""
echo -e "Type ${GREEN}yes${NC}  -> Continue installation"
echo -e "Type ${RED}exit${NC} -> Stop installer"
echo ""

read -p "Enter choice (yes/exit): " USER_INPUT

# ============================================================
# EXIT SAFELY
# ============================================================

if [ "$USER_INPUT" = "exit" ]; then
    echo ""
    echo -e "${RED}[EXIT]${NC} Installer terminated by user."
    echo ""
    echo "Create and activate venv first:"
    echo "--------------------------------------------------"
    echo "python3 -m venv venv"
    echo "source venv/bin/activate"
    echo "bash install.sh"
    echo "--------------------------------------------------"
    echo ""
    exit 1
fi

# ============================================================
# INVALID INPUT
# ============================================================

if [ "$USER_INPUT" != "yes" ]; then
    echo ""
    echo -e "${RED}[ERROR]${NC} Invalid input detected."
    echo "Run installer again and type only: yes or exit"
    echo ""
    exit 1
fi

echo ""
echo -e "${GREEN}[OK]${NC} Continuing installation..."
echo ""

# ============================================================
# PYTHON VERSION CHECK
# ============================================================

PYTHON_VERSION=$(python3 -c 'import sys; print(sys.version_info.major, sys.version_info.minor)' | tr ' ' '.')

echo -e "${GREEN}[OK]${NC} Python $PYTHON_VERSION detected"
echo ""

# ============================================================
# INSTALLATION PROCESS
# ============================================================

echo -e "${BLUE}[1/4]${NC} Upgrading pip..."
pip install --upgrade pip -q

echo ""
echo -e "${BLUE}[2/4]${NC} Installing dependencies..."
pip install -r requirements.txt -q

echo ""
echo -e "${BLUE}[3/4]${NC} Initializing SQLite database..."
python3 -c "import sqlite3; conn = sqlite3.connect('expense_data.db'); conn.close()"

echo ""
echo -e "${BLUE}[4/4]${NC} Finalizing Streamlit environment..."
sleep 1

# ============================================================
# INSTALLATION COMPLETE
# ============================================================

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║               ✅ INSTALLATION COMPLETE ✅                   ║"
echo "║                                                              ║"
echo "║         Advanced 3D Expense Tracker is Ready                ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

echo -e "${GREEN}[SUCCESS]${NC} Database and dependencies configured."
echo ""

# ============================================================
# LAUNCH APPLICATION
# ============================================================

echo -e "${CYAN}🎉 Launching Advanced 3D Expense Tracker...${NC}"
echo -e "${GREEN}🌐 Open your browser at:${NC} http://localhost:8501"
echo ""

python3 -m streamlit run streamlit_app.py