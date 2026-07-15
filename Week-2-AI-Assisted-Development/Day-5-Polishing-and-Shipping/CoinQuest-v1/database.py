import sqlite3
from contextlib import closing
from datetime import date, datetime, timedelta
from pathlib import Path

DB_PATH = Path(__file__).parent / "coinquest.db"

DEFAULT_MONTHLY_BUDGET = "1500"

# --- Idle XP ------------------------------------------------------------
# XP isn't stored — it's derived from how long it's been since the newest
# expense. Every XP_INTERVAL_SECONDS with no new expense, that interval's
# award doubles (100, 200, 400, ... running total), and logging a new
# expense resets it to 0 automatically (the anchor is just "time since the
# newest row", so a new row always restarts the clock).
#
# Set to fast test values (+1 XP per 1 second) right now. For the real
# version — +100 XP after the first hour, doubling every hour after —
# change these two:
XP_BASE_AMOUNT = 100        # -> 100
XP_INTERVAL_SECONDS = 3600   # -> 3600


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create the expenses/settings tables once, if they don't exist yet."""
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

        expense_columns = {row["name"] for row in conn.execute("PRAGMA table_info(expenses)")}
        if "payment_method" not in expense_columns:
            conn.execute(
                "ALTER TABLE expenses ADD COLUMN payment_method TEXT NOT NULL DEFAULT 'Cash'"
            )

        conn.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)

        # One-time split of the old single "monthly_budget" setting into a cash
        # budget (keeps the value the user already had) plus a fresh credit budget.
        has_cash_budget = conn.execute(
            "SELECT 1 FROM settings WHERE key = 'cash_budget'"
        ).fetchone()
        if not has_cash_budget:
            old_budget = conn.execute(
                "SELECT value FROM settings WHERE key = 'monthly_budget'"
            ).fetchone()
            cash_default = old_budget["value"] if old_budget else DEFAULT_MONTHLY_BUDGET
            conn.execute(
                "INSERT OR IGNORE INTO settings (key, value) VALUES ('cash_budget', ?)",
                (cash_default,),
            )
        conn.execute(
            "INSERT OR IGNORE INTO settings (key, value) VALUES ('credit_budget', '0')"
        )
        conn.commit()


def insert_expense(
    amount: float, category: str, note: str, spent_on: str, payment_method: str
) -> dict:
    """Insert one expense and return the saved row as a dict."""
    with closing(get_connection()) as conn:
        row = conn.execute(
            "INSERT INTO expenses (amount, category, note, spent_on, payment_method) "
            "VALUES (?, ?, ?, ?, ?) RETURNING *",
            (amount, category, note, spent_on, payment_method),
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


def delete_expense(expense_id: int) -> bool:
    """Delete one expense by id. Returns True if a row was deleted."""
    with closing(get_connection()) as conn:
        cursor = conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        conn.commit()
        return cursor.rowcount > 0


def delete_expenses(expense_ids: list[int]) -> int:
    """Delete many expenses by id in one transaction. Returns the number deleted."""
    if not expense_ids:
        return 0
    with closing(get_connection()) as conn:
        placeholders = ",".join("?" for _ in expense_ids)
        cursor = conn.execute(
            f"DELETE FROM expenses WHERE id IN ({placeholders})", expense_ids
        )
        conn.commit()
        return cursor.rowcount


def get_budgets() -> dict:
    with closing(get_connection()) as conn:
        rows = conn.execute(
            "SELECT key, value FROM settings WHERE key IN ('cash_budget', 'credit_budget')"
        ).fetchall()
        values = {row["key"]: float(row["value"]) for row in rows}
        cash_budget = values.get("cash_budget", 0.0)
        credit_budget = values.get("credit_budget", 0.0)
        return {
            "cash_budget": cash_budget,
            "credit_budget": credit_budget,
            "total_budget": cash_budget + credit_budget,
        }


def set_budgets(cash_budget: float, credit_budget: float) -> dict:
    with closing(get_connection()) as conn:
        conn.execute(
            "INSERT INTO settings (key, value) VALUES ('cash_budget', ?) "
            "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
            (str(cash_budget),),
        )
        conn.execute(
            "INSERT INTO settings (key, value) VALUES ('credit_budget', ?) "
            "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
            (str(credit_budget),),
        )
        conn.commit()
        return {
            "cash_budget": cash_budget,
            "credit_budget": credit_budget,
            "total_budget": cash_budget + credit_budget,
        }


def get_idle_xp() -> int:
    """XP earned from idle time since the most recent expense, doubling each interval."""
    with closing(get_connection()) as conn:
        row = conn.execute(
            "SELECT created_at FROM expenses ORDER BY created_at DESC, id DESC LIMIT 1"
        ).fetchone()
        if row is None:
            return 0

        last_created = datetime.strptime(row["created_at"], "%Y-%m-%d %H:%M:%S")
        elapsed_seconds = (datetime.utcnow() - last_created).total_seconds()
        intervals = int(elapsed_seconds // XP_INTERVAL_SECONDS)
        if intervals <= 0:
            return 0
        return XP_BASE_AMOUNT * (2**intervals - 1)


def _compute_streak(conn: sqlite3.Connection) -> int:
    """Consecutive days ending today with >=1 logged expense."""
    rows = conn.execute("SELECT DISTINCT spent_on FROM expenses").fetchall()
    logged_days = {row["spent_on"] for row in rows}

    streak = 0
    day = date.today()
    while day.isoformat() in logged_days:
        streak += 1
        day -= timedelta(days=1)
    return streak


def get_summary(month: str) -> dict:
    """Per-category totals (overall and per payment method), cash/credit/total
    spent+budget+remaining, streak, XP for `month`."""
    with closing(get_connection()) as conn:
        rows = conn.execute(
            "SELECT category, payment_method, SUM(amount) AS total FROM expenses "
            "WHERE spent_on LIKE ? GROUP BY category, payment_method",
            (f"{month}-%",),
        ).fetchall()

        category_totals: dict[str, float] = {}
        cash_category_totals: dict[str, float] = {}
        credit_category_totals: dict[str, float] = {}
        for row in rows:
            category_totals[row["category"]] = (
                category_totals.get(row["category"], 0.0) + row["total"]
            )
            bucket = (
                cash_category_totals
                if row["payment_method"] == "Cash"
                else credit_category_totals
            )
            bucket[row["category"]] = row["total"]

        total_spent = sum(category_totals.values())
        cash_spent = sum(cash_category_totals.values())
        credit_spent = sum(credit_category_totals.values())

        budgets = get_budgets()
        cash_budget = budgets["cash_budget"]
        credit_budget = budgets["credit_budget"]
        budget = budgets["total_budget"]

        return {
            "month": month,
            "category_totals": category_totals,
            "cash_category_totals": cash_category_totals,
            "credit_category_totals": credit_category_totals,
            "total_spent": total_spent,
            "cash_spent": cash_spent,
            "credit_spent": credit_spent,
            "budget": budget,
            "cash_budget": cash_budget,
            "credit_budget": credit_budget,
            "remaining": budget - total_spent,
            "cash_remaining": cash_budget - cash_spent,
            "credit_remaining": credit_budget - credit_spent,
            "streak": _compute_streak(conn),
            "xp": get_idle_xp(),
        }
