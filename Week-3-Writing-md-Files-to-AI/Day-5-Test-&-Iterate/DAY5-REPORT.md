# Week 3 — Day 5: Test & Iterate 🧪

> **Theme:** test whether the AI follows your spec; remove ambiguity; finalize.

---

## 🎯 The Task

Test the specification with an AI model and revise the documents until the AI
consistently produces the expected result.

---

## 🔁 The Protocol

Fresh AI session per rebuild, given exactly three inputs — [`system-prompt.txt`](/Week-3-Writing-md-Files-to-AI/Day-4-System-Prompts-&-Documentations/Prompt-&-Documentation/system-prompt.txt),
[`CONTEXT.md`](/Week-3-Writing-md-Files-to-AI/Day-2-Context-Engineering/Context/CONTEXT.md), [`SPEC.md`](/Week-3-Writing-md-Files-to-AI/Day-3-Writing-Clear-Specs/Specifications/SPEC.md) — plus a kickoff message forbidding questions ("every question
it would've asked is a hole in the spec") and locking it inside the Day-5 working
directory. Each output was scored against SPEC.md §9's acceptance checklist, every
failure was diagnosed into one of three categories, and the *matching* thing got fixed:

- **(a)** spec ambiguous/silent → edit **`SPEC.md`**
- **(b)** docs clear, model non-compliant → strengthen the instruction
- **(c)** plain bug → feed the error back

Versions were frozen per iteration in **`Testing/t1/` … `Testing/t3/`** — broken builds
are evidence, not garbage.

## 📉 → 📈 The Four Iterations

| Iter | Result | Key event |
|------|--------|-----------|
| 1 | ❌ blocked | Start button dead — console revealed a `const` reassignment crash inside `selectRandomProblems()` |
| 2 | 🟡 playable | 4 issues: stub missing `{`, **duplicate problems in sessions**, a correct Two Sum solution judged Wrong Answer, syntax errors repeated per test — 3 of 4 were spec gaps |
| 3 | 🟡 recurrence | Fresh rebuild from the fixed spec: stub brace and bad hidden test **survived** — upgraded to model-discipline failures |
| 4 | ✅ accepted | Direct prompt demanding fixes + **executable verification** (reference solution run with node against every test, output shown) — both issues died |

**The confirmed smoking gun:** hidden test `{ input: [[10,20,30,40], 50], expected: [0,3] }`
— but 20+30 also equals 50, so `[1,2]` is equally correct. A provably correct solution
was being rejected by a provably broken test.

## 🧠 What the Log Proves

1. **Models fill unwritten gaps with the cheapest implementation** — "problems are
   drawn from the set" produced sampling with replacement without violating a single
   written word.
2. **A judge is only as correct as its test data** — acceptance criteria must
   constrain the data, not just the code.
3. **Reading is optional; execution isn't** — prose rules got skimmed across a fresh
   rebuild; the failure only died when the instruction forced evidence (run it with
   node, show the output).
4. **Specs for requirements, prompts for discipline** — spec edits cured every
   category-(a) failure; category-(b) failures needed direct, verification-demanding
   prompting.

## 📦 Deliverables

| File | Description |
|------|-------------|
| [`ITERATION-LOG.md`](./Testing/ITERATION-LOG.md) | Full test record: per-iteration scores, notes, screenshots, diagnoses, doc changes, final findings |
| [`Testing/t1/`–`t3/`](Testing/) | Frozen build per iteration — **`coddiction-v1.html`** (crash) through **`coddiction-v3.html`** (accepted) |
| [`Testing/t4/coddiction-v4.html`](./Testing/t4/coddiction-v4.html) | The final build: playable sessions, working verdicts, TLE-safe judging, verified test data |

---

## 🏁 Week 3 complete

Five days, one game, zero hand-written game code: **Coddiction was built entirely
through documents** — a brief, a context file, a spec, a README, and a system prompt —
then debugged by editing those documents and the prompts around them.