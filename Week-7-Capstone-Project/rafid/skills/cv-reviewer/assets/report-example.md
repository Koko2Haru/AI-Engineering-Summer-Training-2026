# Worked Example: Full Report

This is a complete, filled-out sample report for a fictional candidate ("Jordan Lee," a mid-level backend engineer). Use it to calibrate tone, depth, evidence usage, and formatting — the actual report you produce should match this quality bar, not just mimic the section headers.

The example below renders as normal Markdown (no code fence) so its tables and headings display exactly as a real report should. Its headings are nested one level deeper than the real report uses (`##` here where the real report uses `#`, etc.) purely so they sit correctly under this file's own title — when you generate a real report, start it back at `#`/`##` per `review-template.md`.

The source CV excerpt being reviewed (for context — not part of the output):

> **Jordan Lee** — jlee92xoxo@hotmail.com — (555) 123-4567
> **Experience**
> Software Engineer, Acme Corp (2021 - Present)
> - Responsible for backend development tasks
> - Helped with database migrations
> - Worked on various API improvements
> - I was in charge of a small team during a project
>
> Software Engineer, Startup Inc (2019 - 2021)
> - Built features for the mobile app
> - Fixed bugs and improved performance
>
> **Skills:** Python, Java, SQL, Docker, AWS, Communication, Teamwork, Problem Solving

---

## CV Review: Jordan Lee

**Overall Score: 58/100 — Weak**
**Reviewed as:** Mid-level Backend Engineer (3-5 years experience)
**One-line verdict:** Solid underlying experience is being undersold by vague, duty-listing bullets and near-zero quantification — this is a rewrite-the-bullets problem, not a start-over problem.

### Score Summary

| Category | Score | Band |
|---|---|---|
| ATS Compatibility | 82/100 | Strong |
| Content Quality | 48/100 | Weak |
| Impact | 22/100 | Poor |
| Grammar & Spelling | 70/100 | Adequate |
| Readability | 65/100 | Adequate |
| Visual / Layout | 75/100 | Strong |
| Professionalism | 55/100 | Weak |
| **Overall** | **58/100** | **Weak** |

---

### Category Breakdown

#### ATS Compatibility — 82/100
Single-column, standard section headers ("Experience," "Skills"), plain text dates in a consistent format, no tables or graphics detected. This will parse cleanly through Workday/Greenhouse-style systems.

**Working well:** Standard headers, linear layout, parseable date format ("2021 - Present").
**Needs improvement:** No dedicated Education section was found in the extracted text — confirm whether it exists further down the document or is genuinely missing, since its absence would also be an ATS field-completeness issue.
**Evidence:** Section headers appear as plain text: "Experience", "Skills" — no formatting artifacts detected in extraction.

#### Content Quality — 48/100
The bullets describe assigned duties ("Responsible for," "Helped with," "Worked on") rather than what was actually accomplished. The underlying work (backend development, database migrations, API improvements, leading a team) sounds substantive — the writing just isn't surfacing it.

**Working well:** The roles themselves show a reasonable, relevant progression (mobile app engineer → backend engineer with some leadership exposure).
**Needs improvement:** Every bullet in the current role uses duty-listing language instead of outcome language.
**Evidence:** "Responsible for backend development tasks" and "Worked on various API improvements" — both tell the reader an assignment existed, not what happened as a result of it.

#### Impact — 22/100
Zero bullets contain a number, percentage, or concrete scale indicator anywhere in the experience section.

**Working well:** N/A — this is the report's lowest-scoring category and the single highest-leverage fix available.
**Needs improvement:** Every bullet needs at least an attempt at quantification — even directionally accurate estimates ("reduced by roughly a third") beat no number at all.
**Evidence:** "Fixed bugs and improved performance" — no indication of how many bugs, what kind, or how much performance improved.

#### Grammar & Spelling — 70/100
No spelling errors detected. One first-person pronoun slip ("I was in charge of a small team") breaks the implied-first-person convention used everywhere else.

**Working well:** Clean spelling throughout; tense is consistently past for the prior role.
**Needs improvement:** Remove the stray "I" — it's the only bullet in the document written in explicit first person.
**Evidence:** "I was in charge of a small team during a project" → should read "Led a small team during [specific project]."

#### Readability — 65/100
Bullets are short and scannable, but several are vague enough that a reader can't actually picture what was done.

**Working well:** Bullet length is appropriate — no dense paragraphs.
**Needs improvement:** "Various API improvements" and "database migrations" need at least one specific detail each (which API, what kind of migration, what changed).

#### Visual / Layout — 75/100
Clean, single-column, consistent bullet style. Reasonable length for a candidate in this range.

**Working well:** Consistent formatting throughout the excerpt reviewed.
**Needs improvement:** Cannot fully assess overall page layout/whitespace from the extracted text alone — flagged as a lower-confidence sub-score if reviewing from raw extracted text rather than the rendered document.

#### Professionalism — 55/100
The email address undercuts an otherwise professional document.

**Working well:** No inappropriate personal information detected (no age, photo, marital status).
**Needs improvement:** `jlee92xoxo@hotmail.com` reads as a personal, informal handle. A simple `jordan.lee@gmail.com`-style address would remove this friction entirely — this is a 2-minute fix with outsized first-impression payoff.

---

### Deep-Dive Analysis

#### Technical Skills Evaluation
Python, Java, SQL, Docker, and AWS form a coherent, credible backend stack. The list would benefit from being grouped by category (Languages / Infrastructure / Databases) rather than run together, and from specifying AWS services actually used (e.g., "AWS (EC2, RDS, S3)") since generic "AWS" is a weak signal on its own to a technical screener.

#### Soft Skills Evaluation
"Communication," "Teamwork," "Problem Solving" are listed as bare skill-tags with no supporting evidence anywhere in the experience bullets. Bare soft-skill lists are widely discounted by recruiters — the fix isn't to remove them, it's to demonstrate them through the experience bullets instead (e.g., the team-leadership bullet, once quantified, already proves "leadership" and "communication" far more convincingly than the label does).

#### Project Quality Analysis
No dedicated Projects section is present. For a candidate with 3-5 years of professional experience, this is optional rather than critical — professional experience should carry the weight — but a notable side project relevant to a target role (e.g., contributing to an open-source backend tool) would strengthen a borderline application.

#### Experience Evaluation
Two roles shown, reasonable 2-year tenures, plausible scope increase from mobile features to backend + a team-lead moment. The progression story is there; it's just not being told with any specificity or evidence.

#### Education Evaluation
Not present in the reviewed excerpt — flag as a missing section pending confirmation (see ATS Compatibility note above).

#### Achievement Evaluation
No awards, recognitions, or standout achievements called out separately — the team-lead bullet is the closest candidate for a genuine achievement callout once it's rewritten with real detail.

#### Keyword Optimization
No job description was provided for this review, so this assessment uses general backend engineering norms. Present: Python, SQL, Docker, AWS — solid core signals. Commonly expected but absent from the visible skills list: any specific framework (Django/Flask/FastAPI/Spring), any messaging/queue technology (Kafka, RabbitMQ, SQS), and any testing/CI-CD terminology. If these are genuinely part of Jordan's experience, they should be named explicitly rather than implied by "backend development tasks."

#### Missing Sections
- **Education** — not found in the extracted text; confirm it exists elsewhere in the document.
- **Summary** — optional at this experience level, but a 2-line summary could immediately frame "backend engineer with production experience leading small-team initiatives," which the bullets currently bury.
- **Projects** — optional given professional experience is present, but would help if available.

#### Weak Bullet Points

| Original | Issue | Suggested Rewrite |
|---|---|---|
| "Responsible for backend development tasks" | Duty-listing, no specificity, no outcome | "Built and maintained [specific service/system], serving [X] requests/day with [Y]% uptime" |
| "Helped with database migrations" | Downplays contribution, no scale or outcome | "Led migration of [database/table] from [old system] to [new system], with zero downtime across [X] million records" |
| "Worked on various API improvements" | Vague, no specificity | "Redesigned [specific API/endpoint], reducing average response time by [X]%" |
| "I was in charge of a small team during a project" | First-person slip; no team size, project, or outcome given | "Led a team of [N] engineers to deliver [project], completed [on time / X weeks ahead of schedule]" |
| "Fixed bugs and improved performance" | No scale, no specific metric | "Resolved [N] production bugs and improved [specific system]'s response time by [X]%" |

#### Strong Bullet Points
None of the current bullets meet the bar for "strong" as written — this is precisely why Impact and Content Quality are the two lowest scores. This isn't a signal the underlying work was weak, only that it isn't yet written to show its strength.

#### Repetitive Wording
"Worked on" / "Helped with" / "Responsible for" all appear as functionally the same weak opener across 3 of the 6 bullets shown — flag as a pattern, not three separate issues, since fixing the pattern (see `references/action-verbs.md`) fixes all three at once.

#### Action Verb Analysis
Current openers: "Responsible for" (weak phrase), "Helped with" (weak phrase), "Worked on" (weak phrase), "Fixed... improved" (adequate), "Built" (strong), "I was in charge of" (weak phrase + first-person). 4 of 6 bullets open with a flagged weak phrase from `references/action-verbs.md` — the single most impactful, lowest-effort fix available in this review.

#### Quantification Analysis
0 of 6 visible bullets (0%) contain any number, percentage, or scale indicator. This is the primary driver of the low Impact score and should be the first thing addressed — even approximate, honest figures ("roughly 10 engineers," "cut deploy time from ~40 min to ~15 min") would move this from Poor to at least Adequate.

---

### Recruiter & Hiring Manager Perspective

#### Recruiter First-Impression (6-Second Scan)
A recruiter scanning this in 6 seconds sees a plausible backend engineer with the right keywords (Python, AWS, Docker) but nothing that differentiates Jordan from dozens of similarly-titled resumes in the pile — nothing here answers "so what did they actually do." That's a real risk in a competitive applicant pool, even though the underlying experience may be perfectly strong.

#### Hiring Manager Read
Borderline — likely earns a phone screen on keyword/title match alone in a moderately competitive pool, but the interviewer would be going in mostly blind on scope, team size, and actual technical depth, which the resume should have already answered.

#### Junior vs. Senior Appropriateness
The language currently reads slightly junior relative to 3-5 years of experience — "helped with," "worked on," and "was in charge of" (rather than "led") all undersell scope. Once rewritten with real ownership language and metrics, the same underlying experience would read as solidly mid-level, which matches the tenure shown.

---

### Synthesis

#### Biggest Strengths
1. Clean, ATS-parseable structure with no formatting red flags.
2. Coherent, relevant technical stack for a backend engineering target.
3. A credible experience progression story (mobile → backend → team lead) that's currently underwritten rather than genuinely thin.

#### Biggest Weaknesses
1. Zero quantification anywhere in the experience section.
2. Four of six bullets open with a flagged weak phrase ("responsible for," "helped with," "worked on," "was in charge of").
3. Unprofessional email address undercuts an otherwise clean document on first glance.

#### Top 10 Improvements (ordered by impact)
1. Add a quantified outcome to every experience bullet — this alone would likely move Impact from 22 to 60+.
2. Rewrite the 4 bullets that open with weak phrases ("Responsible for," "Helped with," "Worked on," "I was in charge of") using strong verbs from `references/action-verbs.md`.
3. Remove the first-person "I" and convert that bullet to implied-first-person, active voice.
4. Replace the informal email address with a professional firstname.lastname-style handle.
5. Confirm and add the Education section if it's genuinely missing from the document.
6. Group the Skills section by category (Languages / Infrastructure / Databases) instead of one flat list.
7. Name specific technologies within bullets (which API, which database, which AWS services) rather than generic references.
8. Add a 2-line professional summary framing backend experience + team-lead moment upfront.
9. Consider adding a Projects section if any side/open-source work exists relevant to target roles.
10. Once bullets are quantified, verify the resume still fits comfortably on one page — tightening vague bullets usually creates room rather than using it up.

#### Quick Wins (high impact, low effort)
- Fix the email address (2 minutes, removes an unforced first impression risk).
- Fix the single first-person pronoun slip (1 minute).
- Add rough, honest estimates to the 2-3 bullets where an exact number isn't readily available (10 minutes) — approximate is far better than absent.

#### Final Summary
Jordan's underlying experience is plausibly strong for a mid-level backend role, but the resume as written scores 58/100 because it consistently describes duties instead of outcomes and contains no quantification at all. This is a high-leverage, low-effort fix: rewriting the 6 visible bullets using the XYZ formula and adding real numbers would likely move the Overall score from the high-50s into the high-70s or low-80s without changing a single fact about what Jordan actually did.
