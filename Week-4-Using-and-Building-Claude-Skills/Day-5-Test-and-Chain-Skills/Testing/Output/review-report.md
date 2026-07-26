# CV Review: Maria Torres

**Overall Score: 46/100 — Weak**
**Reviewed as:** Entry-to-early-career Software/Backend Developer (0-3 years experience) — no target role or job description was supplied, so this assumption is based on the candidate's own job titles and stack; let me know if a different target role should be used.
**One-line verdict:** The underlying trajectory (two real developer roles, a personal project, a relevant degree) is being actively hidden by duty-listing bullets, zero quantification, a rogue non-standard section header that risks dropping an entire job from ATS parsing, and formatting inconsistencies throughout — this is a fixable rewrite, not a thin-experience problem.

### Score Summary

| Category | Score | Band |
|---|---|---|
| ATS Compatibility | 58/100 | Weak |
| Content Quality | 40/100 | Weak |
| Impact | 10/100 | Poor |
| Grammar & Spelling | 62/100 | Adequate |
| Readability | 63/100 | Adequate |
| Visual / Layout | 50/100 | Weak |
| Professionalism | 45/100 | Weak |
| **Overall** | **46/100** | **Weak** |

---

### Category Breakdown

#### ATS Compatibility — 58/100
The document is plain, single-column text with no tables, graphics, or text boxes — a clean baseline. But one structural issue is severe enough to cap this score well below "Strong": the second job (PixelWorks Studio) is filed under a custom header, **"MY JOURNEY,"** instead of continuing under "Experience." Most ATS platforms parse fields by matching literal, standard section headers — a header like this is not recognized as an Experience-type section by pattern-matching parsers, which creates real risk that the entire PixelWorks role (and its dates, for tenure/gap calculations) is dropped from the parsed candidate profile entirely.

**Working well:** No tables, columns, images, or text-box content; contact info (email, phone) sits in the document body, not a header/footer; standard headers used for Objective, Experience (first job), Projects, Education, and Skills.
**Needs improvement:** Replace "MY JOURNEY" with "Experience" (or fold both jobs under one shared "Experience" header); standardize date formatting, which currently mixes "03/2022 - Present" (slash format) with "June 2019 – August 2020" (full month name) — inconsistent date formats are a common source of ATS tenure/gap-calculation errors.
**Evidence:** `MY JOURNEY` appears as a standalone header directly above "Junior Developer, PixelWorks Studio" — this is exactly the kind of creative section rename that ATS pattern-matching does not reliably recognize.

#### Content Quality — 40/100
Every experience bullet describes an assigned duty rather than an outcome, and the one differentiating asset in the document — a personal project — is described in language too vague to convey any actual skill.

**Working well:** The role progression (Junior Developer → Software Developer) is a plausible, relevant story for an early-career software engineer, and the stack implied (backend systems, databases, APIs) is coherent for that target.
**Needs improvement:** Every bullet in both roles opens with a flagged weak phrase ("Responsible for," "Helped with," "Worked on," "Was in charge of," "Assisted with," "Did"); the Projects section entry gives no indication of what the app actually does technically.
**Evidence:** "Built an app for tracking inventory. Used some technologies to make it work." — this sentence could describe almost any project of any complexity; a technical screener gets zero signal from it.

#### Impact — 10/100
Zero of the nine bullets in this document contain a number, percentage, dollar figure, or concrete scale indicator of any kind.

**Working well:** N/A — this is the report's lowest-scoring category, and fixing it is the single highest-leverage change available.
**Needs improvement:** Every bullet needs at least an attempt at quantification — scale (how many users, how many records, how large a team), frequency, or time saved would all work if an exact percentage isn't available.
**Evidence:** "Worked on improving API performance significantly" — "significantly" reads as an attempt at impact language but contains no actual number, which is a common trap: it sounds quantified without being checkable.

#### Grammar & Spelling — 62/100
No spelling errors were found, but tense is inconsistent within the current role, and one bullet breaks the implied-first-person convention used everywhere else.

**Working well:** Clean spelling throughout; past tense used consistently within the PixelWorks (past role) entry.
**Needs improvement:** Within the current Bright Path role, "Participate in daily code reviews" (present tense) sits alongside "Helped with database migrations" and "Worked on improving API performance" (both past tense) — pick one convention for ongoing-role bullets and apply it throughout that entry.
**Evidence:** "I helped with building a new reporting dashboard for the team" — the only bullet in the document written in explicit first person; should read "Helped build..." or, if scope was larger than "helped," a stronger accurate verb.

#### Readability — 63/100
Bullets are short and scannable, but several are too vague for a reader to picture what actually happened.

**Working well:** No dense paragraphs — every bullet is a single line; logical section grouping overall.
**Needs improvement:** "Worked on improving API performance significantly" and "Used some technologies to make it work" both need at least one concrete detail (which system, which specific technologies) to be understandable as anything beyond filler.
**Evidence:** "Used some technologies to make it work" is the single vaguest line in the document — it communicates literally nothing to the reader.

#### Visual / Layout — 50/100
Formatting is inconsistent in two visible ways: bullet characters switch from `-` (Bright Path, Projects) to `*` (PixelWorks), and the rogue "MY JOURNEY" header breaks the document's visual hierarchy by inserting an unexpected top-level heading mid-Experience.

**Working well:** Reasonable overall length for an early-career candidate (comfortably fits one page); no orphaned lines detected.
**Needs improvement:** Standardize on one bullet character throughout; fold "MY JOURNEY" back into a single consistent "Experience" section; group the (currently very short) Skills list by category once it's expanded, so it doesn't read as an afterthought.
**Evidence:** `- Responsible for maintaining backend systems...` (Bright Path, dash) vs. `* Was in charge of fixing bugs...` (PixelWorks, asterisk) — two different bullet characters used in the same document.

#### Professionalism — 45/100
Three separate signals compound here: an informal-reading email handle, a first-person slip, and a nearly two-year employment gap presented with no acknowledgment at all.

**Working well:** No inappropriate personal information present (no age, photo, marital status, home address).
**Needs improvement:** `mtorres_1995@hotmail.com` reads as a personal, birth-year-style handle rather than a professional address; a `firstname.lastname@`-style Gmail address would remove this friction in minutes. The gap between PixelWorks ending (August 2020) and Bright Path starting (March 2022) — roughly 19 months — is currently silent; a gap itself isn't disqualifying, but leaving it completely unaddressed can read as evasive to a careful reader. "References available upon request" is a universally-assumed, space-wasting line worth cutting.
**Evidence:** August 2020 → March 2022 gap sits between the two experience entries with no framing of any kind.

---

### Deep-Dive Analysis

#### Technical Skills Evaluation
The listed stack — Python, SQL, Git — is plausible for a backend-leaning developer but extremely thin: three items total, with no frameworks, cloud/infrastructure, testing, or CI/CD tooling named anywhere, despite the Experience bullets referencing "backend systems," "database migrations," and "API performance" work that almost certainly involved more specific tools than what's listed. This is very likely an underreporting problem, not a true skills gap — the fix is to surface tools already used in the actual work, not to learn new ones.

#### Soft Skills Evaluation
No bare soft-skill tag list is present (a plus — Maria didn't pad the document with "Team Player" style tags), but there's also no bullet that clearly demonstrates leadership, mentorship, or collaboration depth. "Assisted with onboarding new team members" gestures at this but, as written, undersells whatever the actual contribution was.

#### Project Quality Analysis
One project is listed (Inventory Tracker App) and it is currently the weakest-written entry in the whole document — no tech stack, no scale, no outcome, no indication of whether it was a solo project, a class assignment, or something with real users. For an early-career candidate, a strong Projects section can carry real weight; right now this one carries almost none.

#### Experience Evaluation
Two roles, a plausible junior → mid step up in title and scope (bug-fixing/testing → backend systems/API work), with recent, relevant tenure. The story is there; the writing is not yet telling it. Scope signals (team size for the "onboarding" and "reporting dashboard" bullets, request volume or user count for the API/backend bullets) are entirely absent and would strengthen this section substantially once added.

#### Education Evaluation
BS Computer Science, appropriately placed after Experience given the candidate now has ~2+ years of professional experience; no additional detail (GPA, coursework) is needed at this stage unless something there is unusually strong.

#### Achievement Evaluation
No awards, recognitions, or standalone achievements are listed. None of the current bullets are written with enough specificity to function as a de facto achievement callout either — this is the same underlying issue as the Impact score.

#### Keyword Optimization
No job description was provided, so this uses general early-career backend/software developer norms. Present: Python, SQL, Git — a reasonable, credible starting stack. Commonly expected but absent from the visible Skills list: any web framework (Django/Flask/FastAPI/Express), any cloud platform (AWS/GCP/Azure), any testing framework, and any CI/CD or containerization terminology (Docker, GitHub Actions, etc.) — all plausible candidates for tools actually used in "backend systems," "database migrations," and "API performance" work that simply weren't named.

| Keyword | Present? | Notes |
|---|---|---|
| Python | Yes | Listed in Skills |
| SQL | Yes | Listed in Skills |
| Git | Yes | Listed in Skills |
| Web framework (Django/Flask/FastAPI/etc.) | No | Likely used given "backend systems" and "API" bullets — confirm and add if accurate |
| Cloud platform (AWS/GCP/Azure) | No | Not mentioned anywhere; confirm whether applicable |
| Testing framework / CI-CD | No | "Did testing for new features" implies some testing work with no named tool |
| REST / API terminology | Implied only | "API performance" appears in prose but no API-related term appears in Skills |

#### Missing Sections
- No hard "missing" standard sections — Objective, Experience, Projects, Education, and Skills are all present.
- **Certifications** — not present; only worth adding if genuinely held.
- A dedicated, categorized **Skills** breakdown (Languages / Frameworks / Tools) would read as more substantial than the current three-item flat list, once expanded with tools that are actually used.

#### Weak Bullet Points

| Original | Issue | Suggested Rewrite |
|---|---|---|
| "Responsible for maintaining backend systems supporting the mobile app" | Duty-listing, no scope or outcome | "Maintained [specific system(s)] supporting the mobile app, serving [X] requests/day" |
| "Helped with database migrations to a new schema" | Downplays contribution, no scale | "Migrated [table/database] to a new schema, covering [X] records with [zero downtime / no data loss]" |
| "Worked on improving API performance significantly" | Vague intensifier standing in for a real number | "Improved [specific endpoint]'s response time by [X]%" |
| "Participate in daily code reviews" | Present tense breaks convention used by surrounding bullets; low-signal as written | Consider folding into a broader collaboration bullet with real scope, or cutting if it doesn't add differentiating signal |
| "I helped with building a new reporting dashboard for the team" | First-person slip; downplays contribution; no scope | "Built [specific piece] of a new reporting dashboard used by [X] team members" |
| "Was in charge of fixing bugs in the production system" | Weak phrase; no scale | "Resolved [N] production bugs in [system], reducing [incident rate / customer reports] by [X]%" |
| "Assisted with onboarding new team members" | Downplays contribution, no scale | "Onboarded [N] new team members by [creating documentation / leading training sessions / pairing]" |
| "Did testing for new features" | Weak verb, no method or scale named | "Tested [N] new features using [specific method/tool], catching [N] defects before release" |
| "Built an app for tracking inventory. Used some technologies to make it work." | Extremely vague; no tech stack, scope, or outcome | "Built an inventory tracking app using [tech stack], supporting [scope — e.g., X SKUs, X users] [and achieving Y outcome, if any]" |

#### Strong Bullet Points
None of the current bullets meet the bar for "strong" as written — every one is missing either a quantified outcome, a specific technical detail, or both. This mirrors the Impact and Content Quality scores directly and is not a sign the underlying work was weak, only that it isn't written to show its strength yet.

#### Repetitive Wording
"Helped" or "helped with" appears twice ("Helped with database migrations," "I helped with building a new reporting dashboard") and "technologies" appears twice in a five-word span within the Projects entry ("Used some technologies to make it work" following "Built an app... technologies"). Flag both as patterns to fix via word variety and specificity, not as isolated typos.

#### Action Verb Analysis
Every one of the 9 bullets opens with a flagged weak phrase or weak verb: "Responsible for," "Helped with" (x2), "Worked on," "Participate in" (weak/no real verb signal), "Was in charge of," "Assisted with," "Did," and an implicit weak opener in the Projects bullet ("Built... Used some..."). This is the most impactful, lowest-effort fix available — see `references/action-verbs.md` for direct replacements.

#### Quantification Analysis
0 of 9 bullets (0%) contain any number, percentage, or scale indicator. This is the primary driver of the Impact score and should be the first thing addressed — even directionally honest estimates ("roughly 10 teammates," "cut load time from ~3s to ~1s") would move this from Poor into at least Adequate territory.

---

### Recruiter & Hiring Manager Perspective

#### Recruiter First-Impression (6-Second Scan)
A recruiter scanning this in six seconds sees a plausible junior-to-mid backend developer with a relevant degree and a sensible two-job history, but nothing that answers "what did she actually build or fix." Combined with the rogue "MY JOURNEY" header, there's a real risk the second job doesn't even register as part of a continuous Experience section in a fast scan or an ATS keyword search.

#### Hiring Manager Read
Borderline-to-risky as written. The title and stack are plausible enough to earn a look, but a hiring manager would come away with no sense of scope, ownership, or actual technical depth — and the unexplained ~19-month gap between roles would likely prompt a hesitation the resume should have pre-empted with even a one-line framing.

#### Junior vs. Senior Appropriateness
The language currently reads appropriately junior-to-early-career in tone, which matches the actual tenure shown (roughly 3-4 years combined, with a gap) — this isn't a case of underselling relative to seniority so much as underselling relative to the *actual, specific work performed*. Once rewritten with real scope and numbers, this would read as a solid, credible early-career developer resume rather than a thin one.

---

### Synthesis

#### Biggest Strengths
1. A coherent, relevant two-job progression (Junior Developer → Software Developer) in a plausible backend/software track.
2. A personal project already exists to add differentiating signal, once it's actually described.
3. Clean spelling and a genuinely simple, unadorned document with no ATS-hostile graphics, tables, or columns to strip out.

#### Biggest Weaknesses
1. Zero quantification anywhere in the document (0 of 9 bullets).
2. A non-standard section header ("MY JOURNEY") that puts an entire job at real risk of being dropped from ATS parsing.
3. Every single bullet opens with a flagged weak verb or duty-listing phrase.

#### Top 10 Improvements (ordered by impact)
1. Replace "MY JOURNEY" with "Experience" (or merge both roles under one shared Experience header) — the single highest-risk ATS issue in the document.
2. Add a quantified outcome or scale indicator to every bullet — this alone would likely move Impact from 10 into the 55-65 range.
3. Rewrite all 9 bullets to remove weak openers ("Responsible for," "Helped with," "Worked on," "Was in charge of," "Assisted with," "Did") using strong, accurate verbs.
4. Rewrite the Projects entry with an actual tech stack, scope, and outcome — currently the vaguest line in the document.
5. Standardize date format throughout (pick one: "Mon YYYY – Mon YYYY" or "MM/YYYY – MM/YYYY," not both).
6. Standardize bullet character throughout (currently mixes `-` and `*`).
7. Remove the first-person "I" from the reporting-dashboard bullet.
8. Replace the informal email address with a professional `firstname.lastname@`-style handle.
9. Add a brief, confident one-line framing for the ~19-month gap between roles rather than leaving it silent.
10. Expand and categorize the Skills section with tools actually used in the Experience bullets (framework, cloud platform, testing/CI-CD tools, if applicable) rather than leaving it at three items.

#### Quick Wins (high impact, low effort)
- Fix the section header "MY JOURNEY" → "Experience" (1 minute, removes the single biggest ATS risk in the document).
- Fix the email address (2 minutes).
- Cut "References available upon request" (10 seconds, frees a line for something with actual signal).
- Fix the single first-person pronoun slip (1 minute).

#### Final Summary
Maria's underlying trajectory is a credible, coherent early-career developer story, but the resume as written scores 46/100 because every bullet describes an assigned duty rather than an outcome, contains no quantification at all, and one section header creates a genuine risk of an entire job being dropped by ATS parsing. This is a high-leverage rewrite: fixing the header, standardizing formatting, and rewriting the 9 bullets with real scope and numbers would plausibly move the Overall score from the mid-40s into the 70s-80s without changing a single fact about what Maria actually did.
