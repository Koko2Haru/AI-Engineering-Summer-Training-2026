# 🤝 Week 2 — AI-Assisted Development

**AI Engineering Summer Training 2026**
Instructor: **Eng. Abdullah Barghash**
Student: **Ali** ([koko2haru](https://github.com/Koko2Haru))

The second week of the program: from *a one-page idea* to a **shipped, gamified, AI-powered finance tracker** by the end. Five days, one continuous project — spec writing, AI pair-programming, code review, deliberate debugging, and a final polish-and-ship sprint. The app: **CoinQuest** 🎮💰 — a finance tracker disguised as an RPG, where expenses are *damage*, budgets are *HP bars*, and an Ollama-powered coach roasts your spending.

---

## 🗺️ The week at a glance

| Day | Focus | Outcome | Deliverable |
|:---:|-------|---------|-------------|
| **1** | Vibe-coding start: pick a project & write a spec | A finalized spec + v0.1→v1.0 roadmap | [`SPECS.md`](Day-1-Vibe-Coding-Start/SPECS.md) · [📄 one-page spec PDF](Day-1-Vibe-Coding-Start/CoinQuest%20%E2%80%94%20one-page%20software%20specification.pdf) |
| **2** | Building with an AI partner | The v0.1 working slice, built by Claude Code | [`SKELETON-V01.md`](Day-2-Building-with-an-AI-Partner/SKELETON-V01.md) · [📦 CoinQuest-Skeleton](Day-2-Building-with-an-AI-Partner/CoinQuest-Skeleton) |
| **3** | Reading AI-written code | 10 improvements found & applied → v0.2 | [`COINQUEST-V02.md`](Day-3-Reading-AI-Written-Code/COINQUEST-V02.md) · [📦 CoinQuest-v02](Day-3-Reading-AI-Written-Code/CoinQuest-v02) |
| **4** | Debugging with AI | 8 planted bugs hunted via symptom-only prompts | [`REVIEW.md`](Day-4-Debugging-with-AI/REVIEW.md) · [🖼️ screenshots](Day-4-Debugging-with-AI/screenshots) |
| **5** | Polishing & shipping | CoinQuest **v1.0** — the final deliverable | [`COINQUEST-V10.md`](Day-5-Polishing-and-Shipping/COINQUEST-V10.md) · [📦 CoinQuest-v1](Day-5-Polishing-and-Shipping/CoinQuest-v1) |

> 📁 **Folder convention:** per the supervisor's requirement, each day's work lives in its own snapshot folder. The app is *copied forward* every day, so every stage of its evolution is preserved — Day 2 holds the untouched skeleton, Day 3 the reviewed v0.2, Day 4 the bugged debugger copy, and Day 5 the final v1.0.

---

## 📅 Day 1 — Vibe-Coding Start: Pick a Project & Write the Spec

**Focus:** choosing a project worth a week, and writing a one-page software specification before touching any code.
**Skills:** ideation · scoping · spec writing · multi-AI workflow.
**Tools:** LLM chat (research & critique) · HTML→PDF.

**Task:** pick a project and produce a one-page spec defining the core slice, the v1.0 target, and the stretch goals.

This day was almost entirely *thinking*, and it shows in the paper trail:

- **~3 hours of research** (articles + YouTube) produced a longlist of **~19 project ideas** — build-your-own git/redis/bittorrent, an HTTP server, an algorithm visualizer, a real-time chat app, a finance tracker, and more.
- The winner: a **gamified finance tracker with AI features** — full-stack (frontend + backend + integration), unique enough to stand out, and a perfect fit for AI pair-programming.
- The spec went through a **multi-AI review loop**: ChatGPT suggested additions (the **Monthly Boss Fight** 🐉 was the standout, adopted immediately, along with XP and AI personality modes) — and the process even caught a flaw in ChatGPT's proposed roadmap, which became part of the documented workflow. Documenting *how* the AIs were used is the point of the week.
- Naming: the internal codename *Riyal Quest* was retired for a public-ready name — **CoinQuest** (wordplay on *conquest*).
- Final scope: **core** = expense CRUD slice · **v1.0** = budget HP bars + streak + Chart.js summaries + Ollama Coach/Roast/Pirate + boss fight + XP · **stretch** = AI natural-language expense entry, weekly quests, achievements.
- Stack: **FastAPI + SQLite + vanilla JS + Chart.js + Ollama**, with a day-by-day **v0.1 → v1.0 roadmap** mapped onto Days 2–5.

The spec ships in two forms: a short **one-page PDF** for submission, and a detailed **`SPECS.md`** carrying the full ideation log for the repo.

📄 **[SPECS.md](Day-1-Vibe-Coding-Start/SPECS.md)** — the full spec + ideation log (19-idea longlist, multi-AI review process, roadmap).
📄 **[CoinQuest — one-page software specification.pdf](Day-1-Vibe-Coding-Start/CoinQuest%20%E2%80%94%20one-page%20software%20specification.pdf)** — the submission spec.
Also in the folder: [`coinQuest.html`](https://koko2haru.github.io/AI-Engineering-Summer-Training-2026/Week-2-AI-Assisted-Development/Day-1-Vibe-Coding-Start/coinQuest.html) — the HTML source the PDF was rendered from.

---

## 📅 Day 2 — Building with an AI Partner

**Focus:** AI pair-programming — letting an AI coding agent build the v0.1 slice from the spec.
**Skills:** agentic coding · prompt-driven development · scoping a "walking skeleton".
**Tools:** Claude Code (VS Code extension) · FastAPI · SQLite · vanilla JS.

**Task:** build the project's first working slice alongside an AI partner.

The AI companion of choice: the **Claude Code extension inside VS Code**. Fed the spec, it built the entire v0.1 slice inside `CoinQuest-Skeleton/`:

- **`main.py`** — the FastAPI app and API endpoints,
- **`database.py`** — the SQLite layer,
- **`static/index.html`** — the frontend,
- three sample expenses logged to prove the loop works end-to-end,
- and the database gitignored via `*.db` so no local data ever hits the repo.

v0.1 was deliberately minimal — a *walking skeleton*: log an expense, store it, list it back. Everything later builds on this loop.

📄 **[SKELETON-V01.md](Day-2-Building-with-an-AI-Partner/SKELETON-V01.md)** — the v0.1 build write-up.
📦 **[CoinQuest-Skeleton](Day-2-Building-with-an-AI-Partner/CoinQuest-Skeleton)** — the untouched v0.1 code, preserved as the "before" snapshot.
📊 **[demo-slides-v01-fixed.pdf](Day-2-Building-with-an-AI-Partner/demo-slides-v01-fixed.pdf)** — the demo slides (the *-fixed* suffix has a story — see Day 3's side quest).

---

## 📅 Day 3 — Reading AI-Written Code

**Focus:** never trust, always verify — reviewing the AI's code line by line and finding 5+ improvements.
**Skills:** code review · security awareness · refactoring with an AI.
**Tools:** Claude Code · FastAPI · manual code reading.

**Task:** read every line the AI wrote on Day 2, find at least 5 improvements, and apply them.

Day 2's code was copied into `Day-3-Reading-AI-Written-Code/CoinQuest-v02/` (leaving the Day-2 skeleton untouched), then reviewed line by line. The review found **10 improvements** — double the requirement — written up as an `IMPROVEMENTS` brief and handed back to Claude Code to apply:

- **Readability** and **efficiency** cleanups,
- **Correctness** fixes,
- **Security**: an **XSS** hole in how expenses rendered to the DOM, plus missing **API input validation**,
- **Deprecation**: migrating FastAPI's startup events to the modern **lifespan** pattern.

The day's report tells the story as **10 old-vs-new scenario comparisons** — what could go wrong before, and what happens now.

**Side quest** 🗡️: both demo-slides PDFs in the repo rendered *blank* on GitHub. Root cause: image transparency (SMask) breaks GitHub's PDF.js preview. Fix: rasterize every page onto a white background — which is why Day 2's slides carry the `-fixed` suffix.

📄 **[COINQUEST-V02.md](Day-3-Reading-AI-Written-Code/COINQUEST-V02.md)** — the day narrative + all 10 before/after comparisons.
📦 **[CoinQuest-v02](Day-3-Reading-AI-Written-Code/CoinQuest-v02)** — the reviewed and hardened v0.2 code.

---

## 📅 Day 4 — Debugging with AI

**Focus:** deliberately breaking the app, then measuring how well an AI debugs from symptoms alone.
**Skills:** debugging methodology · symptom description · testing an AI's limits.
**Tools:** Claude Code · the v0.2 codebase.

**Task:** plant 3+ bugs in the working app, then debug them with an AI using only symptom descriptions — no pointing at the code.

v0.2 was copied into `CoinQuest-v02-Debugger/` and sabotaged with **8 planted bugs** on an **easy/medium/hard grid** across all three files — `main.py`, `database.py`, and the frontend (the html-easy cell was skipped deliberately). Then the hunt: Claude Code received **symptom-only prompts** — "the app does X when it should do Y" — never the code location.

Findings worth remembering:

- 👁️ **Visible bugs die instantly.** Anything that throws an error or visibly misbehaves, Claude Code found immediately — and it even fixed *unprompted neighboring bugs* it noticed along the way.
- 🤫 **Silent bugs need precise symptoms.** A missing DB commit and a month off-by-one produced no errors — they only fell when the symptom description was exact.
- 🎭 **The prompt sets the search space.** One experiment deliberately *misled* the AI ("the amount saves as 999") — and it dutifully hunted in the wrong place. The wording of a bug report literally defines where an AI looks.

The whole hunt is documented with screenshots of each debugging exchange.

📄 **[REVIEW.md](Day-4-Debugging-with-AI/REVIEW.md)** — the bug grid, the hunt, and the findings.
📦 **[CoinQuest-v02-Debugger](Day-4-Debugging-with-AI/CoinQuest-v02-Debugger)** — the sabotaged copy (bugs preserved for posterity).
🖼️ **[screenshots](Day-4-Debugging-with-AI/screenshots)** — the debugging sessions, captured.

---

## 📅 Day 5 — Polishing & Shipping

**Focus:** taking the app from *working* to *shippable* — the full v1.0 payload from the spec, plus a design overhaul.
**Skills:** iterative polish · UX judgment · game design logic · shipping.
**Tools:** Claude Code · Chart.js · Ollama · Poppins (Google Fonts).

**Task:** apply everything remaining from `SPECS.md`, polish the app, and ship the final deliverable.

The app was copied one last time into `CoinQuest-v1/`, and the rough post-milestones build (internally **v0.5** — plain white page, default fonts) went through five focused upgrade rounds, one version bump per session:

- **v0.6 — Damage History** 🗡️: the expense list became a proper battle log — multi-select delete with *Select all*, sorting on damage/date/category, color-coded severity levels from **LOW** 🟢 to **FATAL** 💀, and WhatsApp-style expandable notes.
- **v0.7 — Coin Adder** 🪙: calendar date picker, custom category input on *Other*, the form no longer resets to *Food* after each entry, and every damage is tagged **Cash** 💵 or **Credit** 💳.
- **v0.8 — AI Coach** 🧙: multiple Ollama models benchmarked head-to-head; the fastest one with quality responses now powers Coach / Roast / Pirate and the boss report.
- **v0.9 — Cash vs Credit analytics** 📊: the pie chart keeps the combined overview, joined by two dedicated bar charts (Coins / Spent / Remaining per payment method), with percentages on every chart.
- **v1.0 — Final polish** ✨: separate editable Cash + Credit + Total budget bars; a full **XP rework** — the old logic rewarded *adding* expenses (backwards!), the new one grows XP by *time survived without spending* (doubling hour after hour) and resets to **0** the moment a damage lands; **Poppins** typography; and a glossy, wavy **animated background**.

The v2.0 backlog is already written: healing passives (income), healing potions, achievements, periodic reports, an animated boss that gets scarier as you take damage, a player character with earnable equipment, sound design, and multi-currency support.

📄 **[COINQUEST-V10.md](Day-5-Polishing-and-Shipping/COINQUEST-V10.md)** — the full v0.5 → v1.0 journey, with before/after screenshots.
📦 **[CoinQuest-v1](Day-5-Polishing-and-Shipping/CoinQuest-v1)** — the shipped app. **The Week 2 deliverable.** 🚀

---

## 🧵 The through-line

Each day fed the next, which is the point:

- **Day 1's** spec and roadmap → the exact build order for Days 2–5; nothing was improvised.
- **Day 2's** walking skeleton → the foundation every later version was copied from and built upon.
- **Day 3's** line-by-line review → a hardened, secure v0.2 — and the habit of *never merging AI code unread*.
- **Day 4's** bug hunt → firsthand knowledge of where an AI debugger shines (visible errors) and where it's blind (silent logic bugs) — and that the *symptom wording* steers the whole search.
- **Day 5** → all of it converging into one polished, gamified, AI-coached app, shipped as v1.0.

A week that started with a blank spec template and ended with CoinQuest. ⚔️💰

---

*Part of [AI-Engineering-Summer-Training-2026](https://github.com/koko2haru/AI-Engineering-Summer-Training-2026).*