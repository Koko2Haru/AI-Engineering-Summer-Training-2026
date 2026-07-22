# Skill Anatomy — Annotations for the Template

Companion walkthrough for `SKILL.md` in this folder. Where `SKILL.md` has inline `<!-- ANNOTATION -->` comments at the point they're relevant, this file is the linear, readable version — read it top to bottom once, then use `SKILL.md`'s inline comments as in-place reminders when actually filling in a real skill.

---

## 1. What a skill actually is

A skill is a **folder**, not a single file: a `SKILL.md` (instructions + YAML frontmatter) plus optional supporting files — `references/`, `scripts/`, `assets/`. The folder *is* the unit of packaging; `SKILL.md` is just its entry point.

## 2. Progressive disclosure — the three levels

This is the core cost/architecture model behind every design decision below:

| Level | What loads | When |
|---|---|---|
| 1 | `name` + `description` (frontmatter only) | Always, for every skill in the project, all the time |
| 2 | The rest of `SKILL.md` | Only once this skill is selected for the current task |
| 3 | `references/`, `scripts/`, `assets/` | Only when `SKILL.md`'s instructions say to consult them |

**Why it matters:** Level 1 has to be cheap and always-on, so it can't be more than a name and a description. Everything that would make Level 1 expensive belongs in Level 2. Everything in Level 2 that's only needed *sometimes* (a detailed rubric, a big verb list, a worked example) belongs in Level 3. A skill that inlines everything into `SKILL.md` defeats the entire point of the model — it becomes as expensive as just not having a skill at all.

## 3. The frontmatter — `name` and `description`

Only two fields, deliberately minimal (checked against the four official-style skills already in `.claude/skills/` — none of them use a heavier YAML schema):

- **`name`** — kebab-case, matches the folder name. Used for explicit invocation (`/skill-name`) and internal bookkeeping.
- **`description`** — the single most important line in the whole file. It is the *only* thing evaluated when deciding whether this skill applies to the current task. **Description quality is trigger quality** — a vague description ("helps with resumes") competes poorly against specific phrasing a user might actually type ("review my resume," "will this pass ATS"). Write descriptions the way you'd write a search query you expect to match, not a category label.

## 4. Two invocation modes

- **Automatic** — the agent matches the current task against every skill's `description`. This is the default and the one the description has to be written for.
- **Explicit** — the user types `/skill-name`. This bypasses the matching step entirely, so it's a safety net, not a substitute for a good description.

## 5. The trigger-type framework (from Day 1)

Every skill's trigger condition falls into one of three shapes — useful for checking a `description` actually covers what it's meant to:

- **Object-triggered** — fires because of something in the input (a PDF, a markdown deck, a resume file).
- **Intent-triggered** — fires because of what the user is trying to do (prioritize features, design an experiment).
- **Activity/domain-triggered** — fires because of the general kind of work (building a UI, writing a PRD).

Most real skills combine at least two of these. Write the `description` to cover the actual combination, not just the most obvious one.

## 6. Why "When It Should NOT Trigger" is not optional

A skill with only a trigger list tends to over-fire on anything adjacent to its topic, producing shallow, over-general output instead of routing the nearby-but-different request elsewhere (or answering it directly, without the full workflow). Every skill in this repo's `.claude/skills/` that has this section uses it to explicitly hand off narrow, single-fact questions rather than running the whole pipeline on them.

## 7. Recommended folder layout — and why each piece exists

```
your-skill-name/
├── SKILL.md       ← entry point: frontmatter + purpose/triggers/workflow/constraints
├── references/    ← knowledge SKILL.md instructs Claude to *consult*, not restate
├── scripts/       ← deterministic logic that shouldn't be re-derived by the model each run
└── assets/        ← templates, worked examples, machine-readable config (schemas, weights)
```

- **`references/`** exists because rubrics, checklists, and domain knowledge are exactly the kind of thing that's expensive to keep in `SKILL.md` itself but cheap to load only when actually needed. The test for "does this belong in references/": would restating it inline make `SKILL.md` noticeably longer without changing what Claude does most of the time? If yes, move it out.
- **`scripts/`** exists for anything that's deterministic and error-prone to redo by reasoning alone — text extraction, regex-based detection, arithmetic over a fixed formula. A script should also know its own limits: if a piece of the task genuinely needs judgment a script can't provide, the script should say so explicitly rather than returning a fabricated-precise answer.
- **`assets/`** exists for anything that's a *shape* to match rather than a rule to apply: output templates, worked examples, machine-readable config (weights, schemas). Worked examples are for calibration — but see the annotation in `SKILL.md`'s Output Format section about **not** letting a reference file's own display formatting (e.g. a code fence used just so the file reads clearly on its own) leak into the actual instructions.

Not every skill needs all three — `caveman` in this repo's `.claude/skills/` has no `references/` or `assets/` at all, because its entire logic fits in `SKILL.md`. Match the folder layout to the task's actual complexity; don't create empty structure for its own sake.

## 8. Why the `SKILL.md` body is ordered the way it is

The section order in this template (Purpose → Trigger → Non-trigger → Input → Output → Instructions/Workflow → Edge Cases → Constraints → File Usage → Best Practices → Failure Handling) isn't arbitrary — it mirrors the order a reader actually needs the information:

1. **Purpose** first, so the "why" is established before any rule.
2. **Trigger / non-trigger** next, so it's clear *when* everything that follows even applies.
3. **Input/Output contracts** before the workflow, so the workflow's steps have defined start and end points.
4. **Workflow → Edge Cases → Constraints** in that order: the happy path first, then what to do when it's not so happy, then hard limits that apply regardless of path.
5. **File Usage** near the end, once the reader already understands *why* each file might be needed — the table becomes a quick-reference instead of the first thing thrown at them cold.
6. **Best Practices / Failure Handling** last, as a final calibration pass and a safety net.

## 9. See it applied in full

`Structure-Template/SKILL.md` in this folder is the **draft/annotated** version — a first pass with placeholders and inline reasoning, matching Day 3's brief exactly ("design the folder structure and write the first version of a `SKILL.md` file... an annotated skill template").

For the **fully implemented, verified** version of this same anatomy — real content in every section, 5 populated reference docs, 3 working scripts, 3 real assets, and end-to-end testing — see `../../Day-4-Build-Your-Own-Skill/cv-reviewer/SKILL.md`. Reading both side by side is the fastest way to see exactly what "first draft" vs. "implemented and verified" looks like in practice.
