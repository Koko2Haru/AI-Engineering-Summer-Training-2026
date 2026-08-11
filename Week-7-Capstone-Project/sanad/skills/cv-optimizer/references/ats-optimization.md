# ATS Optimization — Fix Reference

Companion to `cv-reviewer`'s ATS best-practices reference, but written for *fixing* rather than *diagnosing*. Each entry pairs a structural problem with the specific rewrite/restructure action to take, so the ATS pass in `references/rewriting-guidelines.md` step 4 has a direct action per issue instead of just a description of the problem.

## Section Headers

**Fix:** Rename any non-standard header to its closest standard equivalent before touching the content underneath it.

| Non-standard | Rewrite to |
|---|---|
| "My Journey" / "Career Story" | "Experience" or "Professional Experience" |
| "What I Bring" / "Superpowers" | "Skills" |
| "Where I've Been" | "Experience" |
| "Learning" | "Education" |

Keep the candidate's actual content — only the header changes.

## Layout Structure

**Fix:** If the source resume uses a multi-column layout, text boxes, or tables for content that must be searchable (skills, dates, contact info), restructure it into a single linear column when producing the optimized version. Note the change explicitly in the Change Report, since this is a visual/formatting change, not just a wording one — the user should know their layout is being flattened and why.

Content inside a header/footer (commonly contact info) should be moved into the main body, typically directly under the candidate's name at the top of the document.

## Contact Info Block

**Fix:** Ensure the top of the optimized resume includes, in plain body text (never inside a graphic, table, or header/footer):
- Full name
- Phone number
- Professional email
- City/state (or "Remote," if relevant)
- LinkedIn/GitHub/portfolio links, if the candidate has them and they add signal

If any of these are missing and plausibly exist, this is a good candidate for a clarifying question (see `references/rewriting-guidelines.md`) rather than a placeholder — contact info gaps are high-value and quick to answer.

## Dates

**Fix:** Standardize every date range in the document to one consistent format, "Mon YYYY – Mon YYYY" (or "Mon YYYY – Present" for current roles). Never omit an end date or leave a range ambiguous — if the source is ambiguous, ask rather than guess which end date is correct.

## Keyword Placement

**Fix:** Ensure every skill/technology that appears only inside a bullet's prose also appears in the dedicated Skills section (in the same terminology used in the prose, not a rough synonym) — many ATS keyword filters weight the Skills section heavily and don't reliably parse skills embedded only in narrative bullets. Never add a skill to this section that isn't already substantiated somewhere in the source CV or confirmed by the user.

## Acronyms

**Fix:** On first use of a domain acronym the candidate already uses (e.g., "CI/CD," "SEO," "SaaS"), spell out the full term alongside it once: "Continuous Integration/Continuous Deployment (CI/CD)." This covers ATS systems that match on either form without adding new claims.

## File-Level Guidance (Note in Change Report, Not the Resume Body)

These aren't line-edits but are worth surfacing once in the Change Report if relevant:
- Recommend exporting the final version as a text-based PDF or DOCX — never a flattened/scanned image.
- Recommend a professional file name pattern: `FirstName_LastName_Resume.pdf`.
- If the source document was extracted from an image-based PDF with near-empty text, flag this as a Critical severity issue that must be resolved outside this rewrite (re-export from the original source) — a rewrite cannot fix a missing text layer.

## What Not to Over-Optimize

Don't chase ATS compatibility past the point of human readability — a resume stuffed with repeated keywords or an unnaturally dense Skills section reads poorly to the recruiter who reads it after the ATS filter. Treat every ATS fix in this file as a floor to clear, not a score to maximize. See `references/keyword-optimization.md` for the density guidance that keeps the keyword pass from tipping into stuffing.
