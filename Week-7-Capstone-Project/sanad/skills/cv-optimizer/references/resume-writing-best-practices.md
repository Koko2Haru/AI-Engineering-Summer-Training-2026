# Resume Writing Best Practices

Structural and stylistic target state for the optimized resume — what "good" looks like once the rewrite passes are complete. Use alongside `references/rewriting-guidelines.md` (which governs *how* to get there without fabricating) and `references/resume-layout-guidelines.md` (formatting mechanics).

## Standard Section Order

1. **Contact Info** — name, phone, email, location, relevant links
2. **Summary** — 2-4 lines; include for career changers, senior candidates, or anyone whose target role isn't obvious from job titles alone; optional for early-career candidates where space is tight
3. **Experience** — reverse chronological
4. **Projects** — promote above Experience for students/career changers when projects better demonstrate target-role skills than the work history does
5. **Education** — reverse chronological; move above Experience for students/new grads with limited work history
6. **Skills** — grouped by category, not a flat list
7. **Certifications / Awards / Leadership / Volunteer** — include only sections that add genuine signal for the target role; don't pad the resume with sections just to fill the page

When rewriting, don't reorder sections purely on aesthetic preference — reorder only when it demonstrably serves the target role or fixes something the review flagged. Always explain a section-order change in the Change Report.

## Length Targets

| Candidate Profile | Target Length |
|---|---|
| Student / entry-level (0-2 yrs) | 1 page |
| Mid-level (3-8 yrs) | 1 page, 2 only if content genuinely earns it |
| Senior / staff+ (8+ yrs) | 1-2 pages |
| Academic/research CV | Not length-constrained the same way — publications/grants justify more |

If a rewrite risks pushing a resume over its target length, cut the lowest-value content (oldest/least-relevant roles, weak bullets that can't be strengthened) rather than shrinking font/margins or letting length creep silently. Note any content cut in the Change Report.

## Tense and Voice

- Past roles: past tense throughout.
- Current role: present tense for ongoing duties, past tense for completed achievements within it — stay internally consistent within that one role.
- Never first person ("I," "my," "me") — bullets are implied first-person.
- Active voice always: "Automated the deployment pipeline," never "The deployment pipeline was automated by me."

When the rewrite pass encounters inconsistent tense across the document, standardize it and note the fix in the Change Report's grammar/formatting section.

## Summary / Objective Statements

A summary should state: role/specialization, years of relevant experience (if it strengthens the read), and 1-2 standout areas of real impact — not generic self-description.

- Weak (leave behind): "Hardworking team player seeking a challenging opportunity to grow."
- Strong (rewrite target): "Backend engineer with 4 years building distributed systems in Python and Go; shipped a payments migration serving 500K+ daily transactions."

If the source resume has no summary and one would help (career changer, senior candidate, or unclear target role from titles alone), draft one from content already in the CV — never invent the years of experience or the headline achievement it references. If the underlying strong achievement doesn't exist in the source, use a placeholder rather than writing a summary that oversells the CV beneath it, per `references/rewriting-guidelines.md`.

## Skills Section

Group by category:

```
Languages: Python, TypeScript, Go
Frameworks: React, Django, FastAPI
Infrastructure: AWS, Docker, Kubernetes
```

Only include skills already present somewhere in the source CV or confirmed by the user during clarification — never add a skill because it's common for the target role if the candidate hasn't actually claimed it.

## Formatting Consistency

- One font family throughout the document (a distinct header font is fine if used consistently).
- One bullet character/style throughout.
- One consistent date format throughout.
- One consistent bolding convention (e.g., always bold job titles, never company names — pick one and apply everywhere).
- Consistent spacing between sections and entries.

See `references/resume-layout-guidelines.md` and `scripts/formatting_helper.py` for the mechanics of detecting and fixing these.

## Section-Specific Notes

- **Education**: full institution name, degree, graduation date (or expected date); GPA only if strong (typically 3.5+) and candidate is early-career; relevant coursework only if Experience/Projects are thin.
- **Certifications**: full name plus issuing body; expired certifications should be labeled or dropped depending on relevance — ask if unclear rather than guessing.
- **Awards**: name the award, issuing body, and (if available) the scale/selectivity that gives it context ("1 of 40 selected nationally" only if the candidate actually knows and states this).
- **Leadership / Volunteer**: hold to the same bullet formula as Experience (`references/achievement-writing.md`) rather than a lower bar — a strong volunteer bullet can carry real weight, especially for early-career candidates.
