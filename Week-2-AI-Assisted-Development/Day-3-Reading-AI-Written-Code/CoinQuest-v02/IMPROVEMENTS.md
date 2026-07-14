# CoinQuest v0.2 — Day 3 Review & Improvement Plan

> **File:** `IMPROVEMENTS.md`
> **Goes in:** `Week-2-AI-Assisted-Development/Day-3-Reading-AI-Written-Code/CoinQuest-v02/`
> **Read this fully before changing anything.**

---

## Context for Claude Code

This is **Week 2, Day 3 — Reading AI-Written Code.** The task is to review the
v0.1 code line by line and apply improvements to **readability, efficiency, and
correctness** (plus the security and deprecation fixes noted below).

**We copied the entire Day-2 folder into Day-3 so we can improve the copy and
leave the original untouched.**

- **Original (do NOT edit):** `Day-2-Building-with-an-AI-Partner/CoinQuest-Skeleton/`
- **Working copy (edit THIS one):** `Day-3-Reading-AI-Written-Code/CoinQuest-v02/`

Apply every change below **only** to the files in the `CoinQuest-v02` folder.

**Ground rules (same as Day 2):**
- One file at a time. Show the diff, wait, then move on.
- No new features — no HP bar, XP, charts, or AI. These are review fixes only.
- Keep it simple and beginner-readable — a beginner reads every line afterward.

---

## What each improvement targets

| # | Change | File | Improves |
|---|--------|------|----------|
| 1 | Escape rendered data (no `innerHTML` injection) | `static/index.html` | **Security**, Correctness |
| 2 | Check the POST response before resetting the form | `static/index.html` | **Correctness** |
| 3 | Validate input at the API (Pydantic) | `main.py` | **Correctness**, Security |
| 4 | Replace deprecated `@app.on_event` with `lifespan` | `main.py` | **Deprecation fix**, Correctness |
| 5 | Fix the UTC default-date bug | `static/index.html` | **Correctness** |
| 6 | Always close DB connections (`closing`) | `database.py` | **Correctness / robustness** |
| 7 | Insert + return row in a single query (`RETURNING`) | `database.py` | **Efficiency** |
| 8 | Batch the list render (`DocumentFragment`) | `static/index.html` | **Efficiency** |
| 9 | Cache DOM lookups + name the date helper | `static/index.html` | **Readability**, minor Efficiency |
| 10 | Docstrings + `Category` enum for clear intent | `database.py`, `main.py` | **Readability** |

Coverage check for today's rubric: **Readability** → 9, 10, plus the enum in 3.
**Efficiency** → 7, 8, 9. **Correctness** → 2, 3, 4, 5, 6, plus 1.

---

## `main.py`

### 3 + 4 + 10 — validation, modern startup, clearer types

Replace the top of the file (imports through the `startup` hook) and the
`ExpenseIn` model with the version below.

**Why:**
- `@app.on_event("startup")` is **deprecated** in current FastAPI/Starlette — it
  emits a warning and will eventually break. `lifespan` is the supported way. *(deprecation, correctness)*
- The old model accepted **any** number, **any** string category, and **any**
  string date — so a crafted request could put junk straight into the DB. The
  `<select>` and `min="0"` in the form are client-side only; the API is the real
  gate. *(correctness, security)*
- The `Category` enum documents the allowed values in one place. *(readability)*

```python
from contextlib import asynccontextmanager
from datetime import date
from enum import Enum

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

import database


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs once on startup: make sure the table exists.
    database.init_db()
    yield


app = FastAPI(lifespan=lifespan)


class Category(str, Enum):
    food = "Food"
    transport = "Transport"
    shopping = "Shopping"
    bills = "Bills"
    other = "Other"


class ExpenseIn(BaseModel):
    amount: float = Field(gt=0)   # no zero or negative spending
    category: Category            # must be one of the known categories
    note: str = ""
    date: date                    # must be a real YYYY-MM-DD date
```

### 3 (cont.) — store clean primitive values

Update `create_expense` so it hands the DB plain values, not an enum object or a
`date` object. This avoids `"Category.food"` ending up in the table and sidesteps
the deprecated sqlite date adapters.

```python
@app.post("/api/expenses")
def create_expense(expense: ExpenseIn):
    return database.insert_expense(
        amount=expense.amount,
        category=expense.category.value,    # store the plain "Food" string
        note=expense.note,
        spent_on=expense.date.isoformat(),  # store as "YYYY-MM-DD" text
    )
```

Leave `list_expenses` and the `StaticFiles` mount as they are.

---

## `database.py`

### 6 + 7 + 10 — safe connections, single-query insert, docstrings

Replace the whole file with the version below.

**Why:**
- `closing(...)` guarantees the connection closes **even if a query throws** — the
  old code leaked the connection on any error between `connect` and `close`. *(correctness/robustness)*
- `INSERT ... RETURNING *` gets the saved row back in **one** query instead of an
  `INSERT` followed by a separate `SELECT` — half the DB round-trips per add. *(efficiency)*
- Short docstrings say what each function does at a glance. *(readability)*

```python
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
```

> **Note on `RETURNING`:** it needs SQLite ≥ 3.35 (2021), which ships with any
> recent Python. If `python -c "import sqlite3; print(sqlite3.sqlite_version)"`
> shows something older, keep the old INSERT-then-SELECT body but still wrap it in
> `with closing(get_connection()) as conn:`.

---

## `static/index.html`

### 1 + 2 + 5 + 8 + 9 — the whole `<script>` block

Replace the entire `<script>...</script>` with the version below. The HTML/CSS
above it stays the same.

**Why:**
- **1 (security):** the old code put `e.note` / `e.category` straight into
  `innerHTML`, so a note like `<img src=x onerror=alert(1)>` would execute.
  Building each cell with `textContent` renders it as plain text — no injection.
- **2 (correctness):** the old code never checked `res.ok`, so a rejected save
  (e.g. a 422 from the new validation) still reset the form and looked successful.
  Now it warns and stops if the save failed.
- **5 (correctness):** `toISOString()` returns the **UTC** date. In Jeddah (UTC+3),
  an expense logged between midnight and 3 AM defaulted to *yesterday*. `todayLocal()`
  builds the date from local time.
- **8 (efficiency):** rows are built in a `DocumentFragment` and inserted once with
  `replaceChildren`, instead of appending one `<li>` at a time (one reflow, not N).
- **9 (readability):** inputs are looked up once at the top instead of re-querying
  the DOM on every submit, and the date logic lives in a named helper.

```html
<script>
  const form = document.getElementById("expense-form");
  const list = document.getElementById("expense-list");
  const amountInput = document.getElementById("amount");
  const categoryInput = document.getElementById("category");
  const noteInput = document.getElementById("note");
  const dateInput = document.getElementById("date");

  // Local YYYY-MM-DD. NOT toISOString(), which is UTC and can roll to yesterday.
  function todayLocal() {
    const d = new Date();
    const mm = String(d.getMonth() + 1).padStart(2, "0");
    const dd = String(d.getDate()).padStart(2, "0");
    return `${d.getFullYear()}-${mm}-${dd}`;
  }

  dateInput.value = todayLocal();

  async function loadExpenses() {
    const res = await fetch("/api/expenses");
    const expenses = await res.json();

    const fragment = document.createDocumentFragment();
    for (const e of expenses) {
      const li = document.createElement("li");

      // textContent (not innerHTML) so user notes can't inject HTML.
      const left = document.createElement("span");
      left.textContent =
        `${e.spent_on} — ${e.category}` + (e.note ? ` (${e.note})` : "");

      const right = document.createElement("span");
      right.className = "amount";
      right.textContent = `${e.amount.toFixed(2)} SAR`;

      li.append(left, right);
      fragment.append(li);
    }

    list.replaceChildren(fragment);  // one DOM update instead of N
  }

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const res = await fetch("/api/expenses", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        amount: parseFloat(amountInput.value),
        category: categoryInput.value,
        note: noteInput.value,
        date: dateInput.value,
      }),
    });

    if (!res.ok) {
      alert("Couldn't save that expense — please check your input and try again.");
      return;  // don't reset the form if it wasn't saved
    }

    form.reset();
    dateInput.value = todayLocal();
    loadExpenses();
  });

  loadExpenses();
</script>
```

---

## After applying

1. Run `uvicorn main:app --reload` from inside `CoinQuest-v02/` and add an expense
   to confirm it still saves and lists.
2. Quick correctness check: try amount `0` and a note like `<b>hi</b>` — the `0`
   should be rejected by the API, and the note should show as literal text.
3. Leave the Day-2 `CoinQuest-Skeleton/` folder untouched as the "before" snapshot.