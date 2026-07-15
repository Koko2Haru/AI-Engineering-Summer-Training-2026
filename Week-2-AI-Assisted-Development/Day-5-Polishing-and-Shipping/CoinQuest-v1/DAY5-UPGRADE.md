# CoinQuest — Day 5 Upgrade Brief: v0.2 → v1.0 (The Payload) 🏆

You are upgrading CoinQuest to its final v1.0 form as defined in the project spec.

## Context
- This folder (`CoinQuest-v03/`) starts as a copy of the Day-3 hardened build (v0.2):
  working expense CRUD across `main.py` (FastAPI), `database.py` (SQLite),
  `static/index.html` (vanilla JS).
- The source of truth is `SPECS.md` in `Week-2-AI-Assisted-Development/Day-1-*/`.
  Read it first — it has the full API surface, data model, and AI rules.
  This brief is the distilled build plan.
- Folder names follow day snapshots, but per the SPECS.md roadmap this build ships
  as **v1.0** — label it v1.0 in the app title and README.

## Hard rules — never break these
1. **Edit only inside `CoinQuest-v03/`.** Every other `Day-N-*` folder in this repo
   is a frozen historical snapshot. Do not touch anything outside this folder.
2. **Keep the stack exactly as-is:** FastAPI + SQLite + vanilla HTML/CSS/JS +
   Chart.js (CDN) + Ollama. No new frameworks, no npm, no build step.
3. **Do not regress the Day-3 hardening:** Pydantic validation at the API boundary,
   Category enum, `textContent` (never `innerHTML`) for user data, `lifespan`
   (not `on_event`), `INSERT...RETURNING`, `contextlib.closing`, local-time dates.
4. **AI rules from the spec:**
   - The model NEVER does arithmetic. Python computes every number; Ollama only
     turns pre-computed stats into words.
   - AI output is advisory display text only — it can never create, edit, or
     delete records.
   - If Ollama is unreachable, everything else still works and the coach panel
     shows a friendly error. Wrap the Ollama call in a timeout (~30s) + try/except.
5. **Derived, never stored:** streak, XP, and the boss are computed at read time
   from the `expenses` table. No new columns for them. One source of truth.
6. `*.db` stays gitignored.

## Build order — milestones with a cut line
Build in this exact order (if time runs out, we cut from the bottom).
**After EACH milestone: STOP, and tell me exactly what to test and screenshot
before you continue.**

### Milestone 0 — Sanity check
Run the app and confirm the baseline works (add an expense → it appears in the
list) before changing anything.

### Milestone 1 — Budget + summary API (backend foundation)
- Add `settings(key TEXT PRIMARY KEY, value TEXT)` table; store `monthly_budget`
  (default 1500).
- `GET /api/budget` and `PUT /api/budget` (validate: positive number).
- `GET /api/summary?month=YYYY-MM` (defaults to current month) returns:
  per-category totals, total spent, remaining budget, streak, XP.
  - **Streak** = consecutive days ending today with ≥1 logged expense.
  - **XP** = +10 per expense ever logged (all-time, derived from row count).

### Milestone 2 — Chart.js monthly summary 📊
- Summary section: Chart.js doughnut (or bar) of this month's spending by
  category + a small totals table (total spent / budget / remaining), in SAR.

### Milestone 3 — Budget HP bar 💚💛❤️
- HP bar at the top: max HP = monthly budget, current HP = remaining.
- Width + color from remaining %: green >50%, yellow 20–50%, red <20%
  (pure CSS classes). Shows "X / Y SAR" on the bar.
- Updates instantly after adding an expense.
- Small budget-edit UI wired to `PUT /api/budget`.

### Milestone 4 — XP counter + streak flame
- Header widgets: `⭐ XP: n` and `🔥 Streak: n days`, fed from `/api/summary`,
  refreshing after every added expense.

### Milestone 5 — AI Coach + Monthly Boss Fight + personality modes 🐉
- `POST /api/coach` with body `{month, mode}` →
  `{review, tip, boss: {name, damage, weakness}}`.
- Backend computes ALL stats first (per-category totals, biggest category + its
  total, budget, remaining, streak) and injects them into the prompt.
- The month's biggest spending category IS the boss: Ollama invents the monster
  name (e.g. "Delivery Demon"), damage = that category's total in SAR,
  weakness = one habit-level tip.
- Modes = three system-prompt strings only, same data different voice:
  **Coach** (supportive analyst) · **Roast** (savage but funny) · **Pirate**
  (talks like a pirate).
- Ask the model for strict JSON and parse defensively — bad JSON or timeout →
  friendly error state, never a crash.
- Model name: run `ollama list`, use an installed model, and put the name in ONE
  constant at the top of the file so I can swap it.
- Frontend: coach panel with a 3-button mode selector, a "Summon" button, a
  loading state, and a boss report card (name / damage dealt / weakness).

### Milestone 6 — Polish + ship prep ✨
- Game-flavored UI pass: title "CoinQuest v1.0", coherent colors, empty states
  ("No expenses yet — your HP bar is safe"), visible error messages.
- `README.md` in this folder: what it is, feature list, one-command run
  instructions, Ollama requirement note, placeholder section for screenshots.
- `requirements.txt` if missing.
- Final check: everything still works with Ollama stopped.

## Out of scope — do NOT build (stretch/future tier)
Natural-language expense entry (`/api/parse`), weekly quests, achievements /
titles / levels, PDF/CSV export, spending calendar, recurring expenses,
dark mode, accounts, deployment.

## Definition of done
1. One command starts the app; adding an expense makes the HP bar visibly drop.
2. Summary shows the chart, totals table, XP, and streak.
3. Summoning the coach in all 3 modes returns review + tip + boss report.
4. Kill Ollama → app still fully usable, coach panel fails gracefully.