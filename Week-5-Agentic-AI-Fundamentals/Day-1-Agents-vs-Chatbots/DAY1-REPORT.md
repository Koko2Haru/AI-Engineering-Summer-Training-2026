# 📘 Day 1 Report — Agents vs Chatbots

**🎯 Focus:** What separates an agentic system from a chatbot, and designing a real-world agent before writing any code

**📝 Assigned task (per the Week 5 plan):** *"Design an AI agent for a real-world scenario. Define its objective, available tools, inputs, outputs, and decision process."*

**📅 Date:** 2026-07-27

**✅ Status:** Completed

---

## 🗂️ Folder structure

```
📁 Day-1-Agents-vs-Chatbots/
├── 📄 DAY1-REPORT.md          ← this report
└── 📁 Design-Idea/
    └── 📄 AGENT-DESIGN.md     ← full agent design doc
```

---

## 🎯 Objective

Design an agent for a genuine real-world problem — not a toy demo — and define its objective, tools, inputs, outputs, and decision process before any implementation begins. The scenario: people lose track of memories buried in tens of thousands of photos, and existing search tools only help when you already know what you're looking for.

## 🧠 1. What got built

**`AGENT-DESIGN.md`** — the design doc for **Star Gazer**, an agent that turns a photo collection into a navigable 3D night sky: every photo is a star, and the user flies freely through the collection instead of searching it.

The core design decision: the agent must work on photos with **no metadata at all** — no GPS, no timestamp, the exact photos people actually lose. That ruled out a metadata-only design (EXIF clustering) and settled on a vision-first approach: the agent looks at each photo, describes what it's of, and only uses timestamp/location as secondary supporting evidence when present.

The doc covers, per the day's brief:

- **Objective** — arrange an unorganised, partially-annotated photo folder into 3D space and named constellations, testable against a concrete success criterion
- **Tools** — `describe_photo` (web API, vision), `reverse_geocode` (web API, Nominatim), plus local metadata reading and constellation-proposal tools
- **Inputs** — a photo folder, a user instruction, and persisted memory from prior sessions
- **Outputs** — `sky.json`, a rendered 3D scene, an "unsorted/sparse" region, and a full reasoning trace
- **Decision process** — an explicit boundary table (what the agent judges vs. what code computes) plus a written ReAct loop showing the agent revising its plan mid-task

## 🧪 2. Why this counts as agentic, not a chatbot

Three reasons, argued explicitly in the design doc:

- A chatbot has no hands — it can't read a file or place a star in a scene.
- A script can cluster by numbers, but it can't look at a photo and recognize "this is the same kitchen," let alone decide nine photos across four years are one story worth naming.
- The number of loop iterations isn't knowable in advance — it depends entirely on what a given collection turns out to contain. That's the actual test: if the flowchart can be drawn before running it, it isn't an agent.

## 🐛 3. Design correction made today

The first draft of the design leaned on EXIF timestamp and GPS as the primary grouping signal, with vision-based tagging left out of scope. On review, that was backwards: the photos most likely to be lost — screenshots, forwards, scans — are exactly the ones with no metadata, so a metadata-first design fails hardest at the actual problem. The doc was rewritten so vision-based description is the primary tool and metadata is corroborating evidence only.

This also sharpened Day 5's most interesting failure mode: an LLM shown unrelated photos will always find *some* shared theme rather than saying "these have nothing in common" — the same failure ancient stargazers made connecting unrelated stars into constellations. Testing whether the agent can correctly refuse to group a random set of photos is now the central Day 5 test.

## 📦 4. Deliverables produced today

1. **`Design-Idea/AGENT-DESIGN.md`** — full agent design (objective, tools, inputs, outputs, decision process, anticipated failure modes, scope).
2. **`DAY1-REPORT.md`** — this report.

---

## 🎓 Reflection

**Daily Task Completed:** Designed Star Gazer, an agent that turns a photo library into a navigable 3D sky, with its objective, tools, inputs, outputs, and decision boundary written up before any code.

**What I Learned:** The real design decision wasn't the 3D part — it was deciding what the agent is allowed to judge versus what has to be deterministic code, and realizing metadata can't carry the hardest cases.

**Challenges Faced:** My first pass leaned on photo timestamps and GPS location to group photos, but that fails on exactly the photos that are hardest to find in real life — the ones with no metadata at all.

**How I Solved Them:** Rebuilt the design so the agent looks at and understands each photo directly, using timestamp and location only as supporting evidence when they happen to exist.

---

## 🚀 Next steps — Day 2 (Tool Use / Function Calling)

Per the plan: build a working single-tool agent using function calling. For Star Gazer that means wiring up `describe_photo` against a real vision API and running the ReAct loop end-to-end on a handful of test photos before scaling up.

---

## 📚 References

- **[`Design-Idea/AGENT-DESIGN.md`](Design-Idea/AGENT-DESIGN.md)** — the full agent design built today.