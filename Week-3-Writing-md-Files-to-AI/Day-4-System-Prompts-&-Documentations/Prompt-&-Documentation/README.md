# 🎮 Coddiction

> **code + addiction.** A mini competitive programming game in a single HTML file —
> no server, no accounts, no install. Open it, beat the timer, get hooked.

---

## What is this?

Coddiction is a browser-only, LeetCode-style coding game. You pick a session length,
get a set of JavaScript problems, solve them in the built-in editor against one
countdown timer, and receive an instant verdict for every submission — `Accepted`,
`Wrong Answer`, `Runtime Error`, or `Time Limit Exceeded`. When the timer dies (or you
finish), an ending screen shows your score and your rank.

## 🚀 Run it

1. Download `coddiction.html`
2. Double-click it

That's the whole installation. Works offline in any modern desktop browser.

## 🕹️ How to play

1. **Start screen** — pick how many problems you want (3–6). Your session timer is 5 minutes per problem.
2. **Solve** — read the problem, write a `solve()` function in the editor.
   - **Run** tests your code against the *visible* examples and shows you exactly what failed.
   - **Submit** runs *all* tests, including hidden ones, and gives the final verdict.
   - **Skip** if you're stuck — no points, no coming back.
3. **Ending screen** — solved count, final score, and your rank:

| Solve ratio | Rank |
|-------------|------|
| 0 | Clean |
| under half | Casual User |
| half or more | Hooked |
| all | Fully Addicted |

**Difficulties** follow the theme: 🟢 `gateway` (100 pts) → 🟠 `habit` (250 pts) → 🔴 `dependency` (500 pts).

## ➕ Adding problems

Every problem is a JSON object in the built-in array inside `coddiction.html`:

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

Write one by hand, or have an AI generate one for you: the generator prompt lives in
`system-prompt.txt` — paste it into any LLM chat and you get back a ready-to-paste
problem in this exact format.

## ⚙️ How judging works

Your code never runs on the page itself. Each execution spins up a **Web Worker**,
calls `solve(...)` with the test's input, and deep-compares the return value with the
expected output. If your code throws, you get the error back as a `Runtime Error`. If
it runs longer than **3 seconds** (hi, `while(true)`), the worker is terminated and
you get `Time Limit Exceeded` — the page never freezes.

## 📂 Project documents

| File | What it's for |
|------|---------------|
| [`coddiction-v(X).html`](/Week-3-Writing-md-Files-to-AI/Day-5-Test-&-Iterate/Testing/) | The game — the only file a player needs |
| [`PROJECT-BRIEF-STRUCTURED.md`](/Week-3-Writing-md-Files-to-AI/Day-1-Why-Structure-Matters/Project-Documents/PROJECT-BRIEF-STRUCTURED.md) | What the project is and why |
| [`CONTEXT.md`](/Week-3-Writing-md-Files-to-AI/Day-2-Context-Engineering/Context/CONTEXT.md) | Constraints, vocabulary, data contract, settled decisions |
| [`SPEC.md`](/Week-3-Writing-md-Files-to-AI/Day-3-Writing-Clear-Specs/Specifications/SPEC.md) | The exact build specification + 14 acceptance criteria |
| [`system-prompt.txt`](/Week-3-Writing-md-Files-to-AI/Day-4-System-Prompts-&-Documentations/Prompt-&-Documentation/system-prompt.txt) | Operating instructions for an AI continuing this project, incl. the problem generator |

Building or modifying the game with an AI assistant? Give it **`system-prompt.txt`**,
**`CONTEXT.md`**, and **`SPEC.md`** — in that order.

## 🔮 Not in v1.0 (maybe v2)

Syntax highlighting · sounds · dark/light themes · saved progress · leaderboards ·
live in-page AI problem generation · importing problems from Codeforces · languages
beyond JavaScript

---

*Built as a documentation-first project: the game is fully specified in Markdown
before a single line of HTML — precise enough that an AI can build it from the docs
alone.*