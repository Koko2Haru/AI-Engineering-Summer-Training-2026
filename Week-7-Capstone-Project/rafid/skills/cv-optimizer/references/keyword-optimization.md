# Keyword Optimization Reference

How to integrate role-relevant terminology into the rewrite without stuffing, and without adding a claim the candidate doesn't actually support. Used during the keyword pass (`references/rewriting-guidelines.md`, step 3), optionally assisted by `scripts/optimize_keywords.py`.

## Where Keywords Come From

Rank sources in this order of reliability:

1. **A job description the user provided** — the single best source; extract the 8-12 most emphasized skills/requirements (repeated terms, terms in a "required" vs. "nice to have" list, terms in the first few lines of the posting).
2. **A stated target role/industry with no specific posting** — use general, well-established terminology for that role (e.g., a "backend engineer" posting norm-set) rather than a specific company's jargon.
3. **No target role stated at all** — don't invent a keyword target; optimize only for the terminology the candidate's own content already implies, and note in the Change Report that keyword optimization was limited without a stated target.

## The Core Rule

**A keyword only gets added if the candidate's existing content already supports it.** Keyword optimization means *surfacing* skills/experience that are already true but underemphasized or phrased differently — never adding a skill from a job posting because it would look good, if the candidate hasn't actually claimed it anywhere in the source material or confirmed it during clarification.

Example: the job posting says "CI/CD pipelines." The candidate's resume says "automated our build and release process using Jenkins." This is a safe keyword integration — rewrite to "Automated CI/CD pipelines using Jenkins," since the underlying fact (they did CI/CD work) was already there, just phrased differently. It is *not* safe to add "CI/CD" to a candidate's Skills list if nothing in their background supports it.

## Matching Terminology Exactly

When the job description and the candidate's resume describe the same thing with different words, prefer the job description's exact phrasing (since many ATS keyword filters do literal or near-literal matching) — but only when it's a genuine synonym, not a stretch:
- Safe: candidate wrote "customer relationship software," posting says "CRM" → use "CRM (customer relationship management)" to cover both terms.
- Not safe: candidate wrote "used a spreadsheet to track leads," posting says "CRM" → a spreadsheet is not a CRM; don't relabel it as one.

## Keyword Density Guidance

There's no fixed "ideal" keyword count — the target is *natural integration*, not a density score. Practical guardrails:

- Every keyword added to prose should also appear (in the same terminology) in the Skills section, and vice versa where relevant — see `references/ats-optimization.md`.
- A keyword should appear at most 2-3 times across the whole document, in different contexts (once in Skills, once in a relevant bullet) — repeating the same term across many bullets reads as stuffing to both a human reader and increasingly to modern ATS ranking systems.
- If achieving "natural" placement of a keyword requires an awkward, forced sentence, it's better to place it plainly in the Skills section only rather than force it into prose.

## Handling Missing Keywords

If the job description emphasizes a skill/technology genuinely absent from the candidate's background:
- Don't add it, and don't quietly omit mentioning the gap.
- Note it in the Change Report under remaining weaknesses, so the candidate knows this posting may value something they should address before applying (a course, a side project, or simply being ready to discuss the gap in an interview).
- If the user separately confirms they do have relevant experience with it that just wasn't on the original draft, treat that as new factual information supplied during clarification — safe to add, same as any other clarification answer.

## Section-Level Keyword Priorities

- **Skills section**: highest keyword weight for ATS parsing — ensure it's plain text, categorized, and uses the posting's terminology where it's a genuine match.
- **Summary**: 1-2 of the most important keywords, integrated naturally, since this is often the first section both a human and an ATS ranking algorithm weight heavily.
- **Experience bullets**: keywords integrated only where they describe what was actually done — never as a disconnected tag list appended to a bullet.
