<div align="center">

# 💸 Expense Tracker

**Track every rupee. See where it goes.**

A sleek dark-mode desktop app for logging expenses and visualizing your spending.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

</div>

---

## ⚡ Features

| | |
|---|---|
| ➕ **Add expenses** | Date, category, amount and note |
| 🗄️ **Local storage** | Everything saved in a SQLite database |
| 🥧 **Live pie chart** | Spending by category, updated instantly |
| 🧮 **Running total** | Always see how much you've spent |
| 🗑️ **Delete entries** | Select a row and remove it |
| 📤 **CSV export** | Download all your data |
| 🌙 **Dark mode UI** | Built with CustomTkinter |

## 🛠️ Built With

- **Python**
- **CustomTkinter** for the GUI
- **SQLite** for the database
- **Matplotlib** for charts
- **pytest** for tests

## 🚀 Quick Start

```bash
git clone https://github.com/<your-username>/expense-tracker.git
cd expense-tracker
pip install -r requirements.txt
python main.py
```

## 📁 Project Structure

```
expense-tracker/
├── main.py
├── requirements.txt
├── src/expense_tracker/
│   ├── config.py
│   ├── db.py
│   └── ui.py
└── tests/
```

## 🧪 Run Tests

```bash
pip install -r requirements-dev.txt
pytest
```

## 📄 License

MIT. See [LICENSE](LICENSE).
