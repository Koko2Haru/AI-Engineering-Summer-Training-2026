# 📘 Day 4 Report — Build Your Own Skill

**🎯 Focus:** Authoring a complete, production-quality Claude Skill from scratch and verifying it actually performs the intended task — not reading or running someone else's

**📝 Assigned task (per the Week 4 plan):** *"Implement your own Claude Skill and verify that it performs the intended task successfully."* Built a fully structured Claude Skill (an AI CV/Resume Reviewer) inside `Day-4-Build-Your-Own-Skill/`, following the same conventions as the official skills studied on Days 1–2, with a `SKILL.md`, `references/`, `scripts/`, and `assets/`

**📅 Date:** 2026-07-22

**✅ Status:** Completed (bug found and fixed post-delivery)

---

## 🗂️ Folder structure

```
📁 Day-4-Build-Your-Own-Skill/
├── 📄 DAY4-REPORT.md              ← this report
└── 📁 cv-reviewer/
    ├── 📄 SKILL.md                ← trigger conditions, workflow, scoring methodology, file map
    ├── 📁 references/
    │   ├── 📄 scoring-rubric.md       ← per-category criteria, bands, weights
    │   ├── 📄 ats-best-practices.md   ← parser rules, common ATS failure patterns
    │   ├── 📄 resume-writing-guide.md ← section order, STAR/XYZ formula, length norms
    │   ├── 📄 action-verbs.md         ← verb bank by category + weak-phrase table
    │   └── 📄 common-mistakes.md      ← content/structural/grammar/ATS/branding checklist
    ├── 📁 scripts/
    │   ├── 📄 extract_text.py     ← PDF/DOCX/txt → raw text, image-PDF detection
    │   ├── 📄 helpers.py          ← section/bullet/quantification/weak-phrase regex analysis
    │   └── 📄 review_cv.py        ← orchestrator: extraction + helpers + scoring → JSON
    └── 📁 assets/
        ├── 📄 review-template.md  ← output skeleton (live Markdown, not fenced)
        ├── 📄 scoring-matrix.json ← machine-readable weights/bands
        └── 📄 report-example.md   ← fully worked sample report (calibration reference)
```

12 files, ~1,490 lines total.

---

## 🎯 Objective

This work was originally started under the Day 3 folder name, but a look back at the actual Week 4 plan makes clear it belongs here instead:

| Day | Task (per plan) | Outcome expected |
|---|---|---|
| 3 — The SKILL.md structure | *"Design the folder structure and write the first version of a SKILL.md file for a custom skill."* | An annotated skill **template** |
| 4 — Build your own skill | *"Implement your own Claude Skill and verify that it performs the intended task successfully."* | A **draft custom skill**, actually working |

Day 3's brief is a design/draft exercise — layout and a first-pass `SKILL.md`. What actually got produced is a fully implemented skill with real reference docs, runnable scripts, and end-to-end verification that it performs the intended task — squarely Day 4's brief, not Day 3's. Hence the folder rename: `Day-3-The-SKILL-md-Structure` → `Day-4-Build-Your-Own-Skill`, `DAY3-REPORT.md` → `DAY4-REPORT.md`. No links elsewhere in the repo pointed at the old path/name (checked: the root `README.md` only had unlinked `⏳ Day 3` / `⏳ Day 4` placeholders, and Day 2's report mentioned "Day 3" only in prose), so the rename was safe.

Days 1–2 were about reading and running other people's skills. Day 4 flipped that: design and build one, matching the architecture, tone, and rigor of the official skills already living in `.claude/skills/` (`caveman`, `experiment-designer`, `md-slides`, `product-manager-toolkit`) — studied first, then used as the structural template rather than guessing at conventions.

The brief specified an unusually large surface area for a single skill: 7 numeric scores, ~20 deep-dive analyses (technical/soft skills, projects, experience, education, achievements, keywords, missing sections, weak/strong bullets, repetition, verbs, quantification), a recruiter/hiring-manager persona layer, and a prioritized-improvements synthesis — all wrapped in the same four-part shape (`SKILL.md` / `references/` / `scripts/` / `assets/`) as the reference skills.

---

## 🧠 1. What got built

- **`SKILL.md`** — frontmatter (`name` + `description` only, matching the reference skills' minimal style, not over-engineered YAML) plus: purpose, explicit trigger and *non*-trigger conditions, input expectations (pasted text / PDF / DOCX / optional job description), a 7-step workflow, a weighted scoring methodology (`Overall = Σ category_score × weight`), a quick-reference rubric, 6 edge cases (non-English resumes, career gaps, academic CVs, students, already-strong resumes, no target role stated), constraints (never fabricate metrics, never hand out a hollow 100, no praise without a fix), a file-usage table, best practices, and failure handling.
- **5 reference docs** — the knowledge base the skill is instructed to consult *every time it scores something*, rather than inventing criteria on the fly: ATS parser mechanics, resume structure/STAR-XYZ formula, a categorized action-verb bank with a weak-phrase table, a common-mistakes checklist, and the master scoring rubric (bands + weights + per-category criteria checklists).
- **3 scripts** — a real, runnable mechanical layer, not placeholders: `extract_text.py` pulls text from PDF (via `pdfplumber`/`pypdf`, with graceful `ImportError` messages) or DOCX (via `python-docx`, including table cells) and flags low text-density as a likely scanned-image PDF; `helpers.py` does section detection, bullet extraction, quantification regex, weak-phrase/first-person detection, and word-repetition counting, stdlib-only; `review_cv.py` composes both plus `assets/scoring-matrix.json` into one JSON pass, explicitly marking judgment-only categories (Content Quality, Grammar, Readability, Visual/Layout) as `requires_manual_review` rather than faking a number the regex layer can't actually justify.
- **3 assets** — `scoring-matrix.json` (the same weights/bands from the rubric, machine-readable), `review-template.md` (the exact section skeleton the final report must follow), and `report-example.md` (a fully worked review of a fictional candidate, used to calibrate depth and tone — "match this quality bar, not just the headers").

---

## 🧪 2. Verification — every script actually run, not just written

| Script | Test | Result |
|---|---|---|
| `extract_text.py` | Ran against a sample `.txt` resume | Correct passthrough extraction |
| `extract_text.py` | Missing file | Clean `{"error": "No such file: ..."}`, exit 1 — no stack trace |
| `extract_text.py` | Unsupported extension (`.rtf`) | Clean rejection with the exact list of supported types |
| `helpers.py` | Same sample resume | Correctly found `experience`/`skills`, flagged `education` missing, caught all 4 weak-phrase bullets ("responsible for," "helped with," "worked on," "was in charge of"), flagged the one first-person slip, 0% quantification rate |
| `review_cv.py` | Same sample resume | Full JSON: ATS 90/Excellent, Impact 0/Poor, 4 other categories correctly deferred to manual review |
| Full suite | Re-run after the mid-session folder rename (`My-Skill-CV-Reviewer` → `cv-reviewer`) | Identical output — confirms no hardcoded folder-name paths anywhere in the scripts |

Generated `__pycache__` artifacts were deleted after each test pass so nothing untracked ships with the skill. This verification step is the actual crux of Day 4's brief ("verify that it performs the intended task successfully") — not an afterthought.

---

## 🐛 3. Real bug found and fixed: the fenced-example trap

After delivery, a screenshot showed `report-example.md`'s tables rendering as literal `| Category | Score | Band |` text instead of an actual table. Root cause: both `assets/report-example.md` and `assets/review-template.md` wrapped their sample content in a ` ```markdown ` code fence, intended only to make the *reference file itself* read unambiguously as "this is example content." Nothing told Claude that fence was a documentation convention rather than a formatting instruction — so it was fully plausible for a real report to inherit the same fence, flattening every table into pipe-delimited text exactly as shown.

**Fix, three-part:**
1. Removed the code fence from both asset files entirely — they now render as live Markdown, so opening either file directly shows real tables, not source text.
2. Demoted the example/template's internal heading levels by one (`#`→`##`, `##`→`###`, etc.) so they nest correctly under each file's own title instead of colliding with it or requiring the fence as a workaround.
3. Added an explicit **Rendering** rule to `SKILL.md`'s Output Format section: never wrap the final report in a code fence; match the heading levels and table structure shown in `review-template.md`/`report-example.md` directly.

This is the kind of defect that only surfaces by actually looking at rendered output, not by reading the Markdown source — consistent with Day 2's lesson that running a thing surfaces bugs that reading it never will, and exactly the kind of check Day 4's "verify it performs the intended task successfully" brief calls for.

---

## 🛠️ 4. How to test the skill — three ways

1. **Live, in a Claude conversation (the real test)** — paste resume text (or give a file path) and ask "review my resume" / "grade my CV out of 100." If the skill is registered (see #3), it auto-triggers off `SKILL.md`'s `description`; otherwise it can be invoked explicitly by pointing Claude at the `SKILL.md` path. This is the only path that exercises the actual judgment layer — scoring Content Quality, writing rewrites, the recruiter/hiring-manager read — since that reasoning lives in the model, not the scripts.
2. **Direct Python from a terminal (the mechanical layer only)** —
   ```powershell
   cd .../cv-reviewer/scripts
   python extract_text.py path\to\resume.txt   # or .pdf / .docx (needs pdfplumber / python-docx)
   python helpers.py path\to\resume.txt
   python review_cv.py path\to\resume.txt       # composes both, prints scored JSON
   ```
   This confirms section detection, quantification rate, and weak-phrase flags mechanically, but does **not** produce the final narrative report — `review_cv.py` deliberately marks 4 of 7 categories `requires_manual_review` instead of guessing.
3. **Register it as an auto-triggering skill** — copy or symlink `cv-reviewer/` into `.claude/skills/cv-reviewer/`, the same location as `caveman`/`experiment-designer`/`md-slides`/`product-manager-toolkit`, so it's picked up in any future conversation without manually pointing Claude at it. Not done yet — the skill currently lives only in the Week-4 exercise folder, un-registered.

---

## 📦 5. Deliverables produced today

1. **`cv-reviewer/SKILL.md`** — full skill specification (197 lines).
2. **`cv-reviewer/references/`** — 5 reference docs (ATS rules, writing guide, action verbs, common mistakes, scoring rubric; 381 lines combined).
3. **`cv-reviewer/scripts/`** — 3 runnable Python utilities, stdlib-only except optional PDF/DOCX extraction (522 lines combined), all verified end-to-end.
4. **`cv-reviewer/assets/`** — scoring matrix JSON, output template, and a fully worked example report (389 lines combined), both now fence-free and rendering correctly.
5. **`DAY4-REPORT.md`** — this report.

---

## 🎓 6. Task core — what the exercise actually taught

- **Progressive disclosure isn't just theory** — writing `SKILL.md` to consult `references/scoring-rubric.md` "every time a score is assigned" rather than restating the rubric inline is what keeps `SKILL.md` itself readable at 197 lines instead of 600.
- **Scripts should know their own limits.** `review_cv.py`'s decision to mark 4 categories `requires_manual_review` instead of hand-waving a number was the right call — a mechanical regex pass genuinely cannot judge Content Quality, and pretending otherwise would have produced a fake-precise, untrustworthy score.
- **A reference file's own formatting can silently become an instruction.** The code-fence bug is the clearest lesson of the day: an example meant purely for the file's own readability was structurally close enough to "the format to produce" that it leaked into behavior. The fix wasn't just removing the fence — it was making the *intent* of every remaining formatting choice explicit in `SKILL.md`, so nothing is left for the model to infer wrong.
- **"Verify it performs the intended task" is a real deliverable, not a footnote.** The bug above was only caught because the report's own worked example was inspected as rendered output, not just as source — the same principle the Day 4 brief names explicitly.

---

## 🚀 Next steps — Day 5 (Test & Chain Skills)

Per the plan, Day 5's brief is: *"Chain two skills together to complete a multi-step workflow. Test and improve reliability through peer review."*

- **Chain candidate:** feed `cv-reviewer`'s output into a second skill — e.g., pipe the "Top 10 Improvements" and rewritten bullets into `product-manager-toolkit`-style prioritization, or into a cover-letter-drafting step that reuses the same candidate/role context. Multi-step workflow: extract → score → rewrite → (new skill) draft supporting material.
- **Reliability testing:** run `cv-reviewer` against a few genuinely different resumes (not just the fictional Jordan Lee example) — a strong one, a career-changer, a student — to see where the rubric or scripts break down, the same way Day 2 surfaced real bugs in `product-manager-toolkit`/`experiment-designer`/`md-slides` only once fed real input.
- **Peer review:** since this is a solo exercise, "peer review" translates to a structured self-review pass — re-reading `SKILL.md` cold, as if seeing it for the first time, specifically hunting for the next code-fence-style ambiguity before it causes a second silent formatting bug.
- Also still open from before: register `cv-reviewer` into `.claude/skills/` so it participates in real auto-triggering, which the chaining exercise will need anyway.

---

## 📚 References

- **[`cv-reviewer/SKILL.md`](cv-reviewer/SKILL.md)** — the skill specification built today.
- **[`cv-reviewer/assets/report-example.md`](cv-reviewer/assets/report-example.md)** — the calibration example central to today's code-fence bug and fix.
- **[`DAY2-REPORT.md`](../Day-2-Using-Existing-Skills/DAY2-REPORT.md)** — prior day's report; today's fence bug is a direct continuation of its closing lesson ("running a thing surfaces bugs that reading it never will").
- **[`DAY1-REPORT.md`](../Day-1-What-is-a-skill/DAY1-REPORT.md)** — original skill-architecture reference this build followed (progressive disclosure, trigger-type framing).
- **`.claude/skills/`** — the four official-style skills (`caveman`, `experiment-designer`, `md-slides`, `product-manager-toolkit`) used as the direct structural/frontmatter template for `SKILL.md`.
