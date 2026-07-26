# Week 4 — Using and Building Claude Skills 🧩🤖

> **Instructor:** Abdullah Barghash
> **Theme:** the Claude Skill model, end to end — reading what a skill is, running
> other people's skills until they break, learning the `SKILL.md` template shape,
> building one from scratch and verifying it actually works, then chaining a second
> skill onto it and proving the pipeline holds together under a real, adversarial test.

**AI Engineering Summer Training 2026**
Student: **Ali** ([koko2haru](https://github.com/Koko2Haru))

---

## 🎯 The Week's Project: A Resume Intelligence Suite

Every day built toward the same destination: a two-skill **CV Reviewer → CV Optimizer**
pipeline. `cv-reviewer` (Day 4) scores and diagnoses a resume across 7 weighted
categories without ever rewriting it; `cv-optimizer` (Day 5) takes that diagnosis
plus the original CV and produces a truthful, strengthened rewrite — asking targeted
clarifying questions instead of inventing facts wherever the source document runs out
of information. Day 5 closed the week by running that exact chain, live, against a
fictional resume engineered to need every kind of fix the skills were built to catch.

---

## 🗓️ Day by Day

| Day | Focus | Deliverables | Report |
|---|---|---|---|
| 1 | What is a skill | [`SKILLS.md`](Day-1-What-is-a-skill/Skills-in-Claude/SKILLS.md) — 4-skill engineering reference (triggers, decision trees, I/O, Mermaid diagrams) | [Day 1](Day-1-What-is-a-skill/DAY1-REPORT.md) |
| 2 | Using existing skills | Real runs of `product-manager-toolkit`, `experiment-designer`, `md-slides` against personal CoinQuest data — see [`Executing-Claude-Skills/`](Day-2-Using-Existing-Skills/Executing-Claude-Skills) | [Day 2](Day-2-Using-Existing-Skills/DAY2-REPORT.md) |
| 3 | The `SKILL.md` structure | [`Structure-Template/`](Day-3-The-SKILL-md-Structure/Structure-Template) — generic, annotated first-draft skill template | [Day 3](Day-3-The-SKILL-md-Structure/DAY3-REPORT.md) |
| 4 | Build your own skill | [`cv-reviewer/`](Day-4-Build-Your-Own-Skill/cv-reviewer) — full working CV-review skill, verified end-to-end | [Day 4](Day-4-Build-Your-Own-Skill/DAY4-REPORT.md) |
| 5 | Test & chain skills | [`cv-optimizer/`](Day-5-Test-and-Chain-Skills/cv-optimizer) + a real chain run in [`Testing/`](Day-5-Test-and-Chain-Skills/Testing) | [Day 5](Day-5-Test-and-Chain-Skills/DAY5-REPORT.md) |

---

## 📅 Day 1 — What Is a Skill

**Focus:** the Claude Skill model — what a skill is, when it triggers, why it exists.
**Skills:** progressive disclosure · trigger-type analysis · skill installation.
**Task:** analyze three existing Claude Skills and explain their triggers and purpose.

Learned the core anatomy: a skill is a folder with a `SKILL.md` (frontmatter +
instructions) plus optional `references/`/`scripts/`/`assets/`, loaded in three
progressive-disclosure levels (name+description always → full body on selection →
supporting files only when needed) so context stays cheap. Two invocation modes
(automatic vs. `/skill-name`), and the load-bearing insight of the day: a skill fires
on one of three trigger types — an **object** in the task, an **intent**, or an
**activity/domain**. Went past the three-skill brief: explored repo cloning
(`git sparse-checkout`, `npx giget`), skill licensing (Apache 2.0 vs. source-available
vs. MIT), and ran six skills live (`pdf`, `saas-metrics-coach`,
`product-manager-toolkit`, `experiment-designer`, `caveman`, `md-slides`), producing
a ~1,400-line, four-skill engineering handbook.

📄 **[`SKILLS.md`](Day-1-What-is-a-skill/Skills-in-Claude/SKILLS.md)** — the full
engineering reference (`product-manager-toolkit`, `experiment-designer`, `md-slides`,
`caveman`; 19 sections each + global comparison/architecture chapters).

---

## 📅 Day 2 — Using Existing Skills

**Focus:** running skills against real personal input instead of bundled sample data.
**Skills:** RICE prioritization · A/B sample-size design · Markdown-to-deck rendering.
**Task:** feed personal inputs into the skills surveyed on Day 1 and document how the
outputs actually behave, not just what the `SKILL.md` claims.

Fed all three task-oriented skills a real ask tied to CoinQuest (the Week 2 finance
tracker) instead of a toy input:

| Skill | Real ask | Result |
|---|---|---|
| `product-manager-toolkit` (RICE) | Prioritize 7 CoinQuest v2.0 features | Healing Passive ranked #1; the Reports tool — arguably the app's core value — ranked *last*, exposing RICE's reach-weighted bias at N=1 users |
| `experiment-designer` | Detect a 20% lift in expense-logging frequency from Roast vs. Coach mode | The tool's two-proportion test doesn't fit a single-subject count metric; reframed, cross-checked by hand, and supplemented with an MDE-vs-duration table |
| `md-slides` | Render Day 1's `SKILLS.md` into an HTML deck | Deck built, but slide bodies fell back to raw `<pre>` text — a silently-swallowed missing-sibling-skill import error |

Every skill assumed a conventional multi-user context; CoinQuest has exactly one
user, so every run needed an explicit reframing step *and* surfaced a real bug or
silent limitation that only shows up by executing the tool, not reading about it.

📄 **[`RICE-Prioritization-CoinQuest-v2.md`](Day-2-Using-Existing-Skills/Executing-Claude-Skills/Product-Manager-Toolkit/Output/RICE-Prioritization-CoinQuest-v2.md)** ·
**[`experiment-design-roast-vs-coach.md`](Day-2-Using-Existing-Skills/Executing-Claude-Skills/Experiment-Designer/Output/experiment-design-roast-vs-coach.md)** ·
**[`deck-skills-md.html`](Day-2-Using-Existing-Skills/Executing-Claude-Skills/MD-Slides/Output/deck-skills-md.html)** — the three real-input outputs, each paired with a hand-written `reflection-notes.md` in its own folder.

---

## 📅 Day 3 — The `SKILL.md` Structure

**Focus:** skill anatomy as a design/first-draft exercise, done *after* Day 4 once a
plan-order mismatch was caught and corrected (Day 4's fully-built skill had
originally been started under this folder's name).
**Skills:** template design · progressive-disclosure annotation.
**Task:** design the folder structure and write the first version of a `SKILL.md`
for a custom skill — outcome: *an annotated skill template*, not a working skill.

Built a generic, reusable, fill-in-the-blank `SKILL.md` template
(`{{double-brace}}` placeholders) covering every section a real skill needs —
frontmatter, Purpose, Trigger/Non-Trigger conditions, I/O expectations, Workflow,
Edge Cases, Constraints, a File Usage table, Best Practices, Failure Handling —
annotated inline with invisible `<!-- ANNOTATION -->` HTML comments (not a code
fence, deliberately, per the bug found on Day 4 — see below) plus a companion
`ANNOTATIONS.md` walking through the reasoning linearly. Kept intentionally
CV-agnostic, so it teaches the *pattern* rather than one instance of it; three
placeholder folders (`references/`, `scripts/`, `assets/`) each hold only a
`README.md` stub pointing at Day 4's `cv-reviewer/` for what a populated version
looks like.

📄 **[`Structure-Template/SKILL.md`](Day-3-The-SKILL-md-Structure/Structure-Template/SKILL.md)** —
the annotated template.
📄 **[`Structure-Template/ANNOTATIONS.md`](Day-3-The-SKILL-md-Structure/Structure-Template/ANNOTATIONS.md)** —
the linear skill-anatomy walkthrough.

---

## 📅 Day 4 — Build Your Own Skill

**Focus:** authoring a complete, production-quality Claude Skill from scratch and
*verifying* it performs the intended task — not reading or running someone else's.
**Skills:** skill authoring · rubric design · Python scripting · rendering-bug diagnosis.
**Task:** implement a custom Claude Skill and verify it performs its intended task
successfully.

Built `cv-reviewer` — a resume-review skill that scores a CV across 7 weighted
categories (ATS Compatibility, Content Quality, Impact, Grammar & Spelling,
Readability, Visual/Layout, Professionalism), each backed by a rubric in
`references/scoring-rubric.md`, plus ~20 deep-dive analyses (weak/strong bullets,
keyword coverage, action-verb variety, quantification rate) and a recruiter/hiring-
manager perspective layer. Three Python scripts (`extract_text.py`, `helpers.py`,
`review_cv.py`) form a real, runnable mechanical layer — stdlib-only, with
categories that genuinely need human judgment (Content Quality, Grammar,
Readability, Visual/Layout) explicitly marked `requires_manual_review` instead of a
faked number. Every script was actually run against a sample resume, not just
written.

A real bug was found and fixed **after** initial delivery: `assets/report-example.md`
wrapped its worked example in a code fence meant only to mark it as sample content —
but nothing told the model that was a documentation convention, so the fence was
fully plausible to copy into a real report, flattening every table into literal
`| pipe | text |`. Fixed by removing the fence from both asset files, demoting their
internal heading levels, and adding an explicit rendering rule to `SKILL.md` — a
defect only catchable by inspecting *rendered* output, not the Markdown source.

📄 **[`cv-reviewer/SKILL.md`](Day-4-Build-Your-Own-Skill/cv-reviewer/SKILL.md)** —
the full skill specification.
📄 **[`cv-reviewer/assets/report-example.md`](Day-4-Build-Your-Own-Skill/cv-reviewer/assets/report-example.md)** —
the calibration example central to the code-fence bug and its fix.

---

## 📅 Day 5 — Test & Chain Skills

**Focus:** building a second skill designed to consume the first one's output, then
proving the two-skill pipeline actually works end-to-end.
**Skills:** multi-skill chain design · clarification-protocol design · reliability testing.
**Task:** chain two skills together to complete a multi-step workflow; test and
improve reliability through peer review.

Built `cv-optimizer` — the missing other half of `cv-reviewer`: it consumes a CV
plus (optionally) a review and rewrites the resume, governed by one hard rule —
*rewriting changes expression, never adds a fact*. Employers, metrics, skills,
and degrees the source never stated may never be invented; genuine gaps get either
a targeted clarifying question or a visible bracketed placeholder, never a guess.
5 references, 5 stdlib-only scripts, and 5 assets (including a pre-delivery QA
checklist built specifically to catch fabrication before it ships) round out the
skill.

Then the chain was actually run, not just described: a fictional, deliberately-flawed
resume (`Testing/Input/sample_cv.md`) went through `cv-reviewer` for a full 7-category
review (46/100, "Weak" — a non-standard section header risking an entire job being
dropped by ATS parsing, zero quantification anywhere, a silent employment gap), then
through `cv-optimizer`, which triggered **two real rounds of clarifying questions**
before rewriting anything. Every number in the final resume — a 35% API-latency
improvement, a ~2-million-record migration, team sizes, an honest gap explanation —
is exactly what was confirmed, nothing rounded up or assumed. Along the way, three
real reliability issues surfaced and were documented rather than smoothed over: a
clarification-tool design flaw (fixed-option answers didn't reliably carry free-text
numbers back into the workflow), a bullet-flagging regex blind spot on indented
continuation lines, and a caught-in-time "led" vs. "contributed to" ownership-
inflation near-miss in a draft summary.

📄 **[`cv-optimizer/SKILL.md`](Day-5-Test-and-Chain-Skills/cv-optimizer/SKILL.md)** —
the second skill's specification.
📄 **[`Testing/Output/review-report.md`](Day-5-Test-and-Chain-Skills/Testing/Output/review-report.md)**,
**[`optimized-cv.md`](Day-5-Test-and-Chain-Skills/Testing/Output/optimized-cv.md)**,
**[`optimization-report.md`](Day-5-Test-and-Chain-Skills/Testing/Output/optimization-report.md)** —
the real, live output of the two-skill chain, clarification transcript included.

---

## 🧵 The Through-Line

Each day fed the next, and the arc is the actual point of the week:

- **Day 1's** trigger-type framework and progressive-disclosure model → the vocabulary
  used to design and critique every skill built afterward.
- **Day 2's** live runs → firsthand proof that a `SKILL.md` tells you what a skill
  *claims*, and only running it against real input tells you what it *actually does*
  and where the seams are.
- **Day 3's** annotated template → the reusable shape every subsequent skill's
  `SKILL.md` was built from — deliberately generic, so it could father two very
  different skills without modification.
- **Day 4's** `cv-reviewer` → a fully verified, single skill that established the
  "never fabricate, always cite evidence" discipline `cv-optimizer` would later have
  to inherit and extend.
- **Day 5's** `cv-optimizer` + real chain run → the same discipline stress-tested
  under the hardest condition of the week: a live clarification exchange where the
  temptation to guess a number or inflate a verb was real, and caught.

**Recurring lesson across all five days:** reading about a skill and running one are
different activities that teach different things — every day that included an actual
execution (Day 2, Day 4, Day 5) surfaced a real bug or near-miss that reading alone
never would have.

---

## 📂 Structure

```
Week-4-Using-and-Building-Claude-Skills/
├── WEEK4-README.md
├── Day-1-What-is-a-skill/
│   ├── DAY1-REPORT.md
│   └── Skills-in-Claude/
│       └── SKILLS.md
├── Day-2-Using-Existing-Skills/
│   ├── DAY2-REPORT.md
│   └── Executing-Claude-Skills/
│       ├── Product-Manager-Toolkit/   (reflection-notes.md + Output/)
│       ├── Experiment-Designer/       (reflection-notes.md + Output/)
│       └── MD-Slides/                 (reflection-notes.md + Output/)
├── Day-3-The-SKILL-md-Structure/
│   ├── DAY3-REPORT.md
│   └── Structure-Template/
│       ├── SKILL.md
│       ├── ANNOTATIONS.md
│       └── references/ · scripts/ · assets/   (README stubs)
├── Day-4-Build-Your-Own-Skill/
│   ├── DAY4-REPORT.md
│   └── cv-reviewer/
│       ├── SKILL.md
│       ├── references/    (5 files)
│       ├── scripts/        (3 files)
│       └── assets/         (3 files)
└── Day-5-Test-and-Chain-Skills/
    ├── DAY5-REPORT.md
    ├── cv-optimizer/
    │   ├── SKILL.md
    │   ├── references/    (7 files)
    │   ├── scripts/        (5 files)
    │   └── assets/         (5 files)
    └── Testing/
        ├── Input/sample_cv.md
        └── Output/         (review-report.md, optimized-cv.md, optimization-report.md)
```

---

*Part of [AI-Engineering-Summer-Training-2026](https://github.com/koko2haru/AI-Engineering-Summer-Training-2026).*
