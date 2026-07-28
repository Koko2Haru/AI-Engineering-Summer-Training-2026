# 📘 Day 4 Report — Planning & Decomposition

**🎯 Focus:** Giving the agent a task big enough that it has to genuinely plan, and documenting the trace of how it broke that plan into steps

**📝 Assigned task (per the Week 5 plan):** *"Give the agent a complex task requiring multiple steps. Observe and document how it plans and executes each step."*

**📅 Date:** 2026-07-28

**✅ Status:** Completed

---

## 🗂️ Folder structure

```
📁 Day-4-Planning-and-Decomposition/
└── 📁 Full-Agent/
    ├── 📄 DAY4-REPORT.md         ← this report
    ├── 📄 full_agent.py          ← full multi-step organize pass, fully logged
    ├── 📄 trace.log              ← the actual deliverable: full plan trace
    ├── 📄 memory.json            ← persisted constellations, carried over from Day 3
    ├── 📁 screenshots/           ← 20 real test photos (10 carried over, 10 added)
    └── 📁 cache/                 ← cached photo descriptions
```

---

## 🎯 Objective

Give the agent one instruction — *"organize my whole sky"* — against a full 20-photo collection in a single run, and log every thought, action, and observation as it happens. The trace is the deliverable, not the resulting constellations.

## 🧠 1. What got built

**`full_agent.py`** — same two tools as Day 3 (`describe_photo`, `propose_constellation`), but the system prompt now spells out an explicit multi-step procedure: describe everything first, look for genuine shared threads rather than surface categories, propose constellations, revise on rejection, and report what's left ungrouped. Every turn is written to `trace.log` with a timestamp, independent of what prints to the terminal.

**Test set expanded to 20 photos** — the original 10 (mostly people-in-groups, plus a few unrelated singletons) plus 10 new ones chosen specifically to have real thematic variety: several fruit close-ups, two butterfly photos, several pet-pair photos.

## 🧪 2. Trace walkthrough

| Turn | What happened |
|---|---|
| 1 | Agent called `describe_photo` on all 20 photos in one batch — decided it needed full information about the whole collection before proposing anything |
| 2 | Agent proposed 4 constellations in a single batch, all accepted on the first attempt: **Garden Visitors** (2 butterfly photos), **Fruit Still Lifes** (6 photos), **Friends and Gatherings** (5 photos), **Friends of Furry Kind** (4 photos) |
| 3 | Final summary, correctly explaining which 3 photos (eye close-up, solo hiker, ferret) were left ungrouped and why |

Compared to Day 3's single shallow grouping, richer source material produced richer results: **Fruit Still Lifes** and **Friends of Furry Kind** are constellations built on a real specific pattern, not just "contains people."

## 🐛 3. Two honest findings

- **The plan didn't need to backtrack.** No `propose_constellation` call was rejected, and no describe step was repeated. That's a clean run, but it also means this trace doesn't show the agent *replanning* — only executing a first-try-correct plan. A future test with a deliberately ambiguous overlap (a photo that could plausibly belong to two groups) would be a better stress test of the plan-revise loop.
- **"Friends and Gatherings" repeats Day 3's weak-constellation pattern.** Its rationale — "groups of young adults... in social settings" — is the same category-not-memory shortfall flagged in the Day 3 report. Five photos of unrelated people posing got merged because they share a subject type, not a specific shared event. This is a consistent limitation across two days now, not a one-off, and it's the strongest candidate for a Day 5 guardrail: require more than "same general category" before a group is accepted.

## 🐞 4. Rate limit hit mid-run

Adding 10 new, previously-uncached photos in one go triggered Gemini's free-tier cap (15 requests/minute) partway through the first attempt. Resolved simply — waited roughly 15 seconds as the error message specified, then reran the script. The full run above is the successful rerun. Worth carrying into Day 5: an agent that silently proceeds after a partial API failure, rather than surfacing it, is a real guardrail-worthy failure mode — and this is a case where it actually happened, not a hypothetical.

## 📦 5. Deliverables produced today

1. **`Full-Agent/full_agent.py`** — the multi-step agent with full trace logging.
2. **`Full-Agent/trace.log`** — the complete run trace.
3. **`Full-Agent/screenshots/`** — 20 real photos, 10 carried over + 10 added for thematic variety.
4. **`DAY4-REPORT.md`** — this report.

---

## 🎓 Reflection

**Daily Task Completed:** Ran the agent against a full 20-photo collection with one instruction, logging every step it took, and it produced four constellations plus a correctly explained ungrouped set.

**What I Learned:** Giving the agent photos with a genuine specific pattern — same fruit, same kind of animal pairing — produced real constellations, while photos that only share a broad category still get lumped together shallowly, same as Day 3.

**Challenges Faced:** Adding 10 new uncached photos at once hit Gemini's free-tier rate limit partway through the run.

**How I Solved Them:** Waited about 15 seconds as the error message suggested, then reran the script — the second attempt completed cleanly.

---

## 🚀 Next steps — Day 5 (Failure Modes & Guardrails)

Per the plan: identify three failure scenarios and implement guardrails preventing incorrect or unsafe behavior. Clear candidates from what's already surfaced:

1. **Category-not-memory grouping** — "Friends and Gatherings" and Day 3's "Social Circle" both show the agent accepting shared subject type as sufficient grounds for a constellation. Guardrail: require corroboration on more than one axis (not just subject) before a proposal is accepted.
2. **Confabulated coherence** — not yet triggered in testing, but the design doc's central risk: shown enough photos, the agent should refuse to find a theme where there isn't one. Test with a deliberately random control group.
3. **Silent rate-limit failure** — already encountered for real today. If the API fails mid-run, the agent should not report success on a partial description pass.

---

## 📚 References

- **[`Full-Agent/full_agent.py`](Full-Agent/full_agent.py)** — the multi-step agent built today.
- **[`Full-Agent/trace.log`](Full-Agent/trace.log)** — the full execution trace, the day's core deliverable.
- **[`../Day-3-Adding-Tools-and-Memory/DAY3-REPORT.md`](../Day-3-Adding-Tools-and-Memory/DAY3-REPORT.md)** — prior day's report; today's "category not memory" finding is a direct continuation of its own weak-constellation note.