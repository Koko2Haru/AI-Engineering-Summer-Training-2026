# Week 5 — Agentic AI Fundamentals 🌌🤖

> **Instructor:** Abdullah Barghash
> **Theme:** the agent loop, end to end — what separates an agent from a chatbot,
> wiring up a real tool through function calling, adding a second tool and memory
> that actually changes behavior, decomposing a genuinely complex task, and finally
> breaking the agent on purpose to build and honestly evaluate guardrails against it.

**AI Engineering Summer Training 2026**
Student: **Ali** ([koko2haru](https://github.com/Koko2Haru))

---

## 🎯 The Week's Project: Star Gazer

**Star Gazer** turns a photo collection into a navigable 3D night sky — every photo
is a star, and the user moves freely through the space instead of searching it.

Existing tools already solve *retrieval*: ask for "photos from Taif" and search finds
them. What nothing solves is *rediscovery* — wandering through a collection to find a
memory you can't put into words. And the photos most likely to be lost are exactly
the ones with the least metadata (screenshots, forwards, scans), so the design was
corrected mid-week to have the agent understand each photo visually rather than
depend on EXIF timestamp/GPS, which would fail hardest on exactly those photos.

Every day built one more piece of the same agent: one tool → two tools + memory → a
full multi-step pass over the whole collection → guardrails tested against failures
the project had already hit for real.

---

## 🗓️ Day by Day

| Day | Focus | Deliverables | Report |
|---|---|---|---|
| 1 | Agents vs. chatbots | [`AGENT-DESIGN.md`](Day-1-Agents-vs-Chatbots/Design-Idea/AGENT-DESIGN.md) — full design doc: objective, tools, inputs/outputs, agent/code decision boundary | [Day 1](Day-1-Agents-vs-Chatbots/DAY1-REPORT.md) |
| 2 | Tool use / function calling | [`basic_agent.py`](Day-2-Tool-Use-and-Function-Calling/Basic-Agent/basic_agent.py) — single-tool agent, `describe_photo` via Gemini vision, real ReAct loop | [Day 2](Day-2-Tool-Use-and-Function-Calling/DAY2-REPORT.md) |
| 3 | Adding tools & memory | [`memory_agent.py`](Day-3-Adding-Tools-and-Memory/Memory-Agent/memory_agent.py) — second tool (`propose_constellation`) + persistent `memory.json` | [Day 3](Day-3-Adding-Tools-and-Memory/DAY3-REPORT.md) |
| 4 | Planning & decomposition | [`full_agent.py`](Day-4-Planning-and-Decomposition/Full-Agent/full_agent.py) — full multi-step organize pass over 20 photos, logged turn by turn | [Day 4](Day-4-Planning-and-Decomposition/DAY4-REPORT.md) |
| 5 | Failure modes & guardrails | [`guardrail_agent.py`](Day-5-Failure-Modes-and-Guardrails/Failure-Testing/guardrail_agent.py) — 3 guardrails, tested; 2 held, 1 confirmed incomplete | [Day 5](Day-5-Failure-Modes-and-Guardrails/DAY5-REPORT.md) |

---

## 📅 Day 1 — Agents vs. Chatbots

**Focus:** what actually makes something agentic, designed before any code.
**Task:** design an agent for a real-world scenario — objective, tools, inputs,
outputs, decision process.

The design went through a real correction mid-day: the first draft leaned on EXIF
timestamp and GPS to group photos, which quietly fails on exactly the photos people
actually lose — screenshots, forwards, anything with no metadata attached. Rewritten
so a vision tool describes every photo directly, with metadata only as corroborating
evidence when present. The doc draws an explicit boundary — the agent judges what a
photo is about and which photos share a memory; code owns coordinate math, validation,
and rate limits — that every later day's guardrails hang off of. Also named the
project's central risk up front: real constellations are unrelated stars humans
connected into stories, and an LLM shown unrelated photos will do the same thing
unless stopped.

📄 **[`AGENT-DESIGN.md`](Day-1-Agents-vs-Chatbots/Design-Idea/AGENT-DESIGN.md)** —
objective, tools, inputs/outputs, decision boundary, anticipated failure modes.

---

## 📅 Day 2 — Tool Use / Function Calling

**Focus:** proving a real think → act → observe loop runs, not just gets described.
**Task:** build a simple agent capable of using one external tool.

Wired `describe_photo` to Gemini vision through real function calling — structured
JSON output (subjects, setting, indoor/outdoor, time of day, confidence) rather than
free prose, specifically to keep the model from producing plausible-sounding
narrative it can't back up. Every result cached to disk by file hash. First real run,
against 5 unrelated photos, produced the correct result on the first try: the agent
called the tool the number of times it decided it needed, then explicitly reported
there was no shared theme across the photos rather than inventing one.

📄 **[`Basic-Agent/basic_agent.py`](Day-2-Tool-Use-and-Function-Calling/Basic-Agent/basic_agent.py)** —
the working single-tool agent.

---

## 📅 Day 3 — Adding Tools & Memory

**Focus:** a second tool with real validation, and memory that changes a later
decision — not just recall.
**Task:** extend the agent with memory and a second tool; demonstrate that previous
interactions influence future decisions.

Added `propose_constellation`, validated by code before being accepted — rejecting
duplicate names, groups under 2 photos, and any attempt to touch a user-locked group.
Memory persisted to `memory.json` across runs. The proof ran across two separate
script invocations: told the agent, outside any organizing prompt, that two
unrelated-looking photos (a butterfly, a strawberry) were from the same garden — then
re-ran `organize` with no mention of either in the new prompt. The agent built "My
Garden Wonders," grouping them using that exact reasoning. Also surfaced a real
limitation, reported rather than hidden: with only generic-category overlap available
in the test photos, the agent's other grouping ("The Social Circle") was shallow —
a category, not a memory.

📄 **[`Memory-Agent/memory_agent.py`](Day-3-Adding-Tools-and-Memory/Memory-Agent/memory_agent.py)** —
two-tool agent with persistent memory.

---

## 📅 Day 4 — Planning & Decomposition

**Focus:** a task big enough to force real multi-step planning, fully traced.
**Task:** give the agent a complex task requiring multiple steps; document how it
plans and executes each step.

Expanded to 20 photos with deliberate thematic variety (fruit close-ups, animal
pairs, butterflies, plus the original people-photos) and ran one instruction —
*"organize my whole sky"* — against the entire collection in a single pass, every
turn logged to `trace.log` with timestamps. The richer source material produced
richer results: two constellations (Fruit Still Lifes, Friends of Furry Kind) built
on genuine specific patterns, alongside a repeat of Day 3's shallow-grouping issue
("Friends and Gatherings"). A real rate-limit error hit mid-run when many new,
uncached photos were described at once — resolved by waiting and rerunning, and
carried forward as a live candidate for Day 5's guardrails rather than a one-off
inconvenience.

📄 **[`Full-Agent/trace.log`](Day-4-Planning-and-Decomposition/Full-Agent/trace.log)** —
the full execution trace, the day's core deliverable.

---

## 📅 Day 5 — Failure Modes & Guardrails

**Focus:** breaking the agent on purpose, building a guardrail for each break, and
reporting honestly on which ones actually held.
**Task:** identify three failure scenarios and implement guardrails preventing
incorrect or unsafe behavior.

Built and tested three guardrails against failure modes the project had already
surfaced across Days 3–4, plus one deliberately untested until now:

| Guardrail | Test | Result |
|---|---|---|
| Duplicate / shallow-category grouping | Re-ran `organize` against an existing collection | ✅ Agent accepted rejections, didn't try to work around them |
| Confabulated coherence | 4 genuinely random unrelated photos | ✅ Agent declined to force a theme |
| Failure transparency | Simulated one photo failing to describe | ❌ Agent's summary falsely claimed full success; only an external post-hoc check caught it |

The third result is the week's most useful finding: a warning written to a log file
nobody reads isn't a guardrail, it's a postmortem. A fix was drafted — forcing the
code to append an honest correction directly into the delivered output whenever the
agent's own summary omits a known failure — but deliberately left unapplied so the
report could show the real gap between *detecting* a failure and *preventing* it
from reaching the user.

📄 **[`Failure-Testing/guardrail_agent.py`](Day-5-Failure-Modes-and-Guardrails/Failure-Testing/guardrail_agent.py)** —
the guardrail-equipped agent, with both test harnesses built in.

---

## 🧵 The Through-Line

- **Day 1's** decision boundary (agent judges, code validates) → the rule every
  later guardrail was built to enforce, not just a design-doc sentence.
- **Day 2's** clean single-tool run → proved the loop itself works before anything
  else was layered on top.
- **Day 3's** memory proof, and its shallow-grouping finding → the first sign that
  "shared subject category" isn't the same thing as "shared memory," reported
  honestly instead of glossed over.
- **Day 4's** richer photo set → confirmed the Day 3 finding wasn't a fluke: rich
  source material produced rich constellations, and thin material produced the same
  shallow one again.
- **Day 5's** guardrails → turned two real running findings (shallow grouping, a
  rate-limit failure actually hit) into tested code, and honestly reported that the
  third guardrail — failure transparency — doesn't yet hold, rather than declaring
  a clean sweep it didn't earn.

**Recurring lesson across all five days:** the same category-not-memory limitation
that showed up on Day 3 was still present on Day 4, and still not fully solved by
Day 5's guardrail — a single real problem tracked honestly across a week, rather
than five disconnected exercises each claiming success.

---

## 📂 Structure

```
Week-5-Agentic-AI-Fundamentals/
├── WEEK5-README.md
├── Day-1-Agents-vs-Chatbots/
│   ├── DAY1-REPORT.md
│   └── Design-Idea/
│       └── AGENT-DESIGN.md
├── Day-2-Tool-Use-and-Function-Calling/
│   ├── DAY2-REPORT.md
│   └── Basic-Agent/
│       ├── basic_agent.py
│       └── screenshots/
├── Day-3-Adding-Tools-and-Memory/
│   ├── DAY3-REPORT.md
│   └── Memory-Agent/
│       ├── memory_agent.py
│       ├── memory.json
│       ├── screenshots/
│       └── cache/
├── Day-4-Planning-and-Decomposition/
│   ├── DAY4-REPORT.md
│   └── Full-Agent/
│       ├── full_agent.py
│       ├── memory.json
│       ├── trace.log
│       ├── screenshots/
│       └── cache/
└── Day-5-Failure-Modes-and-Guardrails/
    ├── DAY5-REPORT.md
    └── Failure-Testing/
        ├── guardrail_agent.py
        ├── memory.json
        ├── trace.log
        ├── screenshots/
        ├── cache/
        └── Output/
            ├── test-organize.txt
            ├── test-confabulation.txt
            └── test-rate-limit.txt
```

---

*Part of [AI-Engineering-Summer-Training-2026](https://github.com/koko2haru/AI-Engineering-Summer-Training-2026).*