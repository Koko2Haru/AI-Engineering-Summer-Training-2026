# Week 3 — Writing .md Files for AI 📝🤖

> **Instructor:** Abdullah Barghash
> **Theme:** documentation as an engineering interface — writing Markdown documents
> precise enough that an AI can build working software from them alone.

---

## 🎮 The Week's Project: Coddiction

**Coddiction** (*code + addiction*) — a mini competitive programming game in a single
HTML file: timed sessions, an in-browser editor, JavaScript submissions judged in a
Web Worker with real verdicts (`Accepted` / `Wrong Answer` / `Runtime Error` /
`Time Limit Exceeded`), scoring, and an ending screen with a rank.

The twist: **no game code was written by hand.** The game was specified entirely in
documents across Days 1–4, then built by an AI from those documents on Day 5 — and
debugged by fixing the *documents*, not the output.

## 🗓️ Day by Day

| Day | Focus | Deliverables | Report |
|-----|-------|--------------|--------|
| 1 | Why structure matters | Messy brain-dump → structured brief ([`project-brief-messy.txt`](Day-1-Why-Structure-Matters/Project-Documents/project-brief-messy.txt), [`PROJECT-BRIEF-STRUCTURED.md`](Day-1-Why-Structure-Matters/Project-Documents/PROJECT-BRIEF-STRUCTURED.md)) | [Day 1](Day-1-Why-Structure-Matters/DAY1-REPORT.md) |
| 2 | Context engineering | [`CONTEXT.md`](Day-2-Context-Engineering/Context/CONTEXT.md) — constraints with reasons, vocabulary, data contract, settled decisions | [Day 2](Day-2-Context-Engineering/DAY2-REPORT.md) |
| 3 | Writing clear specs | [`SPEC.md`](Day-3-Writing-Clear-Specs/Specifications/SPEC.md) — objectives, judging rules, scoring, 16 pass/fail acceptance criteria | [Day 3](Day-3-Writing-Clear-Specs/DAY3-REPORT.md) |
| 4 | System prompts & docs | [`README.md`](Day-4-System-Prompts-&-Documentations/Prompt-&-Documentation/README.md) for humans, [`system-prompt.txt`](Day-4-System-Prompts-&-Documentations/Prompt-&-Documentation/system-prompt.txt) for the AI (incl. a JSON-only problem generator mode) | [Day 4](Day-4-System-Prompts-&-Documentations/DAY4-REPORT.md) |
| 5 | Test & iterate | [`ITERATION-LOG.md`](Day-5-Test-&-Iterate/Testing/ITERATION-LOG.md) + 3 frozen builds in `Testing/t1–t3/`; final game: [`Testing/t4/coddiction-v4.html`](https://koko2haru.github.io/AI-Engineering-Summer-Training-2026/Week-3-Writing-md-Files-to-AI/Day-5-Test-%26-Iterate/Testing/t4/coddiction-v4.html) | [Day 5](Day-5-Test-&-Iterate/DAY5-REPORT.md) |

## 🔁 The Day-5 Arc in One Table

| Iter | Result | What happened |
|------|--------|---------------|
| 1 | ❌ | Start button dead — `const` reassignment crash |
| 2 | 🟡 | Playable, but duplicate problems in sessions, a broken hidden test rejecting correct solutions, stub missing `{`, repeated error display |
| 3 | 🟡 | Fresh rebuild from the fixed spec — two issues survived anyway |
| 4 | ✅ | Direct prompt + forced executable verification (reference solutions run with node) — accepted |

## 🧠 Key Takeaways

- **Models fill unwritten gaps with the cheapest implementation.** "Problems are drawn from the set" produced duplicates — sampling with replacement violated no written word. The missing phrase was *without repetition*.
- **A judge is only as correct as its test data.** One hidden Two Sum input had two valid answers, so a provably correct solution was judged wrong. Specs must constrain data, not just code.
- **Reading is optional; execution isn't.** "Verify the tests" as prose was ignored twice; demanding a reference solution be *executed with node and the output shown* ended it. Instructions that produce evidence get followed.
- **Specs for requirements, prompts for discipline.** Spec edits fixed every ambiguity failure; model-discipline failures needed direct, verification-demanding prompting.

## 📂 Structure

```
Week-3-Writing-md-Files-to-AI/
├── WEEK3-README.md
├── Day-1-Why-Structure-Matters/
│   ├── DAY1-REPORT.md
│   └── Project-Documents/
├── Day-2-Context-Engineering/
│   ├── DAY2-REPORT.md
│   └── Context/
├── Day-3-Writing-Clear-Specs/
│   ├── DAY3-REPORT.md
│   └── Specifications/
├── Day-4-System-Prompts-&-Documentations/
│   ├── DAY4-REPORT.md
│   └── Prompt-&-Documentation/
└── Day-5-Test-&-Iterate/
    ├── DAY5-REPORT.md
    ├── ITERATION-LOG.md
    ├── screenshots/
    └── Testing/
        ├── t1/ … t4/   (one frozen build per iteration **Except t4**)
```