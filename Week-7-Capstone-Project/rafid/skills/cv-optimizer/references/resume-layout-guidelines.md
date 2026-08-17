# Resume Layout Guidelines

Mechanical formatting-consistency rules applied during the formatting pass (`references/rewriting-guidelines.md`, step 5). These are presentation-layer fixes — they change how the document looks, never what it claims. Detected mechanically by `scripts/formatting_helper.py`.

## Bullet Characters

Pick one bullet style and apply it to every bullet in the document. Prefer a simple, universally-rendering character: `•` or `-`. Avoid decorative bullets (arrows, checkmarks, icons) that may not render consistently across viewers or ATS parsers.

## Date Formats

Standardize to one format throughout: `Mon YYYY – Mon YYYY` (e.g., "Jan 2022 – Mar 2024") or `Mon YYYY – Present` for current roles. Never mix formats across entries (e.g., "01/2022" in one role and "January 2022" in another).

## Bolding / Emphasis Convention

Pick exactly one convention and hold it everywhere:
- Bold job titles, regular-weight company names, **or**
- Bold company names, regular-weight job titles

Don't bold both, and don't vary the convention entry to entry. Italics, if used at all, are best reserved for a single consistent purpose (e.g., always the location line) rather than mixed in ad hoc for emphasis.

## Whitespace and Spacing

- Consistent vertical spacing between section headers and their content.
- Consistent spacing between individual entries within a section (e.g., between each job in Experience).
- Avoid cramming multiple entries with zero breathing room to save space — cut weaker content instead (see length guidance in `references/resume-writing-best-practices.md`) rather than compressing whitespace to the point of hurting scannability.

## Section Headers

- Consistent capitalization style across all section headers (e.g., all-caps "EXPERIENCE" or title-case "Experience" — pick one).
- Consistent header size/weight throughout.
- Use standard header names per `references/ats-optimization.md` — this rule serves both ATS parsing and simple visual scannability for a human reader.

## Font

- One font family for body text throughout the document.
- A second font is acceptable only for headers, used consistently.
- Stick to fonts that render reliably everywhere: Arial, Calibri, Georgia, Helvetica, Times New Roman. Avoid decorative or icon fonts.

## Line Length and Bullet Length

Keep individual bullets to roughly 1-2 lines at standard resume margins. A bullet that runs 3+ lines usually contains more than one idea — split it, or cut the less important half, rather than leaving a dense wall of text.

## What This Pass Does Not Touch

Formatting fixes never change wording, add content, or resolve missing quantification — those are the bullet pass's job (`references/achievement-writing.md`). Keep this pass mechanical: if a fix here would require deciding what a sentence should say, it belongs in an earlier pass, not this one.
