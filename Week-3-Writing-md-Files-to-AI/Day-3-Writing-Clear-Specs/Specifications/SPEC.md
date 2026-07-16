# SPEC.md — Coddiction v1.0

> **This is the build instruction.** Read `CONTEXT.md` first for constraints,
> vocabulary, and decisions already made. This document says exactly what to build and
> how to verify it. Anything not specified here or in `CONTEXT.md` is left to the
> builder's judgment — but nothing in the *Out of Scope* list may be added.

---

## 1. Objective

Build **Coddiction**: a single-file, browser-only mini competitive programming game.
The player plays one timed session of JavaScript coding problems in a built-in editor
and receives an instant verdict per submission, ending with a results screen.

## 2. Deliverable

- Exactly **one file**: `coddiction.html`
- Contains all HTML, CSS, and JavaScript inline
- Opens and fully works by double-clicking in a modern desktop browser (Chrome/Edge/Firefox), offline, with no console errors on load

## 3. Inputs & Data

### 3.1 Built-in problem set

The file ships with **6 problems** hardcoded as an array of JSON objects in the format
below (defined in `CONTEXT.md` §5): **2 × `gateway`, 2 × `habit`, 2 × `dependency`**.

```json
{
  "id": "two-sum",
  "title": "Two Sum",
  "difficulty": "habit",
  "statement": "Given an array of numbers and a target...",
  "signature": "function solve(nums, target)",
  "visibleTests": [{ "input": [[2, 7, 11], 9], "expected": [0, 1] }],
  "hiddenTests": [{ "input": [[3, 3], 6], "expected": [0, 1] }]
}
```

Each problem must have ≥ 2 visible tests and ≥ 3 hidden tests. Problem topics are the
builder's choice (arrays, strings, math — classic CP staples), but statements must be
original wording.

### 3.2 Player input

- JavaScript source code typed into the editor. The code must define a function named
  `solve` matching the problem's `signature`.
- UI interactions: selecting session length, pressing **Run**, **Submit**, **Skip**,
  and **Play again**.

## 4. Screens & Flow

### 4.1 Start screen
- Shows the game name **Coddiction**, a one-line tagline, and a **session length picker**: 3, 4, 5, or 6 problems.
- A **Start** button begins the session: the chosen number of problems is drawn from the built-in set (mixed difficulties, hardest last), and the session timer starts.
- Session timer duration = **5 minutes per selected problem** (e.g. 4 problems → 20:00).

### 4.2 Problem screen (the main screen)
Layout: problem panel + editor panel, both visible at once on desktop.

**Problem panel shows:** title, difficulty badge (`gateway` green / `habit` orange / `dependency` red), statement, the required `signature`, and the visible tests rendered as *input → expected*.

**Editor panel shows:**
- A monospace `<textarea>` pre-filled with the problem's signature as a stub:
  ```js
  function solve(nums, target) {
    // your code
  }
  ```
- **Run** button — executes against **visible tests only**; results appear per test: pass/fail, and on fail: input, expected, actual (or the error message).
- **Submit** button — executes against **all tests** (visible + hidden) and produces a single verdict (see §5). Hidden test inputs/expected values are **never displayed**, only their pass/fail count.
- **Skip** button — moves to the next problem, scoring 0 for this one. A skipped problem does not return.

**Persistent HUD (always visible):** session timer counting down (mm:ss), current score, progress (`problem 2 / 4`).

### 4.3 Ending screen
Triggers when (a) all problems are answered/skipped, or (b) the timer hits 0 — whichever comes first. Timer expiry interrupts immediately.

Shows:
- Solved count: **"You solved X / N"**
- Final score
- A rank title based on solve ratio: 0 solved → `Clean` · under half → `Casual User` · half or more → `Hooked` · all → `Fully Addicted`
- A **Play again** button returning to the start screen with all state reset.

## 5. Judging Rules

- User code runs in a **Web Worker** created per execution. Never `eval` on the main thread.
- For each test, the judge calls `solve(...input)` (input array spread as arguments) and **deep-compares** the return value with `expected` (arrays/objects compared by value, not reference).
- **Timeout:** any single execution exceeding **3000 ms** is terminated (`worker.terminate()`) and treated as Time Limit Exceeded.
- Verdict priority for Submit:
  1. Code fails to compile / throws before or during any test → **Runtime Error** (show the error message)
  2. Any test exceeds the time limit → **Time Limit Exceeded**
  3. Any test's actual ≠ expected → **Wrong Answer** (show expected vs actual for the first failing *visible* test; hidden failures show only "failed hidden test")
  4. All tests pass → **Accepted** 🎉 — visually loud (big green banner/animation), advances to the next problem after a short delay.
- An `Accepted` on Submit is final for that problem; Run can be used unlimited times with no penalty.

## 6. Scoring

- `gateway` = 100 · `habit` = 250 · `dependency` = 500 points, awarded once per problem on Accepted.
- Skipped, failed-at-timeout, or unreached problems score 0. No negative scores.

## 7. Non-Functional Requirements

- All constraints from `CONTEXT.md` §3 apply (single file, no libraries, no backend, JS-only, offline).
- An infinite loop in player code must never freeze or crash the page.
- Dark, code-editor-style visual theme; playful arcade tone; verdicts must be unmissable.
- The `<textarea>` must support typing Tab as an indent (not focus-jump).

## 8. Out of Scope

Syntax highlighting, sounds, themes/toggles, persistence between sessions, accounts,
leaderboards, multiplayer, non-JS languages, importing problems from external sites,
and live AI problem generation inside the page (the AI generator is a separate
workflow that produces problem JSON to paste into the built-in array).

## 9. Acceptance Criteria (the Day-5 checklist)

Each item is pass/fail:

- [ ] `coddiction.html` opens from disk with no console errors; start screen renders
- [ ] Start screen offers 3/4/5/6 problems; timer starts at 5 min × count
- [ ] Correct `solve` for a problem + **Run** → all visible tests show pass
- [ ] **Run** with wrong output → failing test shows input, expected, and actual
- [ ] **Submit** with fully correct code → **Accepted**, score increases by the difficulty's value, next problem loads
- [ ] **Submit** with code that passes visible but fails a hidden test → **Wrong Answer**, hidden test data not revealed
- [ ] Code that throws (e.g. `undefined.x`) → **Runtime Error** with the error message shown
- [ ] `while(true){}` submitted → **Time Limit Exceeded** within ~3 s; page stays responsive
- [ ] **Skip** advances without score; skipped problem never reappears
- [ ] HUD timer counts down every second; at 00:00 the ending screen appears immediately
- [ ] Ending screen shows correct solved count, score, and the correct rank title for the ratio
- [ ] **Play again** returns to start with timer, score, and progress fully reset
- [ ] Tab key indents inside the editor
- [ ] The file contains no external `<script>`/`<link>` imports