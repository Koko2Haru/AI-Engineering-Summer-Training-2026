# 📘 Day 3 Report — Adding Tools & Memory

**🎯 Focus:** A second tool with real validation, and memory that visibly changes a later decision — not just recall

**📝 Assigned task (per the Week 5 plan):** *"Extend the agent by adding memory and a second tool. Demonstrate that previous interactions influence future decisions."*

**📅 Date:** 2026-07-28

**✅ Status:** Completed

---

## 🗂️ Folder structure

```
📁 Day-3-Adding-Tools-and-Memory/
├── 📄 DAY3-REPORT.md
└── 📁 Memory-Agent/
    ├── 📄 memory_agent.py   ← two-tool agent + persistent memory
    ├── 📄 memory.json       ← persisted constellations + preferences
    ├── 📁 screenshots/      ← 10 real test photos
    └── 📁 cache/            ← cached photo descriptions (from Day 2)
```

---

## 🎯 Objective

Add a second tool the agent can act with, not just perceive with, and prove that something the user states in one run changes what the agent does in a later, separate run — without the user repeating themselves.

## 🧠 1. What got built

**Second tool: `propose_constellation`.** The agent proposes a group of photos, a name, and a rationale. Code then validates the proposal before accepting it — rejecting duplicate names, groups under 2 photos, and any attempt to touch a user-locked constellation. On rejection the errors go back to the agent to revise. This is the agent/code boundary from the Day 1 design doc actually enforced, not just described.

**Memory: `memory.json`**, read into the system prompt on every run. Two kinds of persisted fact: constellations already created, and preferences the user has explicitly stated. Both survive between separate script runs.

Model in use: `gemini-2.0-flash-lite`, via the `google.generativeai` package (deprecated but still functional, same as Day 2).

## 🧪 2. Verification — 10 real photos, two separate runs

**Run 1 — empty memory.** 10 photos, 6 depicting groups of people in social settings, 4 unrelated singletons (butterfly, eye close-up, strawberry, a hiker).

| What happened | Why it matters |
|---|---|
| Agent described all 10 photos, then proposed one constellation grouping the 6 people-photos | Correctly recognized two identical duplicate photos (1.jpg and 7.jpg) and folded both into the same group rather than treating them as separate evidence |
| Left the 4 singletons ungrouped with a stated reason | The confabulation guardrail from the design doc firing correctly — it did not force unrelated photos into a group just to tidy up |
| `propose_constellation` accepted the group, wrote it to `memory.json` | Confirms the validation tool works and memory persists to disk between runs |

**Run 2 — the memory proof.** Told the agent, separately from any organizing prompt: *"the butterfly and the strawberry are the same collection, they're both from my garden."* Then ran `organize` again, with no mention of butterflies or strawberries in that prompt.

Result: the agent created a new constellation, **"My Garden Wonders"** — `["2.jpg", "4.jpg"]` — with the rationale *"these photos depict a butterfly and a strawberry, both captured in the user's garden."* That reasoning came from the earlier statement, not from anything in the second prompt. This is the deliverable the day's brief asks for: a past interaction, on its own, changed a later decision.

## 🐛 3. Finding worth reporting honestly

"The Social Circle" is a weak constellation compared to the design doc's own bar (*"nine photos, four years, same kitchen — The Hearth"*). Its rationale — "groups of friends together in social settings" — is closer to a category than a memory, because none of the 10 test photos actually share anything more specific than "multiple people." The agent grouped correctly given the evidence available; the evidence itself just wasn't rich enough to produce a genuinely interesting constellation. Noted here rather than hidden — it's a real limitation of the current test set, and it's the reason Day 4's task should use photos with a specific shared thread (a place, a repeated event) rather than a generic theme.

## 📦 4. Deliverables produced today

1. **`Memory-Agent/memory_agent.py`** — two-tool agent with validated constellation proposals and persistent memory.
2. **`Memory-Agent/memory.json`** — the persisted state showing both constellations from the two runs.
3. **`Memory-Agent/screenshots/`** — 10 real test photos.
4. **`DAY3-REPORT.md`** — this report.

---

## 🎓 Reflection

**Daily Task Completed:** Added a second tool that groups photos, with code validating every proposal, and persistent memory that changed what the agent did in a second, separate run without repeating myself.

**What I Learned:** Memory only counts as proven if the same prompt produces a different result across two separate runs — not by asking the agent to recall something mid-conversation.

**Challenges Faced:** My first 10 test photos barely had anything real in common with each other, so the agent's only grouping came out shallow — just "photos with multiple people in them" rather than an actual memory.

**How I Solved Them:** Told the agent a specific fact linking two unrelated-looking photos (butterfly and strawberry, both from my garden) and re-ran it — it built a proper constellation from that stated connection instead of from surface similarity.

---

## 🚀 Next steps — Day 4 (Planning & Decomposition)

Per the plan: give the agent a complex multi-step task and document how it plans and executes it. For Star Gazer, that means a fuller synthetic photo set with a genuinely specific shared thread (not just "groups of people"), and a single instruction like *"organise my whole sky"* that forces the agent through describing, grouping, revising, and reporting sparse regions in one run — logged step by step as the actual deliverable.

---

## 📚 References

- **[`Memory-Agent/memory_agent.py`](Memory-Agent/memory_agent.py)** — the two-tool, memory-backed agent built today.
- **[`../Day-1-Agents-vs-Chatbots/Design-Idea/AGENT-DESIGN.md`](../Day-1-Agents-vs-Chatbots/Design-Idea/AGENT-DESIGN.md)** — the design this build follows, including the human-correction-outranks-machine-grouping principle enforced today via `locked` constellations.
- **[`../Day-2-Tool-Use-and-Function-Calling/DAY2-REPORT.md`](../Day-2-Tool-Use-and-Function-Calling/DAY2-REPORT.md)** — prior day's report; today reuses its `describe_photo` tool and cache unchanged.