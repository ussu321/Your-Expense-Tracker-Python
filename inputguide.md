# 📖 Advanced 3D Expense Tracker - Input Guide

> **Streamlit Edition** | **Developed by issu321** | [GitHub](https://github.com/issu321)

---

## 🖥️ Navigation

The application uses a **sidebar navigation menu** on the left.

| Icon | Page | Description |
|------|------|-------------|
| 🏠 | Dashboard | Overview with metric cards & recent activity |
| 💸 | Expenses | Add, view, edit, search expenses |
| 💰 | Income | Track income sources |
| 📊 | Budgets | Set and monitor monthly budgets |
| 🎯 | Savings | Create and track financial goals |
| 🔄 | Recurring | Manage subscriptions and bills |
| 📈 | Analytics | 3D charts, trends, summaries |
| 🤖 | AI Insights | Smart financial suggestions |
| 📤 | Export | Download CSV/TXT reports |

---

## 👤 Account Examples

### Registration
1. Click **📝 REGISTER** tab on the login screen
2. Enter your username
3. Enter password (minimum 4 characters)
4. Confirm password
5. Click **🚀 CREATE ACCOUNT**

### Login
1. Click **🔐 LOGIN** tab
2. Enter your username
3. Enter your password
4. Click **🚀 LAUNCH**

---

## 💸 Expense Examples

### Adding an Expense
1. Navigate to **💸 Expenses**
2. Click **➕ ADD** tab
3. Fill the form:
   - **Amount**: `45.50`
   - **Category**: `food`
   - **Date**: Select from calendar
   - **Description**: `Lunch at Italian restaurant`
4. Click **💾 SAVE EXPENSE**

### Common Categories
- `food` — Groceries, dining, snacks
- `transport` — Gas, public transit, rideshare
- `entertainment` — Movies, games, streaming
- `bills` — Electricity, water, internet
- `shopping` — Clothing, electronics, online
- `health` — Medical, pharmacy, gym
- `other` — Miscellaneous

---

## 💰 Income Examples

### Adding Income
1. Navigate to **💰 Income**
2. Click **➕ ADD** tab
3. Fill the form:
   - **Amount**: `3500.00`
   - **Source**: `salary`
   - **Date**: Select from calendar
   - **Description**: `Monthly paycheck`
4. Click **💾 SAVE INCOME**

### Common Sources
- `salary` — Regular employment income
- `freelance` — Contract work payments
- `investment` — Dividends, stock gains
- `gift` — Received gifts or bonuses
- `other` — Miscellaneous income

---

## 📊 Budgeting Examples

### Setting a Budget
1. Navigate to **📊 Budgets**
2. Click **➕ SET BUDGET** tab
3. Fill the form:
   - **Category**: `food`
   - **Budget ($)**: `500.00`
   - **Month**: `5`
   - **Year**: `2026`
4. Click **💾 SET BUDGET**

### Viewing Budgets
1. Click **📋 VIEW BUDGETS** tab
2. See 3D gauge charts for each category
3. Green zone = under budget, Yellow = warning, Red = over budget

---

## 🎯 Savings Goals Examples

### Creating a Goal
1. Navigate to **🎯 Savings**
2. Click **➕ CREATE** tab
3. Fill the form:
   - **Goal Name**: `New Laptop`
   - **Target ($)**: `1500.00`
   - **Current ($)**: `300.00`
   - **Deadline**: Select date
4. Click **🚀 CREATE GOAL**

### Updating Progress
1. Click **📋 VIEW / UPDATE** tab
2. See circular progress indicators for each goal
3. Enter amount to add in the input field
4. Click **💰 UPDATE**

---

## 🔄 Recurring Expenses Examples

### Adding a Recurring Bill
1. Navigate to **🔄 Recurring**
2. Click **➕ ADD** tab
3. Fill the form:
   - **Name**: `Netflix Subscription`
   - **Amount**: `15.99`
   - **Category**: `entertainment`
   - **Frequency**: `monthly`
   - **Next Due Date**: Select date
4. Click **💾 SAVE**

### Simulating Recurring Expenses
1. Click **🔁 SIMULATE** tab
2. Click **🔁 SIMULATE RECURRING** button
3. System automatically adds due expenses to your expense log
4. Updates next due dates based on frequency

---

## 📈 Analytics Examples

### 3D Spending Breakdown
- Navigate to **📈 Analytics**
- See 3D bar chart showing spending by category
- Hover over bars for exact values

### 3D Monthly Trend
- See 3D scatter plot with connected lines
- Camera rotates around the data
- Shows spending patterns over time

### Financial Summary
- Four metric cards showing:
  - Total Income
  - Total Expenses
  - Net Balance
  - Savings Progress

### Category Distribution
- Interactive pie chart with donut hole
- Color-coded categories
- Percentage labels

---

## 🤖 AI Insights Examples

Navigate to **🤖 AI Insights** to see messages like:

```
📉 Spending Alert
You spent 35% more this month vs last month.

💡 Top Category
'food' leads at $450.00 this month.

⚠️ Over Budget
'shopping' exceeded by $120.50

🎉 Goal Achieved!
'Emergency Fund' is fully funded!

✅ Excellent Saver
Only spending 42% of your income
```

---

## 🔍 Search & Filter Examples

1. Navigate to **💸 Expenses**
2. Click **🔍 SEARCH** tab
3. Use filters:
   - **Category**: Select `food` or `All`
   - **From**: `2026-05-01`
   - **To**: `2026-05-31`
   - **Keyword**: `restaurant`
4. Click **🔎 SEARCH**
5. Results display in a data table below

---

## 📤 Export Examples

1. Navigate to **📤 Export**
2. Two options available:

### CSV Export
- Click **⬇️ DOWNLOAD CSV** button
- File: `export_username.csv`
- Contains all expenses and income data

### TXT Summary
- Click **⬇️ DOWNLOAD TXT** button
- File: `summary_username.txt`
- Contains formatted financial summary

---

## 🛠️ Troubleshooting

### Issue: "Module not found" error
**Solution:**
```bash
# Linux
source venv/bin/activate
pip install -r requirements.txt

# Windows
venv\Scriptsctivate
pip install -r requirements.txt
```

### Issue: Database is locked
**Solution:** Close any other browser tabs running the app. SQLite allows only one writer.

### Issue: 3D charts not displaying
**Solution:** Ensure your browser supports WebGL. Try Chrome or Firefox. Update your graphics drivers.

### Issue: Three.js background not showing
**Solution:** Check if JavaScript is enabled in your browser. The background requires an internet connection to load Three.js from CDN.

### Issue: Permission denied on install.sh
**Solution:**
```bash
chmod +x install.sh
./install.sh
```

### Issue: Streamlit not found
**Solution:**
```bash
pip install streamlit
# Or
python -m pip install streamlit
```

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `R` | Rerun the app (Streamlit default) |
| `Ctrl+C` | Stop the server (terminal) |

---

## 🌐 Browser Compatibility

| Browser | Support |
|---------|---------|
| Chrome | ✅ Full |
| Firefox | ✅ Full |
| Edge | ✅ Full |
| Safari | ✅ Partial (WebGL) |
| Mobile | ✅ Responsive layout |

---

<div align="center">

**Developed by [issu321](https://github.com/issu321)**

For more help, visit: [github.com/issu321/Advanced-CLI-Expense-Tracker](https://github.com/issu321/Advanced-CLI-Expense-Tracker)

</div>
