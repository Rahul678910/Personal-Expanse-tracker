# 💰 Personal Expense Tracker

[![CI](https://github.com/your-username/expense-tracker/actions/workflows/ci.yml/badge.svg)](https://github.com/your-username/expense-tracker/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue?logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)](https://www.python.org/)

A modern, responsive desktop application for logging personal expenses, visualizing spending habits by category with interactive charts, and exporting financial data to CSV. Built with **Python**, **CustomTkinter**, and **Matplotlib**.

---

## 📸 Preview

![Personal Expense Tracker Screenshot](docs/screenshot.png)

---

## ✨ Features

- **⚡ Instant Expense Logging:** Quickly enter date, category, amount, and notes with real-time field validation.
- **📊 Live Spending Breakdown:** Embedded Matplotlib pie chart dynamically computes category percentages with every change.
- **🌙 Sleek Dark Theme:** Built with CustomTkinter for high-DPI, modern dark-mode aesthetics.
- **🗃️ Zero-Config Local Storage:** Uses embedded SQLite (`expenses.db`) with automatic table creation—no external database servers needed.
- **📤 CSV Export:** Export complete historical expense records to `.csv` format for Excel, Google Sheets, or tax accounting.
- **🗑️ Multi-Row Deletion:** Select and remove one or multiple expense entries in a single action.
- **🧪 Fully Tested Backend:** Unit test suite covering all database queries, edge cases, and calculations.

---

## 🛠️ Tech Stack

| Component | Technology | Description |
|---|---|---|
| **Language** | Python 3.10+ | Core application logic |
| **GUI Framework** | CustomTkinter | Modern dark-themed desktop UI |
| **Data Visualization** | Matplotlib | Embedded dynamic pie chart canvas |
| **Database** | SQLite3 | Embedded ACID-compliant relational storage |
| **Testing** | Pytest & pytest-cov | Automated unit testing and coverage reports |
| **CI/CD** | GitHub Actions | Automated multi-OS test runners on push & PR |

---

## 🚀 Quickstart & Setup

### 1. Prerequisites
- Python 3.10 or higher installed on your system.

### 2. Clone the Repository
```bash
git clone https://github.com/your-username/expense-tracker.git
cd expense-tracker
```

### 3. Create a Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the Application
```bash
python expense_tracker.py
```

---

## 🧪 Running Tests

To run the automated test suite, install development dependencies:

```bash
pip install -r requirements-dev.txt
```

Run unit tests with pytest:
```bash
pytest tests/ -v
```

Generate a test coverage report:
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```

---

## 📂 Project Structure

```text
expense-tracker/
├── .github/
│   └── workflows/
│       └── ci.yml               # GitHub Actions CI workflow
├── docs/
│   └── screenshot.png           # Application UI preview image
├── tests/
│   ├── __init__.py
│   └── test_db.py               # Pytest database layer test suite
├── .gitignore                   # Python & SQLite ignore rules
├── expense_tracker.py           # Main application code (GUI + DB)
├── LICENSE                      # MIT License
├── README.md                    # Project documentation & guide
├── requirements.txt             # Production runtime dependencies
└── requirements-dev.txt         # Development & testing dependencies
```

---

## 🗺️ Roadmap

- [x] Embedded SQLite persistence engine
- [x] CustomTkinter dark-mode graphical user interface
- [x] Live pie chart category expenditure breakdown
- [x] One-click CSV export
- [x] Multi-item table deletion
- [x] Automated pytest test suite for DB operations
- [ ] 🔍 Date-range and text filtering search bar
- [ ] 💵 Multi-currency symbol customization (`$`, `€`, `£`, `₹`, `¥`)
- [ ] 📈 Monthly trend line chart
- [ ] 🎯 Category budget limits with warning alerts
- [ ] 📦 Standalone binary build via PyInstaller

---

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

Copyright (c) 2026 **Ram Das Murmu**.
