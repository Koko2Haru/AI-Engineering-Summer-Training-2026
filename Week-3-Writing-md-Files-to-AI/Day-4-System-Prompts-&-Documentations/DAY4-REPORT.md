# Week 3 — Day 4: System Prompts & Docs 📄🤖

> **Theme:** writing READMEs and instructions an AI can actually act on — same
> project, two very different readers.

---

## 🎯 The Task

Create a professional README and write a system prompt that allows an AI assistant to
understand and continue the project correctly.

---

## 👤 vs 🤖 — Two Documents, Two Audiences

The core lesson of the day is the contrast:

| | [`README.md`](./Prompt-&-Documentation/README.md) | [`system-prompt.txt`](./Prompt-&-Documentation/system-prompt.txt) |
|---|-------------|---------------------|
| Reader | A human who just found the repo | An AI joining the project |
| Job | **Inform** — explain so a person understands | **Constrain** — set rules so a model complies |
| Content | What it is, how to run (download + double-click), how to play, how to add problems, how judging works, which doc to read for what | Reading order, hard rules, working style, output rules |
| Handles gaps | A human fills gaps with common sense | A model fills gaps with guesses — so gaps get closed with rules |

The README was written as if Coddiction lives in its own standalone repo: no mention
of the training program — a stranger should just see a small open-source game.

## 🔒 What Went Into the System Prompt

- **Reading order:** CONTEXT.md → SPEC.md, and SPEC.md wins on conflict.
- **Hard rules:** one inline HTML file, no CDN/libraries, no backend, Web Worker
  execution with a 3 s kill, no out-of-scope features even if asked casually.
- **File safety:** all project documents are read-only for the AI — it may only
  create/modify **`coddiction-v(x).html`** in a designated working directory. If it believes a
  document is wrong, it must say so and stop; humans update documents, not the AI.
  (The docs shape the code — never the reverse.)
- **Working style:** complete file output (never diffs), beginner-readable code,
  self-check against SPEC.md's 14 acceptance criteria, ask instead of silently
  guessing.
- **Problem generation mode:** the AI question generator from the original idea lives
  here — output *only* a JSON object in the exact problem format, ≥2 visible and ≥3
  hidden tests, at least one edge case, mentally solve every test before emitting it,
  original statements only, difficulty definitions per tier.

## 📦 Deliverables

| File | Description |
|------|-------------|
| [`README.md`](Prompt-&-Documentation/README.md) | Standalone-repo-style README for Coddiction — run, play, extend, judge internals, doc map |
| [`system-prompt.txt`](Prompt-&-Documentation/system-prompt.txt) | Operating instructions for an AI continuing the project, incl. the problem generator mode |

---

## 🔜 Next Up — Day 5: Test & Iterate

Fresh AI session, feed it `system-prompt.txt` + `CONTEXT.md` + `SPEC.md`, get
**`coddiction-v(x).html`**, score it against the 14 acceptance criteria, fix the **documents**
(never the output), repeat until it passes reliably.