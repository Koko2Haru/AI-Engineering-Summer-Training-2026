📘 # CoinQuest — Detailed Specification & Ideation Log

> Companion to the submitted one-page spec (PDF). This document carries the full detail — and the story of how the idea was found, because this week is about the AI-assisted workflow, not just the code.
>
> **Author:** Ali · **Program:** AI Engineering Summer Training 2026 · **Week 2 — AI-assisted development, Day 1** · **Instructor:** Eng. Mohammed Mashat · **Date:** 12 Jul 2026

---

## 🧠 1. Ideation log — how CoinQuest happened --> [View in Site for TL;DR](https://koko2haru.github.io/AI-Engineering-Summer-Training-2026/Week-2%20AI-Assisted%20Development/Day-1%20Vibe-Coding%20Start/coinQuest.html)

### 🔍 1.1 Research phase

I spent about three hours before writing a single line of this spec: brainstorming on my own, searching the web, and watching YouTube videos about beginner-to-intermediate project ideas. The goal wasn't to find *a* project — it was to find the project that would extract the most learning from this specific week: build with AI (Day 2), review AI-written code (Day 3), plant and debug bugs with AI (Day 4), and ship to GitHub with a reflection (Day 5).

That research produced a longlist of 19 candidate ideas.

### 💡 1.2 The longlist and what happened to each idea

| Idea | Verdict |
|---|---|
| Portfolio site | The display case, not the exhibit — doing it later, not this week |
| Build your own Git | Great project, but the AI would generate code above my reading level — Day 3 review would collapse |
| To-do list | Too thin: not enough real logic to find five honest review improvements in |
| Smart mirror | Needs hardware I don't have this week |
| **Finance tracker** | **Chosen — real logic in every layer, visible bugs, full-stack** |
| Calculator | Only interesting with a real expression parser; weak story either way |
| Neural network from scratch | On-theme, but bugs don't crash — accuracy just silently drops; debugging week nightmare |
| Real-time chat | Strong runner-up; websocket risk could eat Day 2 |
| Build your own Redis | The ambitious pick — parked for a future week |
| Random quote generator | Half-day project |
| Algorithm visualizer | Best bug *visibility* of the list, but essentially frontend-only |
| Travel booking system | Scope-creep magnet |
| Quiz program | Too thin, same as the to-do list |
| Build your own BitTorrent | Far beyond one-week scope at my level |
| HTTP server from scratch | Serious candidate until I realized I wanted full-stack, not backend internals |
| Real-time collaborative editor | Deceptively hard (sync/conflict resolution) |
| Chatbot | The interesting logic lives inside the model, not in code I can review |
| Video game | Fun, but I wanted the web-app architecture I'll reuse everywhere |
| QR code generator | Trivial with a library, brutal from scratch |

### 🤖 1.3 What the AI conversations changed

I took the longlist to AI assistants (Claude and ChatGPT) and asked for rankings against four criteria: difficulty, learning value, resume value, and one-week finishability. Two insights came out of those conversations that reshaped the decision:

**The project is a vehicle, not a destination.** Days 3 and 4 quietly set the real requirements — I have to find five genuine improvements in AI-generated code, and my three planted bugs need visible symptoms. So the project needs (a) enough real logic to critique, (b) behavior I can watch break, and (c) code I can actually read. That last requirement eliminated the most impressive-sounding ideas: an AI will happily generate a BitTorrent client I can't review, and then the week becomes copy-paste — the exact failure mode this training warns against.

**I wanted the full-stack architecture.** Frontend, backend, database, and the integration between them — because that's the skeleton I'll reuse in every project after this one. That requirement retired the raw HTTP server (backend internals only) and pointed at a framework-based app. A key concept from this discussion: Day 2 builds a *vertical slice* — one thin working path through every layer — not one layer per day. You build a skateboard, then a bike, then a car; every version rolls.

### 🎮 1.4 Differentiation: gamification × AI

A finance tracker on its own is a common student project. The differentiation came from fusing two things that rarely appear together: game mechanics (HP bar, streaks, XP, boss fights) and a **local** LLM (Ollama, building directly on Week 1's work). The design principle that governs the AI's role: **code does math, AI does language.** Python computes every number; the model only interprets and narrates them.

### ⚖️ 1.5 The multi-AI round — and the first "trust vs. verify" moment

I asked ChatGPT to expand the feature set, and it produced an excellent brainstorm: the Monthly Boss Fight (my favorite — the top spending category becomes the month's boss: *"Restaurant Monster dealt 720 SAR — weakness: impulse ordering"*), XP and levels, achievements, personality modes, analytics, and export options.

It also produced a broken schedule. Its recommended version roadmap assigned charts and UI work to v0.2 (Day 3) and the entire gamification layer to v0.3 (Day 4) — but Day 3 is *code review* day and Day 4 is *bug hunting* day in the actual course plan. The output looked polished and would have quietly destroyed the week. I caught it by cross-checking the roadmap against the instructor's table with a second assistant. Before writing any code, I'd already experienced the week's core lesson: **AI output must be verified against real constraints, no matter how confident it looks.** This is going in the Day 5 reflection.

From ChatGPT's list I adopted the boss fight, XP, the color-shifting HP bar, and personality modes (each mode is just one system prompt — nearly free). I demoted natural-language entry to stretch and parked the heavy items (PDF report, calendar, recurring expenses) in the future list below.

### ✨ 1.6 Naming

The working name was *Riyal Quest* — a pun on the Saudi riyal — but it felt too internal. After a shortlist (MoneyQuest, BudgetBoss, WalletWarrior), I landed on **CoinQuest**: remove the "i" and it reads **CONQUEST**. A name that's also the mission.

### 📚 1.7 What Day 1 taught me

Today's activity was "spec-then-generate vs. iterative refinement" — and the spec itself was produced by iterative refinement: brainstorm → rank → constrain → expand → verify → cut → name. Using multiple AI assistants wasn't about getting more ideas; it was about getting *different failure modes* and letting them check each other. My job in the loop was judgment: choosing, cutting, and verifying against the real constraints.

---

## ❓ 2. Problem statement

Expense trackers have a retention problem. Logging what you spend is a chore with no feedback loop, so most people abandon tracking within the first week — and students managing a monthly allowance rarely find out where the money actually went. Mainstream apps respond with bloat: accounts, bank sync, subscriptions, cloud dashboards.

CoinQuest attacks the retention problem directly by making the act of logging rewarding. The monthly budget is a health bar that visibly drains with every expense. Logging daily builds a streak and earns XP. At month's end, a local AI coach reads the (pre-computed) statistics and delivers a verdict — supportive, savage, or piratical, depending on the selected mode — including the month's **boss report**. Tracking money should feel like maintaining a save file, not filing taxes.

## 👤 3. Target user & scenario

A single user (initially: me) running the app locally on their own machine — a student tracking a monthly allowance in SAR. Entries are typed in manually within seconds of spending. All data stays on the device.

## 🚀 4. Features in detail

### 🌱 4.1 Common tier — the core slice (Day 2, v0.1)

| Feature | Behavior | Acceptance check |
|---|---|---|
| Log an expense | Form with amount, category (select), note, date → `POST /api/expenses` → row in SQLite | Submitting the form persists the row; it survives a server restart |
| Expense list | `GET /api/expenses` rendered newest-first | A new entry appears in the list without editing code |

The slice is deliberately ugly. Its only job is to prove the frontend, backend, and database are wired together end to end.

### ⭐ 4.2 Rare tier — v1.0 (Day 5)

| Feature | Behavior | Acceptance check |
|---|---|---|
| Budget HP bar | Monthly budget (default 1500 SAR, editable) rendered as a bar; drains as expenses land; green above 50%, yellow 20–50%, red below 20%; 0 HP shows a "defeated" state | Adding an expense visibly lowers the bar and color thresholds trigger correctly |
| Streak | Consecutive days with ≥1 logged entry; a missed day resets it | Computed from entry dates; verified with seeded test data |
| XP | Every logged entry earns XP (e.g. +10, small bonus for first log of the day) | XP total matches entry history exactly |
| Monthly summary | `GET /api/summary` returns per-category totals, total spent, budget remaining, streak, XP; Chart.js renders a category chart | Chart numbers match a manual SQL check |
| AI coach | `POST /api/coach` sends the pre-computed stats to Ollama with the selected personality's system prompt; returns a short review + one saving tip | Response renders within a reasonable time; graceful error if Ollama is down |
| Monthly boss fight | The top spending category is framed as the month's boss; the model writes the report (boss name, damage = real total, weakness) from provided numbers only | Damage figure always equals the real category total (the model is given it, never asked to compute it) |

### 🏆 4.3 Epic tier — stretch (only if Day 5 has hours left)

| Feature | Behavior |
|---|---|
| AI expense entry | Free-text like "Lunch at AlBaik 28 SAR" → model returns structured JSON `{amount, category, note}` → validated before insert. LLM output is never trusted blindly — malformed JSON is rejected with a friendly error. (Also prime planted-bug material for Day 4.) |
| AI weekly quests | Model turns last week's stats into one challenge ("keep food under 250 SAR") with an XP reward |
| Achievements & titles | "First no-spend day", "7-day streak", "survived the month"; model-assigned titles like *Budget Ninja* |

## 🏗️ 5. Architecture & data

```
Browser (HTML/CSS/JS + Chart.js)
        │  fetch() — JSON over HTTP
        ▼
FastAPI backend (routes, validation, all arithmetic)
        │                        │
        ▼                        ▼
   SQLite (data)          Ollama local LLM (words only)
```

### 🔌 5.1 API surface

| Method & path | Purpose |
|---|---|
| `POST /api/expenses` | Create an expense `{amount, category, note, date}` |
| `GET /api/expenses` | List expenses (optional `?month=`) |
| `GET /api/summary?month=` | Totals per category, total spent, remaining budget, streak, XP |
| `GET/PUT /api/budget` | Read / set the monthly budget |
| `POST /api/coach` | `{month, mode}` → `{review, tip, boss: {name, damage, weakness}}` |
| `POST /api/parse` *(stretch)* | Free text → structured expense JSON |

### 📊 5.2 Data model

- `expenses(id, amount REAL, category TEXT, note TEXT, spent_on DATE, created_at TIMESTAMP)`
- `settings(key TEXT PRIMARY KEY, value TEXT)` — currently just `monthly_budget`

Streak, XP, and the boss are **derived at read time**, never stored — one source of truth, no sync bugs. (A stored-vs-derived mismatch is exactly the kind of subtle bug Day 4 exists to practice on.)

### 🤖 5.3 AI integration rules

1. The model receives **pre-computed statistics** in the prompt; it is never asked to add, subtract, or count.
2. Model output is display text (or, for stretch parsing, JSON that is validated before touching the database).
3. Personality modes (Coach / Roast / Pirate) differ only in system prompt — one string each.
4. If Ollama is unreachable, the app degrades gracefully: numbers and charts still work, the coach panel shows an error.

## 🗺️ 6. Roadmap & repo conventions

| Version | Day | What lands |
|---|---|---|
| — | Day 1 | This spec: first commit of the repo |
| v0.1 | Day 2 | The thin slice: add expense → SQLite → list, end to end |
| v0.2 | Day 3 | Hardening: 5 code-review findings applied, documented in `REVIEW.md` |
| v0.3 | Day 4 | Bug hunt: 3 planted bugs (one frontend, one backend, one integration/AI) → AI-assisted diagnosis → fixes, documented in `BUGLOG.md` |
| v1.0 | Day 5 | The payload: charts, HP bar, streak, XP, AI coach + boss fight, polish — built in that order so the cut line moves up from the bottom if time runs out |

Conventions: one tagged release per day; honest commit messages; a `screenshots/` folder with one image per version; README with a day-by-day evolution section. **The commit history is part of the deliverable** — someone reading only the repo should understand how the project evolved.

`BUGLOG.md` entry format: *bug → symptom → AI diagnosis process → root cause → fix commit.*

## 🚧 7. Constraints & out of scope

**Hard constraints (v1.0 will not do these):**

- No accounts, logins, or multi-user — one player, on localhost
- No bank sync, card data, or any real financial integration — entries are typed in by the user
- No cloud deployment — data never leaves the machine
- The AI never does arithmetic — Python computes every number
- AI output is advisory only — it can never create, edit, or delete records
- One person + one AI assistant + five days — any feature threatening the deadline moves down a tier

**Parked in the future list (deliberately cut for scope, not forgotten):** PDF monthly report, CSV export, spending calendar, recurring expenses, tags, search & filter, savings goals, notifications, dark mode, responsive mobile layout, levels beyond basic XP.

## ✅ 8. Definition of done

1. Clone the repo, run one command, add an expense, and watch the HP bar drop.
2. The monthly summary shows real charted totals plus the AI coach's commentary and boss report.
3. README shows one screenshot per version, v0.1 → v1.0.
4. Repo history tells the week's story: daily tags, `REVIEW.md` with five findings, `BUGLOG.md` with three planted bugs → diagnosis → fix.

## ⚠️ 9. Risks & mitigations

| Risk | Mitigation |
|---|---|
| Ollama returns malformed or bizarre output | Validate/parse defensively; show a fallback message; never let model output touch the DB unvalidated |
| Ollama not running when the app starts | Graceful error in the coach panel; the rest of the app works without it |
| Day 5 overload | Fixed build order (charts → gamification → AI → polish); the cut line moves up from the bottom |
| Scope creep mid-week | The tier system is binding: new ideas go to the future list, not the sprint |