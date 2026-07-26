# 📘 Day 5 Report — Test & Chain Skills

**🎯 Focus:** Building a second skill designed to consume the first one's output, then proving the two-skill pipeline actually works end-to-end — not just that each skill works in isolation

**📝 Assigned task (per the Week 4 plan):** *"Chain two skills together to complete a multi-step workflow. Test and improve reliability through peer review."* Built `cv-optimizer` — a Claude Skill that takes the original CV plus `cv-reviewer`'s output (Day 4) and rewrites the resume without fabricating anything — then ran a full, real execution of the chain: sample CV → CV Reviewer → review report → CV Optimizer (including a live clarification round) → optimized CV + change report

**📅 Date:** 2026-07-26

**✅ Status:** Completed

---

## 🗂️ Folder structure

```
📁 Day-5-Test-and-Chain-Skills/
├── 📄 DAY5-REPORT.md                      ← this report
├── 📁 cv-optimizer/                       ← the second skill, chained after cv-reviewer
│   ├── 📄 SKILL.md                        ← triggers, clarification protocol, rewrite methodology, safety rules
│   ├── 📁 references/
│   │   ├── 📄 rewriting-guidelines.md         ← core methodology: factual audit, placeholder rules, question guidance
│   │   ├── 📄 ats-optimization.md             ← structural ATS fixes (fix-oriented, not just diagnostic)
│   │   ├── 📄 resume-writing-best-practices.md ← section order, length norms, tense/voice
│   │   ├── 📄 action-verbs.md                 ← verb bank + weak-phrase rewrite directions
│   │   ├── 📄 achievement-writing.md          ← XYZ formula, before/after patterns, quantification types
│   │   ├── 📄 resume-layout-guidelines.md     ← formatting-consistency mechanics
│   │   └── 📄 keyword-optimization.md         ← natural keyword integration, density guardrails
│   ├── 📁 scripts/
│   │   ├── 📄 rewrite_bullets.py          ← weak-phrase/quantification/passive-voice/first-person flagging
│   │   ├── 📄 ats_optimizer.py            ← non-standard headers, date-format, contact-info structural checks
│   │   ├── 📄 formatting_helper.py        ← bullet-character/spacing consistency checks
│   │   ├── 📄 optimize_keywords.py        ← resume-vs-job-description keyword coverage
│   │   └── 📄 improve_cv.py               ← orchestrator: composes all four + severity-ranks the findings
│   └── 📁 assets/
│       ├── 📄 optimized-template.md       ← output skeleton for the rewritten resume
│       ├── 📄 change-report-template.md   ← output skeleton for the change report
│       ├── 📄 rewrite-checklist.md        ← pre-delivery QA pass (fabrication/placeholder integrity)
│       ├── 📄 before-after-example.md     ← worked example, including a real clarification exchange
│       └── 📄 improvement-priorities.json ← severity weights consumed by improve_cv.py
└── 📁 Testing/                            ← the actual end-to-end chain run
    ├── 📁 Input/
    │   └── 📄 sample_cv.md                ← intentionally-weak fictional resume (Maria Torres)
    └── 📁 Output/
        ├── 📄 review-report.md            ← full CV Reviewer output (46/100, "Weak")
        ├── 📄 optimized-cv.md             ← rewritten resume, post-clarification
        └── 📄 optimization-report.md      ← full change report, incl. the clarification transcript
```

26 files, ~2,009 lines total (`cv-optimizer/` + `Testing/`).

---

## 🎯 Objective

Day 4 built one skill (`cv-reviewer`) and verified it in isolation. Day 5's brief asks for the next layer up: two skills that form an actual pipeline, plus real evidence the pipeline holds together rather than just existing on paper. The natural chain was already implied by `cv-reviewer`'s own design — it *diagnoses* a resume but deliberately never rewrites it — so the second skill, `cv-optimizer`, was scoped as the missing other half: consume a CV and (optionally) a review, and produce a truthful, strengthened rewrite plus a change report auditing exactly what changed and why.

The harder-to-fake part of "test and improve reliability" is the second half of the brief. It would have been easy to describe the chain in prose. Instead the actual pipeline was run for real: a fictional CV with deliberately-planted flaws was built, `cv-reviewer`'s own mechanical scripts (`helpers.py`, `review_cv.py`) were executed against it to ground a full manual review, `cv-optimizer`'s scripts (`improve_cv.py` and its four sub-checks) were run against the same CV to cross-validate the review's findings mechanically, and — the part most tempting to skip — when the optimizer's own clarification protocol determined it needed information the CV didn't contain, real questions were asked through `AskUserQuestion` and real answers were used, not invented, before the final rewrite was produced.

---

## 🧠 1. What got built — `cv-optimizer`

- **`SKILL.md`** (203 lines) — frontmatter matching `cv-reviewer`'s minimal style, then: purpose, trigger/non-trigger conditions explicitly distinguishing "rewrite" requests from "review" requests (so the two skills don't collide), input expectations (CV + optional review + optional job description), a two-artifact output format (Optimized Resume + Change Report), an 8-workflow-step process, a dedicated **User Clarification Protocol** section (when to ask vs. when to placeholder, question style rules, stop-early guidance), an 8-step rewrite methodology, hard **Safety Rules** (never invent employers/degrees/metrics/skills; bracket-placeholder convention for genuine gaps; the one explicit exception for user-requested suggestions), constraints, 7 edge cases, a file-usage table, best practices, and failure handling.
- **7 reference docs** — `rewriting-guidelines.md` is the load-bearing one: the factual-audit method, the "rewriting changes expression, never adds a fact" rule, placeholder conventions with a pattern table, and the full when-to-ask-vs-when-to-placeholder decision logic with example questions. The other six cover ATS *fixes* (not just diagnosis, unlike `cv-reviewer`'s ATS reference), section/length/tense conventions, a verb bank with weak-phrase rewrite directions, the XYZ achievement formula with three explicit bullet-outcome states, layout mechanics, and keyword integration with an explicit density/stuffing guardrail.
- **5 scripts, all stdlib-only** — `rewrite_bullets.py`, `ats_optimizer.py`, and `formatting_helper.py` are independent mechanical detectors (deliberately not importing from `cv-reviewer/scripts/`, since a skill folder should be self-contained); `optimize_keywords.py` compares resume text against a job description or an explicit keyword list; `improve_cv.py` orchestrates all four and severity-ranks the combined findings using `assets/improvement-priorities.json` — this is the piece that lets the optimizer build its own priority queue when no `cv-reviewer` output is supplied at all.
- **5 assets** — output templates for both required artifacts, a pre-delivery QA checklist (`rewrite-checklist.md`) built specifically to catch fabrication before it ships, a fully worked before/after example that deliberately includes *both* a resolved clarification-question case and a legitimate-placeholder case side by side, and the machine-readable severity config.

---

## 🧪 2. Verification — scripts run for real, not just written

| Script | Test | Result |
|---|---|---|
| `rewrite_bullets.py` | Sample resume text | Correctly flagged all weak phrases/verbs, 0% quantification, the one first-person slip, and the unsupported intensifier ("significantly") |
| `ats_optimizer.py` | Same sample | Correctly caught the non-standard `MY JOURNEY` header → suggested "Experience"; correctly flagged mixed date formats |
| `formatting_helper.py` | Same sample | Correctly flagged mixed bullet characters (`-` vs `*`) |
| `optimize_keywords.py` | Sample resume + a fabricated job description, then an explicit `--keywords` list | Both paths ran cleanly; coverage rates computed correctly (0.47 and 0.33 respectively); term-extraction heuristic pulled some noise ("looking," "tools," "like") alongside real terms — expected and disclosed in the script's own docstring as "heuristic, not exhaustive," the same honesty pattern `cv-reviewer`'s `review_cv.py` uses for judgment-only categories |
| `improve_cv.py` | Same sample, no JD | Correctly composed all three sub-scripts and severity-ranked the combined findings (`weak_or_unquantified_bullets` → high, `non_standard_section_header` → medium, `inconsistent_date_format` → medium, `inconsistent_bullet_characters` → low) |

Every finding from `cv-optimizer`'s independent scripts matched what the manual review (below) found by inspection — good cross-validation that the two skills' mechanical layers agree on the same underlying document without sharing code.

---

## 🔗 3. The actual chain run — `Testing/`

**Input (`Testing/Input/sample_cv.md`):** a fictional candidate, Maria Torres, built with every flaw the brief asked for deliberately planted: nine bullets, all duty-listing, zero quantification; a generic filler objective; a non-standard section header (`MY JOURNEY`) hiding an entire job from ATS parsing; mixed date formats and bullet characters; an informal email; a silent ~19-month employment gap; and a one-line project description with no tech stack or outcome.

**Step 1 — CV Reviewer → `review-report.md`:** Ran `cv-reviewer/scripts/helpers.py` and `review_cv.py` against the sample for a grounded mechanical pass, then layered the full qualitative review on top — all 7 category scores with rubric-justified reasoning (58 ATS, 40 Content Quality, 10 Impact, 62 Grammar, 63 Readability, 50 Visual/Layout, 45 Professionalism → 46 overall, "Weak"), the full deep-dive analysis, a weak-bullet table with suggested rewrite *patterns* (bracketed, per `cv-reviewer`'s own no-fabrication constraint), a keyword table, recruiter/hiring-manager perspective, and a prioritized Top 10 + Quick Wins list — matching `report-example.md`'s depth bar, not just its headers.

**Step 2 — CV Optimizer → clarification phase (the part that actually tests reliability):** Fed both the original CV and the review into `cv-optimizer`'s workflow. Per its own protocol, five gaps were judged high-value enough to ask about directly rather than placeholder immediately: target role, the API-performance and database-migration metrics, team-size scope for two people-facing bullets, and the unexplained employment gap. Two real rounds of `AskUserQuestion` were used — the first established *that* answers existed, the second extracted the actual concrete figures once it became clear the first round's option labels weren't capturing free-text specifics. Real answers came back: Backend/Software Engineer target, 35% API response-time improvement, ~2 million records migrated with zero downtime, 2 onboarded teammates, a ~10-person dashboard-adopting team, and an honest personal/family-leave framing for the gap.

**Step 3 — `optimized-cv.md` + `optimization-report.md`:** Every one of those five confirmed facts was used exactly as given — no rounding, no added scope. Everywhere ownership language could have crept ("helped with" → "Contributed to," never "Led," since the source never claimed sole ownership), the rewrite held the line. Seven remaining gaps that weren't asked about (Projects tech stack/outcome, PixelWorks bug count, testing method, contact links, Skills breadth) are marked as visible bracketed placeholders in the resume and re-listed in the change report's "Suggestions Requiring User Input" table — nothing was silently smoothed over. The change report also documents both clarification rounds verbatim, the non-standard-header fix, the removed low-signal bullet ("Participate in daily code reviews" — cut per the review's own suggested handling rather than padded), and an explicit refusal to fabricate a "professional" replacement email address, since the skill has no way to know what Maria actually owns.

---

## 🐛 4. Reliability observations — where the seams actually showed

- **`AskUserQuestion` with fixed option sets doesn't reliably extract free-text numbers.** Round 1 asked "do you have a number?" with a "yes, I'll specify via Other" option — the tool's answer only returns the selected option's label, not guaranteed follow-up text, so the first round confirmed *that* data existed without capturing *what* it was. Round 2 fixed this by making the concrete figures themselves the selectable options (e.g., "Reduced average response time by 35%") rather than routing through free text. **Lesson for future chains:** design clarification questions so the answer *is* the usable data, not a promise to provide it later.
- **A regex-based bullet extractor misses indented continuation lines.** `rewrite_bullets.py`'s bullet regex correctly caught "- Inventory Tracker App" as a line but not the vague description sentence beneath it (no leading bullet character), so the weakest sentence in the whole document — "Used some technologies to make it work." — was invisible to the mechanical pass and only caught by the manual review. Documented in the script's own docstring scope ("flagging pass, not exhaustive") rather than silently treated as complete; the manual layer is what actually caught it, same division of labor `cv-reviewer`'s `review_cv.py` already establishes for its own judgment-only categories.
- **Two independently-written scanners agreed.** `cv-reviewer`'s and `cv-optimizer`'s ATS/formatting scripts share no code (each skill folder is self-contained, per Day 4's practice) but flagged the identical `MY JOURNEY` header and identical mixed-date/mixed-bullet issues — real evidence the two skills' mechanical layers are consistent with each other, not just individually plausible.
- **The ownership-inflation trap is easy to fall into by accident.** A first draft of the optimized summary read "led a zero-downtime migration" — technically punchier, but the source CV only ever said "helped with," and the clarification answer added a record count, not a promotion in ownership. Caught and corrected to "contributed to" before the file was written — exactly the failure mode `references/rewriting-guidelines.md` names explicitly, and a good sign the guidance is specific enough to actually catch a real near-miss instead of just describing one in the abstract.

---

## 📦 5. Deliverables produced today

1. **`cv-optimizer/SKILL.md`** — full second-skill specification (203 lines).
2. **`cv-optimizer/references/`** — 7 reference docs (rewriting methodology, ATS fixes, writing best practices, action verbs, achievement writing, layout, keywords; 477 lines combined).
3. **`cv-optimizer/scripts/`** — 5 runnable, stdlib-only Python utilities (701 lines combined), all verified end-to-end against the sample CV.
4. **`cv-optimizer/assets/`** — 2 output templates, a pre-delivery checklist, a worked before/after example, and a severity-config JSON (250 lines combined).
5. **`Testing/Input/sample_cv.md`** — the deliberately-flawed fictional resume used to drive the whole chain test.
6. **`Testing/Output/review-report.md`**, **`optimized-cv.md`**, **`optimization-report.md`** — the actual, real output of running the two-skill pipeline end-to-end, including a genuine two-round clarification exchange.
7. **`DAY5-REPORT.md`** — this report.

---

## 🎓 6. Task core — what chaining two skills actually taught

- **A clean handoff contract matters more than either skill individually.** `cv-optimizer` only works well because its Input Expectations section names exactly what `cv-reviewer` produces (category scores, flagged bullets, Top 10/Quick Wins) and states what to do when that input is missing, contradictory, or stale — the chain's reliability lives in that contract, not in either skill's internal logic alone.
- **"Never fabricate" is a design constraint that has to survive contact with a genuinely tempting rewrite.** The "led" vs. "contributed to" near-miss above is the clearest proof this isn't just a line in `SKILL.md` — it's a check that has to actually fire mid-task, and it only fired because `rewriting-guidelines.md`'s self-check ("could the candidate defend this sentence, unprompted, in an interview?") was concrete enough to apply, not just aspirational.
- **Clarification questions are a UI problem, not just a policy problem.** Knowing *when* to ask (the protocol) turned out to be the easy half; getting a tool built around discrete option-selection to reliably carry free-text facts back into the workflow took a second round to get right. A chain's reliability depends on that mechanical detail as much as on the reasoning around it.
- **Independent verification beats a single mechanical pass.** Neither skill's scripts alone would have been trustworthy proof the chain works — it's the fact that two independently-written ATS/formatting scanners, plus a from-scratch manual review, all converged on the same findings that makes today's "Weak → confirmed, fixed" story actually credible rather than asserted.

---

## 🚀 Next steps

- **Register both skills** into `.claude/skills/` (still open from Day 4) so the chain can auto-trigger in a real conversation instead of needing to be invoked by folder path — this is what "peer review" would actually exercise against, since a cold reviewer wouldn't know to look in `Week-4-Using-and-Building-Claude-Skills/` first.
- **Extend `rewrite_bullets.py`** to catch indented continuation lines under a bulleted heading (the Inventory Tracker App gap found today), so the mechanical pass doesn't rely on the manual layer to catch the single vaguest sentence in a document.
- **Run the chain against a second, differently-shaped CV** (a strong resume that shouldn't need much rewriting, and a career-changer with a real narrative gap) — today's test proves the pipeline works on a document engineered to need every fix; a resume that's *already* good is the harder reliability test, since the failure mode there is manufacturing weaknesses that aren't real.
- **A third chain link is now plausible**: `optimization-report.md`'s "Suggestions Requiring User Input" table is already structured enough to feed a follow-up interview-prep or cover-letter-drafting skill that reuses the same confirmed facts (target role, the 35% metric, the 2M-record migration) without re-asking for them.

---

## 📚 References

- **[`cv-optimizer/SKILL.md`](cv-optimizer/SKILL.md)** — the second skill's full specification.
- **[`cv-optimizer/references/rewriting-guidelines.md`](cv-optimizer/references/rewriting-guidelines.md)** — the core no-fabrication methodology central to today's "led vs. contributed to" near-miss.
- **[`Testing/Output/review-report.md`](Testing/Output/review-report.md)** — the CV Reviewer's real output that seeded the chain.
- **[`Testing/Output/optimized-cv.md`](Testing/Output/optimized-cv.md)** and **[`optimization-report.md`](Testing/Output/optimization-report.md)** — the CV Optimizer's real output, including the clarification transcript.
- **[`../Day-4-Build-Your-Own-Skill/cv-reviewer/SKILL.md`](../Day-4-Build-Your-Own-Skill/cv-reviewer/SKILL.md)** — the first half of the chain, built and verified on Day 4.
- **[`../Day-4-Build-Your-Own-Skill/DAY4-REPORT.md`](../Day-4-Build-Your-Own-Skill/DAY4-REPORT.md)** — prior day's report; today's chain is its named "Next steps" plan carried out.
- **`.claude/skills/`** — the four official-style skills whose conventions both `cv-reviewer` and `cv-optimizer` follow.
