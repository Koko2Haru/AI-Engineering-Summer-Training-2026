# Optimization Report: Maria Torres

*Re-run of the Day-5 chain test, `cv-optimizer` half. This version replaces an earlier draft of this file that wrongly reused clarification answers from the original Day-5 test instead of actually asking. This one uses real, freshly-gathered answers — two of which (API performance, migration scale) contradict the reused data, which is exactly why reusing it was the wrong call.*

**Rewrite scope:** Full resume
**Input used:** `Testing-v2/Input/sample_cv.md` (original CV) + `Testing-v2/Output/review-report.md` (CV Reviewer output, Overall 46/100 — Weak, including its Live Intake Q&A)
**Target role/industry:** Backend / Software Engineer — confirmed live

## Clarification Phase

Two real rounds of `AskUserQuestion` were run, answering on Maria's behalf, mirroring the pattern the original Day-5 test established:

**Round 1 — reviewer-level intake (`references/intake-questions.md`), also feeding the optimizer's gap scan**
| Question | Answer |
|---|---|
| Target role | Backend / Software Engineer |
| Actual tech behind the vaguest bullets (Inventory Tracker App, "backend systems") | Python/Django + MySQL |
| Tools used but not listed | Confirmed: a web framework (Django) + basic AWS |
| Anything indefensible in an interview | Confirmed: the "significantly" in the API-performance bullet — no real number was ever tracked |

**Round 2 — optimizer-level fact gaps**
| Question | Answer |
|---|---|
| API-performance estimate, given no exact number | No usable estimate — stays a placeholder |
| Database migration scale | ~500,000 records, completed during a scheduled maintenance window (**not** zero-downtime) |
| Team scope (onboarding / dashboard bullets) | Onboarded 2 teammates; dashboard adopted by a ~10-person team |
| Aug 2020 – Mar 2022 gap | Freelance/contract work, not reflected elsewhere on the CV |

**Two of these answers genuinely overturn what an earlier draft of this file had assumed** (having wrongly reused the original test's fixture answers instead of asking fresh): the API-performance bullet does **not** get a number — "35%" from the earlier draft was never actually confirmed this run, and inventing consistency with a prior test run would have been exactly the kind of fabrication `references/rewriting-guidelines.md` exists to prevent. Likewise, the migration was confirmed at ~500K records with a maintenance window, not ~2M with zero downtime. Both corrections are reflected throughout this report and in `optimized-cv.md`.

The gap framing also changed in kind, not just detail: "freelance/contract work" isn't a silence to explain away, it's real professional activity that belongs on the resume as its own entry — so the rewrite adds a **Freelance / Contract Developer** entry rather than a passive "Career Break" line. Its specifics (client, project, scope) weren't asked about this round — per the protocol's "stop once enough is gathered" guidance, that's left as a placeholder rather than a third round of questions.

## Summary of Improvements

Fixed the one critical ATS risk (the "MY JOURNEY" non-standard header); resolved the Projects entry's tech-stack gap and the Skills section's missing-tools gap using confirmed facts (Django, MySQL, AWS); added a real, defensible figure to the migration bullet; correctly left the API-performance bullet unquantified rather than inventing a number; replaced every weak-phrase/duty-listing bullet with accurate outcome-oriented language; added a new Freelance/Contract entry to honestly account for the previously-silent gap; and standardized formatting (headers, bullet characters, date format) throughout.

## Sections Modified

| Section | Change Type | Why |
|---|---|---|
| Header/Contact | Annotated | Flagged missing LinkedIn/GitHub/portfolio link as a placeholder; email left unchanged (see Remaining Weaknesses) |
| Objective → Summary | Rewritten, renamed | Generic filler replaced with confirmed target role + confirmed stack (Django/MySQL/AWS) + the one confirmed metric (migration scale). Does **not** claim an API-performance improvement, since none was confirmed |
| Experience — "MY JOURNEY" header | Removed / restructured | Non-standard header risked the entire PixelWorks role being dropped by ATS parsing; both roles now sit under standard headers |
| Experience — Freelance/Contract entry | Added (new) | The Aug 2020 – Mar 2022 gap is real professional work, not a break — added as its own entry rather than a passive framing |
| Experience bullets (both roles) | Rewritten | All 9 original bullets flagged for weak phrasing and/or missing quantification; 2 gained confirmed real figures, 1 (API performance) correctly stays a placeholder |
| Experience — "Participate in daily code reviews" | Removed | Low-signal, no confirmed scope, tense-inconsistent, fails the review's So-What Test |
| Projects | Rewritten, tech stack resolved | Confirmed as Python/Django/MySQL — no longer a placeholder; outcome/scope still unconfirmed and remains one |
| Education | Unchanged | Already factual and correctly placed |
| Skills | Rewritten, resolved | Django and AWS (basic) added as confirmed; MySQL named specifically instead of generic "SQL" |

## ATS Improvements

- Replaced the non-standard "MY JOURNEY" header with a standard "Experience" structure covering both roles.
- Standardized all dates to one consistent "Mon YYYY – Mon YYYY" format.
- Removed "References available upon request."
- Left contact info in the main document body, unchanged (already compliant).

## Stronger Wording

| Original | Issue | Rewritten |
|---|---|---|
| "Hardworking and motivated individual seeking a challenging position where I can grow and use my skills." | Generic filler, first person, no real content | "Backend-focused Software Developer with experience building and maintaining backend systems using Python, Django, and MySQL, with basic AWS exposure. Contributed to a database schema migration covering approximately 500,000 records during a scheduled maintenance window." |
| "Worked on improving API performance significantly" | Unsupported intensifier; live intake confirmed no number was ever tracked | "Investigated and applied targeted performance optimizations to backend API endpoints. [Add a measurable outcome here if available...]" — deliberately **not** given a number |
| "Built an app for tracking inventory. Used some technologies to make it work." | Fails the So-What Test; no tech stack named | "Built an inventory tracking application using Python, Django, and MySQL. [Provide the project's outcome or context if available...]" |

## Keywords Added or Surfaced

No job description was supplied, so keyword work followed general backend/software engineering norms. "Django," "MySQL," and "AWS" are newly surfaced in Skills and the Summary — all confirmed live, not guessed from the target role. "API," "database migration," and "backend systems" (already present in the source) are surfaced through stronger verbs.

## Bullets Rewritten

| Original | Rewritten | Why |
|---|---|---|
| "Responsible for maintaining backend systems supporting the mobile app" | "Maintained backend systems supporting the mobile app using Python and Django. [Consider adding scale here...]" | Weak phrase removed; confirmed tech stack named; scale still unconfirmed |
| "Helped with database migrations to a new schema" | "Contributed to a database schema migration covering approximately 500,000 records, completed during a scheduled maintenance window" | Confirmed scale added; verb kept contribution-scoped ("Contributed to," not "Led"); "zero downtime" dropped since it was never confirmed — "scheduled maintenance window" is what was actually confirmed |
| "Worked on improving API performance significantly" | "Investigated and applied targeted performance optimizations to backend API endpoints. [Add a measurable outcome here if available...]" | Confirmed live that no number exists — inventing one (including reusing the unrelated "35%" from a different test run) would be exactly the fabrication `references/rewriting-guidelines.md` forbids |
| "Participate in daily code reviews" | *(removed)* | Low-signal, no confirmed scope, tense-inconsistent, fails the So-What Test |
| "I helped with building a new reporting dashboard for the team" | "Contributed to building a new reporting dashboard, adopted by a 10-person engineering team" | First-person dropped; verb kept contribution-scoped; confirmed team size added |
| "Was in charge of fixing bugs in the production system" | "Resolved production bugs in the system. [Consider adding a count or impact...]" | Weak phrase replaced; no bug count was confirmed, so scale is a placeholder |
| "Assisted with onboarding new team members" | "Onboarded 2 new teammates, helping them ramp up on the production codebase" | Confirmed headcount added |
| "Did testing for new features" | "Tested new features prior to release. [Specify testing method/tool if worth naming...]" | Weak verb replaced; no method/tool confirmed, so it's a placeholder |
| "Built an app for tracking inventory. Used some technologies to make it work." | "Built an inventory tracking application using Python, Django, and MySQL. [Provide the project's outcome or context if available...]" | Tech stack confirmed live and resolved; outcome/scope still unconfirmed |
| *(no prior equivalent — new entry)* | "Completed freelance and contract development work. [Specify client, project scope, or technologies used if available.]" | The employment gap is confirmed as real freelance work, not a break — added as its own entry; specifics weren't asked about this round, so it's a placeholder |

## Grammar & Formatting Fixes

- Removed the sole first-person pronoun.
- Resolved the tense inconsistency by removing the low-signal "Participate in daily code reviews" bullet.
- Standardized bullet characters to `-` throughout.
- Standardized date formatting to "Mon YYYY – Mon YYYY" throughout.
- Removed the redundant near-repetition of "technologies" in the Projects entry.

## Suggestions Requiring User Input

| Location | Placeholder | What's Needed |
|---|---|---|
| Header | `[Add LinkedIn, GitHub, or portfolio link here if available.]` | A link, if one exists |
| Experience — Bright Path, bullet 1 | `[Consider adding scale here...]` | Number of users/requests the backend systems support, if known |
| Experience — Bright Path, bullet 3 (API) | `[Add a measurable outcome here if available...]` | Confirmed live that no number was ever tracked — this needs actual measurement, not just a better memory of one |
| Experience — Freelance/Contract entry | `[Specify client, project scope, or technologies used if available.]` | What the freelance work actually involved |
| Experience — PixelWorks, bullet 1 | `[Consider adding a count or impact here...]` | Number of bugs resolved, or the impact of resolving them |
| Experience — PixelWorks, bullet 3 | `[Specify testing method/tool if worth naming...]` | The QA approach or framework used, if any |
| Projects — Inventory Tracker App | `[Provide the project's outcome or context if available...]` | Whether it was personal/coursework/production use, and any scale or outcome |

**Not a placeholder, but worth acting on:** the email address `mtorres_1995@hotmail.com` reads as informal. Left unchanged — this skill cannot assign Maria an email address she doesn't actually own.

## Remaining Weaknesses

- The API-performance bullet genuinely has no quantified outcome behind it — that's now a confirmed fact about the underlying work, not just an unconfirmed gap, and no amount of further rewriting can fix that without Maria actually measuring something.
- The new Freelance/Contract entry is thin — one more clarification round on client/scope would meaningfully strengthen it.
- The Projects section's outcome/scope remains unconfirmed.
- The professional-email recommendation is unresolved by design.

## Reliability note (this re-run vs. the original Day-5 run and vs. this file's own earlier draft)

Scores on the as-submitted CV are unchanged (still 46/100 — nothing about the source document changed). What's different from the *original* Day-5 run: real, freshly-gathered facts instead of a reused fixture, which surfaced a genuine new CV move (the freelance entry) the original run's "career break" framing never considered. What's different from *this file's own first draft*: that draft skipped live intake and reused old answers wholesale, including a 35%-improvement figure and a zero-downtime migration claim that this round's real answers directly contradict. Catching that — rather than shipping a resume with a plausible-sounding invented number — is the entire point of the no-fabrication safety rule, and it only worked because intake actually ran this time.

## Final Note

This pass moves the resume from a 46/100 ("Weak") diagnosis to a structurally sound, ATS-safe draft with real, confirmed figures where they exist (the migration, the team scope) and honest placeholders where they don't (the API-performance bullet, above all). 7 placeholders remain — honest markers, not finished text.
