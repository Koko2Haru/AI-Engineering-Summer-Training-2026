import sqlite3
from contextlib import closing
from pathlib import Path

DB_PATH = Path(__file__).parent / "coinquest.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create the expenses table once, if it doesn't exist yet."""
    with closing(get_connection()) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                note TEXT,
                spent_on DATE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()


def insert_expense(amount: float, category: str, note: str, spent_on: str) -> dict:
    """Insert one expense and return the saved row as a dict."""
    with closing(get_connection()) as conn:
        row = conn.execute(
            "INSERT INTO expenses (amount, category, note, spent_on) "
            "VALUES (?, ?, ?, ?) RETURNING *",
            (amount, category, note, spent_on),
        ).fetchone()
        conn.commit()
        return dict(row)


def get_expenses() -> list[dict]:
    """Return all expenses, newest first."""
    with closing(get_connection()) as conn:
        rows = conn.execute(
            "SELECT * FROM expenses ORDER BY spent_on DESC, id DESC"
        ).fetchall()
        return [dict(row) for row in rows]
