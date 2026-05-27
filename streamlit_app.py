#!/usr/bin/env python3
"""
Advanced 3D Expense Tracker - Streamlit Edition
Developed by ussu321
https://github.com/ussu321/Your-Expense-Tracker-Python
"""

import os
import sys
import sqlite3
import hashlib
import csv
import json
from datetime import datetime, timedelta
from io import StringIO

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Advanced 3D Expense Tracker",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CONSTANTS ────────────────────────────────────────────────────────────────
DB_FILE = "expense_data.db"
CYBER_BLUE = "#00d4ff"
CYBER_GREEN = "#00ff88"
CYBER_PINK = "#ff00aa"
CYBER_YELLOW = "#ffee00"
CYBER_RED = "#ff3333"
CYBER_PURPLE = "#aa00ff"
CYBER_CYAN = "#00ffff"
CYBER_DARK = "#0a0a0f"
CYBER_CARD = "#11111a"

# RGBA colors for Plotly (Plotly needs proper rgba format, not hex+alpha)
RGBA_BLUE = "rgba(0, 212, 255, 0.8)"
RGBA_GREEN = "rgba(0, 255, 136, 0.8)"
RGBA_PINK = "rgba(255, 0, 170, 0.8)"
RGBA_YELLOW = "rgba(255, 238, 0, 0.8)"
RGBA_RED = "rgba(255, 51, 51, 0.8)"
RGBA_PURPLE = "rgba(170, 0, 255, 0.8)"
RGBA_CYAN = "rgba(0, 255, 255, 0.8)"
RGBA_DARK = "rgba(10, 10, 15, 1)"
RGBA_GRID = "rgba(0, 212, 255, 0.15)"
RGBA_GRID_LIGHT = "rgba(0, 212, 255, 0.08)"

# ─── 3D ANIMATED CSS + THREE.JS BACKGROUND ───────────────────────────────────
CSS_3D = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;500;700&display=swap');

.stApp {
    background: #050508 !important;
    font-family: 'Rajdhani', sans-serif !important;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a0a1a 0%, #111130 100%) !important;
    border-right: 1px solid rgba(0, 212, 255, 0.2) !important;
}
[data-testid="stSidebar"] .stMarkdown {
    color: #00d4ff !important;
}

.cyber-card {
    background: linear-gradient(135deg, #11111a 0%, #1a1a2e 100%) !important;
    border: 1px solid rgba(0, 212, 255, 0.25) !important;
    border-radius: 16px !important;
    padding: 24px !important;
    box-shadow: 0 0 20px rgba(0, 212, 255, 0.05), inset 0 0 20px rgba(0, 212, 255, 0.03) !important;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
    transform-style: preserve-3d !important;
    perspective: 1000px !important;
    position: relative;
    overflow: hidden;
}
.cyber-card::before {
    content: '';
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: conic-gradient(from 0deg, transparent, rgba(0, 212, 255, 0.15), transparent 30%);
    animation: rotate 4s linear infinite;
    opacity: 0;
    transition: opacity 0.3s;
}
.cyber-card:hover::before {
    opacity: 1;
}
.cyber-card:hover {
    transform: translateY(-8px) rotateX(5deg) rotateY(-5deg) scale(1.02) !important;
    box-shadow: 0 20px 40px rgba(0, 212, 255, 0.15), 0 0 60px rgba(0, 212, 255, 0.1) !important;
    border-color: rgba(0, 212, 255, 0.6) !important;
}

@keyframes rotate {
    100% { transform: rotate(360deg); }
}

.neon-text {
    font-family: 'Orbitron', monospace !important;
    color: #00d4ff !important;
    text-shadow: 0 0 10px rgba(0, 212, 255, 0.5), 0 0 20px rgba(0, 212, 255, 0.3), 0 0 40px rgba(0, 212, 255, 0.15) !important;
    letter-spacing: 2px !important;
}
.neon-green {
    color: #00ff88 !important;
    text-shadow: 0 0 10px rgba(0, 255, 136, 0.5), 0 0 20px rgba(0, 255, 136, 0.3) !important;
}
.neon-pink {
    color: #ff00aa !important;
    text-shadow: 0 0 10px rgba(255, 0, 170, 0.5), 0 0 20px rgba(255, 0, 170, 0.3) !important;
}
.neon-yellow {
    color: #ffee00 !important;
    text-shadow: 0 0 10px rgba(255, 238, 0, 0.5), 0 0 20px rgba(255, 238, 0, 0.3) !important;
}

.stButton > button {
    background: linear-gradient(135deg, rgba(0, 212, 255, 0.15), rgba(0, 255, 136, 0.15)) !important;
    border: 1px solid rgba(0, 212, 255, 0.4) !important;
    color: #00d4ff !important;
    font-family: 'Orbitron', monospace !important;
    letter-spacing: 1px !important;
    border-radius: 12px !important;
    transition: all 0.3s !important;
    text-transform: uppercase !important;
    font-size: 0.85rem !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, rgba(0, 212, 255, 0.3), rgba(0, 255, 136, 0.3)) !important;
    box-shadow: 0 0 20px rgba(0, 212, 255, 0.3) !important;
    transform: translateY(-2px) !important;
}

.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stDateInput > div > div > input {
    background: #0a0a1a !important;
    border: 1px solid rgba(0, 212, 255, 0.25) !important;
    color: #00d4ff !important;
    font-family: 'Rajdhani', sans-serif !important;
    border-radius: 10px !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: #00d4ff !important;
    box-shadow: 0 0 15px rgba(0, 212, 255, 0.2) !important;
}

.stSelectbox > div > div > div {
    background: #0a0a1a !important;
    border: 1px solid rgba(0, 212, 255, 0.25) !important;
    color: #00d4ff !important;
    border-radius: 10px !important;
}

.stDataFrame {
    background: #11111a !important;
    border: 1px solid rgba(0, 212, 255, 0.2) !important;
    border-radius: 12px !important;
}
.stDataFrame th {
    background: rgba(0, 212, 255, 0.15) !important;
    color: #00d4ff !important;
    font-family: 'Orbitron', monospace !important;
}
.stDataFrame td {
    color: #e0e0e0 !important;
}

.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #00d4ff, #00ff88) !important;
    box-shadow: 0 0 10px rgba(0, 212, 255, 0.4) !important;
}

@keyframes float {
    0%, 100% { transform: translateY(0px) rotateX(0deg); }
    50% { transform: translateY(-10px) rotateX(2deg); }
}
.float-anim {
    animation: float 3s ease-in-out infinite;
}

@keyframes glitch {
    0% { text-shadow: 2px 0 #ff00aa, -2px 0 #00ff88; }
    25% { text-shadow: -2px 0 #ff00aa, 2px 0 #00ff88; }
    50% { text-shadow: 2px 0 #00d4ff, -2px 0 #ffee00; }
    75% { text-shadow: -2px 0 #00d4ff, 2px 0 #ffee00; }
    100% { text-shadow: 2px 0 #ff00aa, -2px 0 #00ff88; }
}
.glitch-text {
    animation: glitch 2s infinite;
}

.scanlines {
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 2px,
        rgba(0, 0, 0, 0.03) 2px,
        rgba(0, 0, 0, 0.03) 4px
    );
    pointer-events: none;
    z-index: 9999;
}

::-webkit-scrollbar {
    width: 8px;
}
::-webkit-scrollbar-track {
    background: #0a0a1a;
}
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #00d4ff, #00ff88);
    border-radius: 4px;
}

h1, h2, h3 {
    font-family: 'Orbitron', monospace !important;
    color: #00d4ff !important;
}

hr {
    border-color: rgba(0, 212, 255, 0.2) !important;
    box-shadow: 0 0 10px rgba(0, 212, 255, 0.15) !important;
}
</style>
<div class="scanlines"></div>
"""

THREE_JS_BG = """
<div id="three-canvas"></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({alpha: true, antialias: true});
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(window.devicePixelRatio);
document.getElementById('three-canvas').appendChild(renderer.domElement);

const particlesGeometry = new THREE.BufferGeometry();
const particlesCount = 800;
const posArray = new Float32Array(particlesCount * 3);
for(let i=0; i<<particlesCount*3; i++) {
    posArray[i] = (Math.random() - 0.5) * 20;
}
particlesGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
const particlesMaterial = new THREE.PointsMaterial({
    size: 0.02,
    color: 0x00d4ff,
    transparent: true,
    opacity: 0.8,
    blending: THREE.AdditiveBlending
});
const particlesMesh = new THREE.Points(particlesGeometry, particlesMaterial);
scene.add(particlesMesh);

const gridHelper = new THREE.GridHelper(20, 20, 0x00d4ff, 0x00d4ff);
gridHelper.position.y = -3;
scene.add(gridHelper);

const cubes = [];
const cubeColors = [0x00d4ff, 0x00ff88, 0xff00aa, 0xffee00];
for(let i=0; i<<8; i++) {
    const geometry = new THREE.BoxGeometry(0.3, 0.3, 0.3);
    const material = new THREE.MeshBasicMaterial({
        color: cubeColors[i % 4],
        transparent: true,
        opacity: 0.3,
        wireframe: true
    });
    const cube = new THREE.Mesh(geometry, material);
    cube.position.set(
        (Math.random()-0.5)*10,
        (Math.random()-0.5)*6,
        (Math.random()-0.5)*10
    );
    scene.add(cube);
    cubes.push({mesh: cube, speed: Math.random()*0.01+0.005, axis: Math.random()});
}

camera.position.z = 5;
camera.position.y = 1;

function animate() {
    requestAnimationFrame(animate);
    particlesMesh.rotation.y += 0.0005;
    particlesMesh.rotation.x += 0.0002;
    gridHelper.position.z = (Date.now() * 0.001) % 2;
    cubes.forEach(c => {
        c.mesh.rotation.x += c.speed;
        c.mesh.rotation.y += c.speed;
        c.mesh.position.y += Math.sin(Date.now()*0.001 + c.axis)*0.002;
    });
    renderer.render(scene, camera);
}
animate();

window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth/window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});
</script>
"""

st.markdown(CSS_3D, unsafe_allow_html=True)

# ─── DATABASE ─────────────────────────────────────────────────────────────────

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        description TEXT,
        date TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS income (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        source TEXT NOT NULL,
        description TEXT,
        date TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS budgets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        category TEXT NOT NULL,
        amount REAL NOT NULL,
        month INTEGER NOT NULL,
        year INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS savings_goals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        target_amount REAL NOT NULL,
        current_amount REAL DEFAULT 0,
        deadline TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS recurring_expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        frequency TEXT NOT NULL,
        next_due_date TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )""")
    conn.commit()
    conn.close()

def get_db():
    return sqlite3.connect(DB_FILE)

# ─── AUTH ─────────────────────────────────────────────────────────────────────

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    conn = get_db()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                  (username, hash_password(password)))
        conn.commit()
        uid = c.lastrowid
        conn.close()
        return uid
    except sqlite3.IntegrityError:
        conn.close()
        return None

def login_user(username, password):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT id, password_hash FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    if row and row[1] == hash_password(password):
        return row[0]
    return None

# ─── SESSION STATE ────────────────────────────────────────────────────────────

def init_session():
    if "user_id" not in st.session_state:
        st.session_state.user_id = None
    if "username" not in st.session_state:
        st.session_state.username = None
    if "page" not in st.session_state:
        st.session_state.page = "Dashboard"

def logout():
    st.session_state.user_id = None
    st.session_state.username = None
    st.session_state.page = "Dashboard"
    st.rerun()

# ─── UI HELPERS ───────────────────────────────────────────────────────────────

def neon_header(text, color=CYBER_BLUE, size="h1"):
    tag = size
    return f'<{tag} class="neon-text" style="color:{color} !important;text-align:center;">{text}</{tag}>'

def metric_card(title, value, color=CYBER_BLUE):
    html = f"""
    <div class="cyber-card float-anim" style="text-align:center;">
        <div style="font-family:'Orbitron';color:{color};font-size:0.85rem;letter-spacing:2px;margin-bottom:8px;">{title}</div>
        <div style="font-family:'Orbitron';color:#fff;font-size:2rem;font-weight:900;text-shadow:0 0 20px {color}66;">{value}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def animated_divider():
    st.markdown("""
    <div style="height:2px;background:linear-gradient(90deg,transparent,#00d4ff,transparent);
         margin:20px 0;box-shadow:0 0 10px rgba(0,212,255,0.4);"></div>
    """, unsafe_allow_html=True)

# ─── DATA FUNCTIONS ───────────────────────────────────────────────────────────

def get_expenses(user_id):
    conn = get_db()
    df = pd.read_sql_query("SELECT * FROM expenses WHERE user_id = ? ORDER BY date DESC", conn, params=(user_id,))
    conn.close()
    return df

def get_income(user_id):
    conn = get_db()
    df = pd.read_sql_query("SELECT * FROM income WHERE user_id = ? ORDER BY date DESC", conn, params=(user_id,))
    conn.close()
    return df

def get_budgets(user_id, month, year):
    conn = get_db()
    df = pd.read_sql_query("SELECT * FROM budgets WHERE user_id = ? AND month = ? AND year = ?", conn, params=(user_id, month, year))
    conn.close()
    return df

def get_savings(user_id):
    conn = get_db()
    df = pd.read_sql_query("SELECT * FROM savings_goals WHERE user_id = ?", conn, params=(user_id,))
    conn.close()
    return df

def get_recurring(user_id):
    conn = get_db()
    df = pd.read_sql_query("SELECT * FROM recurring_expenses WHERE user_id = ?", conn, params=(user_id,))
    conn.close()
    return df

# ─── 3D CHARTS (FIXED COLORS FOR PLOTLY) ──────────────────────────────────────

def plot_3d_spending_breakdown(df):
    if df.empty:
        return None
    grouped = df.groupby("category")["amount"].sum().reset_index()
    fig = go.Figure(data=[go.Bar(
        x=grouped["category"],
        y=grouped["amount"],
        marker=dict(
            color=grouped["amount"],
            colorscale=[[0, CYBER_BLUE], [0.5, CYBER_PURPLE], [1, CYBER_PINK]],
            line=dict(color=CYBER_BLUE, width=2)
        ),
        text=grouped["amount"].apply(lambda x: f"${x:.2f}"),
        textposition="outside",
        textfont=dict(family="Orbitron", color="#fff", size=12)
    )])
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Orbitron", color=CYBER_BLUE),
        xaxis=dict(showgrid=False, tickfont=dict(color=CYBER_BLUE)),
        yaxis=dict(showgrid=True, gridcolor=RGBA_GRID, tickfont=dict(color=CYBER_BLUE)),
        title=dict(text="SPENDING BREAKDOWN", font=dict(size=20, color=CYBER_GREEN)),
        margin=dict(t=60, b=40, l=40, r=40),
        height=400
    )
    return fig

def plot_3d_monthly_trend(df):
    if df.empty:
        return None
    df["month"] = pd.to_datetime(df["date"]).dt.to_period("M").astype(str)
    grouped = df.groupby("month")["amount"].sum().reset_index()
    fig = go.Figure(data=[go.Scatter3d(
        x=list(range(len(grouped))),
        y=grouped["amount"],
        z=[0]*len(grouped),
        mode="lines+markers",
        line=dict(color=CYBER_GREEN, width=6),
        marker=dict(size=8, color=grouped["amount"], colorscale=[[0, CYBER_BLUE], [1, CYBER_GREEN]],
                    line=dict(color="#fff", width=1)),
        text=grouped["month"],
        hovertemplate="%{text}<br>$%{y:.2f}<extra></extra>"
    )])
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Orbitron", color=CYBER_BLUE),
        title=dict(text="3D MONTHLY TREND", font=dict(size=20, color=CYBER_GREEN)),
        scene=dict(
            xaxis=dict(title="Index", backgroundcolor="rgba(0,0,0,0)", gridcolor=RGBA_GRID, tickfont=dict(color=CYBER_BLUE)),
            yaxis=dict(title="Amount ($)", backgroundcolor="rgba(0,0,0,0)", gridcolor=RGBA_GRID, tickfont=dict(color=CYBER_BLUE)),
            zaxis=dict(title="", backgroundcolor="rgba(0,0,0,0)", gridcolor=RGBA_GRID, tickfont=dict(color=CYBER_BLUE)),
            camera=dict(eye=dict(x=1.5, y=1.5, z=0.8))
        ),
        margin=dict(t=60, b=40, l=40, r=40),
        height=500
    )
    return fig

def plot_3d_budget_gauge(budget, spent, category):
    pct = min((spent / budget * 100), 100) if budget > 0 else 0
    color = CYBER_GREEN if pct < 80 else (CYBER_YELLOW if pct < 100 else CYBER_RED)
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=spent,
        delta={'reference': budget, 'relative': True},
        title={'text': category.upper(), 'font': {'size': 18, 'family': 'Orbitron', 'color': color}},
        gauge={
            'axis': {'range': [0, max(budget * 1.2, spent * 1.1)], 'tickcolor': color},
            'bar': {'color': color, 'thickness': 0.75},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 2, 'bordercolor': color,
            'steps': [
                {'range': [0, budget * 0.8], 'color': 'rgba(0,255,136,0.1)'},
                {'range': [budget * 0.8, budget], 'color': 'rgba(255,238,0,0.1)'},
                {'range': [budget, max(budget * 1.2, spent * 1.1)], 'color': 'rgba(255,51,51,0.1)'}
            ],
            'threshold': {'line': {'color': "#fff", 'width': 4}, 'thickness': 0.8, 'value': budget}
        }
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Orbitron", color=color),
        height=280,
        margin=dict(t=30, b=20, l=20, r=20)
    )
    return fig

def plot_3d_savings_progress(name, current, target):
    pct = (current / target * 100) if target > 0 else 0
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=pct,
        number={'suffix': "%", 'font': {'size': 28, 'family': 'Orbitron', 'color': CYBER_BLUE}},
        title={'text': name.upper(), 'font': {'size': 16, 'family': 'Orbitron', 'color': CYBER_GREEN}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': CYBER_BLUE},
            'bar': {'color': CYBER_GREEN, 'thickness': 0.7},
            'bgcolor': CYBER_CARD,
            'borderwidth': 2, 'bordercolor': 'rgba(0,212,255,0.3)',
            'steps': [
                {'range': [0, 50], 'color': 'rgba(255,51,51,0.15)'},
                {'range': [50, 75], 'color': 'rgba(255,238,0,0.15)'},
                {'range': [75, 100], 'color': 'rgba(0,255,136,0.15)'}
            ],
            'threshold': {'line': {'color': "#fff", 'width': 3}, 'thickness': 0.9, 'value': 100}
        }
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Orbitron"),
        height=260,
        margin=dict(t=30, b=20, l=20, r=20)
    )
    return fig

# ─── AI INSIGHTS ──────────────────────────────────────────────────────────────

def generate_insights_data(user_id):
    conn = get_db()
    c = conn.cursor()
    insights = []
    now = datetime.now()
    this_month = now.strftime("%Y-%m")
    last_month = (now.replace(day=1) - timedelta(days=1)).strftime("%Y-%m")

    c.execute("SELECT COALESCE(SUM(amount),0) FROM expenses WHERE user_id=? AND strftime('%Y-%m',date)=?", (user_id, this_month))
    this_spent = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM expenses WHERE user_id=? AND strftime('%Y-%m',date)=?", (user_id, last_month))
    last_spent = c.fetchone()[0]

    if last_spent > 0:
        change = ((this_spent - last_spent) / last_spent) * 100
        if change > 0:
            insights.append(("Spending Alert", f"You spent {change:.1f}% more this month vs last month.", CYBER_RED))
        else:
            insights.append(("Great Job!", f"You spent {abs(change):.1f}% less this month.", CYBER_GREEN))

    c.execute("SELECT category, SUM(amount) FROM expenses WHERE user_id=? AND strftime('%Y-%m',date)=? GROUP BY category ORDER BY SUM(amount) DESC LIMIT 1", (user_id, this_month))
    top = c.fetchone()
    if top:
        insights.append(("Top Category", f"'{top[0]}' leads at ${top[1]:.2f} this month.", CYBER_YELLOW))

    c.execute("SELECT category, amount FROM budgets WHERE user_id=? AND month=? AND year=?", (user_id, now.month, now.year))
    for cat, budget in c.fetchall():
        c.execute("SELECT COALESCE(SUM(amount),0) FROM expenses WHERE user_id=? AND category=? AND strftime('%Y-%m',date)=?", (user_id, cat, this_month))
        spent = c.fetchone()[0]
        if spent > budget:
            insights.append(("Over Budget", f"'{cat}' exceeded by ${spent-budget:.2f}", CYBER_RED))
        elif spent > budget * 0.8:
            insights.append(("Warning", f"'{cat}' at {(spent/budget*100):.0f}% of budget", CYBER_YELLOW))

    c.execute("SELECT name, target_amount, current_amount FROM savings_goals WHERE user_id=?", (user_id,))
    for name, target, current in c.fetchall():
        pct = (current/target*100) if target>0 else 0
        if pct >= 100:
            insights.append(("Goal Achieved!", f"'{name}' is fully funded!", CYBER_GREEN))
        elif pct >= 75:
            insights.append(("Almost There", f"'{name}' is {pct:.0f}% complete", CYBER_CYAN))

    c.execute("SELECT COALESCE(SUM(amount),0) FROM income WHERE user_id=? AND strftime('%Y-%m',date)=?", (user_id, this_month))
    this_income = c.fetchone()[0]
    if this_income > 0:
        ratio = (this_spent / this_income) * 100
        if ratio > 90:
            insights.append(("High Spend Ratio", f"You're spending {ratio:.0f}% of income", CYBER_RED))
        elif ratio < 50:
            insights.append(("Excellent Saver", f"Only spending {ratio:.0f}% of income", CYBER_GREEN))

    conn.close()
    return insights

# ─── EXPORT ───────────────────────────────────────────────────────────────────

def export_csv(user_id, username):
    conn = get_db()
    exp = pd.read_sql_query("SELECT date, category, amount, description FROM expenses WHERE user_id=? ORDER BY date DESC", conn, params=(user_id,))
    inc = pd.read_sql_query("SELECT date, source, amount, description FROM income WHERE user_id=? ORDER BY date DESC", conn, params=(user_id,))
    conn.close()
    output = StringIO()
    output.write("=== EXPENSES ===\n")
    exp.to_csv(output, index=False)
    output.write("\n=== INCOME ===\n")
    inc.to_csv(output, index=False)
    return output.getvalue()

def export_txt(user_id, username):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM income WHERE user_id=?", (user_id,))
    total_income = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM expenses WHERE user_id=?", (user_id,))
    total_expenses = c.fetchone()[0]
    c.execute("SELECT date, category, amount, description FROM expenses WHERE user_id=? ORDER BY date DESC LIMIT 20", (user_id,))
    recent = c.fetchall()
    conn.close()
    lines = [
        "="*50,
        "   ADVANCED 3D EXPENSE TRACKER - REPORT",
        f"   User: {username}",
        f"   Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "="*50, "",
        f"Total Income:    ${total_income:,.2f}",
        f"Total Expenses:  ${total_expenses:,.2f}",
        f"Net Balance:     ${total_income-total_expenses:,.2f}", "",
        "Recent Expenses:", "-"*50
    ]
    for row in recent:
        lines.append(f"{row[0]} | {row[1]:15} | ${row[2]:8.2f} | {row[3]}")
    lines.append("")
    lines.append("Developed by ussu321 | github.com/ussu321")
    return "\n".join(lines)

# ─── PAGES ──────────────────────────────────────────────────────────────────────

def page_login():
    st.markdown(neon_header("ADVANCED 3D EXPENSE TRACKER", CYBER_BLUE, "h1"), unsafe_allow_html=True)
    st.markdown(f'<p style="text-align:center;color:#00ff88;font-family:Orbitron;letter-spacing:3px;">MULTI-USER • AI INSIGHTS • 3D ANALYTICS</p>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["LOGIN", "REGISTER"])
        with tab1:
            username = st.text_input("Username", key="login_user")
            password = st.text_input("Password", type="password", key="login_pass")
            if st.button("LAUNCH", use_container_width=True):
                uid = login_user(username, password)
                if uid:
                    st.session_state.user_id = uid
                    st.session_state.username = username
                    st.success("Access Granted")
                    st.rerun()
                else:
                    st.error("Invalid Credentials")
        with tab2:
            new_user = st.text_input("Username", key="reg_user")
            new_pass = st.text_input("Password", type="password", key="reg_pass")
            conf_pass = st.text_input("Confirm Password", type="password", key="reg_conf")
            if st.button("CREATE ACCOUNT", use_container_width=True):
                if new_pass != conf_pass:
                    st.error("Passwords don't match")
                elif len(new_pass) < 4:
                    st.error("Minimum 4 characters")
                else:
                    uid = register_user(new_user, new_pass)
                    if uid:
                        st.session_state.user_id = uid
                        st.session_state.username = new_user
                        st.success("Account Created")
                        st.rerun()
                    else:
                        st.error("Username exists")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(f'<p style="text-align:center;color:#666;font-size:0.8rem;">Developed by ussu321 | github.com/ussu321</p>', unsafe_allow_html=True)

def page_dashboard():
    st.markdown(neon_header(f"{st.session_state.username.upper()} COMMAND CENTER", CYBER_GREEN, "h2"), unsafe_allow_html=True)
    animated_divider()

    conn = get_db()
    c = conn.cursor()
    uid = st.session_state.user_id

    c.execute("SELECT COALESCE(SUM(amount),0) FROM income WHERE user_id=?", (uid,))
    total_income = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM expenses WHERE user_id=?", (uid,))
    total_expenses = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(current_amount),0) FROM savings_goals WHERE user_id=?", (uid,))
    total_savings = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(target_amount),0) FROM savings_goals WHERE user_id=?", (uid,))
    total_targets = c.fetchone()[0]
    conn.close()

    balance = total_income - total_expenses

    c1, c2, c3, c4 = st.columns(4)
    with c1: metric_card("TOTAL INCOME", f"${total_income:,.2f}", color=CYBER_GREEN)
    with c2: metric_card("TOTAL EXPENSES", f"${total_expenses:,.2f}", color=CYBER_RED)
    with c3: metric_card("NET BALANCE", f"${balance:,.2f}", color=CYBER_BLUE)
    with c4: metric_card("SAVINGS", f"${total_savings:,.2f}", color=CYBER_YELLOW)

    animated_divider()

    st.markdown(neon_header("QUICK ACTIONS", CYBER_CYAN, "h3"), unsafe_allow_html=True)
    q1, q2, q3, q4 = st.columns(4)
    with q1:
        if st.button("Add Expense", use_container_width=True):
            st.session_state.page = "Expenses"; st.rerun()
    with q2:
        if st.button("Add Income", use_container_width=True):
            st.session_state.page = "Income"; st.rerun()
    with q3:
        if st.button("Add Goal", use_container_width=True):
            st.session_state.page = "Savings"; st.rerun()
    with q4:
        if st.button("Analytics", use_container_width=True):
            st.session_state.page = "Analytics"; st.rerun()

    animated_divider()
    st.markdown(neon_header("RECENT ACTIVITY", CYBER_PURPLE, "h3"), unsafe_allow_html=True)
    exp_df = get_expenses(uid)
    if not exp_df.empty:
        st.dataframe(exp_df.head(10)[["date", "category", "amount", "description"]], use_container_width=True, hide_index=True)
    else:
        st.info("No transactions yet. Start by adding an expense!")

def page_expenses():
    st.markdown(neon_header("EXPENSE MANAGEMENT", CYBER_RED, "h2"), unsafe_allow_html=True)
    animated_divider()
    uid = st.session_state.user_id

    tab1, tab2, tab3 = st.tabs(["ADD", "VIEW / EDIT", "SEARCH"])

    with tab1:
        with st.form("add_expense"):
            c1, c2 = st.columns(2)
            with c1:
                amount = st.number_input("Amount ($)", min_value=0.01, step=0.01)
                category = st.selectbox("Category", ["food", "transport", "entertainment", "bills", "shopping", "health", "other"])
            with c2:
                date = st.date_input("Date", datetime.now())
                description = st.text_input("Description")
            if st.form_submit_button("SAVE EXPENSE", use_container_width=True):
                conn = get_db()
                c = conn.cursor()
                c.execute("INSERT INTO expenses (user_id, amount, category, description, date) VALUES (?,?,?,?,?)",
                          (uid, amount, category, description, date.strftime("%Y-%m-%d")))
                conn.commit(); conn.close()
                st.success("Expense saved"); st.rerun()

    with tab2:
        df = get_expenses(uid)
        if not df.empty:
            st.dataframe(df, use_container_width=True, hide_index=True)
            del_id = st.number_input("Enter ID to delete", min_value=1, step=1)
            if st.button("DELETE", use_container_width=True):
                conn = get_db()
                c = conn.cursor()
                c.execute("DELETE FROM expenses WHERE id=? AND user_id=?", (del_id, uid))
                conn.commit(); conn.close()
                st.success("Deleted"); st.rerun()
        else:
            st.info("No expenses found")

    with tab3:
        c1, c2, c3 = st.columns(3)
        with c1: scat = st.selectbox("Category", ["All", "food", "transport", "entertainment", "bills", "shopping", "health", "other"], key="search_cat")
        with c2: sfrom = st.date_input("From", datetime.now().replace(day=1), key="search_from")
        with c3: sto = st.date_input("To", datetime.now(), key="search_to")
        skey = st.text_input("Keyword in description", key="search_key")
        if st.button("SEARCH", use_container_width=True):
            conn = get_db()
            query = "SELECT * FROM expenses WHERE user_id=?"
            params = [uid]
            if scat != "All":
                query += " AND category=?"; params.append(scat)
            query += " AND date BETWEEN ? AND ?"; params.extend([sfrom.strftime("%Y-%m-%d"), sto.strftime("%Y-%m-%d")])
            if skey:
                query += " AND LOWER(description) LIKE ?"; params.append(f"%{skey}%")
            query += " ORDER BY date DESC"
            res = pd.read_sql_query(query, conn, params=params)
            conn.close()
            st.dataframe(res, use_container_width=True, hide_index=True)

    animated_divider()
    fig = plot_3d_spending_breakdown(df)
    if fig:
        st.plotly_chart(fig, use_container_width=True)

def page_income():
    st.markdown(neon_header("INCOME MANAGEMENT", CYBER_GREEN, "h2"), unsafe_allow_html=True)
    animated_divider()
    uid = st.session_state.user_id

    tab1, tab2 = st.tabs(["ADD", "VIEW"])
    with tab1:
        with st.form("add_income"):
            c1, c2 = st.columns(2)
            with c1:
                amount = st.number_input("Amount ($)", min_value=0.01, step=0.01)
                source = st.selectbox("Source", ["salary", "freelance", "investment", "gift", "other"])
            with c2:
                date = st.date_input("Date", datetime.now())
                description = st.text_input("Description")
            if st.form_submit_button("SAVE INCOME", use_container_width=True):
                conn = get_db()
                c = conn.cursor()
                c.execute("INSERT INTO income (user_id, amount, source, description, date) VALUES (?,?,?,?,?)",
                          (uid, amount, source, description, date.strftime("%Y-%m-%d")))
                conn.commit(); conn.close()
                st.success("Income saved"); st.rerun()

    with tab2:
        df = get_income(uid)
        if not df.empty:
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No income records")

    animated_divider()
    exp_df = get_expenses(uid)
    if not df.empty or not exp_df.empty:
        inc_total = df["amount"].sum() if not df.empty else 0
        exp_total = exp_df["amount"].sum() if not exp_df.empty else 0
        fig = go.Figure(data=[
            go.Bar(name="Income", x=["Total"], y=[inc_total], marker_color=CYBER_GREEN, text=[f"${inc_total:.2f}"], textposition="outside"),
            go.Bar(name="Expenses", x=["Total"], y=[exp_total], marker_color=CYBER_RED, text=[f"${exp_total:.2f}"], textposition="outside")
        ])
        fig.update_layout(
            barmode="group",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Orbitron", color=CYBER_BLUE),
            height=400,
            title=dict(text="INCOME VS EXPENSES", font=dict(size=18, color=CYBER_GREEN)),
            xaxis=dict(showgrid=False, tickfont=dict(color=CYBER_BLUE)),
            yaxis=dict(showgrid=True, gridcolor=RGBA_GRID, tickfont=dict(color=CYBER_BLUE))
        )
        st.plotly_chart(fig, use_container_width=True)

def page_budgets():
    st.markdown(neon_header("BUDGET MANAGEMENT", CYBER_YELLOW, "h2"), unsafe_allow_html=True)
    animated_divider()
    uid = st.session_state.user_id
    now = datetime.now()

    tab1, tab2 = st.tabs(["SET BUDGET", "VIEW BUDGETS"])
    with tab1:
        with st.form("set_budget"):
            c1, c2, c3 = st.columns(3)
            with c1: category = st.selectbox("Category", ["food", "transport", "entertainment", "bills", "shopping", "health", "other"])
            with c2: amount = st.number_input("Budget ($)", min_value=1.0, step=10.0)
            with c3:
                month = st.number_input("Month", min_value=1, max_value=12, value=now.month)
                year = st.number_input("Year", min_value=2020, max_value=2030, value=now.year)
            if st.form_submit_button("SET BUDGET", use_container_width=True):
                conn = get_db()
                c = conn.cursor()
                c.execute("DELETE FROM budgets WHERE user_id=? AND category=? AND month=? AND year=?", (uid, category, month, year))
                c.execute("INSERT INTO budgets (user_id, category, amount, month, year) VALUES (?,?,?,?,?)", (uid, category, amount, month, year))
                conn.commit(); conn.close()
                st.success("Budget set"); st.rerun()

    with tab2:
        budgets = get_budgets(uid, now.month, now.year)
        if not budgets.empty:
            conn = get_db()
            c = conn.cursor()
            c.execute("SELECT category, SUM(amount) FROM expenses WHERE user_id=? AND strftime('%m',date)=? AND strftime('%Y',date)=? GROUP BY category",
                      (uid, f"{now.month:02d}", str(now.year)))
            spent = {row[0]: row[1] for row in c.fetchall()}
            conn.close()

            cols = st.columns(min(len(budgets), 3))
            for idx, row in budgets.iterrows():
                cat = row["category"]
                budget = row["amount"]
                s = spent.get(cat, 0)
                with cols[idx % 3]:
                    fig = plot_3d_budget_gauge(budget, s, cat)
                    st.plotly_chart(fig, use_container_width=True)
                    st.markdown(f"<div style='text-align:center;color:#fff;font-family:Orbitron;'>${s:.2f} / ${budget:.2f}</div>", unsafe_allow_html=True)
        else:
            st.info("No budgets set for this month")

def page_savings():
    st.markdown(neon_header("SAVINGS GOALS", CYBER_PINK, "h2"), unsafe_allow_html=True)
    animated_divider()
    uid = st.session_state.user_id

    tab1, tab2 = st.tabs(["CREATE", "VIEW / UPDATE"])
    with tab1:
        with st.form("add_goal"):
            c1, c2, c3 = st.columns(3)
            with c1: name = st.text_input("Goal Name")
            with c2: target = st.number_input("Target ($)", min_value=1.0, step=10.0)
            with c3: current = st.number_input("Current ($)", min_value=0.0, step=10.0)
            deadline = st.date_input("Deadline (optional)", datetime.now() + timedelta(days=365))
            if st.form_submit_button("CREATE GOAL", use_container_width=True):
                conn = get_db()
                c = conn.cursor()
                c.execute("INSERT INTO savings_goals (user_id, name, target_amount, current_amount, deadline) VALUES (?,?,?,?,?)",
                          (uid, name, target, current, deadline.strftime("%Y-%m-%d")))
                conn.commit(); conn.close()
                st.success("Goal created"); st.rerun()

    with tab2:
        goals = get_savings(uid)
        if not goals.empty:
            cols = st.columns(min(len(goals), 3))
            for idx, row in goals.iterrows():
                with cols[idx % 3]:
                    fig = plot_3d_savings_progress(row["name"], row["current_amount"], row["target_amount"])
                    st.plotly_chart(fig, use_container_width=True)
                    st.markdown(f"<div style='text-align:center;color:#fff;font-family:Orbitron;font-size:0.9rem;'>${row['current_amount']:.2f} / ${row['target_amount']:.2f}</div>", unsafe_allow_html=True)
                    add_amt = st.number_input(f"Add to {row['name']}", min_value=0.0, step=10.0, key=f"add_{row['id']}")
                    if st.button(f"UPDATE", key=f"btn_{row['id']}"):
                        conn = get_db()
                        c = conn.cursor()
                        c.execute("UPDATE savings_goals SET current_amount = current_amount + ? WHERE id=? AND user_id=?", (add_amt, row["id"], uid))
                        conn.commit(); conn.close()
                        st.success("Updated"); st.rerun()
        else:
            st.info("No savings goals yet")

def page_recurring():
    st.markdown(neon_header("RECURRING EXPENSES", CYBER_PURPLE, "h2"), unsafe_allow_html=True)
    animated_divider()
    uid = st.session_state.user_id

    tab1, tab2, tab3 = st.tabs(["ADD", "VIEW", "SIMULATE"])
    with tab1:
        with st.form("add_recurring"):
            c1, c2 = st.columns(2)
            with c1:
                name = st.text_input("Name (e.g., Netflix)")
                amount = st.number_input("Amount ($)", min_value=0.01, step=0.01)
            with c2:
                category = st.selectbox("Category", ["food", "transport", "entertainment", "bills", "shopping", "health", "other"])
                freq = st.selectbox("Frequency", ["weekly", "monthly", "yearly"])
            next_due = st.date_input("Next Due Date", datetime.now())
            if st.form_submit_button("SAVE", use_container_width=True):
                conn = get_db()
                c = conn.cursor()
                c.execute("INSERT INTO recurring_expenses (user_id, name, amount, category, frequency, next_due_date) VALUES (?,?,?,?,?,?)",
                          (uid, name, amount, category, freq, next_due.strftime("%Y-%m-%d")))
                conn.commit(); conn.close()
                st.success("Saved"); st.rerun()

    with tab2:
        df = get_recurring(uid)
        if not df.empty:
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No recurring expenses")

    with tab3:
        if st.button("SIMULATE RECURRING", use_container_width=True):
            conn = get_db()
            c = conn.cursor()
            c.execute("SELECT * FROM recurring_expenses WHERE user_id=?", (uid,))
            rows = c.fetchall()
            today = datetime.now().date()
            added = 0
            for row in rows:
                due = datetime.strptime(row[6], "%Y-%m-%d").date()
                if due <= today:
                    c.execute("INSERT INTO expenses (user_id, amount, category, description, date) VALUES (?,?,?,?,?)",
                              (uid, row[3], row[4], f"Recurring: {row[2]}", today.strftime("%Y-%m-%d")))
                    if row[5] == "weekly": nd = due + timedelta(weeks=1)
                    elif row[5] == "monthly": nd = due + timedelta(days=30)
                    elif row[5] == "yearly": nd = due + timedelta(days=365)
                    else: nd = due + timedelta(days=30)
                    c.execute("UPDATE recurring_expenses SET next_due_date=? WHERE id=?", (nd.strftime("%Y-%m-%d"), row[0]))
                    added += 1
            conn.commit(); conn.close()
            st.success(f"Simulated {added} recurring expense(s)")

def page_analytics():
    st.markdown(neon_header("3D ANALYTICS CENTER", CYBER_CYAN, "h2"), unsafe_allow_html=True)
    animated_divider()
    uid = st.session_state.user_id

    exp_df = get_expenses(uid)
    inc_df = get_income(uid)

    c1, c2 = st.columns(2)
    with c1:
        fig = plot_3d_spending_breakdown(exp_df)
        if fig: st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig2 = plot_3d_monthly_trend(exp_df)
        if fig2: st.plotly_chart(fig2, use_container_width=True)

    animated_divider()
    st.markdown(neon_header("FINANCIAL SUMMARY", CYBER_BLUE, "h3"), unsafe_allow_html=True)

    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM income WHERE user_id=?", (uid,))
    ti = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM expenses WHERE user_id=?", (uid,))
    te = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(current_amount),0), COALESCE(SUM(target_amount),0) FROM savings_goals WHERE user_id=?", (uid,))
    sv = c.fetchone()
    conn.close()

    m1, m2, m3, m4 = st.columns(4)
    with m1: metric_card("INCOME", f"${ti:,.2f}", color=CYBER_GREEN)
    with m2: metric_card("EXPENSES", f"${te:,.2f}", color=CYBER_RED)
    with m3: metric_card("BALANCE", f"${ti-te:,.2f}", color=CYBER_BLUE)
    with m4: metric_card("SAVINGS", f"${sv[0]:,.2f} / ${sv[1]:,.2f}" if sv else "$0", color=CYBER_YELLOW)

    if not exp_df.empty:
        grouped = exp_df.groupby("category")["amount"].sum().reset_index()
        fig_pie = go.Figure(data=[go.Pie(
            labels=grouped["category"], values=grouped["amount"],
            hole=0.4, textinfo="label+percent",
            marker=dict(
                colors=[CYBER_BLUE, CYBER_GREEN, CYBER_PINK, CYBER_YELLOW, CYBER_PURPLE, CYBER_CYAN, CYBER_RED],
                line=dict(color="#050508", width=2)
            ),
            textfont=dict(family="Orbitron", color="#fff", size=12)
        )])
        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Orbitron", color=CYBER_BLUE),
            title=dict(text="CATEGORY DISTRIBUTION", font=dict(size=18, color=CYBER_BLUE)),
            height=450,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5,
                       font=dict(family="Orbitron", color=CYBER_BLUE))
        )
        st.plotly_chart(fig_pie, use_container_width=True)

def page_ai_insights():
    st.markdown(neon_header("AI FINANCIAL INSIGHTS", CYBER_PURPLE, "h2"), unsafe_allow_html=True)
    animated_divider()
    uid = st.session_state.user_id

    insights = generate_insights_data(uid)
    if insights:
        for title, msg, color in insights:
            st.markdown(f"""
            <div class="cyber-card" style="border-left: 4px solid {color} !important; margin-bottom: 16px;">
                <div style="font-family:'Orbitron';color:{color};font-size:1.1rem;font-weight:700;margin-bottom:6px;">{title}</div>
                <div style="color:#e0e0e0;font-size:1rem;">{msg}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Add more data to generate AI insights")

def page_export():
    st.markdown(neon_header("EXPORT DATA", CYBER_YELLOW, "h2"), unsafe_allow_html=True)
    animated_divider()
    uid = st.session_state.user_id
    uname = st.session_state.username

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
        st.markdown("### CSV Export")
        csv_data = export_csv(uid, uname)
        st.download_button("DOWNLOAD CSV", csv_data, file_name=f"export_{uname}.csv", mime="text/csv", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
        st.markdown("### TXT Summary")
        txt_data = export_txt(uid, uname)
        st.download_button("DOWNLOAD TXT", txt_data, file_name=f"summary_{uname}.txt", mime="text/plain", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ─── SIDEBAR ────────────────────────────────────────────────────────────────────

def render_sidebar():
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align:center;margin-bottom:20px;">
            <div style="font-family:'Orbitron';font-size:1.5rem;color:#00d4ff;text-shadow:0 0 20px rgba(0,212,255,0.5);">EXPENSE<br>TRACKER</div>
            <div style="font-size:0.75rem;color:#00ff88;margin-top:5px;">v4.0 STREAMLIT EDITION</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr style='border-color:rgba(0,212,255,0.2);margin:15px 0;'>", unsafe_allow_html=True)

        menu = {
            "Dashboard": "🏠",
            "Expenses": "💸",
            "Income": "💰",
            "Budgets": "📊",
            "Savings": "🎯",
            "Recurring": "🔄",
            "Analytics": "📈",
            "AI Insights": "🤖",
            "Export": "📤"
        }

        for page, icon in menu.items():
            active = st.session_state.page == page
            if st.button(f"{icon} {page}", key=f"nav_{page}", use_container_width=True):
                st.session_state.page = page
                st.rerun()

        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="text-align:center;padding:15px;background:#11111a;border-radius:12px;border:1px solid rgba(0,212,255,0.2);">
            <div style="font-family:'Orbitron';color:#00d4ff;font-size:0.9rem;">{st.session_state.username}</div>
            <div style="color:#666;font-size:0.7rem;margin-top:5px;">Logged In</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("LOGOUT", use_container_width=True):
            logout()

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f'<div style="text-align:center;color:#444;font-size:0.7rem;">Developed by ussu321</div>', unsafe_allow_html=True)

# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    init_db()
    init_session()

    st.components.v1.html(THREE_JS_BG, height=0)

    if st.session_state.user_id is None:
        page_login()
    else:
        render_sidebar()
        page = st.session_state.page
        if page == "Dashboard": page_dashboard()
        elif page == "Expenses": page_expenses()
        elif page == "Income": page_income()
        elif page == "Budgets": page_budgets()
        elif page == "Savings": page_savings()
        elif page == "Recurring": page_recurring()
        elif page == "Analytics": page_analytics()
        elif page == "AI Insights": page_ai_insights()
        elif page == "Export": page_export()
        else: page_dashboard()

if __name__ == "__main__":
    main()