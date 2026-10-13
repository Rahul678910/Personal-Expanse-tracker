"""Personal Expense Tracker
Modern desktop application to log expenses, visualize category spending, and export CSV reports.

Install: pip install customtkinter matplotlib pillow
Run:     python expense_tracker.py
"""
import csv
import sqlite3
from datetime import date
from tkinter import ttk, messagebox, filedialog

import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

CATEGORIES = ["Food", "Transport", "Study", "Games", "Bills", "Other"]


class DB:
    """SQLite Database manager for tracking personal expenses."""

    def __init__(self, path="expenses.db"):
        self.path = path
        self.conn = sqlite3.connect(path)
        self.create_table()

    def create_table(self):
        """Initialize the expenses table if it does not already exist."""
        self.conn.execute(
            """CREATE TABLE IF NOT EXISTS expenses(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                day TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                note TEXT)"""
        )
        self.conn.commit()

    def add(self, day: str, cat: str, amount: float, note: str = "") -> int:
        """Add a new expense record and return its row ID."""
        cursor = self.conn.execute(
            "INSERT INTO expenses(day, category, amount, note) VALUES (?,?,?,?)",
            (day, cat, amount, note),
        )
        self.conn.commit()
        return cursor.lastrowid

    def delete(self, row_id: int) -> None:
        """Delete an expense record by its row ID."""
        self.conn.execute("DELETE FROM expenses WHERE id=?", (row_id,))
        self.conn.commit()

    def all(self):
        """Fetch all expenses sorted chronologically in descending order."""
        return self.conn.execute(
            "SELECT id, day, category, amount, note FROM expenses ORDER BY day DESC, id DESC"
        ).fetchall()

    def get_by_id(self, row_id: int):
        """Fetch a single expense by its ID."""
        return self.conn.execute(
            "SELECT id, day, category, amount, note FROM expenses WHERE id=?", (row_id,)
        ).fetchone()

    def totals_by_category(self):
        """Return total spending grouped by category."""
        return self.conn.execute(
            "SELECT category, SUM(amount) FROM expenses GROUP BY category ORDER BY SUM(amount) DESC"
        ).fetchall()

    def total_amount(self) -> float:
        """Return the sum of all recorded expense amounts."""
        row = self.conn.execute("SELECT SUM(amount) FROM expenses").fetchone()
        return float(row[0]) if row and row[0] is not None else 0.0

    def close(self):
        """Close the database connection."""
        self.conn.close()


class App(ctk.CTk):
    """Personal Expense Tracker GUI Application."""

    def __init__(self):
        super().__init__()
        self.title("Personal Expense Tracker")
        self.geometry("980x600")
        self.minsize(800, 500)
        ctk.set_appearance_mode("dark")
        self.db = DB()
        self._build_form()
        self._build_table()
        self._build_chart()
        self.refresh()

    # ---------- UI Builders ----------
    def _build_form(self):
        f = ctk.CTkFrame(self)
        f.pack(fill="x", padx=12, pady=(12, 6))

        self.date_e = ctk.CTkEntry(f, width=110)
        self.date_e.insert(0, date.today().isoformat())
        self.cat_m = ctk.CTkOptionMenu(f, values=CATEGORIES, width=120)
        self.amt_e = ctk.CTkEntry(f, width=100, placeholder_text="Amount")
        self.note_e = ctk.CTkEntry(f, width=220, placeholder_text="Note (optional)")

        for w in (self.date_e, self.cat_m, self.amt_e, self.note_e):
            w.pack(side="left", padx=6, pady=10)

        ctk.CTkButton(f, text="Add", width=70, command=self.add_expense).pack(side="left", padx=6)
        ctk.CTkButton(
            f, text="Delete", width=70, fg_color="#b33", hover_color="#922",
            command=self.delete_selected
        ).pack(side="left", padx=6)
        ctk.CTkButton(f, text="Export CSV", width=100, command=self.export_csv).pack(side="left", padx=6)

    def _build_table(self):
        body = ctk.CTkFrame(self)
        body.pack(fill="both", expand=True, padx=12, pady=6)

        left = ctk.CTkFrame(body)
        left.pack(side="left", fill="both", expand=True, padx=(0, 6))

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background="#2b2b2b",
            fieldbackground="#2b2b2b",
            foreground="white",
            rowheight=26,
        )
        style.configure("Treeview.Heading", background="#1f1f1f", foreground="white")

        cols = ("day", "category", "amount", "note")
        self.tree = ttk.Treeview(left, columns=cols, show="headings")
        for c, w in zip(cols, (100, 100, 80, 220)):
            self.tree.heading(c, text=c.title())
            self.tree.column(c, width=w)
        self.tree.pack(fill="both", expand=True, padx=6, pady=6)

        self.total_lbl = ctk.CTkLabel(left, text="Total: $0.00", font=("Arial", 16, "bold"))
        self.total_lbl.pack(pady=(0, 8))

        self.chart_frame = ctk.CTkFrame(body, width=340)
        self.chart_frame.pack(side="right", fill="both", padx=(6, 0))

    def _build_chart(self):
        self.fig = Figure(figsize=(3.4, 3.4), facecolor="#2b2b2b")
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    # ---------- User Actions ----------
    def add_expense(self):
        raw_date = self.date_e.get().strip()
        raw_amt = self.amt_e.get().strip()
        try:
            amount = float(raw_amt)
            if amount <= 0:
                raise ValueError
            date.fromisoformat(raw_date)
        except ValueError:
            messagebox.showerror("Invalid input", "Use a positive amount and date formatted as YYYY-MM-DD.")
            return

        self.db.add(raw_date, self.cat_m.get(), amount, self.note_e.get().strip())
        self.amt_e.delete(0, "end")
        self.note_e.delete(0, "end")
        self.refresh()

    def delete_selected(self):
        sel = self.tree.selection()
        if not sel:
            return
        for item in sel:
            self.db.delete(int(self.tree.item(item)["tags"][0]))
        self.refresh()

    def export_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if not path:
            return
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["Date", "Category", "Amount", "Note"])
            w.writerows(r[1:] for r in self.db.all())
        messagebox.showinfo("Export Successful", f"Expenses exported to {path}")

    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        rows = self.db.all()
        for r in rows:
            self.tree.insert("", "end", values=(r[1], r[2], f"${r[3]:.2f}", r[4]), tags=(r[0],))
        self.total_lbl.configure(text=f"Total: ${self.db.total_amount():.2f}")

        self.ax.clear()
        self.ax.set_facecolor("#2b2b2b")
        self.ax.axis("off")
        data = self.db.totals_by_category()
        if data:
            labels, vals = zip(*data)
            self.ax.pie(
                vals,
                labels=labels,
                autopct="%1.0f%%",
                textprops={"color": "white", "fontsize": 9},
            )
        else:
            self.ax.text(0.5, 0.5, "No data yet", ha="center", va="center", color="white")
        self.canvas.draw()


if __name__ == "__main__":
    App().mainloop()
