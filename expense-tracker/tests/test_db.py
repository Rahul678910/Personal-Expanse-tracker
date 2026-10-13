"""Unit tests for the Expense Tracker Database Layer (DB)."""
import os
import tempfile
import pytest

# Ensure expense_tracker can be imported from parent directory
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from expense_tracker import DB


@pytest.fixture
def db():
    """Fixture providing a fresh in-memory SQLite database instance."""
    database = DB(":memory:")
    yield database
    database.close()


@pytest.fixture
def file_db():
    """Fixture providing a temporary file-based SQLite database."""
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    database = DB(path)
    yield database
    database.close()
    if os.path.exists(path):
        os.remove(path)


class TestDatabaseLayer:
    """Test suite for the DB class."""

    def test_initialization(self, db):
        """Test that the database initializes with an empty expenses table."""
        rows = db.all()
        assert rows == []
        assert db.total_amount() == 0.0
        assert db.totals_by_category() == []

    def test_add_expense(self, db):
        """Test adding a single expense record."""
        row_id = db.add("2026-10-13", "Food", 15.50, "Lunch with friends")
        assert row_id == 1

        rows = db.all()
        assert len(rows) == 1
        assert rows[0] == (1, "2026-10-13", "Food", 15.50, "Lunch with friends")

    def test_get_by_id(self, db):
        """Test retrieving a specific expense by row ID."""
        row_id = db.add("2026-10-12", "Transport", 24.00, "Train ticket")
        row = db.get_by_id(row_id)
        assert row is not None
        assert row == (1, "2026-10-12", "Transport", 24.00, "Train ticket")

        # Non-existent ID returns None
        assert db.get_by_id(999) is None

    def test_delete_expense(self, db):
        """Test deleting an expense by ID."""
        id1 = db.add("2026-10-10", "Study", 50.00, "Books")
        id2 = db.add("2026-10-11", "Games", 30.00, "Steam Sale")

        assert len(db.all()) == 2
        db.delete(id1)

        remaining = db.all()
        assert len(remaining) == 1
        assert remaining[0][0] == id2

    def test_delete_nonexistent_expense_does_not_error(self, db):
        """Test that deleting a non-existent ID does not raise an exception."""
        db.delete(999)
        assert db.all() == []

    def test_ordering(self, db):
        """Test that all() orders by day DESC, id DESC."""
        db.add("2026-10-01", "Food", 10.0, "Oldest")
        db.add("2026-10-05", "Food", 20.0, "Newer 1")
        db.add("2026-10-05", "Bills", 50.0, "Newer 2")

        rows = db.all()
        assert len(rows) == 3
        # Both on 2026-10-05 should be first, sorted by id DESC
        assert rows[0][1] == "2026-10-05" and rows[0][0] == 3
        assert rows[1][1] == "2026-10-05" and rows[1][0] == 2
        assert rows[2][1] == "2026-10-01" and rows[2][0] == 1

    def test_totals_by_category(self, db):
        """Test grouping and summation across multiple categories."""
        db.add("2026-10-10", "Food", 25.0, "Breakfast")
        db.add("2026-10-11", "Food", 35.0, "Dinner")
        db.add("2026-10-12", "Transport", 40.0, "Bus Pass")
        db.add("2026-10-13", "Bills", 100.0, "Electricity")

        totals = db.totals_by_category()
        # Grouped totals should reflect SUM(amount)
        totals_dict = dict(totals)
        assert totals_dict["Bills"] == 100.0
        assert totals_dict["Food"] == 60.0
        assert totals_dict["Transport"] == 40.0

    def test_total_amount(self, db):
        """Test calculation of grand total spending."""
        assert db.total_amount() == 0.0

        db.add("2026-10-10", "Food", 12.50, "")
        db.add("2026-10-11", "Transport", 7.50, "")
        db.add("2026-10-12", "Games", 20.00, "")

        assert db.total_amount() == 40.00

    def test_optional_note_and_special_characters(self, db):
        """Test notes with empty strings, emojis, and special punctuation."""
        db.add("2026-10-13", "Food", 18.25, "")
        db.add("2026-10-13", "Study", 99.99, "Math & Science course (vol. 2) [discounted] - 50% off!")

        rows = db.all()
        assert rows[0][4] == "Math & Science course (vol. 2) [discounted] - 50% off!"
        assert rows[1][4] == ""

    def test_file_persistence(self, file_db):
        """Test that data written to a file-based DB persists after closing and reopening."""
        path = file_db.path
        file_db.add("2026-10-13", "Bills", 150.00, "Internet")
        file_db.close()

        # Reopen
        reopened = DB(path)
        rows = reopened.all()
        assert len(rows) == 1
        assert rows[0][2] == "Bills"
        assert rows[0][3] == 150.00
        reopened.close()
