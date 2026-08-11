# 🗺️ Sanad — Project Plan

**Capstone:** Agentic AI Application
**Project name:** **Sanad** (سند — *support, backing, the thing you lean on*)
**Date:** 2026-08-11 (Day 1)
**Status:** Planned, scope locked

> Companion documents: [REQUIREMENTS.md](REQUIREMENTS.md) · [Additional-Info/ARCHITECTURE.md](Additional-Info/ARCHITECTURE.md) · [Additional-Info/RISKS.md](Additional-Info/RISKS.md)

---

## 1. 🎯 The problem

Applying for freelance work has two failure points, and they compound.

The first is the CV. Most people's CVs are honest but badly written — responsibilities instead of results, no numbers, formatting an ATS can't parse. The person can't see it, because they wrote it.

The second is the search. Freelance boards return hundreds of projects a day, almost none of them relevant. Reading them is the whole job.

Week 6's **FreelanceScout** solved the second problem: upload a CV, get the five best-matching live projects with a pitch for each. But it assumed the CV was already good, and it assumed a person willing to open a web form and wait.

**Sanad closes both gaps.** It fixes the CV *first*, then matches with the improved version, and it lives in a chat window instead of a form — including sending one gig every morning without being asked.

---

## 2. 🤖 What Sanad is

A **Discord DM bot** that:

1. **Reviews** your CV (`cv-reviewer` skill) → summary in chat + full report as a PDF
2. **Rewrites** it (`cv-optimizer` skill) → optimised CV + change report, both PDFs
3. **Matches** the optimised CV against live freelance projects, with a pitch per job
4. **Remembers** your CV between sessions
5. **Sends one job suggestion every morning, unprompted**

Point 5 is what makes it an automation rather than a chatbot, and it is central to the pitch.

### Why this is genuinely *agentic*

Week 6 was a deterministic pipeline: a fixed trigger, a fixed order, one path. Week 7 adds the layer above it.

| | Week 6 — FreelanceScout | Week 7 — Sanad |
|---|---|---|
| **Entry** | one web form | free-form chat, any message |
| **Control flow** | fixed node order | agent decides intent per message |
| **Decisions made by AI** | scoring, pitch writing | *plus* what the user actually wants |
| **The pipeline** | is the product | is a **tool the agent calls** |
| **Memory** | none | CV persists across sessions |
| **Initiative** | none — waits to be triggered | acts on its own every morning |

The agent has to answer, every single message: *is this a CV upload, an approval, a job request, a parameter change, or a plain question?* Nothing in the flow is pre-ordained. That is the requirement the capstone title asks for, and Week 6 deliberately left it out so that Week 7 would have a real job to do.

---

## 3. 🚶 The use case — the walkthrough that is the spec

This is the target experience, start to finish. It is the acceptance test for the whole project.

1. Alex opens Discord; Sanad sits in his DMs like any other bot
2. First message → welcome + short instructions
3. He sends his messy CV → Sanad runs **cv-reviewer** and asks its intake questions in the DM
4. Sanad replies with a **text summary** plus the **full review as a PDF attachment**
5. Sanad asks whether he wants it fixed (→ **cv-optimizer**)
6. Alex says yes
7. Sanad returns the **optimised CV** and a **change report**
8. Sanad asks whether he likes it or wants changes *(v2)*
9. Both documents are delivered **as PDFs**
10. Sanad offers to find freelance work; Alex accepts
11. Alex sets parameters — money, difficulty, skills gained, resume worth — or asks for **one job per parameter** *(v1.5)*
12. Sanad matches using the CV + parameters
13. Returns the **top 3–5 jobs** with a pitch each
14. Alex keeps / drops / refreshes *(v2)*
15. If he drops any, Sanad offers replacements *(v2)*
16. Alex has his links
17. Later: *"add this new project to my CV"* → Sanad updates it → new PDF *(v1.5)*
18. **Sanad remembers the CV** between sessions
19. **Every morning at 08:00, one unseen gig arrives** — or "nothing new today"

---

## 4. 📦 Scope — decided, not up for redesign

### ✅ v1 — must build

| # | Feature | Day |
|:-:|---|:-:|
| 1 | Discord DM in/out, welcome on first contact | 2 |
| 2 | CV → `cv-reviewer` → summary in chat + review PDF | 2 |
| 3 | → `cv-optimizer` → optimised CV + change report, both PDF | 3 |
| 4 | Job matching on request — top 5 with pitches | 3 |
| 5 | CV persisted between sessions | 3 |
| 6 | Daily 08:00 — one unseen gig, or "nothing new today" | 3 |

### 🔶 v1.5 — build only if Day 3 lands early

| # | Feature | Why it's next in line |
|:-:|---|---|
| 7 | One job per parameter — the money one, the learning one, the portfolio one | Cheap to add and the best-demoing feature in the whole list |
| 8 | *"Add this new project"* → updated CV | Closes the loop; shows the CV is genuinely persistent state |

### 🔴 v2 — designed and documented, **not built**

| # | Feature | Why it's cut |
|:-:|---|---|
| 9 | Revision loop on the rewrite — *"any changes?"* | Multi-turn editing state; a day's work on its own |
| 10 | Keep / drop / refresh / replacements | Needs per-match state and a re-query path |
| 11 | Full four-axis scoring — difficulty, skills gained, resume worth | Three of the four axes are LLM judgment, not API data; needs evaluation to be honest |
| 12 | A second job source | Week 6 proved the alternatives are poor; finding a good one is research, not build |

**Single user.** Each person self-hosts their own instance. No user table, no per-user state, no cadence storage — configuration is a handful of fixed values.

Cutting multi-user is what makes the rest fit in three days. It is stated as a limitation, not hidden.

---

## 5. 🏁 Where Day 1 starts from

Sanad is **not** starting at zero. Two things already exist and are proven:

**From Week 4** — the two skills, `cv-reviewer` and `cv-optimizer`, already built, tested and installed in `~/.claude/skills/`.

**From Week 6** — FreelanceScout: a 23-node end-to-end n8n automation that fetches live projects, scores them against a CV profile, ranks, writes pitches, gates on approval, saves to Sheets and notifies. It works. It is the pipeline Sanad's agent will call as a tool.

**From pre-week prep (2026-08-10)** — the integration spikes, all verified:

| What | Result |
|---|---|
| Claude Code CLI, headless `-p` mode | ✅ v2.1.226, subscription auth |
| Skills discovered and triggered headlessly | ✅ both skills, on a real PDF |
| Session continuity across separate processes | ✅ `--session-id` then `--resume` |
| Skills chain themselves | ✅ reviewer offered the optimizer unprompted |
| `sanad_bridge.py` — HTTP → Claude Code | ✅ `/health` ok, two-turn memory over HTTP |
| `md2pdf.py` — Markdown → PDF | ✅ headings, tables, bullets, blockquotes |
| Discord DM — create, send, read, attachments | ✅ end to end, bot `Sanad-AI#1718` |
| n8n 2.33.7 self-hosted natively | ✅ installed, DB initialised |
| Demo fixture | ✅ messy CV scores **46/100**, polished **85/100** |

So the build days are **assembly and integration**, not discovery. That is deliberate: the unknowns were burned down *before* the clock started.

---

## 6. 📅 Day-by-day plan

### Day 1 — Project Planning *(2026-08-11)* ← today
Scope locked, requirements written, architecture documented, risks registered. No code.

**Out:** this plan, `REQUIREMENTS.md`, `ARCHITECTURE.md`, `RISKS.md`, `DAY1-REPORT.md`.

### Day 2 — Build Core *(2026-08-12)*
The conversation loop, working end to end for one feature.

1. ⚠️ **First task, before anything else:** prove n8n's HTTP Request node can reach `sanad_bridge.py`. This is the last open unknown in the architecture (see [RISKS.md](Additional-Info/RISKS.md), R-1). Estimated 30 minutes; a fallback exists if it fails.
2. Discord polling loop — Schedule Trigger every 15s, read new messages, deduplicate against already-seen message IDs
3. Welcome message on first contact
4. Agent node for intent routing
5. **CV → review → summary in chat + PDF back** — the first complete round trip

**Definition of done:** send the messy fixture CV as a Discord DM, answer the intake questions in chat, receive the summary and the review PDF back in the same DM.

### Day 3 — Build Integration *(2026-08-13)*
Everything else in v1, hung off the loop Day 2 built.

1. `cv-optimizer` chained after the review → optimised CV + change report, both as PDFs
2. CV persistence to the `CVs` sheet, and reload on the next session
3. Job matching — port Week 6's fetch → score → rank → pitch, called as a tool by the agent
4. Daily 08:00 digest — one unseen gig or "nothing new today"
5. **Carry-over fixes applied while porting:** `notable_projects` in the profile schema, pitch must cite a real past project, `language` filter on Freelancer results, temperature pinned for ranking (see [RISKS.md](Additional-Info/RISKS.md) §3)

**If this finishes early → v1.5**, feature 7 first.

**Definition of done:** the full walkthrough in §3 runs, steps 1–7, 10–13, 18–19.

### Day 4 — Testing and Evaluation *(2026-08-14)*
1. Run the whole walkthrough against both fixtures — messy and polished
2. Failure paths: unsupported file type, no attachment, bridge down, Discord rate-limited, empty job results, LLM returns malformed JSON
3. Determinism check — the same CV matched twice, differences recorded honestly
4. Evaluation: does the optimised CV actually score higher than the original? Both numbers reported
5. **Record the full demo video** — the night before Demo Day, not on the day

### Day 5 — Demo Day *(2026-08-15)*
Live demo, `README.md`, `SETUP.md`, and the write-up covering limitations and the v2 design.

---

## 7. ✅ Definition of done

Sanad is finished when a person who has never seen it can:

- [ ] Follow `SETUP.md` and get a running instance
- [ ] Send a CV in a Discord DM and get a review PDF back
- [ ] Say yes and get an optimised CV plus a change report
- [ ] Ask for freelance work and get five relevant live projects with pitches
- [ ] Close Discord, come back tomorrow, and find Sanad still knows their CV
- [ ] Wake up to one job suggestion they didn't ask for

And when the write-up states, without softening: what it can't do, what isn't deterministic, and what only works while the PC is on.

---

## 8. 🧭 Principles for the build

1. **The unknown gets tested first.** Day 2 opens with the bridge check, not with the fun part.
2. **n8n is a thin pipe.** Claude Code owns the conversation — it asks the intake questions, holds the session, chains the skills. n8n moves text and files. This was proven, not assumed: the reviewer offered the optimizer on its own.
3. **Ship the default that costs nothing.** The repo ships with Gemini and ported Code nodes so a classmate without a Claude subscription can still run it.
4. **Every key is a placeholder.** Same pattern as Week 6 — `PASTE_YOUR_..._HERE`. Nothing personal is committed.
5. **Only the synthetic CV is used in testing.** Marcus Silva is fictional; no real personal data reaches any model.
6. **Limitations get written down the day they are found**, not discovered by a supervisor during the demo.
