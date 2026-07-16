# CONTEXT.md — Coddiction

> **Purpose of this document:** everything an AI model needs to know *around* the task
> before touching it. This is not the task itself — the task lives in [`SPEC.md`](/Week-3-Writing-md-Files-to-AI/Day-3-Writing-Clear-Specs/Specifications/SPEC.md). Read
> this first, then the spec.

---

## 1. What This Project Is

**Coddiction** (*code + addiction*) is a single-page, browser-only mini competitive
programming site. A player opens one HTML file, gets a timed session of coding
problems, solves them in a built-in editor, and receives instant verdicts. It is a
personal training project, not a commercial product.

**Reference point:** think LeetCode/Codeforces, shrunk to one file and gamified.

## 2. Who It's For

- **Player:** one person, on a desktop browser, wanting a quick "one more problem" grind session. No accounts, no data saved between sessions.
- **Developer audience for the code:** a beginner-to-intermediate programmer must be able to read and understand the source. Prefer clear code over clever code.

## 3. Hard Technical Constraints (non-negotiable)

| Constraint | Reason |
|-----------|--------|
| One single `.html` file — HTML, CSS, and JS all inline | Zero-setup: double-click to run; makes testing and sharing trivial |
| No external libraries, no CDN imports | The file must work offline; a plain `<textarea>` is the code editor |
| No backend, no database, no accounts, no build step | Browser-only by design |
| Submissions are **JavaScript only** | JS executes natively in the browser; Python would require Pyodide (large WASM download, fragile) |
| User code runs inside a **Web Worker**, never `eval` on the main thread | Errors return as messages instead of crashing the page; the Worker can be `terminate()`d on timeout so an infinite loop becomes a "Time Limit Exceeded" verdict, never a frozen tab |
| Site must function with **no AI connection** | Ships with built-in problems; AI generation is an add-on, not a dependency |

## 4. Domain Vocabulary

| Term | Meaning here |
|------|--------------|
| **Problem** | One coding challenge: statement + function signature + test cases |
| **Visible tests** | Example test cases shown to the player; used by the *Run* button |
| **Hidden tests** | Unseen test cases; *Submit* runs visible + hidden together |
| **Verdict** | Result of a submission: `Accepted`, `Wrong Answer`, `Runtime Error`, `Time Limit Exceeded` |
| **Session** | One timed playthrough: start screen → problems → ending screen |
| **Difficulty names** | Themed, matching the addiction concept: `gateway` = easy, `habit` = medium, `dependency` = hard |

## 5. Data Format

Every problem — built-in or AI-generated — is a JSON object with this exact shape:

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

- The player's code must define `solve(...)`; the judge calls it with each test's `input` (spread as arguments) and deep-compares the return value to `expected`.
- This format is also the **target output format** for the AI problem generator — a generated problem is valid only if it parses into this shape.

## 6. Design Decisions Already Made (do not revisit)

- **Why not import problems from Codeforces/LeetCode:** their APIs expose metadata or statements at most — never hidden test cases, because hidden tests *are* the judge. Scraping is also a ToS gray zone. Decision: a small hand-written problem set ships built-in; additional problems are AI-generated in the JSON format above.
- **Why themed difficulty names:** the brand is "addiction"; the UI leans into it (dopamine-hit `Accepted` screen, "one more problem" flow, score, ending rank/title).
- **Timer is per-session, not per-problem.** Pressure comes from one countdown over the whole set.

## 7. Tone & Visual Direction

- Playful, arcade-like, meme-adjacent — a game first, a tool second.
- Big, unmissable verdicts: `Accepted` should feel like a win (green, loud); `Wrong Answer` shows *expected vs actual* so failure teaches.
- Dark, code-editor-style aesthetic fits the theme; exact palette is the builder's choice.

## 8. Out of Scope for v1.0

Syntax highlighting, sounds/BGM, themes/dark-mode toggle, Codeforces import,
multiplayer, leaderboards, persistence between sessions, languages other than
JavaScript. Do **not** add any of these unless the spec says so.

## 9. Related Documents

| File | Role |
|------|------|
| [`PROJECT-BRIEF-STRUCTURED.md`](/Week-3-Writing-md-Files-to-AI/Day-1-Why-Structure-Matters/Project-Documents/PROJECT-BRIEF-STRUCTURED.md) | What the project is (Day 1) |
| [`CONTEXT.md`](#) | This file — background, constraints, decisions (Day 2) |
| [`SPEC.md`](/Week-3-Writing-md-Files-to-AI/Day-3-Writing-Clear-Specs/Specifications/SPEC.md) | The exact build instructions: objectives, inputs, outputs, acceptance criteria (Day 3) |
| [`README.md`](/Week-3-Writing-md-Files-to-AI/Day-4-System-Prompts-&-Documentations/Prompt-&-Documentation/README.md) + [system prompt](/Week-3-Writing-md-Files-to-AI/Day-4-System-Prompts-&-Documentations/Prompt-&-Documentation/system-prompt.txt) | Human onboarding + AI operating instructions (Day 4) |