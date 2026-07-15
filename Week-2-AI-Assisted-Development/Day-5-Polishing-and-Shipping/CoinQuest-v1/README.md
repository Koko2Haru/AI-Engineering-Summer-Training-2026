# CoinQuest v1.0 🎮

A gamified expense tracker: log spending in SAR and watch a monthly budget HP
bar drain, build a daily streak, earn XP, and get a local AI coach's verdict —
plus a boss fight where your biggest spending category is the monster.

Full stack: FastAPI + SQLite + vanilla HTML/CSS/JS + Chart.js (CDN) + Ollama
(local LLM). No frameworks, no npm, no build step — one Python process serves
both the API and the static frontend.

## Features

- **Expense CRUD** — log an expense (amount, category, note, date) and see it
  appear instantly in the list, newest first.
- **Budget HP bar** — the monthly budget is a health bar. It drains as you
  spend, changes color at 50%/20% remaining (green → yellow → red), and shows
  a "Defeated" state once you go over budget. Editable from the UI.
- **Monthly summary + chart** — a Chart.js doughnut of this month's spending
  by category, plus a totals table (spent / budget / remaining).
- **XP + streak** — `⭐ XP` for every expense ever logged, `🔥 Streak` for
  consecutive days with at least one logged expense.
- **AI Coach & Boss Fight** — summon a local Ollama model in one of three
  personality modes (**Coach**, **Roast**, **Pirate**) for a short review, a
  saving tip, and a boss report on your biggest spending category — the
  monster's name and weakness are written by the model, but the damage number
  is always the real, Python-computed total. The model never does arithmetic
  and can never create, edit, or delete records.

## Run it

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Then open **http://127.0.0.1:8000**.

The SQLite database (`coinquest.db`) is created automatically on first run.

## Ollama (for the AI Coach)

The AI Coach panel needs a local [Ollama](https://ollama.com) install with at
least one model pulled:

```bash
ollama pull llama3.2
```

The model used is set in one constant, `OLLAMA_MODEL`, at the top of
`main.py` — swap it for any model you have installed (check with
`ollama list`).

If Ollama isn't running, everything else in the app still works — the coach
panel just shows a friendly error instead of a result.

## Screenshots

_Add screenshots here: v0.1 add-expense flow, v0.2 hardened UI, v0.3 bug
fixes, and v1.0's HP bar / chart / AI coach + boss fight._
