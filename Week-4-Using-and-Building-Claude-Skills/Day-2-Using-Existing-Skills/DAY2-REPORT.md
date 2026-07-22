# 📘 Day 2 Report — Using Existing Skills

**🎯 Focus:** Running existing Claude Skills against real, personal inputs — not sample data — and documenting how each one actually behaves

**📝 Assigned task:** Execute the skills surveyed on Day 1 with my own inputs (CoinQuest v2.0 backlog, a real behavioral question about the app, a real document to convert) and compare outputs to what the skill promises on paper

**📅 Date:** 2026-07-22

**✅ Status:** Completed

---

## 🗂️ Folder structure

```
📁 Day-2-Using-Existing-Skills/
├── 📄 DAY2-REPORT.md                          ← this report
└── 📁 Executing-Claude-Skills/
    ├── 📁 Product-Manager-Toolkit/
    │   ├── 📄 reflection-notes.md
    │   └── 📁 Output/
    │       ├── 📄 coinquest-v2-features.csv
    │       ├── 📄 rice_results.json
    │       └── 📄 RICE-Prioritization-CoinQuest-v2.md
    ├── 📁 Experiment-Designer/
    │   ├── 📄 reflection-notes.md
    │   └── 📁 Output/
    │       ├── 📄 experiment-design-roast-vs-coach.md
    │       └── 📄 sample_size_raw_output.txt
    └── 📁 MD-Slides/
        ├── 📄 reflection-notes.md
        └── 📁 Output/
            ├── 📄 slides.json
            ├── 📄 deck.json
            └── 📄 deck-skills-md.html
```

---

## 🎯 Objective

Day 1 was about reading skills — what they are, how they trigger, what they claim to do. Day 2 was about *running* them, on purpose, against a real project I actually care about (CoinQuest, the finance-tracker RPG from Week 2) instead of the bundled sample CSVs and demo decks. The goal set at the end of Day 1 was explicit: "feed personal inputs into RICE and document the output differences." That expanded naturally to all three task-oriented skills from `SKILLS.md`, each fed a real ask instead of a toy one.

The throughline that emerged, unplanned: **every one of these skills was built assuming a conventional multi-user product context**, and CoinQuest has exactly one user — me, ~1 session/day. Every single run required an explicit reframing step before the numbers meant anything, and every single run also surfaced at least one real bug or silent limitation that only shows up when you actually execute the scripts instead of reading about them.

---

## 🧪 1. Skills executed today — with real inputs

| Skill | My real ask | Adaptation required | Result |
|---|---|---|---|
| `product-manager-toolkit` (RICE) | Prioritize 7 CoinQuest v2.0 features (healing passive, potions, achievements, reports, boss, character, sound) | `Reach` redefined as *sessions/quarter the feature is touched* (~90), since "users affected" collapses to 1 for a single-user app | Healing Passive ranked #1 (54.0); Reports & Comparison Tool ranked *last* (3.2) despite being the tracker's core value — a direct demonstration of RICE's daily-touch bias |
| `experiment-designer` | Does Roast-mode vs Coach-mode change how often I log an expense? Baseline 3/week, detect a 20% lift | Tool's two-proportion z-test doesn't fit a single-subject count metric; reframed as daily-logging proportion for the tool, then cross-checked by hand with a two-sample t-test on weekly counts | Both methods agree: a 20% lift is undetectable in any practical timeframe at N=1 (533 days/arm vs. 131 weeks/arm). Built an MDE-vs-duration table instead — a 100% lift is detectable in ~3 months |
| `md-slides` | Turn `SKILLS.md` (yesterday's own 1,433-line deliverable) into an HTML deck | None needed for input shape — but the renderer's own dependencies were missing from this install | 16-slide deck built and opened fine, but slide bodies render as raw `<pre>` text (0 parsed `<h2>`/`<table>`) because sibling skills `md-document`/`design-system` aren't installed and the import failure is swallowed silently |

**😑 Also observed today:** two encoding-adjacent snags on Windows — one from `rice_prioritizer.py` printing emoji into a `cp1252` console (fixed with `PYTHONIOENCODING=utf-8`), one from a byte-count mismatch between the deck renderer's own reported size and the file's actual size on disk (Windows CRLF translation on `Path.write_text`, ~3.3 KB difference on a 90 KB file). Neither is a functional bug, both are exactly the kind of thing you only catch by running the tool for real.

---

## 🔁 2. The recurring pattern — framework mismatch at N=1

Every skill today hit the same wall from a different angle:

- **RICE's `Reach`** assumes "users affected per period." One user breaks that outright — every feature would score `Reach = 1` and the ranking would collapse to noise. Fix: redefine Reach as session-frequency, document the substitution, and flag where it distorts the ranking (Reports & Comparison Tool scoring last despite being the actual point of the app).
- **The sample-size calculator's two-proportion test** assumes independent trials across a population. A single person's weekly logging habit is neither a proportion nor independent across days. Fix: use the tool as directed, but cross-validate with the statistically correct design (paired/crossover, count-based) and report both, since they converge on the same practical conclusion even though the raw numbers disagree by orders of magnitude.
- **`md-slides`'s renderer** assumes a full sibling-skill install (`md-document`, `design-system`). Neither exists here, so it silently degrades to raw-text slides instead of erroring loudly. Fix: nothing to reframe — this one's just a limitation to disclose, not a number to adjust.

None of the three skills detects or warns about its own mismatch. That check has to come from outside — from me, or from Claude reading the actual script instead of trusting the `SKILL.md` description at face value.

---

## 📦 3. Deliverables produced today

1. **`RICE-Prioritization-CoinQuest-v2.md`** (+ CSV/JSON) — full RICE run on the real v2.0 backlog, with a judgment-adjusted build order overriding the raw score where RICE's bias distorts it.
2. **`experiment-design-roast-vs-coach.md`** (+ raw sample-size output) — full N-of-1 experiment design: hypothesis, metrics, crossover design, dual sample-size methodology, MDE/duration tradeoff table, stopping rule, validity threats.
3. **`deck-skills-md.html`** (+ `slides.json`, `deck.json`) — 16-slide HTML deck rendered from Day 1's `SKILLS.md`, with two documented rendering bugs.
4. **Three `reflection-notes.md` files** — one per skill, hand-written (explicitly *not* skill output), each covering: how it was invoked, input/output, what got created, what those files mean, and behavior actually observed — with a token-usage line per session pulled from `/usage`.
5. **`DAY2-REPORT.md`** — this report.

---

## 🎓 4. Task core — three skills, three real bugs

Using the same trigger-type framing from Day 1's `SKILLS.md`:

- **`product-manager-toolkit`** — trigger: *intent* to prioritize. Ran clean, but exposed RICE's structural blind spot (reach-weighted scoring undervalues low-frequency/high-value features) on real data, not a hypothetical.
- **`experiment-designer`** — trigger: *intent* to validate a change statistically. Ran clean, but exposed that its one built-in tool (two-proportion test) doesn't cover the single-subject/count-metric case at all — had to supplement, not just invoke.
- **`md-slides`** — trigger: *object* — a markdown deck to render. Ran and produced a working file, but two real defects surfaced only by inspecting the actual HTML output: a notes-parser false positive (its own regex tripped on the doc's *description* of that regex's syntax) and a silent dependency-fallback that degrades every slide's formatting.

**Lesson for Day 3+:** reading a `SKILL.md` tells you what a skill *claims*. Running it against a real, personal input — not the bundled sample — is what tells you what it actually *does*, and where the seams are.

---

## 🚀 Next steps — Day 3

- Try feeding a skill an input specifically designed to break its stated hard rules (e.g., a markdown file that's borderline on `md-slides`'s HR/H1 boundary thresholds) to map refusal behavior directly instead of by reading the refusal code.
- Consider patching the two `md-slides` bugs found today (backtick-aware notes regex; a loud warning instead of a silent `except ImportError` when sibling skills are missing) — good candidates for a "build/modify a skill" exercise later in the week.
- Keep the CoinQuest v2.0 RICE ranking and the Roast/Coach experiment design as live inputs for whichever skill Day 3 covers next (e.g., if a PRD-writing or roadmap skill comes up, it can consume today's ranked output directly).

---

## 📚 References

- **[`SKILLS.md`](../Day-1-What-is-a-skill/Skills-in-Claude/SKILLS.md)** — Day 1's four-skill engineering reference; also today's `md-slides` input.
- **[`DAY1-REPORT.md`](../Day-1-What-is-a-skill/DAY1-REPORT.md)** — prior day's report; this document follows its structure.
- **[RICE-Prioritization-CoinQuest-v2.md](Executing-Claude-Skills/Product-Manager-Toolkit/Output/RICE-Prioritization-CoinQuest-v2.md)** — full RICE run + portfolio analysis.
- **[experiment-design-roast-vs-coach.md](Executing-Claude-Skills/Experiment-Designer/Output/experiment-design-roast-vs-coach.md)** — full experiment design + sample-size methodology.
- **[deck-skills-md.html](Executing-Claude-Skills/MD-Slides/Output/deck-skills-md.html)** — rendered deck from `SKILLS.md`.
- **Reflection notes:** [Product-Manager-Toolkit](Executing-Claude-Skills/Product-Manager-Toolkit/reflection-notes.md) · [Experiment-Designer](Executing-Claude-Skills/Experiment-Designer/reflection-notes.md) · [MD-Slides](Executing-Claude-Skills/MD-Slides/reflection-notes.md)
