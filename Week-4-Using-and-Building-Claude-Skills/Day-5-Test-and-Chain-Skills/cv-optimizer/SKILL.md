---
name: cv-optimizer
description: Use when a user wants their CV/resume rewritten and strengthened — especially after running a CV review — rather than critiqued. Triggers on requests like "improve my resume", "rewrite my CV based on this feedback", "fix the weak sections in my resume", "make this ATS-friendly", "polish my resume for submission", "apply these review suggestions to my CV", or "turn this into a stronger resume". Designed to run after the cv-reviewer skill: takes the original CV plus (optionally) its review output and produces a rewritten, recruiter-ready resume without inventing facts.
---

# CV Optimizer

Transforms an existing CV into its strongest truthful version — rewriting weak content, tightening language, and improving ATS compatibility — without ever inventing experience, credentials, or achievements the candidate didn't provide.

## Purpose

A resume review tells you what's wrong. This skill does the next job: fix it. Given an original CV — and ideally the diagnostic output of the `cv-reviewer` skill — it rewrites the document section by section, upgrading weak verbs, vague duty-statements, and generic summaries into concrete, quantified, ATS-friendly language, while treating every fact in the source document as fixed and non-negotiable.

The hard constraint that shapes this entire skill: **rewriting is not embellishment.** A stronger sentence describing a real accomplishment is in scope. A new accomplishment, metric, skill, or credential the candidate never mentioned is not — no matter how much it would improve the resume. Where a stronger bullet genuinely needs a fact the candidate hasn't supplied (a metric, an outcome, a technology list), the skill's job is to either ask for it or mark the gap visibly, never to fill it silently.

## When This Skill Should Trigger

- The user asks to have their resume improved, rewritten, polished, or strengthened — with or without an accompanying review.
- The user pastes or attaches a CV together with review output from `cv-reviewer` (a scored report, a list of weaknesses, or "here's what a reviewer said, can you fix it") and wants the CV updated accordingly.
- The user asks to apply specific feedback ("make my bullets more quantified", "fix the ATS issues it found", "rewrite my summary") to an existing resume.
- The user asks to tailor an existing resume to a specific job description after already having a draft.
- The user says something like "here's my resume and its review — give me the improved version."

## When It Should NOT Trigger

- The user wants a review, score, or critique with no rewrite — that's `cv-reviewer`'s job. If a user asks "how's my resume?" with no request to rewrite it, route them there (or run it first) instead of jumping straight to rewriting.
- The user wants a resume built from nothing, with no existing draft to work from — this is a drafting task. This skill can still be useful for structure and language conventions (`references/`), but say so explicitly rather than pretending to "optimize" a document that doesn't exist yet; in that case, gather the candidate's actual background through questions before writing anything.
- The user wants only a narrow, single-fact answer ("what's a good resume font?") — answer directly from `references/resume-layout-guidelines.md` rather than running the full rewrite workflow.
- The document provided isn't a resume (a cover letter, LinkedIn summary, job description) — clarify scope before proceeding.

## Input Expectations

The user should provide:

1. **The original CV** (required) — pasted text or a file. Treat this as the sole source of truth for every fact that appears in the output.
2. **The CV Reviewer output** (optional but strongly preferred) — a score report, weakness list, or informal notes ("the reviewer said my bullets weren't quantified"). When present, use it to prioritize what gets rewritten first (see Workflow, step 3) instead of re-deriving weaknesses from scratch.
3. **Target role / job description** (optional) — if supplied, use it to guide keyword selection (`references/keyword-optimization.md`) and section emphasis. If absent, optimize for the role implied by the CV's own content and state that assumption.

If only a CV is provided with no review, don't block on it — run a lightweight internal weakness scan (the same categories `cv-reviewer` would flag: weak verbs, missing quantification, generic summary, ATS structure issues, inconsistent formatting) before rewriting, so the rewrite is still prioritized rather than applied uniformly line-by-line. `scripts/improve_cv.py` automates this scan.

If the CV is missing entirely (only a review was pasted), say so — there is nothing to rewrite without the source document.

## Output Format

Produce **two artifacts**, in this order, as live Markdown in the conversation (no wrapping code fence — a fenced block flattens tables into unreadable pipe-delimited text; see `assets/optimized-template.md` for the same rendering note):

1. **Optimized Resume** — the fully rewritten CV, structured per `assets/optimized-template.md`, ready to copy into a document. Every bracketed placeholder like `[Consider adding a measurable outcome here]` must stand out clearly as **not** part of the final copy-paste-ready text — call this out explicitly immediately below the resume.
2. **Change Report** — structured per `assets/change-report-template.md`, covering: summary of improvements, sections modified, ATS improvements, wording upgrades, keywords added, bullets rewritten (before/after table), grammar/formatting fixes, open placeholders needing user input, and remaining weaknesses that couldn't be fixed without more information.

Always produce both, even for a small, targeted rewrite request — the change report is what lets the user verify nothing was fabricated.

## Instructions for Claude

### Workflow

1. **Ingest the CV.** If it's a file, extract text (reuse the same extraction approach `cv-reviewer` uses — a text-based PDF/DOCX/plain text). If pasted, use directly.

2. **Ingest the review, if provided.** Parse out: category scores, flagged weak bullets, missing sections, ATS issues, and the "Top 10 Improvements" / "Quick Wins" lists if present. This becomes the initial priority queue for rewriting — see `assets/improvement-priorities.json` for how to rank issue types when a review doesn't already rank them.

3. **Run the gap scan.** Whether or not a review was provided, identify — per `references/rewriting-guidelines.md` — every place where a stronger rewrite would require a fact not present in the source: an unquantified bullet, a project with no stated outcome, a summary with no target role, a skill claim with no evidence. Do **not** treat this as a blocking step; note the gaps and continue.

4. **Decide whether to pause for clarification.** Apply the User Clarification Protocol below. If there are high-value gaps worth asking about, ask before rewriting those specific sections. Otherwise proceed straight to rewriting using placeholders for genuine gaps.

5. **Rewrite section by section**, following `references/rewriting-guidelines.md` and drawing on:
   - `references/action-verbs.md` for verb upgrades
   - `references/achievement-writing.md` for turning duty-statements into outcome statements
   - `references/keyword-optimization.md` for ATS/keyword integration
   - `references/ats-optimization.md` for structural fixes
   - `references/resume-layout-guidelines.md` for formatting consistency
   - `references/resume-writing-best-practices.md` for section order, length, and tone

   Preserve every fact. Strengthen every sentence that can be strengthened using only what's already there. Insert a bracketed placeholder wherever a stronger version needs missing information (exact wording rules in `references/rewriting-guidelines.md` — Placeholder Conventions).

6. **Assemble the Optimized Resume** using `assets/optimized-template.md`.

7. **Write the Change Report** using `assets/change-report-template.md`, cross-checking against `assets/rewrite-checklist.md` before finalizing — this is the last safety net against an accidental fabrication slipping through.

8. **Deliver both artifacts** together, in the Output Format order above.

### User Clarification Protocol

Before rewriting sections where missing information would materially limit the result, pause and ask targeted questions rather than filling gaps with placeholders by default. Placeholders are the fallback for *low-value or numerous* gaps, not the first move for gaps that would meaningfully change the resume's strength.

**When to ask:**
- A bullet describes clear responsibility but has no measurable outcome, and the role/context suggests one likely exists (e.g., "Managed a team" → ask team size; "Optimized the database" → ask for the performance gain).
- A project is listed with no outcome, users, or tech stack.
- The target role or industry is unstated and materially changes what to emphasize.
- A summary/objective is generic or absent and a target role would let it be written concretely.
- An employment gap is visible with no framing.
- Certifications, links (GitHub/portfolio/LinkedIn), or a clear list of core technical skills are absent but plausibly exist.

**When not to ask:** the existing document already has enough to produce a strong, honest rewrite; the gap is minor (one weak bullet in an otherwise strong section); or the user has explicitly asked for a quick pass rather than a deep one. Don't interrogate a resume that doesn't need it.

**Question style** (see `references/rewriting-guidelines.md` for the full rationale and more examples):
- One topic per question, short and specific — never "tell me more about yourself."
- Ordered by expected impact on the final resume: target role and missing quantification first, polish-level details last.
- Stop as soon as enough is gathered for a strong rewrite — don't run the full checklist by rote if the first few answers already unblock most of the document.

Good questions: "What role or industry are you targeting?" / "Can you put a number on that — team size, % improvement, revenue, users?" / "What was the outcome of that project — did it ship, get adopted, solve the problem?" / "Do you have a GitHub or portfolio link to include?"

Bad questions: "Tell me about your work experience." / "What else should I know?"

### Rewrite Methodology

For every section, apply these passes in order (detailed in `references/rewriting-guidelines.md`):

1. **Factual audit** — list every claim (employer, title, dates, degree, certification, metric) exactly as given; this list is the boundary the rewrite may never cross.
2. **Structural pass** — fix section order, headers, and missing standard sections (`references/resume-writing-best-practices.md`).
3. **Bullet pass** — rewrite each bullet using [strong verb] + [what was done] + [quantified result, if available] + [method, if space allows], per `references/achievement-writing.md`. Use `scripts/rewrite_bullets.py` to flag weak verbs/phrases and missing quantification mechanically before rewriting by hand.
4. **Keyword pass** — integrate role-relevant terminology naturally, per `references/keyword-optimization.md`; use `scripts/optimize_keywords.py` if a target role or job description is available.
5. **ATS pass** — fix structural parseability issues per `references/ats-optimization.md`; use `scripts/ats_optimizer.py`.
6. **Formatting pass** — normalize bullet characters, date formats, and spacing per `references/resume-layout-guidelines.md`; use `scripts/formatting_helper.py`.
7. **Readability pass** — trim redundancy, fix grammar/spelling, ensure consistent tense and voice.
8. **Final verification** — run every rewritten line through the Safety Rules below before including it in the output.

### Safety Rules

The optimizer must **never**:

- Invent employers, job titles, dates, degrees, certifications, or awards.
- Invent skills, tools, or technologies the candidate never mentioned.
- Invent or upgrade a metric (a percentage, dollar figure, headcount, or timeframe) that wasn't in the source material or supplied by the user during clarification.
- State that a project had a specific outcome, scale, or user base that wasn't confirmed.
- Silently drop a factual constraint that made a bullet weaker (e.g., don't strip "as an intern" if doing so implies more seniority than actually held).

Where a stronger bullet would require missing information, insert a clearly bracketed placeholder rather than fabricating — e.g. `[Consider adding a measurable outcome here — e.g., % improvement, users affected, time saved.]` or `[Provide the project's outcome if available.]`. Placeholders must be visually distinct from finished content (bracketed, and called out again in the Change Report) so the user can never mistake a suggestion for a stated fact.

**Exception:** if the user explicitly asks for generated suggestions or filler placeholders ("just give me a template summary I can fill in," "suggest what a strong version might look like even if I don't have the numbers yet"), clearly-labeled suggested language is allowed — but it must still be visually distinguished from factual content and never merged into the "final" resume text without the user's confirmation.

### Constraints

- Never present a placeholder-filled bullet as finished, submit-ready text — flag it inline and again in the Change Report.
- Never change the substance of a claim while rewording it (a "contributed to" bullet may become sharper prose, but must not become "led" unless the source or user confirms that framing).
- Keep the Change Report honest about what's still weak even after the rewrite — don't imply every gap was fixed if placeholders remain.
- Don't restructure section order or drop a section without explaining why in the Change Report.
- Match tone/seniority to the candidate's actual level — don't inflate an internship into "spearheaded a company-wide initiative."

### Edge Cases

- **No review provided, CV is already strong**: don't manufacture weaknesses to justify rewriting — make the genuinely available improvements (verb variety, formatting consistency, keyword coverage) and say plainly that the document was already in good shape.
- **Review provided but contradicts the CV** (e.g., review references a section not present in the CV pasted this session): flag the mismatch and ask which is current rather than guessing.
- **CV in a language other than English**: rewrite in that language, and note that keyword/ATS guidance may vary regionally.
- **Career changer / employment gaps**: strengthen the framing already present, or ask a clarifying question per the protocol above — don't invent a bridging narrative unprompted.
- **User wants only one section rewritten** ("just fix my summary"): scope the workflow to that section, but still produce a (shorter) Change Report for the section touched.
- **User provides a job description instead of/alongside a review**: treat it as the keyword-optimization target (`references/keyword-optimization.md`) in place of, or in addition to, generic industry norms.
- **Resume is already at 1-2 pages and rewrites would push it over**: prioritize cutting low-value content over letting it grow past the length norms in `references/resume-writing-best-practices.md`.

## File Usage

| Path | Purpose | When to consult |
|---|---|---|
| `references/rewriting-guidelines.md` | Core rewrite methodology, factual-preservation rules, placeholder conventions, clarification-question guidance | Every rewrite pass — this is the operating manual for the whole skill |
| `references/ats-optimization.md` | Structural ATS rules and how to fix (not just detect) them | ATS pass |
| `references/resume-writing-best-practices.md` | Section order, length norms, tense/voice conventions | Structural pass, final assembly |
| `references/action-verbs.md` | Strong verbs by category, weak-verb replacement map | Bullet pass |
| `references/achievement-writing.md` | STAR/XYZ bullet formula, before/after rewrite patterns | Bullet pass |
| `references/resume-layout-guidelines.md` | Formatting consistency rules (fonts, bullets, spacing, dates) | Formatting pass |
| `references/keyword-optimization.md` | How to integrate keywords naturally without stuffing; density guidance | Keyword pass, when a target role/JD is available |
| `scripts/improve_cv.py` | End-to-end orchestrator: runs the gap scan and priority queue when no review is supplied | Step 3 (gap scan), or anytime a mechanical first pass is useful |
| `scripts/rewrite_bullets.py` | Flags weak verbs/phrases and unquantified bullets per line | Bullet pass |
| `scripts/optimize_keywords.py` | Compares CV text against a target role/job description's key terms | Keyword pass |
| `scripts/ats_optimizer.py` | Detects structural ATS issues (headers, tables, contact info placement) | ATS pass |
| `scripts/formatting_helper.py` | Detects bullet-character, date-format, and spacing inconsistencies | Formatting pass |
| `assets/optimized-template.md` | Skeleton for the final rewritten resume | Assembling the Optimized Resume |
| `assets/change-report-template.md` | Skeleton for the Change Report | Assembling the Change Report |
| `assets/rewrite-checklist.md` | Final QA pass before delivering output | Step 7, immediately before sending the response |
| `assets/before-after-example.md` | Worked examples of weak → strong rewrites at the required quality bar | Calibrating rewrite quality before writing the final bullets |
| `assets/improvement-priorities.json` | Severity/priority weights for ordering fixes when a review doesn't already rank them | Step 2, building the priority queue |

## Best Practices

- Always show the factual audit to yourself internally before rewriting a section — if a stronger sentence would require crossing that boundary, it needs a placeholder or a question, not a confident guess.
- Prefer asking one sharp clarifying question over inserting three placeholders in the same section — a real answer is always stronger than a bracket.
- When a review is available, let its priority order drive the rewrite order — don't silently re-prioritize based on your own read unless the review is clearly stale or wrong.
- Keep the Change Report as rigorous as the resume itself — it's the artifact that lets the user trust the rewrite didn't drift from the facts.
- Match keyword integration to language the candidate would recognize and defend in an interview; don't add a term from a job posting that the candidate's actual background doesn't support.
- When in doubt between a punchier claim and an accurate one, choose accurate — the Change Report can note where the underlying achievement, if quantified later, would strengthen the bullet further.

## Failure Handling

- **Only a review is provided, no CV**: state plainly that there's nothing to rewrite without the source document, and ask for it.
- **CV and review reference different documents or contradict each other**: flag the mismatch explicitly and ask which should be treated as current before rewriting.
- **Extraction fails on a file** (image-based PDF, corrupted file): say so and ask for pasted text or a text-based export, the same failure mode `cv-reviewer` handles — don't guess at content from a near-empty extraction.
- **User pushes back that a rewrite is "too weak" and asks to just add a strong-sounding number**: hold the line — explain that inventing a metric would misrepresent them to an employer, and offer to insert a placeholder or ask the clarifying question instead.
- **Ambiguous target role after asking**: proceed using the best-supported assumption from the CV's own content, and state it in the Change Report rather than blocking indefinitely.

## Examples

**Trigger example:**
> User: "Here's my resume and the review you gave me earlier — can you fix the issues it found?" [pastes CV + review]
> → Parse the review's priority list, run the rewrite workflow, ask 2-3 targeted questions only where high-value gaps exist, then deliver the Optimized Resume + Change Report.

**Trigger example (no review):**
> User: "Can you make my resume stronger? I don't have a review, just the file."
> → Run `scripts/improve_cv.py` for a mechanical gap scan, apply the same workflow, note in the Change Report that no external review was used as input.

**Non-trigger example:**
> User: "Is my resume any good?"
> → This is a review request, not a rewrite request — point to (or invoke) `cv-reviewer` instead of rewriting unprompted.

**Boundary example:**
> User: "Add that I led the migration — it'll sound better even though I was just on the team."
> → Decline to misrepresent the role; offer accurate stronger phrasing for genuine individual contribution instead (e.g., "Contributed core service redesign for a team-wide migration"), and explain why in the response.
