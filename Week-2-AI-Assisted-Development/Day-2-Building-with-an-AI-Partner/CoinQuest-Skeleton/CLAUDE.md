# CoinQuest v0.1 — project context for Claude Code

Full specification: ../../Day-1-Vibe-Coding-Start/SPECS.md — read it before doing anything.
All work happens INSIDE this folder (CoinQuest-Skeleton). Do not create or edit files outside it.

## What we're building TODAY (Day 2): v0.1 only
- POST /api/expenses — save {amount, category, note, date} to SQLite
- GET /api/expenses — list, newest first
- One plain index.html: a form + the list, wired with fetch()
- Nothing else. No HP bar, no XP, no AI, no charts, no auth — those
  come on later days BY DESIGN. Do not build ahead.

## Stack (fixed — don't substitute)
- FastAPI + uvicorn, Python 3 (the venv already exists at the repo root)
- sqlite3 from the standard library (db file: coinquest.db — gitignored)
- Frontend: one index.html, vanilla JS, no frameworks, no build step

## Rules
- Propose a plan before writing code; build in small steps, one file at a time
- Keep code simple and readable — a beginner reviews every line of it tomorrow
- Basic input handling only; deliberate hardening happens on Day 3