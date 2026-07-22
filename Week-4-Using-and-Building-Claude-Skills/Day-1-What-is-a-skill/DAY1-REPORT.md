# 📘 Day 1 Report — What Is a Skill

**🎯 Focus:** Understanding the Claude Skill model — what a skill is, when it triggers, and why it's useful

**📝 Assigned task:** Analyze three existing Claude Skills and explain when each should be triggered and what problem it solves

**📅 Date:** 2026-07-21 

**✅ Status:** Completed (scope exceeded)

---

## 🗂️ Folder structure

```
📁 Day-1-What-is-a-skill/
├── 📄 DAY1-REPORT.md          ← this report
└── 📁 Skills-in-Claude/
    └── 📄 SKILLS.md           ← four-skill engineering reference
```

---

## 🎯 Objective

The Day 1 goal was a clear grasp of the skill model. The assigned deliverable was to analyze three existing Claude Skills and explain their triggers and purpose. In practice the day went further: I explored the wider skills ecosystem, ran several skills live, learned how to clone and install skills, and produced a full four-skill engineering reference.

---

## 🧠 1. Concepts learned — what a skill actually is

- **Definition:** a skill is a folder containing a `SKILL.md` (instructions + YAML frontmatter) plus optional supporting files (scripts, references, templates).
- **Progressive disclosure (3 levels):** (1) only name + description are always loaded; (2) the full `SKILL.md` loads when the skill is selected; (3) supporting files load only when needed. This keeps context cheap.
- **Two invocation modes:** *automatic* (the agent matches the task to a skill's description) and *explicit* (`/skill-name`). Description quality **is** trigger quality.
- **Three trigger types** (the core insight): a skill fires on an **object** in the task (e.g. a PDF), an **intent** (e.g. "build a skill"), or an **activity/domain** (e.g. building UI).
- **Why skills exist:** to package specialized, reliable instructions for tasks the model *could* improvise but does better with a packaged recipe + deterministic scripts.

---

## 📥 2. Repository & cloning techniques

- You **cannot** `git clone` a single file — cloning pulls the whole repo. Options for one file: raw URL via `curl`/`wget`.
- For a **folder**: `git sparse-checkout` (cone mode) or `npx giget@latest`.
- Practiced against two repos: `anthropics/skills` (the `pdf` folder) and `alirezarezvani/claude-skills`.

```bash
# Single folder via sparse checkout
git clone --no-checkout --depth 1 <repo>.git
cd repo && git sparse-checkout init --cone
git sparse-checkout set path/to/folder && git checkout
```

---

## ⚖️ 3. Licensing & copyright

| Source | License | What it allows |
|---|---|---|
| `anthropics/skills` — example skills | Apache 2.0 | Full open-source reuse (keep license/attribution) |
| `anthropics/skills` — document skills (docx/pdf/pptx/xlsx) | Source-available | Read & reference only; check terms before redistributing |
| `alirezarezvani/claude-skills` | MIT | Full reuse with attribution |
| `caveman` skill | MIT (derived from Matt Pocock) | Reuse with attribution preserved |

**Rule of thumb:** analyzing a skill and writing about it in your own words is always fine. Before *redistributing* files, check the per-folder license.

---

## 🧪 4. Skills explored & run live

| Skill | Source | What it does | Observed result |
|---|---|---|---|
| `pdf` | Anthropic | Create/read/manipulate PDFs | Generated a real 2-page analysis PDF |
| `saas-metrics-coach` | alirezarezvani | SaaS metrics dashboard | MRR $82k → ARR $984k, LTV:CAC 5.75:1 |
| `product-manager-toolkit` (RICE) | alirezarezvani | Feature prioritization | Ranked "Onboarding" (20000) → "Collab" (461) |
| `experiment-designer` | alirezarezvani | A/B sample-size calc | 10% baseline, +2pt → 7,686 users, ~4 days |
| `caveman` | alirezarezvani | Token-compression mode | Cut a verbose sentence ~28% (helper), full voice ~75% |
| `md-slides` | alirezarezvani | Markdown → HTML deck | Reviewed: single-file HTML, presenter mode, print-to-PDF |

**😂 Funny/personality skills discovered:** `roast` (5-angle idea panel), `grill-me` (relentless plan interrogation), `andreessen` (blunt market-first persona), `fable-goal` (ramble → clean prompt).

---

## 🛠️ 5. Installing & calling skills (Claude Code / VS Code)

- **Location:** project-level `your-project/.claude/skills/<name>/SKILL.md`, or global `~/.claude/skills/`.
- **Invoke:** `/skill-name`, or just describe the task and let auto-invocation match.
- **Verify:** run `/doctor` to confirm the skill was picked up and see its context cost.
- **VS Code:** skills run *through* Claude Code — invoke in the Claude panel, or run `claude` in a project-root terminal. Not via VS Code's own command palette.

---

## 📦 6. Deliverables produced today

1. **`day1-analysis.pdf`** — analysis of three skills (`pdf`, `skill-creator`, `frontend-design`), built with the Anthropic `pdf` skill.
2. **`skills-pack.zip`** — four cloned skills (`md-slides`, `product-manager-toolkit`, `experiment-designer`, `caveman`) packaged for install, with MIT `LICENSE` + `README`.
3. **`SKILLS.md`** — a ~1,400-line engineering handbook documenting all four skills (19 sections each: triggers, decision trees, I/O, confidence bands, Mermaid diagrams) plus global chapters. → see [📚 References](#-references).
4. **`DAY1-REPORT.md`** — this report.

---

## 🎓 7. Task core — three skills analyzed

The assigned task (analyze three skills + explain triggers/purpose) was met and extended to four in `SKILLS.md`. Summary using the trigger-type framework:

- **`product-manager-toolkit`** — trigger: *intent* to prioritize/synthesize product work. Problem solved: reproducible, auditable product decisions (RICE) instead of opinion-driven roadmaps.
- **`experiment-designer`** — trigger: *intent* to design/interpret an experiment. Problem solved: correctly powered, defensible A/B tests instead of underpowered guesses.
- **`md-slides`** — trigger: *object/activity* — a markdown deck to present. Problem solved: portable, presentable HTML decks (with print-to-PDF) instead of hand-written slide HTML.
- **`caveman`** — trigger: *intent* for terseness. Problem solved: deterministic token savings with technical fidelity, and safety-aware suspension for critical output.

---

## 🚀 Next steps — Day 2

Day 2 focus is running existing skills with different inputs and comparing their outputs — already begun today (five skills executed live). Next: feed personal inputs (e.g. own feature list into RICE) and document the output differences.

---

## 📚 References

- **[`SKILLS.md`](./Skills-in-Claude/SKILLS.md)** — the full four-skill engineering reference produced on Day 1 (`product-manager-toolkit`, `experiment-designer`, `md-slides`, `caveman`). 19 sections per skill + global chapters (comparison matrix, interaction graph, decision pipeline, taxonomy, architecture) + 12 Mermaid diagrams. Located at `Skills-in-Claude/SKILLS.md`.
- **[anthropics/skills](https://github.com/anthropics/skills)** — Anthropic's official skills repo (example skills Apache 2.0; document skills source-available).
- **[alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills)** — MIT-licensed community skills repo; source of the four skills documented in `SKILLS.md`.
- **[mattpocock/skills](https://github.com/mattpocock/skills)** — original `caveman` skill (MIT), from which this repo's version is derived.