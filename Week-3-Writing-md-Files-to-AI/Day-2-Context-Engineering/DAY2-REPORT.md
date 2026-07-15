# Week 3 — Day 2: Context Engineering 🧠

> **Theme:** giving the model the right info, in the right order — before it ever sees
> the task.

---

## 🎯 The Task

Build a context document that provides an AI model with all the information needed to
complete a software task accurately.

---

## 🧩 What Context Engineering Meant Here

Yesterday's brief says *what* Coddiction is. But an AI asked to build it would still
have to guess a hundred things — which library to use, whether to add a backend, what
"difficulty" means, whether infinite loops matter. Every guess is a place where the
output drifts from what I want.

`CONTEXT.md` exists to remove the guessing. It deliberately contains **zero build
instructions** — those belong to Day 3's `spec.md`. Instead it carries everything
*around* the task:

| Section | What it prevents |
|---------|------------------|
| Hard constraints **with reasons** | The model "helpfully" adding CodeMirror, a backend, or Python support — the *why* is what makes a constraint stick |
| Domain vocabulary | Ambiguity — "verdict", "session", "hidden tests", and the themed difficulty names (`gateway`/`habit`/`dependency`) mean exactly one thing |
| The problem JSON format | Format drift — it's the shared data contract between the judge, the built-in problems, and the AI question generator |
| Decisions already made | The model relitigating settled questions (e.g. why problems aren't imported from Codeforces: their APIs never expose hidden test cases — hidden tests *are* the judge) |
| Explicit out-of-scope list | Feature creep — "do not add unless the spec says so" |
| Tone & visual direction | A generic corporate UI on a project whose whole brand is an arcade dopamine loop |

## 📐 The "Right Order" Part

The sections are sequenced so a model reading top-to-bottom always has the
prerequisites for the current section already loaded:

**identity → audience → constraints → vocabulary → data format → past decisions →
style → scope → related docs**

By the time the JSON format appears, the reader already knows why it's JS-only and
what a hidden test is. Context isn't just *what* you say — it's *when* you say it.

---

## 📦 Deliverable

| File | Description |
|------|-------------|
| [`CONTEXT.md`](Context/CONTEXT.md) | The structured context document for Coddiction — constraints, vocabulary, data contract, settled decisions, scope |

---

## 🔜 Next Up — Day 3: Writing Clear Specs

`spec.md` sits on top of this context and says only *what to build and how to verify
it*: objectives, inputs, outputs, and acceptance criteria written as literally
checkable statements.