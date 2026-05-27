#!/usr/bin/env python3
"""
Advanced CLI Expense Tracker
Developed by issu321
https://github.com/issu321/Advanced-CLI-Expense-Tracker
"""

import os
import sys
import time
import sqlite3
import hashlib
import csv
import json
from datetime import datetime, timedelta
from getpass import getpass

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.align import Align
from rich.columns import Columns
from rich import box
import plotext as plt
import pandas as pd

# ─── CONFIG ───────────────────────────────────────────────────────────────────
console = Console()
DB_FILE = "expense_data.db"
CYBER_BLUE = "#00d4ff"
CYBER_GREEN = "#00ff88"
CYBER_PINK = "#ff00aa"
CYBER_YELLOW = "#ffee00"
CYBER_RED = "#ff3333"
CYBER_PURPLE = "#aa00ff"
CYBER_CYAN = "#00ffff"

# ─── 3D ANIMATED STARTUP ────────────────────────────────────────────────────


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def animated_banner():
    clear_screen()
    banner_frames = [
        [
            "    █████╗ ██████╗ ██╗   ██╗ █████╗ ███╗   ██╗███████╗██████╗ ███████╗",
            "   ██╔══██╗██╔══██╗██║   ██║██╔══██╗████╗  ██║██╔════╝██╔══██╗██╔════╝",
            "   ███████║██║  ██║██║   ██║███████║██╔██╗ ██║█████╗  ██████╔╝█████╗  ",
            "   ██╔══██║██║  ██║╚██╗ ██╔╝██╔══██║██║╚██╗██║██╔══╝  ██╔══██╗██╔══╝  ",
            "   ██║  ██║██████╔╝ ╚████╔╝ ██║  ██║██║ ╚████║███████╗██║  ██║███████╗",
            "   ╚═╝  ╚═╝╚═════╝   ╚═══╝  ╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚══════╝",
        ],
        [
            "  ░░█████╗░██████╗░██╗░░░░░██╗░░░██╗███████╗██████╗░███████╗██████╗░",
            "  ░░██╔══██╗██╔══██╗██║░░░░░██║░░░██║██╔════╝██╔══██╗██╔════╝██╔══██╗",
            "  ░░███████║██║░░██║██║░░░░░██║░░░██║█████╗░░██████╔╝█████╗░░██████╔╝",
            "  ░░██╔══██║██║░░██║██║░░░░░██║░░░██║██╔══╝░░██╔══██╗██╔══╝░░██╔══██╗",
            "  ░░██║░░██║██████╔╝███████╗╚██████╔╝███████╗██║░░██║███████╗██║░░██║",
            "  ░░╚═╝░░╚═╝╚═════╝░╚══════╝░╚═════╝░╚══════╝╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝",
        ],
        [
            "   ▄▄▄· ▄▄▄  ▄• ▄▌▐ ▄ ▄▄▌  ▄▄▄ .▄▄▄  ▄▄▄ .",
            "  ▐█ ▀█ ▀▄ █·█▪██▌•█▌▐███•  ▀▄.▀·▀▄ █·▀▄.▀·",
            "  ▄█▀▀█ ▀▀▄ █·█▌▐█▌▐█▐▐▌██▪  ▐▀▀▪▄▐▀▀▄ ▐▀▀▪▄",
            "  ▐█ ▪▐▌▐█•█▌▐█▄█▌███▐█▌▐█▌▐▌▐█▄▄▌▐█•█▌▐█▄▄▌",
            "   ▀  ▀ .▀  ▀ ▀▀▀ ▀▀▀ ▀▪.▀▀▀  ▀▀▀ .▀  ▀ ▀▀▀ ",
        ],
    ]

    colors = [CYBER_BLUE, CYBER_GREEN, CYBER_PINK]

    for frame_idx, frame in enumerate(banner_frames):
        clear_screen()
        color = colors[frame_idx % len(colors)]
        for line in frame:
            console.print(f"[{color}]{line}[/]")
        time.sleep(0.15)

    # Final 3D layered effect
    clear_screen()
    console.print(
        f"[bold {CYBER_BLUE}]    ╔══════════════════════════════════════════════════════════════╗[/]"
    )
    console.print(
        f"[bold {CYBER_GREEN}]    ║  ADVANCED CLI EXPENSE TRACKER v4.0                           ║[/]"
    )
    console.print(
        f"[bold {CYBER_PINK}]    ║  Multi-User • AI Insights • Financial Analytics                ║[/]"
    )
    console.print(
        f"[bold {CYBER_YELLOW}]    ║  Developed by issu321                                          ║[/]"
    )
    console.print(
        f"[bold {CYBER_BLUE}]    ╚══════════════════════════════════════════════════════════════╝[/]"
    )

    # Progress animation
    with Progress(
        SpinnerColumn(spinner_name="dots", style=f"bold {CYBER_CYAN}"),
        TextColumn(f"[bold {CYBER_GREEN}]{{task.description}}[/]"),
        BarColumn(bar_width=40, style=CYBER_BLUE, complete_style=CYBER_GREEN),
        TextColumn(f"[bold {CYBER_YELLOW}]{{task.percentage:>3.0f}}%[/]"),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task("Initializing Cyber Systems...", total=100)
        for i in range(0, 101, 5):
            progress.update(task, completed=i)
            time.sleep(0.03)

    console.print(
        f"[bold {CYBER_GREEN}]✓ Systems Online[/]  [dim]Database Connected[/]  [dim]Analytics Engine Ready[/]"
    )
    time.sleep(0.3)


def display_banner():
    if os.path.exists("assets/banner.txt"):
        with open("assets/banner.txt", "r", encoding="utf-8") as f:
            banner = f.read()
        console.print(f"[bold {CYBER_BLUE}]{banner}[/]")
    else:
        console.print(
            f"[bold {CYBER_BLUE}]    ╔══════════════════════════════════════════════════════════════╗[/]"
        )
        console.print(
            f"[bold {CYBER_GREEN}]    ║  ADVANCED CLI EXPENSE TRACKER v4.0                           ║[/]"
        )
        console.print(
            f"[bold {CYBER_PINK}]    ║  Multi-User • AI Insights • Financial Analytics                ║[/]"
        )
        console.print(
            f"[bold {CYBER_YELLOW}]    ║  Developed by issu321                                          ║[/]"
        )
        console.print(
            f"[bold {CYBER_BLUE}]    ╚══════════════════════════════════════════════════════════════╝[/]"
        )


# ─── DATABASE ─────────────────────────────────────────────────────────────────


def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"
    )
    c.execute(
        "CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, amount REAL NOT NULL, category TEXT NOT NULL, description TEXT, date TEXT NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (user_id) REFERENCES users(id))"
    )
    c.execute(
        "CREATE TABLE IF NOT EXISTS income (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, amount REAL NOT NULL, source TEXT NOT NULL, description TEXT, date TEXT NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (user_id) REFERENCES users(id))"
    )
    c.execute(
        "CREATE TABLE IF NOT EXISTS budgets (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, category TEXT NOT NULL, amount REAL NOT NULL, month INTEGER NOT NULL, year INTEGER NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (user_id) REFERENCES users(id))"
    )
    c.execute(
        "CREATE TABLE IF NOT EXISTS savings_goals (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, name TEXT NOT NULL, target_amount REAL NOT NULL, current_amount REAL DEFAULT 0, deadline TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (user_id) REFERENCES users(id))"
    )
    c.execute(
        "CREATE TABLE IF NOT EXISTS recurring_expenses (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, name TEXT NOT NULL, amount REAL NOT NULL, category TEXT NOT NULL, frequency TEXT NOT NULL, next_due_date TEXT NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (user_id) REFERENCES users(id))"
    )

    conn.commit()
    conn.close()


def get_db():
    return sqlite3.connect(DB_FILE)


# ─── AUTH ─────────────────────────────────────────────────────────────────────


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def register_user():
    console.print(f"[bold {CYBER_BLUE}]═══ USER REGISTRATION ═══[/]")
    username = console.input(f"[{CYBER_GREEN}]Username:[/] ").strip()
    if not username:
        console.print(f"[bold {CYBER_RED}]✗ Username required[/]")
        return None

    password = getpass("Password: ")
    confirm = getpass("Confirm Password: ")
    if password != confirm:
        console.print(f"[bold {CYBER_RED}]✗ Passwords do not match[/]")
        return None
    if len(password) < 4:
        console.print(f"[bold {CYBER_RED}]✗ Password must be at least 4 characters[/]")
        return None

    conn = get_db()
    c = conn.cursor()
    try:
        c.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, hash_password(password)),
        )
        conn.commit()
        user_id = c.lastrowid
        console.print(f"[bold {CYBER_GREEN}]✓ Account created successfully![/]")
        return user_id
    except sqlite3.IntegrityError:
        console.print(f"[bold {CYBER_RED}]✗ Username already exists[/]")
        return None
    finally:
        conn.close()


def login_user():
    console.print(f"[bold {CYBER_BLUE}]═══ USER LOGIN ═══[/]")
    username = console.input(f"[{CYBER_GREEN}]Username:[/] ").strip()
    password = getpass("Password: ")

    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT id, password_hash FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()

    if row and row[1] == hash_password(password):
        console.print(f"[bold {CYBER_GREEN}]✓ Welcome back, {username}![/]")
        return row[0], username
    else:
        console.print(f"[bold {CYBER_RED}]✗ Invalid credentials[/]")
        return None, None


# ─── UI HELPERS ───────────────────────────────────────────────────────────────


def print_header(title: str):
    console.print(f"[bold {CYBER_BLUE}]{'═' * 60}[/]")
    console.print(f"[bold {CYBER_GREEN}]{title.center(60)}[/]")
    console.print(f"[bold {CYBER_BLUE}]{'═' * 60}[/]")


def print_footer():
    console.print(f"[dim]Developed by issu321 | github.com/issu321[/]")
    console.print(f"[bold {CYBER_BLUE}]{'═' * 60}[/]")


def menu_panel(options: list, title: str = "MENU") -> int:
    table = Table(show_header=False, box=box.ROUNDED, border_style=CYBER_BLUE, width=50)
    for i, opt in enumerate(options, 1):
        table.add_row(f"[bold {CYBER_YELLOW}]{i}.[/] [bold white]{opt}[/]")
    table.add_row(f"[bold {CYBER_RED}]0.[/] [bold white]Back / Exit[/]")
    console.print(
        Panel(table, title=f"[bold {CYBER_GREEN}]{title}[/]", border_style=CYBER_BLUE)
    )

    while True:
        choice = console.input(f"[{CYBER_CYAN}]Select option:[/] ").strip()
        if choice.isdigit() and 0 <= int(choice) <= len(options):
            return int(choice)
        console.print(f"[bold {CYBER_RED}]✗ Invalid choice[/]")


def confirm(msg: str = "Are you sure?") -> bool:
    resp = console.input(f"[{CYBER_YELLOW}]{msg} (y/n):[/] ").strip().lower()
    return resp == "y"


# ─── EXPENSES ─────────────────────────────────────────────────────────────────


def add_expense(user_id: int):
    print_header("ADD EXPENSE")
    try:
        amount = float(console.input(f"[{CYBER_GREEN}]Amount:[/] "))
        category = (
            console.input(
                f"[{CYBER_GREEN}]Category (food/transport/entertainment/bills/shopping/health/other):[/] "
            )
            .strip()
            .lower()
        )
        description = console.input(f"[{CYBER_GREEN}]Description:[/] ").strip()
        date_str = console.input(
            f"[{CYBER_GREEN}]Date (YYYY-MM-DD, default today):[/] "
        ).strip()
        if not date_str:
            date_str = datetime.now().strftime("%Y-%m-%d")

        conn = get_db()
        c = conn.cursor()
        c.execute(
            "INSERT INTO expenses (user_id, amount, category, description, date) VALUES (?, ?, ?, ?, ?)",
            (user_id, amount, category, description, date_str),
        )
        conn.commit()
        conn.close()
        console.print(f"[bold {CYBER_GREEN}]✓ Expense added successfully[/]")
    except ValueError:
        console.print(f"[bold {CYBER_RED}]✗ Invalid amount[/]")


def view_expenses(user_id: int):
    print_header("EXPENSE HISTORY")
    conn = get_db()
    c = conn.cursor()
    c.execute(
        "SELECT id, amount, category, description, date FROM expenses WHERE user_id = ? ORDER BY date DESC",
        (user_id,),
    )
    rows = c.fetchall()
    conn.close()

    if not rows:
        console.print(f"[dim]No expenses found[/]")
        return

    table = Table(show_header=True, box=box.ROUNDED, border_style=CYBER_BLUE)
    table.add_column("ID", style=CYBER_YELLOW, width=4)
    table.add_column("Date", style=CYBER_GREEN, width=12)
    table.add_column("Category", style=CYBER_CYAN, width=15)
    table.add_column("Amount", style=CYBER_PINK, justify="right")
    table.add_column("Description", style="white")

    for row in rows:
        table.add_row(str(row[0]), row[4], row[2], f"${row[1]:.2f}", row[3] or "-")
    console.print(table)


def edit_expense(user_id: int):
    view_expenses(user_id)
    try:
        exp_id = int(console.input(f"[{CYBER_GREEN}]Enter Expense ID to edit:[/] "))
        conn = get_db()
        c = conn.cursor()
        c.execute(
            "SELECT * FROM expenses WHERE id = ? AND user_id = ?", (exp_id, user_id)
        )
        if not c.fetchone():
            console.print(f"[bold {CYBER_RED}]✗ Expense not found[/]")
            conn.close()
            return

        amount = float(console.input(f"[{CYBER_GREEN}]New Amount:[/] "))
        category = console.input(f"[{CYBER_GREEN}]New Category:[/] ").strip().lower()
        description = console.input(f"[{CYBER_GREEN}]New Description:[/] ").strip()
        date_str = console.input(f"[{CYBER_GREEN}]New Date (YYYY-MM-DD):[/] ").strip()

        c.execute(
            "UPDATE expenses SET amount=?, category=?, description=?, date=? WHERE id=?",
            (amount, category, description, date_str, exp_id),
        )
        conn.commit()
        conn.close()
        console.print(f"[bold {CYBER_GREEN}]✓ Expense updated[/]")
    except ValueError:
        console.print(f"[bold {CYBER_RED}]✗ Invalid input[/]")


def delete_expense(user_id: int):
    view_expenses(user_id)
    try:
        exp_id = int(console.input(f"[{CYBER_GREEN}]Enter Expense ID to delete:[/] "))
        if confirm("Delete this expense?"):
            conn = get_db()
            c = conn.cursor()
            c.execute(
                "DELETE FROM expenses WHERE id = ? AND user_id = ?", (exp_id, user_id)
            )
            conn.commit()
            conn.close()
            console.print(f"[bold {CYBER_GREEN}]✓ Expense deleted[/]")
    except ValueError:
        console.print(f"[bold {CYBER_RED}]✗ Invalid ID[/]")


# ─── INCOME ───────────────────────────────────────────────────────────────────


def add_income(user_id: int):
    print_header("ADD INCOME")
    try:
        amount = float(console.input(f"[{CYBER_GREEN}]Amount:[/] "))
        source = (
            console.input(
                f"[{CYBER_GREEN}]Source (salary/freelance/investment/gift/other):[/] "
            )
            .strip()
            .lower()
        )
        description = console.input(f"[{CYBER_GREEN}]Description:[/] ").strip()
        date_str = console.input(
            f"[{CYBER_GREEN}]Date (YYYY-MM-DD, default today):[/] "
        ).strip()
        if not date_str:
            date_str = datetime.now().strftime("%Y-%m-%d")

        conn = get_db()
        c = conn.cursor()
        c.execute(
            "INSERT INTO income (user_id, amount, source, description, date) VALUES (?, ?, ?, ?, ?)",
            (user_id, amount, source, description, date_str),
        )
        conn.commit()
        conn.close()
        console.print(f"[bold {CYBER_GREEN}]✓ Income added successfully[/]")
    except ValueError:
        console.print(f"[bold {CYBER_RED}]✗ Invalid amount[/]")


def view_income(user_id: int):
    print_header("INCOME HISTORY")
    conn = get_db()
    c = conn.cursor()
    c.execute(
        "SELECT id, amount, source, description, date FROM income WHERE user_id = ? ORDER BY date DESC",
        (user_id,),
    )
    rows = c.fetchall()
    conn.close()

    if not rows:
        console.print(f"[dim]No income records found[/]")
        return

    table = Table(show_header=True, box=box.ROUNDED, border_style=CYBER_BLUE)
    table.add_column("ID", style=CYBER_YELLOW, width=4)
    table.add_column("Date", style=CYBER_GREEN, width=12)
    table.add_column("Source", style=CYBER_CYAN, width=15)
    table.add_column("Amount", style=CYBER_PINK, justify="right")
    table.add_column("Description", style="white")

    for row in rows:
        table.add_row(str(row[0]), row[4], row[2], f"${row[1]:.2f}", row[3] or "-")
    console.print(table)


# ─── BUDGETS ──────────────────────────────────────────────────────────────────


def set_budget(user_id: int):
    print_header("SET MONTHLY BUDGET")
    category = console.input(f"[{CYBER_GREEN}]Category:[/] ").strip().lower()
    try:
        amount = float(console.input(f"[{CYBER_GREEN}]Budget Amount:[/] "))
        month = int(console.input(f"[{CYBER_GREEN}]Month (1-12):[/] "))
        year = int(console.input(f"[{CYBER_GREEN}]Year:[/] "))

        conn = get_db()
        c = conn.cursor()
        c.execute(
            "DELETE FROM budgets WHERE user_id=? AND category=? AND month=? AND year=?",
            (user_id, category, month, year),
        )
        c.execute(
            "INSERT INTO budgets (user_id, category, amount, month, year) VALUES (?, ?, ?, ?, ?)",
            (user_id, category, amount, month, year),
        )
        conn.commit()
        conn.close()
        console.print(
            f"[bold {CYBER_GREEN}]✓ Budget set for {category} - ${amount:.2f}[/]"
        )
    except ValueError:
        console.print(f"[bold {CYBER_RED}]✗ Invalid input[/]")


def view_budgets(user_id: int):
    print_header("BUDGET OVERVIEW")
    now = datetime.now()
    month, year = now.month, now.year

    conn = get_db()
    c = conn.cursor()
    c.execute(
        "SELECT category, amount FROM budgets WHERE user_id=? AND month=? AND year=?",
        (user_id, month, year),
    )
    budgets = {row[0]: row[1] for row in c.fetchall()}

    c.execute(
        "SELECT category, SUM(amount) FROM expenses WHERE user_id=? AND strftime('%m', date)=? AND strftime('%Y', date)=? GROUP BY category",
        (user_id, f"{month:02d}", str(year)),
    )
    spent = {row[0]: row[1] for row in c.fetchall()}
    conn.close()

    if not budgets:
        console.print(f"[dim]No budgets set for {now.strftime('%B %Y')}[/]")
        return

    table = Table(show_header=True, box=box.ROUNDED, border_style=CYBER_BLUE)
    table.add_column("Category", style=CYBER_CYAN)
    table.add_column("Budget", style=CYBER_GREEN, justify="right")
    table.add_column("Spent", style=CYBER_YELLOW, justify="right")
    table.add_column("Remaining", style=CYBER_PINK, justify="right")
    table.add_column("Status", style="bold")

    for cat, budget in budgets.items():
        s = spent.get(cat, 0)
        rem = budget - s
        pct = (s / budget * 100) if budget > 0 else 0
        if pct > 100:
            status = f"[bold {CYBER_RED}]OVER BUDGET[/]"
        elif pct > 80:
            status = f"[bold {CYBER_YELLOW}]WARNING[/]"
        else:
            status = f"[bold {CYBER_GREEN}]OK[/]"
        table.add_row(cat, f"${budget:.2f}", f"${s:.2f}", f"${rem:.2f}", status)
    console.print(table)


# ─── SAVINGS GOALS ────────────────────────────────────────────────────────────


def add_savings_goal(user_id: int):
    print_header("CREATE SAVINGS GOAL")
    name = console.input(f"[{CYBER_GREEN}]Goal Name:[/] ").strip()
    try:
        target = float(console.input(f"[{CYBER_GREEN}]Target Amount:[/] "))
        current = float(
            console.input(f"[{CYBER_GREEN}]Current Amount (default 0):[/] ") or 0
        )
        deadline = console.input(
            f"[{CYBER_GREEN}]Deadline (YYYY-MM-DD, optional):[/] "
        ).strip()

        conn = get_db()
        c = conn.cursor()
        c.execute(
            "INSERT INTO savings_goals (user_id, name, target_amount, current_amount, deadline) VALUES (?, ?, ?, ?, ?)",
            (user_id, name, target, current, deadline if deadline else None),
        )
        conn.commit()
        conn.close()
        console.print(f"[bold {CYBER_GREEN}]✓ Savings goal created[/]")
    except ValueError:
        console.print(f"[bold {CYBER_RED}]✗ Invalid amount[/]")


def view_savings_goals(user_id: int):
    print_header("SAVINGS GOALS")
    conn = get_db()
    c = conn.cursor()
    c.execute(
        "SELECT id, name, target_amount, current_amount, deadline FROM savings_goals WHERE user_id = ?",
        (user_id,),
    )
    rows = c.fetchall()
    conn.close()

    if not rows:
        console.print(f"[dim]No savings goals found[/]")
        return

    table = Table(show_header=True, box=box.ROUNDED, border_style=CYBER_BLUE)
    table.add_column("ID", style=CYBER_YELLOW, width=4)
    table.add_column("Goal", style=CYBER_CYAN)
    table.add_column("Target", style=CYBER_GREEN, justify="right")
    table.add_column("Current", style=CYBER_PINK, justify="right")
    table.add_column("Progress", style=CYBER_YELLOW)
    table.add_column("Deadline", style="white")

    for row in rows:
        pct = (row[3] / row[2] * 100) if row[2] > 0 else 0
        bar_len = 20
        filled = int(bar_len * pct / 100)
        bar = f"[{'█' * filled}{'░' * (bar_len - filled)}] {pct:.1f}%"
        color = (
            CYBER_GREEN if pct >= 100 else (CYBER_YELLOW if pct >= 50 else CYBER_RED)
        )
        table.add_row(
            str(row[0]),
            row[1],
            f"${row[2]:.2f}",
            f"${row[3]:.2f}",
            f"[{color}]{bar}[/]",
            row[4] or "-",
        )
    console.print(table)


def update_savings_goal(user_id: int):
    view_savings_goals(user_id)
    try:
        goal_id = int(console.input(f"[{CYBER_GREEN}]Enter Goal ID to update:[/] "))
        amount = float(console.input(f"[{CYBER_GREEN}]Add to current amount:[/] "))

        conn = get_db()
        c = conn.cursor()
        c.execute(
            "UPDATE savings_goals SET current_amount = current_amount + ? WHERE id = ? AND user_id = ?",
            (amount, goal_id, user_id),
        )
        conn.commit()
        conn.close()
        console.print(f"[bold {CYBER_GREEN}]✓ Savings updated[/]")
    except ValueError:
        console.print(f"[bold {CYBER_RED}]✗ Invalid input[/]")


# ─── RECURRING EXPENSES ───────────────────────────────────────────────────────


def add_recurring(user_id: int):
    print_header("ADD RECURRING EXPENSE")
    name = console.input(f"[{CYBER_GREEN}]Name (e.g., Netflix, Rent):[/] ").strip()
    try:
        amount = float(console.input(f"[{CYBER_GREEN}]Amount:[/] "))
        category = console.input(f"[{CYBER_GREEN}]Category:[/] ").strip().lower()
        freq = (
            console.input(f"[{CYBER_GREEN}]Frequency (weekly/monthly/yearly):[/] ")
            .strip()
            .lower()
        )
        next_due = console.input(
            f"[{CYBER_GREEN}]Next Due Date (YYYY-MM-DD):[/] "
        ).strip()

        conn = get_db()
        c = conn.cursor()
        c.execute(
            "INSERT INTO recurring_expenses (user_id, name, amount, category, frequency, next_due_date) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, name, amount, category, freq, next_due),
        )
        conn.commit()
        conn.close()
        console.print(f"[bold {CYBER_GREEN}]✓ Recurring expense added[/]")
    except ValueError:
        console.print(f"[bold {CYBER_RED}]✗ Invalid amount[/]")


def view_recurring(user_id: int):
    print_header("RECURRING EXPENSES")
    conn = get_db()
    c = conn.cursor()
    c.execute(
        "SELECT id, name, amount, category, frequency, next_due_date FROM recurring_expenses WHERE user_id = ?",
        (user_id,),
    )
    rows = c.fetchall()
    conn.close()

    if not rows:
        console.print(f"[dim]No recurring expenses found[/]")
        return

    table = Table(show_header=True, box=box.ROUNDED, border_style=CYBER_BLUE)
    table.add_column("ID", style=CYBER_YELLOW, width=4)
    table.add_column("Name", style=CYBER_CYAN)
    table.add_column("Amount", style=CYBER_PINK, justify="right")
    table.add_column("Category", style=CYBER_GREEN)
    table.add_column("Frequency", style=CYBER_YELLOW)
    table.add_column("Next Due", style="white")

    for row in rows:
        table.add_row(str(row[0]), row[1], f"${row[2]:.2f}", row[3], row[4], row[5])
    console.print(table)


def simulate_recurring(user_id: int):
    print_header("SIMULATE RECURRING EXPENSES")
    conn = get_db()
    c = conn.cursor()
    c.execute(
        "SELECT id, name, amount, category, frequency, next_due_date FROM recurring_expenses WHERE user_id = ?",
        (user_id,),
    )
    rows = c.fetchall()

    if not rows:
        console.print(f"[dim]No recurring expenses to simulate[/]")
        conn.close()
        return

    today = datetime.now().date()
    added = 0
    for row in rows:
        due = datetime.strptime(row[5], "%Y-%m-%d").date()
        if due <= today:
            c.execute(
                "INSERT INTO expenses (user_id, amount, category, description, date) VALUES (?, ?, ?, ?, ?)",
                (
                    user_id,
                    row[2],
                    row[3],
                    f"Recurring: {row[1]}",
                    today.strftime("%Y-%m-%d"),
                ),
            )

            if row[4] == "weekly":
                next_due = due + timedelta(weeks=1)
            elif row[4] == "monthly":
                next_due = due + timedelta(days=30)
            elif row[4] == "yearly":
                next_due = due + timedelta(days=365)
            else:
                next_due = due + timedelta(days=30)

            c.execute(
                "UPDATE recurring_expenses SET next_due_date = ? WHERE id = ?",
                (next_due.strftime("%Y-%m-%d"), row[0]),
            )
            added += 1

    conn.commit()
    conn.close()
    console.print(
        f"[bold {CYBER_GREEN}]✓ Simulated {added} recurring expense(s) added to expenses[/]"
    )


# ─── ANALYTICS ─────────────────────────────────────────────────────────────────


def spending_breakdown(user_id: int):
    print_header("SPENDING BREAKDOWN")
    conn = get_db()
    c = conn.cursor()
    c.execute(
        "SELECT category, SUM(amount) FROM expenses WHERE user_id = ? GROUP BY category ORDER BY SUM(amount) DESC",
        (user_id,),
    )
    rows = c.fetchall()
    conn.close()

    if not rows:
        console.print(f"[dim]No expense data[/]")
        return

    total = sum(r[1] for r in rows)
    table = Table(show_header=True, box=box.ROUNDED, border_style=CYBER_BLUE)
    table.add_column("Category", style=CYBER_CYAN)
    table.add_column("Amount", style=CYBER_PINK, justify="right")
    table.add_column("Percentage", style=CYBER_YELLOW, justify="right")

    for row in rows:
        pct = (row[1] / total * 100) if total > 0 else 0
        table.add_row(row[0], f"${row[1]:.2f}", f"{pct:.1f}%")
    table.add_row("[bold]TOTAL", f"[bold]${total:.2f}", "[bold]100%")
    console.print(table)

    console.print(f"[bold {CYBER_GREEN}]📊 Terminal Chart:[/]")
    categories = [r[0] for r in rows]
    amounts = [r[1] for r in rows]
    plt.clear_figure()
    plt.bar(categories, amounts, color="cyan")
    plt.title("Spending by Category")
    plt.xlabel("Category")
    plt.ylabel("Amount ($)")
    plt.show()


def monthly_trends(user_id: int):
    print_header("MONTHLY TRENDS")
    conn = get_db()
    c = conn.cursor()
    c.execute(
        "SELECT strftime('%Y-%m', date) as month, SUM(amount) FROM expenses WHERE user_id = ? GROUP BY month ORDER BY month DESC LIMIT 12",
        (user_id,),
    )
    rows = c.fetchall()
    conn.close()

    if not rows:
        console.print(f"[dim]No data available[/]")
        return

    table = Table(show_header=True, box=box.ROUNDED, border_style=CYBER_BLUE)
    table.add_column("Month", style=CYBER_CYAN)
    table.add_column("Total Spent", style=CYBER_PINK, justify="right")

    months = []
    amounts = []
    for row in reversed(rows):
        table.add_row(row[0], f"${row[1]:.2f}")
        months.append(row[0])
        amounts.append(row[1])
    console.print(table)

    console.print(f"[bold {CYBER_GREEN}]📈 Trend Chart:[/]")
    plt.clear_figure()
    plt.plot(months, amounts, color="green", marker="dot")
    plt.title("Monthly Spending Trend")
    plt.xlabel("Month")
    plt.ylabel("Amount ($)")
    plt.show()


def financial_summary(user_id: int):
    print_header("FINANCIAL SUMMARY")
    conn = get_db()
    c = conn.cursor()

    c.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM income WHERE user_id = ?", (user_id,)
    )
    total_income = c.fetchone()[0]

    c.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE user_id = ?", (user_id,)
    )
    total_expenses = c.fetchone()[0]

    c.execute(
        "SELECT COALESCE(SUM(current_amount), 0) FROM savings_goals WHERE user_id = ?",
        (user_id,),
    )
    total_savings = c.fetchone()[0]

    c.execute(
        "SELECT COALESCE(SUM(target_amount), 0) FROM savings_goals WHERE user_id = ?",
        (user_id,),
    )
    total_targets = c.fetchone()[0]

    conn.close()

    balance = total_income - total_expenses

    grid = Table.grid(expand=True)
    grid.add_column(justify="center")
    grid.add_column(justify="center")
    grid.add_column(justify="center")
    grid.add_column(justify="center")

    grid.add_row(
        Panel(
            f"[bold {CYBER_GREEN}]${total_income:,.2f}[/]\n[dim]Total Income[/]",
            border_style=CYBER_GREEN,
        ),
        Panel(
            f"[bold {CYBER_RED}]${total_expenses:,.2f}[/]\n[dim]Total Expenses[/]",
            border_style=CYBER_RED,
        ),
        Panel(
            f"[bold {CYBER_BLUE}]${balance:,.2f}[/]\n[dim]Net Balance[/]",
            border_style=CYBER_BLUE,
        ),
        Panel(
            f"[bold {CYBER_YELLOW}]${total_savings:,.2f} / ${total_targets:,.2f}[/]\n[dim]Savings Progress[/]",
            border_style=CYBER_YELLOW,
        ),
    )
    console.print(grid)


# ─── AI INSIGHTS ──────────────────────────────────────────────────────────────


def generate_insights(user_id: int):
    print_header("AI FINANCIAL INSIGHTS")
    conn = get_db()
    c = conn.cursor()

    insights = []

    now = datetime.now()
    this_month = now.strftime("%Y-%m")
    last_month = (now.replace(day=1) - timedelta(days=1)).strftime("%Y-%m")

    c.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE user_id = ? AND strftime('%Y-%m', date) = ?",
        (user_id, this_month),
    )
    this_spent = c.fetchone()[0]

    c.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE user_id = ? AND strftime('%Y-%m', date) = ?",
        (user_id, last_month),
    )
    last_spent = c.fetchone()[0]

    if last_spent > 0:
        change = ((this_spent - last_spent) / last_spent) * 100
        if change > 0:
            insights.append(
                f"[bold {CYBER_RED}]📉 You spent {change:.1f}% more this month compared to last month.[/]"
            )
        elif change < 0:
            insights.append(
                f"[bold {CYBER_GREEN}]📈 Great job! You spent {abs(change):.1f}% less this month.[/]"
            )

    c.execute(
        "SELECT category, SUM(amount) FROM expenses WHERE user_id = ? AND strftime('%Y-%m', date) = ? GROUP BY category ORDER BY SUM(amount) DESC LIMIT 1",
        (user_id, this_month),
    )
    top = c.fetchone()
    if top:
        insights.append(
            f"[bold {CYBER_YELLOW}]💡 Your top spending category this month is '{top[0]}' at ${top[1]:.2f}.[/]"
        )

    c.execute(
        "SELECT category, amount FROM budgets WHERE user_id = ? AND month = ? AND year = ?",
        (user_id, now.month, now.year),
    )
    budgets = c.fetchall()
    for cat, budget in budgets:
        c.execute(
            "SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE user_id = ? AND category = ? AND strftime('%Y-%m', date) = ?",
            (user_id, cat, this_month),
        )
        spent = c.fetchone()[0]
        if spent > budget:
            over = spent - budget
            insights.append(
                f"[bold {CYBER_RED}]⚠️  OVER BUDGET: You exceeded your '{cat}' budget by ${over:.2f}.[/]"
            )
        elif spent > budget * 0.8:
            insights.append(
                f"[bold {CYBER_YELLOW}]⚡ WARNING: You've used {(spent/budget*100):.0f}% of your '{cat}' budget.[/]"
            )

    c.execute(
        "SELECT name, target_amount, current_amount FROM savings_goals WHERE user_id = ?",
        (user_id,),
    )
    goals = c.fetchall()
    for name, target, current in goals:
        pct = (current / target * 100) if target > 0 else 0
        if pct >= 100:
            insights.append(
                f"[bold {CYBER_GREEN}]🎉 GOAL ACHIEVED: '{name}' is fully funded![/]"
            )
        elif pct >= 75:
            insights.append(
                f"[bold {CYBER_CYAN}]🚀 Almost there! '{name}' is {pct:.0f}% complete.[/]"
            )

    c.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM income WHERE user_id = ? AND strftime('%Y-%m', date) = ?",
        (user_id, this_month),
    )
    this_income = c.fetchone()[0]
    if this_income > 0:
        ratio = (this_spent / this_income) * 100
        if ratio > 90:
            insights.append(
                f"[bold {CYBER_RED}]🚨 You're spending {ratio:.0f}% of your income. Consider saving more.[/]"
            )
        elif ratio < 50:
            insights.append(
                f"[bold {CYBER_GREEN}]✅ Excellent! You're only spending {ratio:.0f}% of your income.[/]"
            )

    conn.close()

    if insights:
        for insight in insights:
            console.print(Panel(insight, border_style=CYBER_PURPLE, padding=(0, 2)))
    else:
        console.print(f"[dim]Add more data to generate insights[/]")


# ─── SEARCH ───────────────────────────────────────────────────────────────────


def search_expenses(user_id: int):
    print_header("SEARCH EXPENSES")
    console.print(f"[dim]Leave blank to skip filter[/]")

    category = console.input(f"[{CYBER_GREEN}]Category:[/] ").strip().lower()
    date_from = console.input(f"[{CYBER_GREEN}]Date From (YYYY-MM-DD):[/] ").strip()
    date_to = console.input(f"[{CYBER_GREEN}]Date To (YYYY-MM-DD):[/] ").strip()
    keyword = (
        console.input(f"[{CYBER_GREEN}]Keyword in description:[/] ").strip().lower()
    )

    query = (
        "SELECT id, amount, category, description, date FROM expenses WHERE user_id = ?"
    )
    params = [user_id]

    if category:
        query += " AND category = ?"
        params.append(category)
    if date_from:
        query += " AND date >= ?"
        params.append(date_from)
    if date_to:
        query += " AND date <= ?"
        params.append(date_to)
    if keyword:
        query += " AND LOWER(description) LIKE ?"
        params.append(f"%{keyword}%")

    query += " ORDER BY date DESC"

    conn = get_db()
    c = conn.cursor()
    c.execute(query, params)
    rows = c.fetchall()
    conn.close()

    console.print(f"[bold {CYBER_GREEN}]Found {len(rows)} result(s)[/]")

    if rows:
        table = Table(show_header=True, box=box.ROUNDED, border_style=CYBER_BLUE)
        table.add_column("ID", style=CYBER_YELLOW, width=4)
        table.add_column("Date", style=CYBER_GREEN, width=12)
        table.add_column("Category", style=CYBER_CYAN, width=15)
        table.add_column("Amount", style=CYBER_PINK, justify="right")
        table.add_column("Description", style="white")
        for row in rows:
            table.add_row(str(row[0]), row[4], row[2], f"${row[1]:.2f}", row[3] or "-")
        console.print(table)


# ─── EXPORT ───────────────────────────────────────────────────────────────────


def export_csv(user_id: int, username: str):
    print_header("EXPORT TO CSV")
    filename = console.input(
        f"[{CYBER_GREEN}]Filename (default: export_{username}.csv):[/] "
    ).strip()
    if not filename:
        filename = f"export_{username}.csv"
    if not filename.endswith(".csv"):
        filename += ".csv"

    conn = get_db()
    c = conn.cursor()

    c.execute(
        "SELECT date, category, amount, description FROM expenses WHERE user_id = ? ORDER BY date DESC",
        (user_id,),
    )
    expenses = c.fetchall()

    c.execute(
        "SELECT date, source, amount, description FROM income WHERE user_id = ? ORDER BY date DESC",
        (user_id,),
    )
    income_rows = c.fetchall()
    conn.close()

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["=== EXPENSES ==="])
        writer.writerow(["Date", "Category", "Amount", "Description"])
        writer.writerows(expenses)
        writer.writerow([])
        writer.writerow(["=== INCOME ==="])
        writer.writerow(["Date", "Source", "Amount", "Description"])
        writer.writerows(income_rows)

    console.print(f"[bold {CYBER_GREEN}]✓ Exported to {filename}[/]")

    def export_txt(user_id: int, username: str):
        print_header("EXPORT TO TXT")

    filename = console.input(
        f"[{CYBER_GREEN}]Filename (default: summary_{username}.txt):[/] "
    ).strip()
    if not filename:
        filename = f"summary_{username}.txt"
    if not filename.endswith(".txt"):
        filename += ".txt"

    conn = get_db()
    c = conn.cursor()

    c.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM income WHERE user_id = ?", (user_id,)
    )
    total_income = c.fetchone()[0]
    c.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE user_id = ?", (user_id,)
    )
    total_expenses = c.fetchone()[0]

    c.execute(
        "SELECT date, category, amount, description FROM expenses WHERE user_id = ? ORDER BY date DESC LIMIT 20",
        (user_id,),
    )
    recent_expenses = c.fetchall()
    conn.close()

    report_lines = [
        "=" * 50,
        "   ADVANCED CLI EXPENSE TRACKER - REPORT",
        f"   User: {username}",
        f"   Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "=" * 50,
        "",
        f"Total Income:    ${total_income:,.2f}",
        f"Total Expenses:  ${total_expenses:,.2f}",
        f"Net Balance:     ${total_income - total_expenses:,.2f}",
        "",
        "Recent Expenses:",
        "-" * 50,
    ]

    for row in recent_expenses:
        report_lines.append(f"{row[0]} | {row[1]:15} | ${row[2]:8.2f} | {row[3]}")

    report_lines.append("")
    report_lines.append("Developed by issu321 | github.com/issu321")

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    console.print(f"[bold {CYBER_GREEN}]✓ Exported to {filename}[/]")


# ─── MENUS ────────────────────────────────────────────────────────────────────


def expense_menu(user_id: int):
    while True:
        print_header("EXPENSE MANAGEMENT")
        choice = menu_panel(
            [
                "Add Expense",
                "View Expenses",
                "Edit Expense",
                "Delete Expense",
                "Search Expenses",
            ],
            "EXPENSES",
        )

        if choice == 1:
            add_expense(user_id)
        elif choice == 2:
            view_expenses(user_id)
        elif choice == 3:
            edit_expense(user_id)
        elif choice == 4:
            delete_expense(user_id)
        elif choice == 5:
            search_expenses(user_id)
        elif choice == 0:
            break
        console.input(f"[{CYBER_BLUE}]Press Enter to continue...[/]")


def income_menu(user_id: int):
    while True:
        print_header("INCOME MANAGEMENT")
        choice = menu_panel(["Add Income", "View Income"], "INCOME")

        if choice == 1:
            add_income(user_id)
        elif choice == 2:
            view_income(user_id)
        elif choice == 0:
            break
        console.input(f"[{CYBER_BLUE}]Press Enter to continue...[/]")


def budget_menu(user_id: int):
    while True:
        print_header("BUDGET MANAGEMENT")
        choice = menu_panel(["Set Budget", "View Budgets"], "BUDGET")

        if choice == 1:
            set_budget(user_id)
        elif choice == 2:
            view_budgets(user_id)
        elif choice == 0:
            break
        console.input(f"[{CYBER_BLUE}]Press Enter to continue...[/]")


def savings_menu(user_id: int):
    while True:
        print_header("SAVINGS GOALS")
        choice = menu_panel(["Create Goal", "View Goals", "Update Progress"], "SAVINGS")

        if choice == 1:
            add_savings_goal(user_id)
        elif choice == 2:
            view_savings_goals(user_id)
        elif choice == 3:
            update_savings_goal(user_id)
        elif choice == 0:
            break
        console.input(f"[{CYBER_BLUE}]Press Enter to continue...[/]")


def recurring_menu(user_id: int):
    while True:
        print_header("RECURRING EXPENSES")
        choice = menu_panel(
            ["Add Recurring", "View Recurring", "Simulate & Add to Expenses"],
            "RECURRING",
        )

        if choice == 1:
            add_recurring(user_id)
        elif choice == 2:
            view_recurring(user_id)
        elif choice == 3:
            simulate_recurring(user_id)
        elif choice == 0:
            break
        console.input(f"[{CYBER_BLUE}]Press Enter to continue...[/]")


def analytics_menu(user_id: int):
    while True:
        print_header("FINANCIAL ANALYTICS")
        choice = menu_panel(
            [
                "Spending Breakdown",
                "Monthly Trends",
                "Financial Summary",
                "AI Insights",
            ],
            "ANALYTICS",
        )

        if choice == 1:
            spending_breakdown(user_id)
        elif choice == 2:
            monthly_trends(user_id)
        elif choice == 3:
            financial_summary(user_id)
        elif choice == 4:
            generate_insights(user_id)
        elif choice == 0:
            break
        console.input(f"[{CYBER_BLUE}]Press Enter to continue...[/]")


def export_menu(user_id: int, username: str):
    while True:
        print_header("EXPORT DATA")
        choice = menu_panel(["Export to CSV", "Export to TXT Summary"], "EXPORT")

        if choice == 1:
            export_csv(user_id, username)
        elif choice == 2:
            export_txt(user_id, username)
        elif choice == 0:
            break
        console.input(f"[{CYBER_BLUE}]Press Enter to continue...[/]")


# ─── MAIN ─────────────────────────────────────────────────────────────────────


def main():
    init_db()
    animated_banner()

    user_id = None
    username = None

    while not user_id:
        clear_screen()
        display_banner()
        console.print(f"[bold {CYBER_BLUE}]═══ AUTHENTICATION ═══[/]")
        choice = menu_panel(["Login", "Register"], "WELCOME")

        if choice == 1:
            result = login_user()
            if result[0]:
                user_id, username = result
        elif choice == 2:
            uid = register_user()
            if uid:
                user_id = uid
                username = console.input(
                    f"[{CYBER_GREEN}]Enter your username again:[/] "
                ).strip()
        elif choice == 0:
            console.print(f"[bold {CYBER_RED}]Goodbye![/]")
            sys.exit(0)

        console.input(f"[{CYBER_BLUE}]Press Enter to continue...[/]")

    while True:
        clear_screen()
        display_banner()
        console.print(f"[bold {CYBER_GREEN}]👤 Logged in as: {username}[/]")

        choice = menu_panel(
            [
                "💸 Expense Management",
                "💰 Income Management",
                "📊 Budget Management",
                "🎯 Savings Goals",
                "🔄 Recurring Expenses",
                "📈 Analytics & Insights",
                "🔍 Search & Filter",
                "📤 Export Data",
                "🤖 AI Financial Insights",
            ],
            "MAIN MENU",
        )

        if choice == 1:
            expense_menu(user_id)
        elif choice == 2:
            income_menu(user_id)
        elif choice == 3:
            budget_menu(user_id)
        elif choice == 4:
            savings_menu(user_id)
        elif choice == 5:
            recurring_menu(user_id)
        elif choice == 6:
            analytics_menu(user_id)
        elif choice == 7:
            search_expenses(user_id)
        elif choice == 8:
            export_menu(user_id, username)
        elif choice == 9:
            generate_insights(user_id)
        elif choice == 0:
            console.print(f"[bold {CYBER_GREEN}]👋 Logging out...[/]")
            break

    console.print(f"[bold {CYBER_BLUE}]{'═' * 60}[/]")
    console.print(
        f"[bold {CYBER_GREEN}]Thanks for using Advanced CLI Expense Tracker[/]"
    )
    console.print(f"[dim]Developed by issu321 | github.com/issu321[/]")
    console.print(f"[bold {CYBER_BLUE}]{'═' * 60}[/]")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print(f"[bold {CYBER_RED}]Interrupted by user[/]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[bold {CYBER_RED}]Error: {e}[/]")
        sys.exit(1)
