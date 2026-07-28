# 📘 Day 2 Report — Tool Use / Function Calling

**🎯 Focus:** Building a working single-tool agent and proving the ReAct loop actually runs, not just gets described

**📝 Assigned task (per the Week 5 plan):** *"Build a simple agent capable of using one external tool (calculator, weather API, search, etc.)."*

**📅 Date:** 2026-07-28

**✅ Status:** Completed

---

## 🗂️ Folder structure

```
📁 Day-2-Tool-Use-and-Function-Calling/
├── 📄 DAY2-REPORT.md
└── 📁 Basic-Agent/
    ├── 📄 basic_agent.py   ← single-tool agent (describe_photo via Gemini vision)
    └── 📁 screenshots/     ← 5 real test photos
```

---

## 🎯 Objective

Wire up exactly one external tool — `describe_photo`, backed by the Gemini vision API — and prove the model runs a real think → act → observe loop against it, rather than a single hardcoded call.

## 🧠 1. What got built

**`basic_agent.py`** — a single-tool agent using Gemini's function-calling API. The model is given one tool it's told it must use to see anything (`describe_photo(path)`), a folder of real photos, and a loop that keeps feeding tool results back until the model stops requesting tools on its own. Every tool call and result is printed as it happens, so the loop is visible, not just its final answer.

`describe_photo` calls Gemini vision with a constrained JSON schema (subjects, setting, indoor/outdoor, time of day, notable details, confidence) rather than free prose — decided on Day 1 specifically to keep the model from producing plausible-sounding narrative it can't back up. Every result is cached to disk by file hash so repeated runs don't re-spend API quota.

## 🧪 2. Verification — real run against real photos

Ran the agent against 5 real photos (a group photo, a butterfly, a close-up eye, a strawberry, a man with a camera) with the prompt *"tell me what these have in common, if anything."*

| What happened | Why it matters |
|---|---|
| Turn 1: agent requested all 5 `describe_photo` calls in one batch | Confirms the model is deciding how many tool calls it needs, not following a fixed count |
| Turn 2: agent gave a final answer with no further tool calls | Confirms it can recognize when it has enough information and stop the loop itself |
| Final answer: correctly said there's no common theme across 5 unrelated photos | This is the important result — an agent that invents a shared theme across unrelated photos is exactly the Day 5 failure mode this project is built around. It didn't. |

One thing flagged for Day 5, not fixed today: every photo returned `confidence: 1.0`, with no variation across five very different subjects. Worth testing on a genuinely ambiguous photo later — if confidence never actually drops, the field isn't doing real work yet.

## 🐛 3. Environment issues hit and resolved

- **`.env` not loading** — `basic_agent.py` was missing `load_dotenv()`, so `os.environ["GEMINI_API_KEY"]` raised a `KeyError`. Fixed by adding `from dotenv import load_dotenv` + `load_dotenv()` before the `genai.configure(...)` call.
- **`google.generativeai` deprecation warning** — the package still works but is frozen (no further updates). Left as-is for this project; noted `google.genai` as the migration path if needed later, but not switching mid-build.

## 📦 4. Deliverables produced today

1. **`Basic-Agent/basic_agent.py`** — working single-tool agent with a real function-calling loop.
2. **`Basic-Agent/screenshots/`** — 5 real test photos used to verify it.
3. **`DAY2-REPORT.md`** — this report.

---

## 🎓 Reflection

**Daily Task Completed:** Built and ran a single-tool agent that looks at real photos through a vision API and reasons about what it sees, using a genuine tool-calling loop rather than one fixed call.

**What I Learned:** The loop's real proof isn't that it calls the tool — it's that the model decides on its own when it has enough information and stops asking for more.

**Challenges Faced:** The script failed with a missing API key error because the `.env` file wasn't actually being loaded into the script.

**How I Solved Them:** Added `load_dotenv()` so the script reads the key from `.env` instead of expecting it to already be in the environment.

---

## 🚀 Next steps — Day 3 (Adding Tools & Memory)

Per the plan: add a second tool and introduce memory, and demonstrate that a past interaction changes a future decision. For Star Gazer that's `reverse_geocode` as the second tool, plus persisting user corrections and stated preferences so the agent doesn't forget them between sessions.

---

## 📚 References

- **[`Basic-Agent/basic_agent.py`](Basic-Agent/basic_agent.py)** — the single-tool agent built today.
- **[`../Day-1-Agents-vs-Chatbots/Design-Idea/AGENT-DESIGN.md`](../Day-1-Agents-vs-Chatbots/Design-Idea/AGENT-DESIGN.md)** — the design this build follows, including the vision-first decision this day's test confirmed was right.