# Week 3 — Day 3: Writing Clear Specs 📐

> **Theme:** turning a vague task into a precise .md instruction file.

---

## 🎯 The Task

Write a complete specification ([`SPEC.md`](./Specifications/SPEC.md)) for an AI coding task using clear
objectives, constraints, inputs, and outputs.

---

## 🔨 From Vague to Precise

The brief said things like "there's a timer" and "you get a score." A spec can't —
every vague phrase had to be forced into a number or a rule an AI can't misread:

| Vague (brief) | Precise (SPEC.md) |
|---------------|-------------------|
| "there's a timer" | Session timer = 5 min × problem count; at 00:00 the ending screen interrupts immediately |
| "you get points" | `gateway` 100 · `habit` 250 · `dependency` 500, awarded once, on Accepted only |
| "AI decides how many questions" | Player picks 3/4/5/6 on the start screen from a built-in set of 6 (2 per difficulty) |
| "shows the error" | Verdict priority: Runtime Error → TLE → Wrong Answer → Accepted, with exact display rules per verdict |
| "shouldn't freeze on infinite loops" | Per-execution Web Worker, `terminate()` at 3000 ms → Time Limit Exceeded |
| "ending screen with how many u solved" | "You solved X / N" + score + rank title by ratio: Clean / Casual User / Hooked / Fully Addicted |

## ⚖️ The Biggest Spec Decision

**AI problem generation was moved out of the HTML file.** A live "generate" button
would need an internet connection, an exposed API key, and would make every session
different — killing repeatable testing. Instead, generation is a separate workflow: a
prompt produces problem JSON in the exact format from [`CONTEXT.md`](../Day-2-Context-Engineering/Context/CONTEXT.md) §5, which gets
pasted into the built-in array. The feature survives; the file stays offline,
keyless, and deterministic. (And a generated problem is itself a spec-following test —
it's only valid if the AI matched the JSON format exactly.)

## ✅ Acceptance Criteria = The Day 5 Test Protocol

The spec ends with **14 pass/fail checkboxes** — open with no console errors, wrong
answers show expected-vs-actual, `while(true){}` yields TLE within ~3 s with the page
still responsive, Play-again fully resets state, no external imports, and so on.
"The model reliably follows the spec" stops being a feeling and becomes a number:
**14/14, more than once in a row.**

---

## 📦 Deliverable

| File | Description |
|------|-------------|
| [`SPEC.md`](Specifications/SPEC.md) | Complete build specification: objective, deliverable, data formats, screens & flow, judging rules, scoring, non-functional requirements, out-of-scope, 14 acceptance criteria |

---

## 🔜 Next Up — Day 4: System Prompts & Docs

Two documents for two audiences: a [`README.md`](../Day-4-System-Prompts-&-Documentations/DAY4-REPORT.md) a *human* can onboard from, and a
system prompt an *AI* can operate under — including the problem-generator prompt.