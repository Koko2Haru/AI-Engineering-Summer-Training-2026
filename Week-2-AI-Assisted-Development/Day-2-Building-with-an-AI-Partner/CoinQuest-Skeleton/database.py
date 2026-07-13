import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "coinquest.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
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
    conn.close()


def insert_expense(amount: float, category: str, note: str, spent_on: str) -> dict:
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO expenses (amount, category, note, spent_on) VALUES (?, ?, ?, ?)",
        (amount, category, note, spent_on),
    )
    conn.commit()
    new_id = cursor.lastrowid
    row = conn.execute("SELECT * FROM expenses WHERE id = ?", (new_id,)).fetchone()
    conn.close()
    return dict(row)


def get_expenses() -> list[dict]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM expenses ORDER BY spent_on DESC, id DESC"
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]
