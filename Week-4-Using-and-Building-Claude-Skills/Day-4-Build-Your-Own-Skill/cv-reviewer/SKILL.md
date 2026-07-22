---
name: cv-reviewer
description: Use when a user uploads or pastes a CV/resume (PDF, DOCX, or plain text) and wants feedback, a score, editing help, or an assessment of how it will perform with recruiters and ATS systems. Triggers on requests like "review my resume", "how's my CV", "will this pass ATS", "help me improve my resume for a [role] application", or "grade my CV out of 100".
---

# CV Reviewer

Comprehensive, recruiter-grade CV/resume review that scores, diagnoses, and prioritizes fixes across ATS compatibility, content quality, impact, and professionalism — the way an experienced technical recruiter and hiring manager would read it.

## Purpose

Most resume feedback is either too vague ("make it more impactful") or too shallow (a spellcheck pass). This skill performs a structured, multi-dimensional audit that:

1. Scores the CV numerically across 7 weighted categories plus an overall score.
2. Explains *why* each score is what it is, with evidence quoted from the document.
3. Rewrites weak bullet points into strong, quantified ones.
4. Produces a prioritized action list so the user knows what to fix first.

The output should read like it came from a senior recruiter who has screened thousands of resumes for the user's target industry — direct, specific, and immediately actionable.

## When This Skill Should Trigger

- The user uploads or pastes a CV/resume and asks for a review, critique, score, or feedback.
- The user asks whether their resume will "pass ATS" or survive an applicant tracking system.
- The user asks for help tailoring a resume to a specific job posting or industry.
- The user asks to rewrite or strengthen specific bullet points from their resume.
- The user asks "is my resume good enough for [role/level]?"

## When It Should NOT Trigger

- The user wants help writing a resume from scratch with no draft to review — this is a *drafting* task, not a review. Offer to draft one, but note this skill is for reviewing an existing document (you may still use `references/resume-writing-guide.md` and `references/action-verbs.md` to inform the draft).
- The user shares a cover letter, LinkedIn profile, or portfolio site instead of a CV — clarify scope before proceeding; the scoring rubric here is resume-specific.
- The user asks a narrow, single-fact question ("what's a good resume font size?") that doesn't warrant a full audit — answer directly from `references/resume-writing-guide.md` instead of running the full workflow.
- The document provided is not actually a resume (e.g., a job description, a transcript, an essay) — say so rather than forcing a review.

## Input Expectations

The user may provide the CV as:

- **Pasted plain text** — use directly.
- **A PDF file** — use `scripts/extract_text.py` to extract raw text before analysis. Flag if extraction suggests the PDF is image-based (near-empty output), since that itself is a critical ATS failure worth reporting.
- **A DOCX file** — use `scripts/extract_text.py` (docx path) to pull text and paragraph structure.
- **A job description alongside the CV** — if provided, weight keyword optimization and industry-fit feedback against that specific posting rather than generic industry norms.

If no target role, seniority level, or industry is stated, ask the user in one short question, or state the assumption you're proceeding with (e.g., "Reviewing this as a mid-level software engineering resume — let me know if that's off"). Don't block the whole review on missing context; a reasonable default assumption is better than stalling.

## Output Format

Produce a single structured Markdown report following `assets/review-template.md`. It must include, in order:

1. **Header** — overall score out of 100, one-line verdict, target role/level assumed.
2. **Score summary table** — all 7 category scores + overall, at a glance.
3. **Category-by-category breakdown** — for each of the 7 categories: score, explanation, what's working, what's not, concrete quoted examples, suggested rewrites where relevant.
4. **Deep-dive sections** — technical skills, soft skills, projects, experience, education, achievements, keyword optimization, missing sections, weak/strong bullets, repetitive wording, action verb analysis, quantification analysis.
5. **Recruiter & hiring-manager perspective** — first-impression read (6-second scan), hiring recommendation, junior-vs-senior fit check.
6. **Closing synthesis** — biggest strengths, biggest weaknesses, top 10 prioritized improvements, quick wins, final summary verdict.

Use tables wherever comparing multiple items (scores, bullet rewrites, missing sections). Quote the CV's actual text when critiquing a specific line — never critique in the abstract when a concrete example is available.

**Rendering:** Output the report as live Markdown directly in the conversation — headings, tables, and bold text must render as formatted output, not as literal text with visible `#`/`|` characters. Do **not** wrap the whole report in a code fence (` ``` `); a fenced block renders as plain preformatted text, which flattens every table into unreadable pipe-delimited lines. `assets/review-template.md` and `assets/report-example.md` demonstrate the exact heading levels and table structure to use — match those directly rather than nesting the whole output inside a fence.

## Instructions for Claude

### Workflow

1. **Ingest the document.**
   - If it's a file path (PDF/DOCX), run `scripts/extract_text.py <path>` to get raw text. Read the tool's warnings (e.g., "low text density — possible scanned/image PDF") and carry them into the ATS section.
   - If it's pasted text, use it as-is but still run it through `scripts/helpers.py` section-detection logic conceptually (you can reason through this manually; the script exists to formalize the logic, not gate it).

2. **Detect structure.** Identify which standard sections exist: Contact Info, Summary/Objective, Experience, Education, Skills, Projects, Certifications, Achievements/Awards. Note anything present that's non-standard (e.g., "Hobbies," "References available upon request" — usually a weak-signal section).

3. **Run the category evaluations** described below, in this order, because later categories depend on facts gathered earlier (e.g., you can't score Impact until you've identified all bullet points):
   1. ATS Compatibility
   2. Visual / Layout
   3. Readability
   4. Grammar & Spelling
   5. Professionalism
   6. Content Quality
   7. Impact

4. **Run the deep-dive analyses**: technical skills, soft skills, projects, experience, education, achievements, keyword optimization vs. target role/JD, missing sections, weak bullets, strong bullets, repetitive wording, action verb usage, quantification coverage.

5. **Synthesize.** Compute the overall score using `assets/scoring-matrix.json` weights (see Scoring Methodology). Write the recruiter first-impression read as if you scanned the resume for 6 seconds. Write the hiring-manager read as if deciding whether to schedule a phone screen. Determine junior-vs-senior fit by comparing years of experience, scope of ownership language, and leadership signals against the stated or inferred target level.

6. **Prioritize.** Rank the top 10 improvements by expected impact on interview conversion, not by how easy they are to fix. Separately call out 3-5 "quick wins" (high impact, low effort — e.g., adding numbers to existing bullets) since users often want something they can fix in the next 10 minutes.

7. **Write the report** using `assets/review-template.md` as the skeleton. See `assets/report-example.md` for the target tone, depth, and formatting bar — match that quality level, not just the section headers.

### Step-by-Step Reasoning Process

For every score, follow this sequence before writing the number down:

1. Gather evidence (quote specific lines/sections relevant to this category).
2. Compare evidence against the criteria in `references/scoring-rubric.md` for that category.
3. Land on a band (see Scoring Methodology below), then a specific number within the band based on how many criteria were fully vs. partially met.
4. Write the explanation *before* finalizing the number if writing it out surfaces a different score — the explanation should never feel bolted on after an arbitrary number. If the explanation and the number disagree, trust the explanation and adjust the number.

### Scoring Methodology

Each of the 7 categories is scored 0-100 independently, then combined into the overall score using fixed weights (see `assets/scoring-matrix.json`):

| Category | Weight |
|---|---|
| ATS Compatibility | 20% |
| Content Quality | 20% |
| Impact (quantification & achievements) | 15% |
| Grammar & Spelling | 15% |
| Readability | 10% |
| Visual / Layout | 10% |
| Professionalism | 10% |

`Overall = Σ(category_score × weight)`, rounded to the nearest whole number.

Score bands (apply to every category, not just overall):

| Band | Range | Meaning |
|---|---|---|
| Excellent | 90-100 | Meets or exceeds professional/recruiter expectations with no notable gaps |
| Strong | 75-89 | Solid, minor polish would help |
| Adequate | 60-74 | Functional but has clear, fixable gaps |
| Weak | 40-59 | Multiple significant issues that will cost interviews |
| Poor | 0-39 | Fundamental problems likely to cause rejection or ATS failure |

Full per-category criteria checklists live in `references/scoring-rubric.md` — always consult it rather than inventing criteria on the fly, so scores stay consistent across reviews.

### Evaluation Rubric (Quick Reference)

- **ATS Compatibility** — parseable structure, standard section headers, no tables/columns/text boxes/images carrying critical text, standard fonts, reverse-chronological dates, file format sanity. See `references/ats-best-practices.md`.
- **Visual / Layout** — whitespace balance, consistent formatting (fonts, bullet styles, spacing), length appropriate to seniority, scannability.
- **Readability** — sentence length, bullet length, jargon density, logical grouping, active voice.
- **Professionalism** — tone, absence of first-person pronouns, consistent tense, appropriate contact info, no unprofessional email/photo/personal info where inappropriate for region/industry.
- **Content Quality** — relevance of content to target role, specificity over generality, evidence of scope and ownership.
- **Impact** — proportion of bullets with quantified outcomes (numbers, %, $, time saved), use of results-oriented framing (STAR/XYZ) over duty-listing.
- **Grammar & Spelling** — typos, punctuation consistency, subject-verb agreement, verb tense consistency within and across entries.

### Edge Cases

- **Resume in a language other than English**: note this explicitly, review in that language if capable, and flag that ATS/keyword guidance may vary by region.
- **Career changer / employment gaps**: don't penalize gaps automatically — evaluate whether the resume handles the gap/transition credibly (e.g., a brief, confident framing vs. no acknowledgment at all).
- **Academic/research CV** (multi-page, publications-heavy): note that standard length/section norms don't apply the same way; adjust Visual/Layout and Content Quality reasoning accordingly rather than penalizing length.
- **Extremely short resume (student/first job)**: don't penalize thin Experience if Education, Projects, and relevant coursework are used well to compensate — evaluate what's there rather than what's structurally absent at this career stage.
- **Resume is actually strong**: don't manufacture weaknesses to fill the "top 10 improvements" list. If there are only 4 genuine improvements, list 4 and say so — padding erodes trust.
- **No target role specified**: proceed with a stated, reasonable assumption (see Input Expectations) rather than blocking.

### Constraints

- Never fabricate content the CV doesn't contain (don't invent metrics, dates, or job titles when suggesting rewrites — suggest the *pattern* to fill in, e.g., "reduced [metric] by [X]%," with brackets for the user to complete).
- Never assign a perfect 100 in any category unless it is genuinely flawless against the rubric — reserve it for truly exceptional cases.
- Don't just list problems — every weakness raised must come with a concrete suggested fix.
- Keep quoted CV excerpts short (one bullet or line at a time) rather than reproducing large blocks of the original document.
- Be honest and direct, but never insulting — critique the document, not the person.

### File Usage

| Path | Purpose | When to consult |
|---|---|---|
| `references/scoring-rubric.md` | Per-category scoring criteria and bands | Every time a score is assigned |
| `references/ats-best-practices.md` | ATS parsing rules and pitfalls | ATS Compatibility scoring, keyword section |
| `references/resume-writing-guide.md` | Structural/formatting conventions, STAR/XYZ bullet formula | Content Quality, Visual/Layout, bullet rewrites |
| `references/action-verbs.md` | Strong verbs by category + weak verbs/phrases to flag | Action verb analysis, bullet rewrites |
| `references/common-mistakes.md` | Checklist of frequent resume errors | Sanity-check pass before finalizing the report |
| `scripts/extract_text.py` | Pull raw text from PDF/DOCX | Whenever input is a file, not pasted text |
| `scripts/helpers.py` | Section detection, bullet splitting, quantification/verb/repetition regex helpers | Reference for the *logic* of each analysis; may be run directly for large CVs |
| `scripts/review_cv.py` | End-to-end orchestrator tying extraction + helpers + scoring together, emits JSON | Optional — for programmatic/batch scoring or to sanity-check manual scoring |
| `assets/scoring-matrix.json` | Canonical weights and score bands | Computing the overall score |
| `assets/review-template.md` | Output report skeleton | Structuring the final report |
| `assets/report-example.md` | Fully worked example report | Calibrating tone, depth, and formatting before writing the final report |

### Best Practices

- Lead every section with the score and a one-sentence verdict before the detail — the user should get the headline even if they only skim.
- Quote, don't paraphrase, when pointing at a specific weakness — "Responsible for managing a team" is more convincing evidence than "the experience section uses passive phrasing."
- Always pair a weak bullet with a rewritten strong version, not just a critique.
- Calibrate feedback to seniority — a bootcamp grad's resume and a staff engineer's resume are held to different content expectations even under the same rubric.
- When a job description is provided, make keyword optimization concrete: name the specific missing keywords from that posting, not generic industry buzzwords.
- Treat the "Top 10 Improvements" list as the most important artifact in the whole report — order it strictly by expected impact on getting an interview.

### Failure Handling

- **Extraction fails or returns near-empty text** (`scripts/extract_text.py` reports low text density): stop and tell the user directly — likely a scanned/image-based PDF — and ask them to paste the text or provide a text-based export instead of guessing at content.
- **Document isn't a resume**: say so plainly and ask what they'd like reviewed instead; don't force the rubric onto the wrong document type.
- **Ambiguous or missing target role**: state the assumption being used and proceed (see Edge Cases); don't block the whole review on it.
- **Partial/corrupted extraction** (some sections garbled): note which sections had extraction issues and review the rest normally, rather than discarding the whole review.

## Examples

**Trigger example:**
> User: "Can you review my resume? I'm applying for backend engineering roles." [attaches resume.pdf]
> → Run `extract_text.py`, execute the full workflow, produce the full report per `assets/review-template.md`.

**Non-trigger example:**
> User: "What font should I use on my resume?"
> → Answer directly from `references/resume-writing-guide.md` (a couple of sentences); don't launch the full audit workflow.

**Boundary example:**
> User: "Here's my LinkedIn About section, can you review it like a resume?"
> → Clarify that LinkedIn copy and resume bullets serve different goals (narrative vs. scannable achievement statements) before proceeding; offer to adapt the rubric rather than applying it unchanged.
