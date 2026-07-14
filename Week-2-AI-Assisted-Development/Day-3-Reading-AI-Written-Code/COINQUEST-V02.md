# 📖 CoinQuest — Day 3 Report: Reading AI-Written Code



## 🗓️ What we did today

Day 3's task: read every line of the AI-written v0.1 code, find **5+ improvements**
covering **readability, efficiency, and correctness**, and apply them.

**The workflow:**

1. 📋 **Snapshot first** — copied the whole Day-2 folder into
   `Day-3-Reading-AI-Written-Code/CoinQuest-v02/`, leaving
   `Day-2-.../CoinQuest-Skeleton/` untouched as the "before" version.
   This is what makes the comparison below possible.
2. 🔍 **Line-by-line review** (with Claude in chat) — went through `main.py`,
   `database.py`, and `static/index.html` and found **10 improvements**, each
   tagged with what it improves (readability / efficiency / correctness — plus
   two bonus finds: a security hole and a deprecated API).
3. 📝 **Wrote the plan as a file** — all 10 changes went into `IMPROVEMENTS.md`
   with before/after code, so the plan itself is reviewable and lives in the repo.
4. 🤖 **Claude Code applied it** — pointed the Claude Code VS Code extension at
   `IMPROVEMENTS.md` and had it apply the changes **one file at a time**, reviewing
   each diff before moving on.
5. ✅ **Verified** — ran the app, added expenses, and tested the exact attack /
   failure scenarios below against both versions.

**The 10 improvements:**

| # | Change | Improves |
|---|--------|----------|
| 1 | Escape rendered data (no `innerHTML` injection) | 🔒 Security, Correctness |
| 2 | Check the POST response before resetting the form | ✅ Correctness |
| 3 | Validate input at the API (Pydantic `Field(gt=0)`, `Category` enum, real `date`) | ✅ Correctness, 🔒 Security |
| 4 | Replace deprecated `@app.on_event("startup")` with `lifespan` | 🧹 Deprecation, Correctness |
| 5 | Local-time default date instead of UTC | ✅ Correctness |
| 6 | `contextlib.closing` on every DB connection | ✅ Correctness / robustness |
| 7 | `INSERT ... RETURNING` — one query instead of two | ⚡ Efficiency |
| 8 | Batch list rendering with `DocumentFragment` | ⚡ Efficiency |
| 9 | Cache DOM lookups + named `todayLocal()` helper | 📖 Readability, ⚡ Efficiency |
| 10 | Docstrings + `Category` enum documenting intent | 📖 Readability |

---

## ⚔️ Old vs New: same action, different outcome

> The important part. Each scenario is something you can actually try in both
> folders. **Skeleton** = Day-2 original, **v02** = Day-3 improved.

### 🧨 Scenario 1 — Log an expense with the note `<img src=x onerror=alert('hacked')>`

- **Skeleton:** the note is injected into the page via `innerHTML`… and the
  JavaScript inside it **executes**. An alert pops. In a real app that's a stored
  XSS — any script in a note runs in the browser of *everyone* who views the list. 💀
- **v02:** the note shows up as boring literal text:
  `<img src=x onerror=alert('hacked')>`. Nothing runs. 😌
- **Thanks to:** improvement **#1** (render with `textContent`, never `innerHTML`).

### 💸 Scenario 2 — Send an expense of `-500` SAR straight to the API

```bash
curl -X POST localhost:8000/api/expenses -H "Content-Type: application/json" \
  -d '{"amount": -500, "category": "Food", "note": "", "date": "2026-07-14"}'
```

- **Skeleton:** `200 OK` — negative spending saved to the database. Congrats, you
  just *earned* money by eating. 🤡 (The form's `min="0"` never protected the API —
  curl goes around it.)
- **v02:** `422 Unprocessable Entity` — Pydantic's `Field(gt=0)` rejects it with a
  clear error message. Nothing touches the DB. 🛡️
- **Thanks to:** improvement **#3** (validation at the API, the real boundary).

### 🗑️ Scenario 3 — Send `category: "Blah"` and `date: "not-a-date"`

- **Skeleton:** `200 OK` — both saved as-is. The DB slowly fills with garbage
  categories and unparseable dates that would crash future features (charts,
  monthly boss reports…). 📉
- **v02:** `422` — category must be one of the five known values (`Category` enum),
  and date must be a real `YYYY-MM-DD`. The DB stays clean for the features coming
  on Day 4–5. ✨
- **Thanks to:** improvement **#3** again.

### 🤥 Scenario 4 — The save fails (e.g. the 422 from Scenario 2, via the form)

- **Skeleton:** the form **resets and looks successful anyway** — it never checked
  the response. You think the expense was logged; it wasn't. Silent data loss. 🕳️
- **v02:** an alert says the save failed, and the form **keeps what you typed** so
  you can fix and resubmit. ✅
- **Thanks to:** improvement **#2** (check `res.ok` before resetting).

### 🌙 Scenario 5 — Log an expense at 1:30 AM in Jeddah

- **Skeleton:** the default date is built with `toISOString()`, which is **UTC**.
  At 1:30 AM local (UTC+3) it's still *yesterday* in UTC — so the expense is
  silently filed under the wrong day. Streaks and daily totals would lie. 📆❌
- **v02:** `todayLocal()` builds the date from local time — 1:30 AM on the 14th is
  logged as the 14th. 📆✅
- **Thanks to:** improvement **#5**.

### 🐢 Scenario 6 — Add one expense (what the server does)

- **Skeleton:** **two** DB queries — an `INSERT`, then a separate `SELECT` to read
  the row back.
- **v02:** **one** query — `INSERT ... RETURNING *` saves and returns the row in a
  single round-trip. Half the DB work per add. ⚡
- **Thanks to:** improvement **#7**.

### 🖼️ Scenario 7 — Render a list of 500 expenses

- **Skeleton:** 500 separate `appendChild` calls into the live page — the browser
  can reflow after each one.
- **v02:** all 500 rows are built in an off-page `DocumentFragment` and inserted
  with **one** `replaceChildren` call — one layout pass total. ⚡
- **Thanks to:** improvement **#8** (and #9's cached DOM lookups mean the submit
  handler doesn't re-query the DOM every time either).

### 💥 Scenario 8 — A DB query throws halfway through

- **Skeleton:** the function exits before reaching `conn.close()` — the connection
  **leaks**. Do this enough times and the file can stay locked. 🔓
- **v02:** `with closing(get_connection()) as conn:` guarantees the connection
  closes **even on error**. 🧯
- **Thanks to:** improvement **#6**.

### ⚠️ Scenario 9 — Just start the app and read the logs

- **Skeleton:** FastAPI prints a `DeprecationWarning` — `@app.on_event("startup")`
  is on its way out and will break on a future upgrade. ⏳
- **v02:** clean startup with the modern `lifespan` handler. Future-proof. 🧹
- **Thanks to:** improvement **#4**.

### 👓 Scenario 10 — A beginner opens the code for the first time

- **Skeleton:** works, but you have to *infer* things: what categories are allowed?
  what does this function return? why `slice(0, 10)` on a date string?
- **v02:** the `Category` enum lists the allowed values in one place, every DB
  function has a one-line docstring, and the date logic has a name
  (`todayLocal`) and a comment explaining the UTC trap. The code explains itself. 📖
- **Thanks to:** improvements **#9** and **#10**.

---

## 🏁 Takeaway

The AI-written v0.1 *worked* — every scenario above starts from an app that runs
fine in a happy-path demo. The improvements only show up when you ask *"what if
someone does X?"* — malicious input, invalid data, a failed request, an error
mid-query, a late-night entry. That's exactly why Day 3 exists: **AI code must be
read, not just run.** 🔍🤝🤖

> The original untouched version lives at
> `../Day-2-Building-with-an-AI-Partner/CoinQuest-Skeleton/` — that's the
> "before" for every scenario below. 🔍

## 📁 Folder structure

```
Day-3-Reading-AI-Written-Code/
├── COINQUEST-V02.md            # 📖 This report — day narrative + old-vs-new scenarios
└── CoinQuest-v02/              # ⚔️ The improved copy (Day-2 code + all 10 fixes applied)
    ├── main.py                 # 🚀 FastAPI app — routes, Pydantic validation, lifespan startup
    ├── database.py             # 🗄️ SQLite layer — safe connections, single-query insert
    ├── IMPROVEMENTS.md         # 📋 The 10-change review plan Claude Code read and applied
    ├── coinquest.db            # 💾 Local SQLite data (gitignored — not in the repo)
    ├── static/
    │   └── index.html          # 🖥️ Frontend — form + list, XSS-safe rendering, local dates
    └── __pycache__/            # ⚙️ Python bytecode cache (auto-generated, gitignored)
```