# Rewriting Guidelines

The core operating manual for this skill. Every other reference file covers a specific technique (verbs, keywords, layout); this one covers the rules that govern how those techniques get applied — what may change, what may never change, and what to do when a stronger rewrite needs information that isn't there.

## The One Rule Everything Else Follows

**Rewriting improves how a fact is expressed. It never adds a fact that wasn't given.**

Every technique in this skill — stronger verbs, tighter phrasing, quantification, keyword integration, reordering — operates on *expression*, not *substance*. If a rewrite would only be true because a number, scope, or outcome was assumed rather than confirmed, it's not a rewrite; it's a fabrication, and it's out of scope no matter how much it would improve the resume.

This holds even when the fabrication would be small and plausible. "Managed a team" becoming "Managed a team of 6" is not a safe rounding error — it's an invented headcount. The correct move is a placeholder or a clarifying question, never a plausible-sounding guess.

## The Factual Audit (Do This First, Every Time)

Before rewriting any section, extract a plain list of every verifiable claim it contains:

- Employers, job titles, employment dates
- Degrees, institutions, graduation dates, GPA if listed
- Certifications and their issuing bodies
- Any number already present (metrics, headcounts, percentages, dollar amounts, durations)
- Named tools, languages, frameworks, methodologies
- Named projects and any stated outcome

This list is the boundary. Every rewritten sentence must be checkable against it: does this sentence claim anything beyond what's on this list (or what the user supplied during clarification)? If yes, it needs a placeholder, a question, or it doesn't get written.

## Rewrite Passes, In Order

Apply these in sequence per section — later passes assume earlier ones are done, so don't skip ahead:

1. **Structural pass** — is the content in the right section, in the right order? (`references/resume-writing-best-practices.md`)
2. **Bullet pass** — rewrite each line using [strong, accurate verb] + [what was actually done] + [quantified result, only if it exists] + [method, if space allows]. (`references/achievement-writing.md`, `references/action-verbs.md`)
3. **Keyword pass** — work in role-relevant terminology the candidate's actual background supports. (`references/keyword-optimization.md`)
4. **ATS pass** — fix structural parseability issues. (`references/ats-optimization.md`)
5. **Formatting pass** — normalize bullets, dates, spacing. (`references/resume-layout-guidelines.md`)
6. **Readability pass** — grammar, spelling, tense consistency, redundancy trim.

Doing the bullet pass before the keyword pass matters: a bullet rewritten for impact first, then checked for natural keyword fit, reads better than one written keyword-first and retrofitted with impact language.

## Severity Prioritization

When a `cv-reviewer` output is available, its priority ordering (Top 10 Improvements, Quick Wins) drives the rewrite order directly — don't re-derive priority from scratch when a review already did that work.

When no review is available, use this default severity ordering (see `assets/improvement-priorities.json` for the machine-readable version):

1. **Critical** — ATS-blocking structural issues (missing text layer, broken section headers, contact info unparseable).
2. **High** — no quantification anywhere; generic/absent summary; weak verbs throughout; missing standard sections.
3. **Medium** — inconsistent formatting; keyword gaps against a stated target role; repetitive verb usage.
4. **Low** — minor grammar/spelling polish; section-order optimization; whitespace balance.

Fix critical and high-severity issues even if it means asking clarifying questions first; medium/low issues can usually be resolved with placeholders or silently fixed without user input.

## Placeholder Conventions

Use a placeholder whenever a stronger rewrite is blocked by missing information and a clarifying question either wasn't asked or wasn't answered. Placeholders must:

- Be wrapped in square brackets so they're unmistakably not final text: `[Consider adding a measurable outcome here — e.g., % improvement, users affected, time saved.]`
- Describe *what kind* of information would strengthen the line, not just flag that something is missing — `[Add outcome]` is less useful than `[Provide the result of this migration — performance gain, downtime avoided, or scale reached]`.
- Never be silently dropped from the visible resume text — a placeholder that only appears in the Change Report but not inline in the resume risks being missed entirely by the user.
- Be re-listed in the Change Report's "Suggestions Requiring User Input" section so there's one place the user can scan for every open item.

Common placeholder patterns:

| Situation | Placeholder |
|---|---|
| Bullet has action but no measurable result | `[Consider adding a measurable outcome here — e.g., % improvement, time saved, revenue impact.]` |
| Project has no stated outcome | `[Provide the project's outcome or impact if available — did it ship, get adopted, solve a specific problem?]` |
| Team size implied but not stated | `[Add team size if this involved leading or coordinating others.]` |
| Summary needs a target role to be concrete | `[Specify target role/industry to sharpen this summary.]` |
| Certification/skill claim lacks a level or context | `[Confirm proficiency level or context for this skill if it should be emphasized.]` |

## When to Ask Instead of Placeholder

A clarifying question is preferable to a placeholder whenever:
- The gap is in a high-visibility section (summary, top 1-2 bullets of the most recent role) where a placeholder would be jarring.
- The missing information plausibly exists and is easy for the candidate to supply (a number they'd know off the top of their head).
- There are few enough gaps that a short round of questions won't overwhelm the user.

A placeholder is preferable to a question whenever:
- There are many small gaps and asking about all of them would be tedious relative to their impact.
- The user has signaled they want a fast pass, not a deep back-and-forth.
- The missing information is genuinely uncertain even to the candidate (e.g., "was there a broader business outcome to this?" when they may not know).

### Writing Good Clarifying Questions

- **One topic, one question.** Don't bundle "what's your target role and can you quantify this and do you have a GitHub link" into one message.
- **Specific over open-ended.** "Can you put a number on the team size you managed?" beats "Tell me more about this role."
- **Ordered by impact.** Ask about target role and missing quantification on high-visibility bullets before asking about minor polish items.
- **Stop early.** Once enough is gathered to write a strong resume, proceed — don't work through a fixed checklist by rote if the document is already mostly unblocked.

Examples of well-formed questions, roughly in priority order:
1. "What role or industry are you targeting with this resume?"
2. "For [specific bullet], can you quantify the result — a percentage, dollar figure, user count, or time saved?"
3. "Which project are you most proud of, and what was its outcome?"
4. "Did [specific bullet] involve leading or coordinating other people? If so, how many?"
5. "Do you have a GitHub, portfolio, or LinkedIn link to include?"
6. "What certifications do you currently hold, if any aren't listed?"
7. "Is there anything relevant you intentionally left off this draft?"

Examples of questions to avoid: "Tell me about yourself." / "What else should I know?" / "Is there anything you want to add?" — all too broad to act on directly.

## Preserving Meaning While Strengthening Language

A rewrite is safe when it changes *how* a true statement is expressed without changing *what* it claims. Quick self-check before finalizing any bullet: could the candidate defend this exact sentence, unprompted, in an interview? If a stronger verb or framing would make them hesitate ("well, I didn't really *lead* it..."), it's overreaching.

- Safe: "Helped build the internal reporting tool" → "Built core data-aggregation logic for the internal reporting tool" (sharper, still accurate about scope of contribution).
- Unsafe: "Helped build the internal reporting tool" → "Led development of the internal reporting tool" (changes ownership level without confirmation).
- Safe: "Worked on reducing page load time" → "Reduced page load time by optimizing image delivery" (names the actual mechanism, still no invented number).
- Unsafe: "Worked on reducing page load time" → "Reduced page load time by 40%" (invents a metric).

## Handling a Provided Review

When `cv-reviewer` output is supplied:

1. Extract its category scores, flagged weak bullets, missing sections, and prioritized improvement list.
2. Map each flagged item to a rewrite pass above.
3. Address items in the review's own priority order unless it's clearly stale (references a section no longer present) or contradicts the current CV — in either case, flag the mismatch to the user rather than silently reconciling it.
4. Don't re-run a full independent audit from scratch when a review is present — that duplicates work and can produce a different, confusing priority order. Use the review as the source of truth for *what's* wrong; this skill's job is fixing it, not re-diagnosing it.

## Self-Check Before Finalizing

For every rewritten bullet, confirm:
- [ ] Every noun and number traces back to the factual audit or a user-supplied answer.
- [ ] No verb implies a greater scope of ownership than the source supports.
- [ ] Any gap that blocked a stronger version is either asked about or marked with a visible placeholder — never silently smoothed over.
- [ ] The sentence is something the candidate could defend, unprompted, in an interview.

If any box doesn't check, the rewrite isn't done — either fix it, ask, or placeholder it.
