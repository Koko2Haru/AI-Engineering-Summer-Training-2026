# 📘 Day 1 Report — Project Planning

**🎯 Focus:** Lock the capstone — what it is, what it isn't, how it's built, and what could go wrong

**📝 Assigned task:** *Project planning — define the capstone, its requirements and its architecture before writing any of it.*

**📅 Date:** 2026-08-11

**✅ Status:** Completed

---

## 🗂️ Folder structure

```
📁 Day-1-Project-Planning/
├── 📄 DAY1-REPORT.md                       ← this report
└── 📁 Plan-and-Require/
    ├── 📄 PROJECT-PLAN.md                  the problem, the use case, scope, day-by-day plan
    ├── 📄 REQUIREMENTS.md                  32 functional + 10 non-functional reqs, each with an acceptance test
    └── 📁 Additional-Info/
        ├── 📄 ARCHITECTURE.md              diagrams, component contracts, data model, rejected alternatives
        └── 📄 RISKS.md                     15-item risk register + the Week 6 carry-over fixes
```

---

## 🎯 Objective

The capstone is **"Agentic AI Application."** Day 1 spends the whole day not building, on purpose.

Week 6 ended with FreelanceScout: a 23-node n8n automation that takes a CV and returns five matching freelance projects with a pitch for each. It works. The temptation was to open n8n and start bolting things onto it.

The reason not to: **FreelanceScout is a pipeline, and a pipeline is not an agent.** Getting from one to the other is a design change, not a feature. That deserved a day.

---

## 🤖 1. What I decided to build

**Sanad** (سند — *support, backing, the thing you lean on*). A Discord DM bot that:

1. Reviews your CV → summary in chat + full report as a PDF
2. Rewrites it → optimised CV + change report, both PDFs
3. Matches the improved CV against live freelance projects, with a pitch per job
4. Remembers your CV between sessions
5. **Sends one job suggestion every morning, unprompted**

It extends Week 6 rather than replacing it: CV review and optimisation go *in front of* the matching, and a chat interface wraps the whole thing.

Point 5 is the one I care most about. Everything before it is a chatbot that waits to be spoken to. A message that arrives at 08:00 with a gig I didn't ask for is an **automation** — and it's what makes the project worth demoing.

---

## 🧠 2. Making the "agentic" part honest

The capstone title asks for an agentic application, so I wrote down exactly what changes:

| | Week 6 — FreelanceScout | Week 7 — Sanad |
|---|---|---|
| **Entry** | one web form | free-form chat, any message |
| **Control flow** | fixed node order | agent decides intent per message |
| **AI decides** | scoring, pitch writing | *plus* what the user actually wants |
| **The pipeline** | is the product | is a **tool the agent calls** |
| **Memory** | none | CV persists across sessions |
| **Initiative** | waits to be triggered | acts on its own every morning |

The real difference is that the agent has to answer, on every single message: *is this a CV upload, an answer to my question, an approval, a job request, or just a question about me?* Nothing is pre-ordained by the trigger.

Week 6 deliberately skipped the AI Agent node — the whole point of that week was deterministic orchestration. That decision is what left Week 7 a real job to do instead of a cosmetic one.

---

## ✂️ 3. Cutting scope before it cut me

The build window is **three days**. I wrote the full use case out as 19 steps, then split it into three tiers and committed to the line.

| Tier | Contents | Rule |
|---|---|---|
| 🟢 **v1** | Discord in/out · CV → review → PDF · → optimise → 2 PDFs · matching with pitches · CV persisted · daily gig | Must ship |
| 🟠 **v1.5** | one job per parameter · *"add this new project"* | Only if Day 3 lands early |
| 🔴 **v2** | revision loop · keep/drop/refresh · four-axis scoring · second job source | Designed, documented, **not built** |

Two cuts were harder than they look:

**Multi-user is out.** One instance, one person, each user self-hosts. No user table, no auth, no per-user state. This is what makes the rest fit in three days, and it gets stated as a limitation rather than quietly omitted.

**Four-axis scoring is out.** The use case wants jobs ranked on money, difficulty, skills gained and resume worth. Only **money** is real data — the other three are LLM judgments with no field behind them in any API. Shipping three invented axes without evaluating them would look impressive and mean nothing. It moves to v2 with the reason written down.

Writing v2 down properly instead of deleting it matters: it turns "I ran out of time" into "I scoped it".

---

## 🏗️ 4. The architecture, and the two rules behind it

```
Discord DM  ──poll every 15s──►  n8n (self-hosted, native npm)
                                   │
                                   ├─ HTTP ──►  sanad_bridge.py  ──►  Claude Code
                                   │            (localhost:8900)      + skills
                                   │
                                   ├──────────►  Freelancer.com API
                                   ├──────────►  Gemini / Groq / OpenRouter
                                   └──────────►  Google Sheets (Jobs / CVs / Matches)
```

**Rule 1 — no inbound networking.** Discord is *polled*, never pushed to. Every connection is outbound. No public URL, no tunnel, no VPS, no certificate. The entire system runs on one laptop with nothing exposed.

**Rule 2 — n8n is a thin pipe.** Claude Code owns the conversation; n8n moves text and files.

Rule 2 wasn't a design choice, it was a finding. When I tested the skills, `cv-reviewer` finished its report by **offering the optimizer unprompted**. It already knew how to chain. Orchestrating that from n8n would have meant rebuilding a conversation I was getting for free.

The full diagrams — mermaid for the system, ASCII for each of the three flows — are in [ARCHITECTURE.md](Plan-and-Require/Additional-Info/ARCHITECTURE.md).

---

## 🔗 5. The detail the whole thing depends on

Every 15-second poll is a **separate n8n execution** with no memory of the previous one. But `cv-reviewer` asks intake questions and waits for answers — an inherently multi-turn conversation.

```
Message 1  ──►  session_id = <uuid>  ──►  --session-id <uuid>  ──►  new session
Message 2  ──►  session_id = <uuid>  ──►  --resume <uuid>      ──►  full history
Message 3  ──►  session_id = <uuid>  ──►  --resume <uuid>      ──►  full history
```

n8n generates the UUID once and stores it in the `CVs` sheet. Claude Code keeps the actual transcript on disk, and `sanad_bridge.py` detects which of the two flags to use by checking whether the transcript file exists.

**n8n stores a pointer; Claude Code stores the conversation.** Tested across genuinely separate processes — a two-turn conversation over HTTP kept its memory.

---

## 📋 6. Requirements with teeth

I wrote **32 functional** and **10 non-functional** requirements, and gave every single one an **acceptance test** — not a description of the feature, but the specific thing that has to be demonstrated.

Not *"the bot replies to messages"* but:

> **FR-4** — Each message is processed exactly once.
> *Test:* two polls over the same message produce one reply, not two.

> **FR-31** — A job already sent is never sent again.
> *Test:* two consecutive daily runs produce two different jobs.

> **FR-22** — Each pitch cites a specific past project and avoids filler.
> *Test:* 5/5 pitches name a real project; none contain the banned phrases.

That last one is a direct answer to a Week 6 failure. Day 4 becomes a checklist to work through rather than a day of poking at things hoping they work.

---

## ⚠️ 7. Finding the one thing that isn't proven

I spent the pre-week burning down integration unknowns rather than saving them for the build days. Nine things were tested and confirmed: Claude Code headless, skills triggering on a real PDF, session continuity, the skills chaining themselves, the bridge over HTTP, `md2pdf.py`, n8n installed, Discord DM in/out with attachments, and a demo fixture that scores **46/100** messy against **85/100** polished.

Auditing that list against the architecture left exactly one gap:

> **R-1 — n8n's HTTP Request node calling `sanad_bridge.py` has never been tried.**
>
> The bridge is proven standalone. The HTTP Request node is one of n8n's most-used nodes. Nothing shell-related is involved — which is the exact thing that broke Execute Command. Risk is low, impact is **critical**, cost to test is **30 seconds**.
>
> **It is the first task of Day 2, before anything else is built.** A file-drop fallback is already designed in case it fails.

That is the only remaining unknown in the entire architecture. Finding that out on Day 1 rather than Day 4 is most of what today was for.

---

## 🔧 8. Collecting the debts

Week 6 produced nine known problems that I deliberately logged instead of patching — each day's rubric was already met, and fixing them properly belonged here. Today they became line items with owners:

| Week 6 problem | Lands on |
|---|:-:|
| Pitches generic, never cite past projects | Day 3 · FR-22 |
| Non-English gigs unfiltered | Day 3 · FR-23 |
| LLM ranking non-deterministic | Day 3 · R-4 |
| Truncated JSON returned as HTTP 200 | Day 3 · R-5 |
| Sheets silently restructuring on header mismatch | Day 3 · R-10 |
| Imported JSON dropping dropdown values | Days 2–3 · R-9 |
| Error workflows only firing in production | Day 4 · R-14 |
| Free-tier claims unverified | Day 3 · R-11 |
| Arbeitnow a weak second source | **dropped** → v2 |

The pitch fix is the one worth naming. I'd blamed the model in Week 6; it was my schema. The profiling step extracted **skills only**, so the pitch step never saw the projects and literally could not cite them. Adding `notable_projects` to the schema is the actual fix.

---

## 📦 9. Deliverables produced today

1. **[PROJECT-PLAN.md](Plan-and-Require/PROJECT-PLAN.md)** — problem, the 19-step use case that serves as the spec, the three scope tiers, the day-by-day plan, and the definition of done
2. **[REQUIREMENTS.md](Plan-and-Require/REQUIREMENTS.md)** — 32 functional + 10 non-functional requirements with acceptance tests, explicit out-of-scope, and the full system/setup requirements
3. **[ARCHITECTURE.md](Plan-and-Require/Additional-Info/ARCHITECTURE.md)** — mermaid system diagram, ASCII flows for all three paths, the bridge API contract, the three-sheet data model, and ten rejected alternatives with reasons
4. **[RISKS.md](Plan-and-Require/Additional-Info/RISKS.md)** — 15-item risk register, the nine carry-over fixes, accepted limitations, and the demo-day contingency

**No code was written today**, which was the point.

---

## 🧭 10. What Day 2 opens with

1. ⚠️ **Prove n8n can reach the bridge over HTTP** — R-1, 30 seconds, before anything else
2. Discord polling loop with deduplication
3. Welcome message on first contact
4. The agent node for intent routing
5. **CV → review → summary + PDF back in the DM** — the first complete round trip

**Done when:** I can send the messy fixture CV as a Discord DM from my phone, answer the intake questions in chat, and get the summary and the review PDF back in the same conversation.
