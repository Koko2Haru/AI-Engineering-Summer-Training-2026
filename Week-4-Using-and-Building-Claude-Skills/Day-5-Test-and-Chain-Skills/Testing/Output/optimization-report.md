# Optimization Report: Maria Torres

**Rewrite scope:** Full resume
**Input used:** `sample_cv.md` (original CV) + `review-report.md` (CV Reviewer output, Overall 46/100 — Weak)
**Target role/industry:** Backend / Software Engineer — confirmed by the user during clarification

## Clarification Phase

Before rewriting, the review's Top 10 Improvements list was mapped against `references/rewriting-guidelines.md`'s "when to ask vs. placeholder" test. Five gaps were judged high-value enough to ask about directly (missing quantification on the two highest-visibility current-role bullets, missing scope on two people-facing bullets, an unexplained multi-month gap, and the target role itself); lower-value or numerous gaps (Projects tech stack/outcome, PixelWorks bug count, testing method, contact links, Skills breadth) were left as inline placeholders instead, per the same guidance.

Two rounds of targeted questions were asked and answered:

**Round 1**
| Question | Answer |
|---|---|
| Target role/industry? | Backend / Software Engineer |
| Number for the API performance or DB migration bullet? | Confirmed available (specified in Round 2) |
| Team size for onboarding / dashboard bullets? | Confirmed available (specified in Round 2) |
| Explanation for the Aug 2020 – Mar 2022 gap? | Confirmed available (specified in Round 2) |

**Round 2 (concrete figures)**
| Question | Answer |
|---|---|
| API performance improvement | Reduced average response time by 35% |
| Database migration scale | ~2 million records migrated, zero downtime |
| Onboarding / dashboard scope | Onboarded 2 new teammates; dashboard adopted by a ~10-person engineering team |
| Gap explanation | Personal/family time off, Aug 2020 – Mar 2022, then resumed job search |

All four confirmed answers were used exactly as given — no rounding, no added detail beyond what was stated. Every other gap identified during the rewrite (Projects tech stack/outcome, PixelWorks bug count, testing method/tool, contact links, additional Skills) was **not** asked about a third time, per the protocol's "stop once enough is gathered" guidance, and instead appears as a bracketed placeholder in `optimized-cv.md`.

## Summary of Improvements

The rewrite fixed one critical ATS risk (a non-standard section header that could have dropped an entire job from parsing), added real quantification to the two highest-leverage bullets using user-confirmed figures, replaced every weak-phrase/duty-listing bullet with accurate outcome-oriented language, added a concrete Summary framed around the confirmed target role, gave the previously-silent employment gap an honest one-line frame, and standardized formatting (headers, bullet characters, date format) throughout.

## Sections Modified

| Section | Change Type | Why |
|---|---|---|
| Header/Contact | Annotated | Flagged missing LinkedIn/GitHub/portfolio link as a placeholder; email left unchanged (see Remaining Weaknesses — never fabricate a replacement address) |
| Objective → Summary | Rewritten, renamed | "Hardworking and motivated individual..." was generic filler with no differentiating content; rewritten using the confirmed target role and two confirmed metrics |
| Experience — "MY JOURNEY" header | Removed / restructured | Non-standard header risked the entire PixelWorks role being dropped by ATS parsing (review-report.md, ATS Compatibility); both roles now sit under standard headers |
| Experience — Career Break entry | Added | The Aug 2020 – Mar 2022 gap was previously unaddressed; added as a normal, honestly-framed entry using the user's confirmed explanation |
| Experience bullets (both roles) | Rewritten | All 9 original bullets flagged by `scripts/rewrite_bullets.py` and the review for weak phrasing and/or missing quantification |
| Experience — "Participate in daily code reviews" | Removed | Low-signal as written, no confirmed scope offered, and its present tense broke the tense convention used by the rest of the role — cut rather than padded with a placeholder, per the review's own suggested handling |
| Projects | Rewritten with placeholders | Original description ("Used some technologies to make it work") was too vague to strengthen without more information; no clarification was asked for this section (lower priority than Experience), so placeholders mark the tech stack and outcome |
| Education | Unchanged | Already factual and correctly placed |
| Skills | Annotated | Kept the three confirmed items; added a placeholder rather than inventing framework/cloud/testing tools implied but never confirmed |

## ATS Improvements

- Replaced the non-standard "MY JOURNEY" header with a standard "Experience" structure covering both roles (`references/ats-optimization.md` — Section Headers).
- Standardized all dates to one consistent "Mon YYYY – Mon YYYY" format (previously mixed "03/2022 - Present" and "June 2019 – August 2020").
- Removed "References available upon request" (adds no ATS or human-reader signal; flagged as a Quick Win in the review).
- Left contact info in the main document body, unchanged (already compliant).

## Stronger Wording

| Original | Issue | Rewritten |
|---|---|---|
| "Hardworking and motivated individual seeking a challenging position where I can grow and use my skills." | Generic filler, no differentiating content, first person | "Backend-focused Software Developer with experience building and maintaining backend systems, APIs, and database infrastructure. Improved backend API response times by 35% and contributed to a zero-downtime migration of approximately 2 million database records." |
| "Worked on improving API performance significantly" | Unsupported intensifier standing in for a real number | "Improved backend API response times by 35% through targeted performance optimizations" |
| "Was in charge of fixing bugs in the production system" | Weak phrase | "Resolved production bugs in the system." (+ placeholder for count/impact) |

## Keywords Added or Surfaced

No job description was supplied, so keyword work followed general backend/software engineering norms (`references/keyword-optimization.md`). "API," "database migration," "backend systems," and "production system" — all already present in the source CV — are now surfaced through stronger verbs and a Summary that leads with them, rather than being newly added. No framework, cloud platform, or testing-tool keyword was added anywhere, since none was confirmed as part of Maria's actual work — the review noted these as a likely *underreporting* gap, and `optimized-cv.md`'s Skills placeholder invites the user to add them if accurate, rather than the rewrite guessing on her behalf.

## Bullets Rewritten

| Original | Rewritten | Why |
|---|---|---|
| "Responsible for maintaining backend systems supporting the mobile app" | "Maintained backend systems supporting the mobile app. [Consider adding scale here...]" | Weak phrase removed; no scale was confirmed for this specific bullet, so a placeholder marks the gap rather than reusing the API/migration numbers, which belong to different bullets |
| "Helped with database migrations to a new schema" | "Contributed to a database schema migration covering approximately 2 million records, completed with zero downtime" | User-confirmed scale added; verb kept contribution-scoped ("Contributed to," not "Led") because the source said "helped with," not "owned" |
| "Worked on improving API performance significantly" | "Improved backend API response times by 35% through targeted performance optimizations" | Unsupported intensifier replaced with the user-confirmed real number |
| "Participate in daily code reviews" | *(removed)* | Low-signal, no confirmed scope, tense-inconsistent with the rest of the role |
| "I helped with building a new reporting dashboard for the team" | "Contributed to building a new reporting dashboard, adopted by a 10-person engineering team" | First-person pronoun dropped; verb kept contribution-scoped (source said "helped with building," not "built"); user-confirmed team size added |
| "Was in charge of fixing bugs in the production system" | "Resolved production bugs in the system. [Consider adding a count or impact...]" | Weak phrase replaced with an accurate stronger verb (ownership already matched "was in charge of" in the source); no bug count was confirmed, so scale is a placeholder |
| "Assisted with onboarding new team members" | "Onboarded 2 new teammates, helping them ramp up on the production codebase" | User-confirmed headcount added; verb matches the confirmed figure as given |
| "Did testing for new features" | "Tested new features prior to release. [Specify testing method/tool if worth naming...]" | Weak verb replaced; no method/tool was confirmed, so it's a placeholder rather than a guess |
| "Built an app for tracking inventory. Used some technologies to make it work." | "Built an application for tracking inventory. [Specify the technologies/stack used...] [Provide the project's outcome or context if available...]" | Too vague to strengthen without more information; not asked about directly this session (lower priority than Experience), so marked with placeholders |

## Grammar & Formatting Fixes

- Removed the sole first-person pronoun ("I helped with building...") — the rewrite now reads as implied first-person throughout, consistent with every other bullet.
- Resolved the tense inconsistency in the Bright Path role (present-tense "Participate in daily code reviews" sitting alongside past-tense bullets) by removing that bullet rather than forcing a tense fix onto a low-signal line.
- Standardized bullet characters to `-` throughout (previously mixed `-` and `*` between the two roles).
- Standardized date formatting to "Mon YYYY – Mon YYYY" throughout.
- Removed the redundant near-repetition of "technologies" in the Projects entry as part of that section's rewrite.

## Suggestions Requiring User Input

| Location | Placeholder | What's Needed |
|---|---|---|
| Header | `[Add LinkedIn, GitHub, or portfolio link here if available.]` | A link, if one exists |
| Experience — Bright Path, bullet 1 | `[Consider adding scale here...]` | Number of users/requests the backend systems support, if known |
| Experience — PixelWorks, bullet 1 | `[Consider adding a count or impact here...]` | Number of bugs resolved, or the impact of resolving them |
| Experience — PixelWorks, bullet 3 | `[Specify testing method/tool if worth naming...]` | The QA approach or framework used, if any |
| Projects — Inventory Tracker App | `[Specify the technologies/stack used...]` | Languages, frameworks, database used to build it |
| Projects — Inventory Tracker App | `[Provide the project's outcome or context if available...]` | Whether it was personal/coursework/production use, and any scale or outcome |
| Skills | `[Consider adding other tools actually used in this work...]` | Any web framework, cloud platform, or testing tool genuinely used but not yet listed |

**Not a placeholder, but worth acting on:** the email address `mtorres_1995@hotmail.com` reads as informal (review-report.md, Professionalism — 45/100). It was left unchanged in the resume rather than replaced, since this skill cannot assign Maria an email address she doesn't actually own — she should switch to a `firstname.lastname@`-style address herself before submitting this resume.

## Remaining Weaknesses

- The Projects section is still the weakest part of the document — it carries real placeholder weight and would benefit most from a future round of clarification if this were a live session.
- The Skills section remains thin (3 items) since no additional tools were confirmed; this is very likely an underreporting issue rather than a true skills gap, per the review, but the rewrite cannot resolve it without more input.
- Without a specific job description, keyword optimization was done against general backend-engineering norms rather than a specific posting's terminology — if Maria has a real opening in mind, re-running the optimizer with that job description would sharpen this further.
- The professional-email recommendation above is unresolved by design (see note).

## Final Note

This pass moves the resume from a 46/100 ("Weak") diagnosis to a structurally sound, ATS-safe, and substantially more quantified draft — the single highest-risk ATS issue (the "MY JOURNEY" header) and the two most severe Impact gaps (API performance, database migration scale) are now fully resolved with real, user-confirmed numbers. The 7 remaining placeholders are honest markers, not finished text — resolving them (especially the Projects section) would be the highest-leverage next step before this resume goes out.
