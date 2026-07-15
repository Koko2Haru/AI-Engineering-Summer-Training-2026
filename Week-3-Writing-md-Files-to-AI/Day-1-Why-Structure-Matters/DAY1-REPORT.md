# Week 3 — Day 1: Why Structure Matters 📝

> **Theme:** How machines read text — turning an unstructured project description into a
> clean, machine-actionable Markdown document.

---

## 🎯 The Task

Convert an unstructured project description into a clean Markdown document using
headings, lists, tables, and code blocks. But first, I needed a project to describe.

---

## 🕹️ Choosing the Week 3 Project

Week 2 gave me **CoinQuest**. Week 3 needed a *new* small project — something an AI
could realistically build from documents alone, since Day 5 tests exactly that.

The idea: a **mini competitive programming site**. You get problems, type code into an
in-browser IDE, run it, and get results or errors back — LeetCode, shrunk down to a
single page. The name: **Coddiction** (*code + addiction*), keeping the naming brand
going after CoinQuest.

### Scoping decisions made before writing anything

| Decision | Choice | Why |
|----------|--------|-----|
| Submission language | JavaScript only | Runs natively in the browser; Python needs Pyodide (huge WASM download, fragile) |
| Code execution | Web Worker | Errors come back as messages instead of crashing the page, and a `terminate()` timeout turns infinite loops into a clean **Time Limit Exceeded** verdict |
| Problem storage | Plain JSON objects | Each problem = title, difficulty, statement, signature, visible + hidden test cases — easy to judge, easy for an AI to generate |
| Problem source | Hand-written + AI-generated | Researched the Codeforces API and LeetCode's unofficial GraphQL endpoint — both expose metadata/statements at most, **never hidden test cases** (those *are* the judge). AI generation fits the project theme better anyway |
| Architecture | Single HTML file | No server, no accounts, no build step — a 30-second test loop for Day 5 |

---

## ✍️ The Actual Exercise: Messy → Structured

**Step 1 — the messy version.** I brain-dumped the project description the way ideas
actually arrive: unordered, half-decided, features mixed with vibes, typos included.
Ambiguities were left in on purpose (e.g. does the *user* pick the question count, or
the AI?) — real client descriptions always have them.

**Step 2 — the structured version.** The same content converted into clean Markdown
with every element the task asked for:

- **Headings** — Overview, Goals, Core Features, Behavior Rules, Constraints, Out of Scope, Success Criteria
- **Lists** — goals, behavior rules, constraints
- **Table** — the nine v1.0 core features
- **Code block** — the problem JSON format (which will become the backbone of Day 3's `spec.md` and the target format for the AI question generator)

The point of the exercise became obvious in the diff: the messy version needs a human
to *interpret* it; the structured version can be *executed* — by a person or a model.

---

## 📦 Deliverables

| File | Description |
|------|-------------|
| [`project-brief-messy.txt`](Project-Documents/project-brief-messy.txt) | The raw, unstructured project description — the "before" |
| [`PROJECT-BRIEF-STRUCTURED.md`](Project-Documents/PROJECT-BRIEF-STRUCTURED.md) | The clean Markdown conversion — the "after" |

---

## 🔜 Next Up — Day 2: Context Engineering

Build `CONTEXT.md`: everything an AI needs *besides* the task itself — tech
constraints with their reasons, definitions, scope boundaries. Half of it already
exists in today's scoping table.