# <div align="center">🚀 Advanced 3D Expense Tracker</div>

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?style=flat-square&logo=python&logoColor=white&color=%2300d4ff)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Web%20App-red?style=flat-square&logo=streamlit&logoColor=white&color=%23ff4b4b)](https://streamlit.io)
[![Plotly](https://img.shields.io/badge/Plotly-3D%20Charts-blue?style=flat-square&logo=plotly&logoColor=white&color=%233f4f75)](https://plotly.com)
[![SQLite](https://img.shields.io/badge/SQLite-Database-yellow?style=flat-square&color=%23ffee00)](https://sqlite.org)
[![License](https://img.shields.io/badge/License-MIT-red?style=flat-square&color=%23ff3333)](LICENSE)

**A futuristic, multi-user 3D web-based financial management system with AI insights, Three.js animations, and cyberpunk aesthetics.**

*Developed by [issu321](https://github.com/issu321)*

</div>

---

## 🌌 Project Introduction

Welcome to the **Advanced 3D Expense Tracker** — a next-generation web-based personal finance application powered by **Streamlit** and **Three.js**.

Transform your browser into a futuristic financial command center with:
- 🎨 **3D animated cyberpunk UI** with neon glow effects
- 📊 **Interactive 3D charts** powered by Plotly
- ✨ **Three.js particle background** with floating wireframe cubes
- 🤖 **AI financial insights** engine
- 👥 **Multi-user system** with secure authentication

> *"Your money, your dashboard, your rules."*

---

## ✨ Features Overview

| Feature | Description |
|---------|-------------|
| 👥 **Multi-User System** | Secure registration & login with SHA-256 password hashing |
| 💸 **Expense Tracking** | Add, view, edit, delete, search, and categorize expenses |
| 💰 **Income Tracking** | Log multiple income sources with full history |
| 📊 **3D Budget Gauges** | Interactive gauge charts showing budget vs actual spending |
| 🎯 **Savings Goals** | Circular progress indicators with 3D styling |
| 🔄 **Recurring Expenses** | Manage subscriptions, rent, bills with auto-simulation |
| 📈 **3D Analytics** | 3D bar charts, 3D line charts, pie charts, trend analysis |
| 🤖 **AI Insights** | Smart suggestions, budget alerts, spending comparisons |
| 📤 **Export System** | CSV and TXT report generation with download buttons |
| 🔍 **Search & Filter** | Advanced filtering by category, date range, keywords |
| 🎨 **Cyberpunk UI** | Neon colors, 3D card hover effects, scanlines, floating animations |
| 🌐 **Three.js Background** | Animated particles, floating wireframe cubes, grid floor |

---

## 🚀 Installation Guide

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)

### Quick Start

```bash
# Clone the repository
git clone https://github.com/issu321/Advanced-CLI-Expense-Tracker.git
cd Advanced-CLI-Expense-Tracker
```

---

## 🪟 Windows Setup

### Option 1: Automatic Installation (Recommended)
```cmd
install.bat
```

### Option 2: Manual Installation
```cmd
python -m venv venv
venv\Scriptsctivate
pip install -r requirements.txt
streamlit run app.py
```

Then open your browser at: **http://localhost:8501**

---

## 🐧 Linux Setup

### Option 1: Automatic Installation (Recommended)
```bash
chmod +x install.sh
./install.sh
```

### Option 2: Manual Installation
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Then open your browser at: **http://localhost:8501**

---

## 📖 Usage Instructions

### First Launch

When you run the application:
1. 🎬 **3D Login Screen** — Cyberpunk-styled authentication with neon text
2. 🔐 **Register or Login** — Create an account or sign in
3. 🏠 **3D Dashboard** — Navigate through the futuristic sidebar menu

### Sidebar Navigation

```
🏠 Dashboard        → Overview with metric cards & recent activity
💸 Expenses         → Add, view, edit, search expenses + 3D bar chart
💰 Income           → Track income + income vs expense comparison
📊 Budgets          → Set budgets + 3D gauge visualizations
🎯 Savings           → Create goals + circular progress indicators
🔄 Recurring         → Manage subscriptions + auto-simulation
📈 Analytics         → 3D charts, trends, financial summary
🤖 AI Insights      → Smart financial suggestions & alerts
📤 Export           → Download CSV and TXT reports
```

---

## 📸 Screenshots

### 🎬 3D Login Screen
```
╔══════════════════════════════════════════════════════════════╗
║  🔮 ADVANCED 3D EXPENSE TRACKER                                ║
║  MULTI-USER • AI INSIGHTS • 3D ANALYTICS                       ║
╚══════════════════════════════════════════════════════════════╝

    ┌─────────────────────────────────────────┐
    │  🔐 LOGIN        │  📝 REGISTER         │
    │  Username: [________]                    │
    │  Password: [________]                  │
    │  [🚀 LAUNCH]                           │
    └─────────────────────────────────────────┘

    [Background: Three.js particles + floating cubes]
```

### 📊 3D Dashboard
```
┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│ $5,200.00   │  │ $2,100.00   │  │ $3,100.00   │  │ $800.00     │
│ TOTAL       │  │ TOTAL       │  │ NET         │  │ SAVINGS     │
│ INCOME      │  │ EXPENSES    │  │ BALANCE     │  │             │
└─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘

⚡ QUICK ACTIONS: [➕ Add Expense] [➕ Add Income] [🎯 Add Goal] [📊 Analytics]
```

### 📈 3D Monthly Trend Chart
```
    [3D Scatter Plot with green line + dot markers]
    X: Index  Y: Amount  Z: 0
    Camera rotates around the data
```

---

## 🗄️ Database Explanation

The application uses **SQLite3** (`expense_data.db`) with the following schema:

| Table | Purpose |
|-------|---------|
| `users` | Stores user accounts with SHA-256 hashed passwords |
| `expenses` | All expense transactions per user |
| `income` | All income records per user |
| `budgets` | Monthly budget allocations by category |
| `savings_goals` | Savings targets with progress tracking |
| `recurring_expenses` | Automated recurring bill/subscription data |

### Data Security
- All passwords are hashed using **SHA-256**
- Each user has fully isolated financial records
- No data leaves your local machine

---

## 📈 Analytics Explanation

### 3D Spending Breakdown
- Interactive 3D bar chart with gradient colors
- Categories on X-axis, amounts on Y-axis
- Hover tooltips show exact values

### 3D Monthly Trends
- 3D scatter plot with connected lines
- Camera orbit view for immersive experience
- Time-based spending visualization

### 3D Budget Gauges
- Circular gauge indicators per category
- Color-coded zones (green/yellow/red)
- Real-time budget vs spending comparison

### AI Insights Engine
The system automatically generates insights such as:
- Month-over-month spending comparisons
- Budget overspending warnings
- Top spending category alerts
- Savings goal progress notifications
- Income-to-expense ratio analysis

---

## 📁 Folder Structure

```
Advanced-CLI-Expense-Tracker/
│
├── app.py               # Main Streamlit application (all logic)
├── requirements.txt     # Python dependencies
├── README.md            # This file
├── install.sh           # Linux auto-installer
├── install.bat          # Windows auto-installer
├── inputguide.md        # Detailed usage guide
├── expense_data.db      # SQLite database (auto-created)
├── .gitignore           # Git ignore rules
└── assets/
    └── banner.txt       # ASCII art banner
```

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| **Python 3.11+** | Core language |
| **Streamlit** | Web application framework |
| **Plotly** | Interactive 3D charts and visualizations |
| **Three.js** | 3D particle background animation |
| **Pandas** | Data manipulation for analytics |
| **SQLite3** | Local embedded database |
| **Hashlib** | SHA-256 password hashing |

---

## 🗺️ Future Roadmap

- [ ] Dark/Light theme toggle
- [ ] Multi-currency support
- [ ] Data backup & restore
- [ ] Custom color themes
- [ ] Transaction photo attachments
- [ ] Debt tracking module
- [ ] Investment portfolio tracker
- [ ] Email report notifications
- [ ] Docker containerization
- [ ] Deploy to Streamlit Cloud

---

## 🤝 Contribution Guide

1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/your-username/Advanced-CLI-Expense-Tracker.git`
3. **Create** a feature branch: `git checkout -b feature/amazing-feature`
4. **Commit** your changes: `git commit -m 'Add amazing feature'`
5. **Push** to the branch: `git push origin feature/amazing-feature`
6. **Open** a Pull Request

### Coding Standards
- Follow PEP 8 style guidelines
- Keep functions focused and lightweight
- Add docstrings for new features
- Test on both Windows and Linux

---

## 📜 License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2026 issu321

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

<div align="center">

**Developed by [issu321](https://github.com/issu321)**

⭐ Star this repo if you find it useful!

[Report Bug](https://github.com/issu321/Advanced-CLI-Expense-Tracker/issues) • [Request Feature](https://github.com/issu321/Advanced-CLI-Expense-Tracker/issues)

</div>
