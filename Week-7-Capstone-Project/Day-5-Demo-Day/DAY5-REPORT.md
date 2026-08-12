# 📘 Day 5 Report — Demo Day

**🎯 Focus:** Package everything so the project can be understood without me in the room

**📝 Assigned task:** *Demo the capstone and document it.*

**📅 Date:** 2026-08-12

**✅ Status:** Documentation complete — demo recording and live demo outstanding

---

## 🗂️ Folder structure

```
📁 Day-5-Demo-Day/
├── 📄 DAY5-REPORT.md                        ← this report
├── 📁 Resources/                            source pack, written for NotebookLM
│   ├── 📄 00-WHAT-IS-SANAD.md               the pitch, use case, why it's agentic
│   ├── 📄 01-ARCHITECTURE.md                workflows, bridge API, data model
│   ├── 📄 02-BUILD-LOG.md                   five days, every bug that mattered
│   ├── 📄 03-EVALUATION-AND-RESULTS.md      every number and its method
│   ├── 📄 04-SETUP-GUIDE.md                 clean-machine install
│   ├── 📄 05-DECISIONS-AND-REJECTED.md      choices, rejections, plans that changed
│   └── 📄 06-LIMITATIONS-AND-FUTURE.md      honest defects, v2
└── 📁 NotebookLM-Outputs/                   generated artefacts land here
```

---

## 🎯 Objective

Four days produced a working system and four day-reports. Those reports are chronological — they answer *"what happened on Tuesday"*, not *"what is this and does it work"*.

Day 5's job was to turn a build log into something a person can be handed.

The approach: **write a source pack for NotebookLM** rather than a single README. Feed it structured sources and it generates study guides, FAQs, briefing documents and an audio overview — so the same seven documents serve the write-up, the demo introduction, and supervisor questions, without writing three different things.

---

## 📚 1. The resource pack

Seven documents, ~72 KB, each **self-contained**. That constraint is deliberate: NotebookLM answers from whichever sources are relevant, so a document that says *"as described in the architecture file"* is a document that fails when asked in isolation. Every one restates what Sanad is in its first two lines.

| Document | Answers |
|---|---|
| **00 — What Is Sanad** | What is this? Who is it for? What does a conversation look like? Why is it "agentic"? |
| **01 — Architecture** | How is it built? What owns what? How does memory survive between messages? |
| **02 — Build Log** | How did it get built, and what went wrong? |
| **03 — Evaluation and Results** | Does it work, and how do you know? |
| **04 — Setup Guide** | How do I run this myself? |
| **05 — Decisions and Rejected** | Why this way and not another way? |
| **06 — Limitations and Future** | What doesn't work, and what would you do next? |

Two editorial choices worth defending:

**The build log keeps the bugs.** It would be shorter without them, and much less useful. The five-day story is largely a story of things that appeared to work for the wrong reason, and that is the genuine engineering content of the project.

**The limitations document leads with the defects that have numbers.** *"Score compression: 55% of matches score exactly 80"* is more useful than a vague admission that ranking could be better — and it comes with a diagnosis and a fix.

---

## 🔍 2. Writing the pack surfaced things the day-reports had missed

Consolidating four days of work revealed a pattern nobody noticed while living through it.

**Nearly every serious bug had the same shape: something worked, and the reason it worked was not the reason assumed.**

| What appeared to work | Why it actually worked |
|---|---|
| The CV review ran | Claude Code found the file **by name after being given a malformed path** |
| The pitches were generic | the **profile schema omitted projects**, so the pitch step could not cite them |
| The CV PDF rendered flat | the model **emitted no Markdown at all**; the renderer was innocent |
| The intake asked 3 shallow questions | the **orchestration prompt was overriding the skill**, which asked for more |
| Scores clustered at 80 | the **prompt offered four bands** and the model anchored to boundaries |

In every case the fix only became obvious after establishing **why** it worked rather than **that** it worked. That is a more useful conclusion than any individual bug, and it only became visible when the four days were written down together.

A second pattern also emerged: **three of the plans changed during the build**, and each change produced a better design than the plan.

- n8n was going to orchestrate the CV conversation — until testing showed the skills chain themselves, so n8n became a thin pipe.
- The bridge was going to be a 40-line shim — it became the single place where side effects live, because n8n could not touch files or hold a lock during slow work.
- An AI Agent node was going to call matching as a tool — until it became clear an agent returns *narration* of a result, not structured data.

Both patterns are now in `02-BUILD-LOG.md` and `05-DECISIONS-AND-REJECTED.md`. Neither was in any daily report.

---

## ✅ 3. Where the project stands

**Feature-complete against the v1 scope agreed on Day 1.** Every requirement built and demonstrated.

| | Requirement | Evidence |
|---|---|---|
| ✅ | Discord DM in/out, welcome on first contact | canned welcome, no model call |
| ✅ | CV → review → summary + PDF | 14 intake questions, 5-page report |
| ✅ | → rewrite → optimised CV + change report | both PDFs, 1-page CV |
| ✅ | Job matching, top 5 with pitches | live Freelancer projects |
| ✅ | CV persisted between sessions | matched with no re-upload |
| ✅ | Daily 08:00 — one unseen gig | delivered unprompted |

**The headline measurement:** a CV went from **42/100 to 73/100**, two points short of a professionally written version of the same person. Pitches cite real past projects **91%** of the time, against **0%** in the predecessor project.

---

## ⚠️ 4. What is still outstanding

Stated plainly rather than glossed.

| | Item | Why it matters |
|---|---|---|
| ⏳ | **Record the demo** | The highest-impact item in the risk register. The live demo depends on the laptop, Discord, Claude Code, the Freelancer API and three LLM providers all working simultaneously |
| ⏳ | **`WEEK7-README.md`** | Currently empty; the repo's week index links to it |
| ⏳ | **Placeholders for personal values** | DM channel ID, sheet ID and the Windows path are hardcoded. Not secrets — no tokens or keys are in the repo — but they make the workflows unrunnable for anyone else |
| ⏳ | **Live demo** | The point of the day |

The recording is the one that cannot be skipped. Everything Sanad does depends on six services being simultaneously healthy, and three of them are free tiers with per-minute limits.

---

## 📦 5. Deliverables

1. **`Resources/`** — seven self-contained source documents, ~72 KB
2. **`NotebookLM-Outputs/`** — with a note on what is worth generating
3. **`DAY5-REPORT.md`** — this report

---

## 🎬 6. The demo script

The order that tells the story in about six minutes:

1. **`hi`** → instant welcome. Point out it is canned, not generated — the fast path is deliberate
2. **Send the messy CV** → acknowledgement, then **14 numbered questions**. This is where the skill does something a template cannot
3. **Answer them, deliberately vaguely** on one — *"saved 2-10 hrs"* → it comes back asking *per week or one-off?* **This is the invention guard, live**
4. **The review arrives** — score, three problems, PDF attached
5. **`yes`** → optimised CV and change report. Open the CV: one page, real numbers, placeholders where facts were missing
6. **`find me work`** → five live projects, each pitch citing a real past project by name
7. **Show the digest message** from that morning — nobody asked for it
8. **Close on the number:** 42 → 73, versus 75 for a hand-written CV of the same person

Step 3 is the one worth rehearsing. It is the least obvious feature and the most defensible.
