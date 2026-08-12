# Week 7 — Capstone: Agentic AI Application 🎓🤖

> **Instructors:** Abdullah Barghash & Mohammad Mashat
> **Theme:** one week to turn a deterministic pipeline into something that decides.
> A day of planning with no code, three days building a Discord bot that reviews a CV,
> rewrites it, and hunts live freelance work for it, a day measuring whether any of
> that actually worked, and a demo.

**AI Engineering Summer Training 2026**
Student: **Ali** ([koko2haru](https://github.com/Koko2Haru))

---

## 🎯 The Capstone: Sanad

**Sanad** (سند — *support, backing, the thing you lean on*) is a Discord DM bot that
takes a badly written CV, rewrites it into a strong one, then finds live freelance work
that fits it — and sends one job suggestion every morning without being asked.

### The measured result

> **A CV went from 42/100 to 73/100. A professionally written version of the same
> person scored 75.**
>
> Pitches cite the candidate's real past projects **91%** of the time, against **0%** in
> Week 6.

### Why it exists

Applying for freelance work has two failure points and they compound. **The CV** is
usually honest but badly written — duties instead of results, no numbers, formatting an
ATS cannot parse — and the person cannot see it, because they wrote it. **The search**
returns hundreds of irrelevant projects a day.

Week 6's FreelanceScout solved the second problem and assumed the first away. Sanad
fixes the CV **first**, then matches with the improved version.

### What makes it agentic

Week 6 was a fixed pipeline behind a web form. Sanad has to answer, on **every single
message**: *is this a CV upload, an answer to a question I asked, an approval, a job
request, or just chat?* A language model reads each message and routes it — **there is
no keyword matching anywhere.** The Week 6 pipeline is no longer the product; it is a
tool the agent calls.

And it acts on its own. Everything else waits to be spoken to; the 08:00 digest doesn't.

---

## 🗓️ Day by Day

| Day | Focus | Deliverables | Report |
|---|---|---|---|
| 1 | Project planning | [Plan](Day-1-Project-Planning/Plan-and-Require/PROJECT-PLAN.md) · [Requirements](Day-1-Project-Planning/Plan-and-Require/REQUIREMENTS.md) · [Architecture](Day-1-Project-Planning/Plan-and-Require/Additional-Info/ARCHITECTURE.md) · [Risks](Day-1-Project-Planning/Plan-and-Require/Additional-Info/RISKS.md) — 42 requirements, each with an acceptance test | [Day 1](Day-1-Project-Planning/DAY1-REPORT.md) |
| 2 | Build core | [`sanad-poll-loop.json`](Day-2-Build-Core/Core-Loop/sanad-poll-loop.json) — Discord loop, CV → review → PDF back | [Day 2](Day-2-Build-Core/DAY2-REPORT.md) |
| 3 | Build integration | [`sanad-poll-loop.json`](Day-3-Build-Integration/Integration/sanad-poll-loop.json) · [`sanad-job-matching.json`](Day-3-Build-Integration/Integration/sanad-job-matching.json) · [`sanad-daily-digest.json`](Day-3-Build-Integration/Integration/sanad-daily-digest.json) — 65 nodes across 3 workflows | [Day 3](Day-3-Build-Integration/DAY3-REPORT.md) |
| 4 | Testing & evaluation | [`fr15-test.py`](Day-4-Testing-and-Evalualation/Testing/fr15-test.py) · [`match-quality-test.py`](Day-4-Testing-and-Evalualation/Testing/match-quality-test.py) — the headline number, and the rates behind it | [Day 4](Day-4-Testing-and-Evalualation/DAY4-REPORT.md) |
| 5 | Demo day | [`Resources/`](Day-5-Demo-Day/Resources/) — 7 self-contained source documents | [Day 5](Day-5-Demo-Day/DAY5-REPORT.md) |

---

## 📅 Day 1 — Project Planning

**Focus:** decide what this is before building any of it.
**Task:** plan the capstone — scope, requirements, architecture, risks.

Week 6's pipeline already worked, so the temptation was to open the editor and bolt
features on. The reason not to: **a pipeline is not an agent**, and getting from one to
the other is a design change, not a feature.

Wrote **32 functional and 10 non-functional requirements, each with an acceptance
test** — not *"the bot replies to messages"* but *"two polls over the same message
produce one reply, not two."* That turned Day 4 from a vague testing day into a
checklist.

Two scope cuts made here carried the whole week. **Multi-user was cut** — one instance
per person, which is what made the rest fit in three days. **Four-axis job scoring was
cut**, because only *money* is real data; the other three axes are model judgements with
no field behind them in any API. Shipping three invented axes would look impressive and
mean nothing.

The most valuable hour was auditing nine pre-verified integrations against the
architecture, which found exactly **one** untested link: could n8n's HTTP node actually
reach the local bridge? That became Day 2's first task.

---

## 📅 Day 2 — Build Core

**Focus:** the conversation loop, working end to end for one feature.
**Task:** build the core of the application.

Opened by closing the unknown. The test was designed to prove more than it needed to —
two turns, *"remember the number 7"* then *"what number?"* — because the real dependency
wasn't connectivity, it was whether **session memory survives separate n8n executions**.
It does.

Then four bugs, each teaching something:

- **n8n 2.x refuses to touch the filesystem.** The documented workaround is an
  environment variable every future user would also need. Instead the bridge took over
  all file I/O — **n8n now speaks nothing but HTTP.**
- **An HTTP node overwrites `$json`.** A side-effect node sitting mid-chain replaced the
  workflow's own data with Discord's response. Rule adopted for the rest of the build:
  anything downstream of an HTTP node references its source node by name.
- **Claude Code is sandboxed to its working directory** — it said so, in chat, rather
  than throwing a stack trace.
- **Overlapping executions.** One CV upload produced **five acknowledgements and five
  different intake questions**. The cursor lived in n8n's static data, which is only
  written when an execution *finishes* — so a dozen 15-second polls during a 3-minute
  review all read a stale cursor. **A lock that only exists after the work is not a
  lock.** Moved to the bridge, written under a mutex before anything slow starts.

And a fifth found by reading state rather than output: a malformed file path meant the
review had **only worked by luck**. A green run is not proof of correctness.

---

## 📅 Day 3 — Build Integration

**Focus:** everything else in v1.
**Task:** integrate the pieces into the complete application.

Chained the optimizer, ported Week 6's matching as a 25-node sub-workflow, added the
agent layer, and built the 08:00 digest. Feature-complete by the end of the day.

**The most interesting problem was invention.** The first rewrite claimed *"saving 2–10
hours **per week**"* when the source said *"saved between 2-10 hrs"*; turned *"a tool
**used by** 100+ clients"* into *"a **client base** of 100+"*; and promoted *"many happy
clients"* to *"a **majority**"*.

None is a hallucination. The model invented nothing — it **resolved ambiguity in the
candidate's favour**, three times, which is subtler and far more dangerous. The
instruction *"never invent facts"* was already in the prompt and stopped none of it,
because none of it *felt* like inventing a fact. The rule only worked once it named the
exact moves: don't add a rate, don't re-attribute a number, don't strengthen a
quantifier, and **if an answer is ambiguous, don't pick the more impressive reading.**

**A second finding was uncomfortable:** the intake was shallow — three questions, one at
a time — because my orchestration prompt said *"ask ONE at a time, three maximum"* while
the skill it was driving said *"don't drip-feed one question at a time."* I was
overriding my own skill and making it worse. Removing the cap took it to **14 questions
in a single message**, and halved the number of model invocations.

Four Week 6 carry-over fixes were applied during the port and all four held.

---

## 📅 Day 4 — Testing & Evaluation

**Focus:** stop building, start measuring.
**Task:** test and evaluate the application.

Three days of building produced a system that worked every time it was run. That is not
the same as knowing it works.

**The headline.** Everything pinned except the document — same skill, same target role,
no intake questions:

| Document | Score |
|---|:-:|
| Original messy fixture | **42** |
| Original, second run | **42** |
| **Sanad's rewrite** | **73** |
| Hand-written "polished" version | **75** |

The two identical 42s corrected a standing assumption: earlier variation (46, 49, 40)
was **not** model noise, it was different inputs between runs.

**Rates, not anecdotes.** Mining every stored execution rather than burning new ones:
**10/11 pitches cite a real past project (91%)** against 0/5 in Week 6, and **0/11
contain banned filler** against 3/5.

**And one finding that only appears with a sample size:**

```
 90 : #        (1)
 85 : ##       (2)
 80 : ######   (6)   ← 55% of every match ever scored
 70 : ##       (2)
```

Six of eleven matches were **tied**, so "top 5, ranked" is partly an illusion. The cause
is a prompt-design flaw, not a model failure: the prompt offers four score bands and the
model anchors to band boundaries. **It is scoring categorically while being asked for a
continuous number.**

Also recorded: what *couldn't* be tested. Job-ranking determinism is methodologically
blocked, because the live job pool changes between runs. Written down as unmeasured
rather than guessed.

---

## 📅 Day 5 — Demo Day

**Focus:** package it so it can be understood without me in the room.

Four chronological day-reports answer *"what happened Tuesday"*, not *"what is this and
does it work."* Day 5 restructured everything **by question** into seven self-contained
source documents, written to be fed to NotebookLM — so one pack generates the write-up,
the demo introduction, and answers to supervisor questions.

Writing it surfaced a pattern none of the daily reports had caught.

---

## 🧵 The Through-Line

**Nearly every serious bug this week had the same shape: something worked, and the
reason it worked was not the reason I assumed.**

| What appeared to work | Why it actually worked |
|---|---|
| The CV review ran | Claude Code found the file **by name after a malformed path** |
| The pitches were generic | **my schema omitted projects**, so the model couldn't cite them |
| The CV PDF rendered flat | the model **emitted no Markdown**; the renderer was innocent |
| The intake asked 3 questions | **my prompt was overriding the skill**, which wanted more |
| Scores clustered at 80 | **my prompt offered bands** and the model anchored to them |

In every case the fix only became obvious after establishing *why* it worked rather than
*that* it worked.

**Three plans changed during the build, and each change beat the plan.** n8n was going
to orchestrate the CV conversation — until testing showed the skills chain themselves,
so n8n became a thin pipe. The bridge was going to be a 40-line shim — it became the
single place where every side effect lives, because n8n can't touch files or hold a lock
during slow work. An AI Agent node was going to call matching as a tool — until it
became clear an agent returns *narration* of a result, not structured data.

**One plan from Week 6 also changed:** the capstone was going to use WhatsApp. Its
24-hour messaging window would have made the unprompted daily digest a paid, pre-approved
template message — **the single most important feature would have been the one that cost
money.** Discord has no such restriction.

---

## 🧰 Stack

| Layer | Choice |
|---|---|
| Interface | **Discord DM**, polled every 15s — no inbound networking at all |
| Orchestration | **n8n 2.33.7**, self-hosted natively — 3 workflows, 65 nodes |
| CV review & rewrite | **Claude Code CLI** + two Claude Skills from Week 4 |
| Bridge | **`sanad_bridge.py`** — 9 endpoints; owns files, state, PDFs, the lock |
| PDF | **`md2pdf.py`** — `reportlab` only, two style profiles |
| Job source | **Freelancer.com API** |
| Models | **Gemini** (routing, profiling) · **DeepSeek** (scoring) · **Groq** (pitches) |
| Storage | **Google Sheets** (Jobs, Matches) + a JSON state file |
| Cost | **$0** — free tiers and an existing subscription throughout |

---

## 📂 Structure

```
Week-7-Capstone-Project/
├── WEEK7-README.md                    this file
├── sanad/                             the application
│   ├── bridge/        sanad_bridge.py · md2pdf.py
│   ├── skills/        cv-reviewer · cv-optimizer
│   ├── fixtures/      the messy and polished demo CVs
│   └── scripts/       start-sanad.bat · stop-sanad.bat
├── Day-1-Project-Planning/            plan, requirements, architecture, risks
├── Day-2-Build-Core/                  the conversation loop
├── Day-3-Build-Integration/           matching, the agent, the digest
├── Day-4-Testing-and-Evalualation/    the numbers and the harnesses
└── Day-5-Demo-Day/                    Resources/ + NotebookLM-Outputs/
```

**Start here:** [`Day-5-Demo-Day/Resources/00-WHAT-IS-SANAD.md`](Day-5-Demo-Day/Resources/00-WHAT-IS-SANAD.md)
for what it is, or [`04-SETUP-GUIDE.md`](Day-5-Demo-Day/Resources/04-SETUP-GUIDE.md) to
run it yourself.

---

## ⚠️ Honest limitations

- **It only runs while the PC is on**, with both n8n and the bridge running
- **One user per instance** — no auth, no user table. Each person self-hosts
- **Ranking within the top five is close to arbitrary** — 55% of scores are tied at 80
- **~9% of pitches overstate experience**; the guard reports it, the prompt doesn't stop it
- **Budgets aren't normalised** — one result set had CAD, USD, AUD and INR
- **Job-ranking determinism is unmeasured**, not unmeasurable-in-principle: it needs a
  frozen job pool this build never had
- **Sample sizes are small** — 11 matches, 4 scoring runs. The claims that survive are
  directional: citation went from none to nearly all, filler from most to none

Full detail, with fixes identified for each, in
[`06-LIMITATIONS-AND-FUTURE.md`](Day-5-Demo-Day/Resources/06-LIMITATIONS-AND-FUTURE.md).
