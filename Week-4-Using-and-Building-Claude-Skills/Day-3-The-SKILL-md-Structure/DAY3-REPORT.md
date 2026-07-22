# 📘 Day 3 Report — The SKILL.md Structure

**🎯 Focus:** Skill anatomy — folder layout, frontmatter, and the shape of a `SKILL.md` file, as a design/first-draft exercise rather than a full implementation

**📝 Assigned task (per the Week 4 plan):** *"Design the folder structure and write the first version of a SKILL.md file for a custom skill."* Expected outcome: *"An annotated skill template."*

**📅 Date:** 2026-07-22

**✅ Status:** Completed

---

## 🗂️ Folder structure

```
📁 Day-3-The-SKILL-md-Structure/
├── 📄 DAY3-REPORT.md              ← this report
└── 📁 Structure-Template/
    ├── 📄 SKILL.md                ← first-draft, annotated skill template (generic, reusable)
    ├── 📄 ANNOTATIONS.md          ← linear walkthrough: skill anatomy + folder-layout rationale
    ├── 📁 references/
    │   └── 📄 README.md           ← stub explaining this folder's purpose
    ├── 📁 scripts/
    │   └── 📄 README.md           ← stub explaining this folder's purpose
    └── 📁 assets/
        └── 📄 README.md           ← stub explaining this folder's purpose
```

5 files, ~198 lines in the two substantive documents (`SKILL.md` + `ANNOTATIONS.md`).

---

## 🎯 Objective

This is a course-correction day, not a new topic. Day 4's work was originally built under this folder's name before a look at the actual Week 4 plan clarified the two days are different exercises:

| Day | Task | Outcome | Depth |
|---|---|---|---|
| 3 — The SKILL.md structure | Design the folder structure and write the first version of a `SKILL.md` file | An **annotated skill template** | Draft/design — placeholders, no working content |
| 4 — Build your own skill | Implement your own Claude Skill and verify it performs the task | A **draft custom skill**, actually working | Full implementation, tested end-to-end |

Day 4 (already completed, in `../Day-4-Build-Your-Own-Skill/cv-reviewer/`) is the fully populated, verified version of a skill. Day 3's actual brief — done today — is the step that logically comes *before* that: a generic, reusable, **annotated** `SKILL.md` template that teaches skill anatomy, plus a deliberately-empty folder skeleton showing where content would go. Kept generic rather than CV-specific so this reads as "how to design any skill," distinct from Day 4's fully worked example.

---

## 🧠 1. What got built

- **`Structure-Template/SKILL.md`** — a first-draft, fill-in-the-blank skill template (`{{double-brace}}` placeholders, matching the convention already used in `cv-reviewer/assets/review-template.md`) covering every section a real `SKILL.md` needs: frontmatter, Purpose, Trigger/Non-Trigger conditions, Input/Output expectations, Workflow, Edge Cases, Constraints, a File Usage table, Best Practices, and Failure Handling. Annotated inline with `<!-- ANNOTATION -->` HTML comments at the exact point each design decision matters — invisible when rendered, visible in source, so the template stays usable as a real starting point and not just a lecture.
- **`Structure-Template/ANNOTATIONS.md`** — the linear, readable companion to those inline comments: what a skill actually is, the three-level progressive disclosure model, why `description` quality *is* trigger quality, the three trigger-type framework from Day 1 (object/intent/activity), why a "when NOT to trigger" section matters, the recommended `references/`/`scripts/`/`assets/` layout with a rationale for each folder, and why the body section order isn't arbitrary.
- **Three placeholder folders** (`references/`, `scripts/`, `assets/`) — each holding only a `README.md` stub stating the folder's purpose and pointing at Day 4's `cv-reviewer/` for what a fully populated version looks like. Deliberately empty of real content: Day 3's brief is the *shape*, not the substance — populating them is Day 4's job, already done.

---

## 🧪 2. Design choices worth calling out

- **Generic, not CV-specific.** Reusing `cv-reviewer` as the annotated example was considered and rejected — a generic template with placeholders teaches the *pattern*, whereas annotating an already-specific skill would teach one skill's specifics. `ANNOTATIONS.md` §9 explicitly points at `cv-reviewer/SKILL.md` for anyone who wants to see the pattern fully realized.
- **HTML comments for inline annotation, not a code fence.** Given the exact bug found and fixed on Day 4 (a `` ```markdown `` fence around a worked example silently became something the model could copy into real output), inline annotations here use `<!-- -->` HTML comments instead — invisible in rendered Markdown, so there's no risk of the same failure mode recurring, and the template file itself stays copy-paste-usable.
- **Folders present but empty, not omitted.** The brief says "design the folder structure" — so the folders themselves needed to exist (with a stated purpose) even though populating them with real references/scripts/assets is explicitly out of scope for this exercise.

---

## 📦 3. Deliverables produced today

1. **`Structure-Template/SKILL.md`** — annotated first-draft template (118 lines).
2. **`Structure-Template/ANNOTATIONS.md`** — linear skill-anatomy walkthrough (80 lines).
3. **`Structure-Template/references/README.md`**, **`scripts/README.md`**, **`assets/README.md`** — folder-purpose stubs, each cross-referencing the populated equivalent in Day 4's `cv-reviewer/`.
4. **`DAY3-REPORT.md`** — this report.

(Day 4's reflection questions — Daily Task Completed / What I Learned / Challenges Faced / How I Solved Them — were answered directly in conversation today rather than written into `DAY4-REPORT.md`, per the scope restriction keeping today's edits to `Structure-Template/` and this report only.)

---

## 🎓 4. Task core — what this exercise clarified

- **A template earns its keep by being usable, not just illustrative.** The `{{placeholder}}` + inline-comment approach means `Structure-Template/SKILL.md` can be copied directly as a starting point for a real skill, not just read as documentation about one.
- **Folder layout is a design decision, not boilerplate.** `ANNOTATIONS.md` §7 makes the point explicit: not every skill needs all three folders (`caveman` in `.claude/skills/` needs none of them) — the layout should match the task's actual complexity, decided at design time, which is exactly what Day 3 asks for before any implementation happens.
- **Lessons transfer forward, not just back.** The code-fence bug from Day 4 became a forward-looking annotation here (in both `SKILL.md`'s Output Format section and `ANNOTATIONS.md` §9) — a concrete example of a reference file's own formatting silently becoming an instruction, flagged at design time so a future skill author doesn't have to rediscover it the hard way.

---

## 🚀 Next steps

Day 4 (build + verify) and the reflection questions are already complete; Day 5's brief remains chaining `cv-reviewer` with a second skill and testing reliability through peer review — see `../Day-4-Build-Your-Own-Skill/DAY4-REPORT.md`'s "Next steps" section for the concrete plan. Nothing further is blocked on today's work; `Structure-Template/` stands on its own as a design reference for whichever skill gets built next.

---

## 📚 References

- **[`Structure-Template/SKILL.md`](Structure-Template/SKILL.md)** — the annotated first-draft template built today.
- **[`Structure-Template/ANNOTATIONS.md`](Structure-Template/ANNOTATIONS.md)** — the linear skill-anatomy walkthrough.
- **[`../Day-4-Build-Your-Own-Skill/cv-reviewer/SKILL.md`](../Day-4-Build-Your-Own-Skill/cv-reviewer/SKILL.md)** — the fully implemented, verified counterpart to this template.
- **[`../Day-4-Build-Your-Own-Skill/DAY4-REPORT.md`](../Day-4-Build-Your-Own-Skill/DAY4-REPORT.md)** — prior day's report, including the code-fence bug this template's annotations reference directly.
- **[`../Day-1-What-is-a-skill/DAY1-REPORT.md`](../Day-1-What-is-a-skill/DAY1-REPORT.md)** — source of the progressive-disclosure and trigger-type framing reused throughout `ANNOTATIONS.md`.
- **`.claude/skills/`** — the four official-style skills used as the structural reference point for what a minimal vs. fully-populated skill folder looks like.
