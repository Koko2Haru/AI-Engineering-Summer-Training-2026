# ATS Optimization Best Practices

Applicant Tracking Systems (ATS) — Workday, Greenhouse, Lever, Taleo, iCIMS, and similar — parse resumes into structured fields before a human ever sees them. A resume that reads perfectly to a person can still fail here if the underlying document structure confuses the parser. This reference covers what to check and why it matters.

## How ATS Parsing Actually Works

Most modern ATS platforms convert the resume to plain text (or use a PDF text layer directly) and then apply pattern matching to sort content into fields: name, contact info, work history, education, skills. Anything that pattern matching can't confidently place either gets dropped, misfiled, or dumps into a single unsearchable blob. Recruiters then search/filter on those parsed fields — a candidate who is a great fit but was parsed incorrectly may never surface in a keyword search.

## Structural Rules

- **Use standard section headers.** "Experience," "Work Experience," "Professional Experience," "Education," "Skills," "Certifications." Creative alternatives ("My Journey," "What I Bring") often aren't recognized as the section type they represent.
- **Avoid multi-column layouts.** Many parsers read left-to-right, top-to-bottom across the whole page width — a two-column layout can interleave unrelated lines (e.g., a date from the left column merging mid-sentence with a bullet from the right column).
- **Avoid tables for content that must be searchable.** Table cells are inconsistently parsed across ATS vendors; skills or dates placed in table cells can vanish entirely from the parsed output.
- **Avoid text boxes and headers/footers for contact information.** Content inside a text frame or the document header/footer is frequently skipped by parsers that only read the main body flow. Contact info should sit in the main body, typically at the top.
- **Avoid embedding text as images or icons.** Any text inside a graphic (including "creative" resume templates that render whole sections as an image) is invisible to a parser — it does not exist as far as the ATS is concerned.
- **Use standard fonts.** Stick to fonts installed on virtually all systems (Arial, Calibri, Georgia, Times New Roman, Helvetica). Custom or icon fonts can render as garbled characters when the parser or downstream viewer doesn't have the font.
- **File format:** a text-based PDF (exported from a word processor, not scanned/flattened) or a .docx are both broadly safe. A scanned image saved as PDF has no text layer at all and will fail parsing completely — this is one of the most common and most severe ATS failures.

## Content Rules

- **Use exact keyword matches from the job description where truthful.** If the posting says "CI/CD pipelines" and the candidate has done exactly that, use that exact phrase at least once rather than only a paraphrase — many ATS keyword filters do literal or near-literal matching.
- **Spell out acronyms at least once.** "Search Engine Optimization (SEO)" covers both a parser matching the acronym and one matching the full phrase.
- **List skills in a dedicated, plainly-labeled Skills section**, not only embedded in prose within bullet points — this is the section most heavily weighted by keyword-search ATS features.
- **Use standard date formats.** "Jan 2022 – Mar 2024" or "01/2022 – 03/2024" parse reliably. Avoid unusual formats or omitting dates entirely, since date range is a commonly parsed field used for tenure and gap calculations.
- **Don't keyword-stuff.** Repeating a keyword unnaturally or hiding keywords in white-on-white text is both ineffective (modern ATS and recruiters both catch it) and, in the case of hidden text, can get an application flagged as manipulative.
- **File naming matters at the margins.** `FirstName_LastName_Resume.pdf` is safer than `Document1.pdf` or a name with special characters — some systems use the filename as an initial candidate-name signal.

## Common ATS Failure Patterns to Flag During Review

| Symptom | Likely Cause | Fix |
|---|---|---|
| Extracted text is empty or near-empty | Scanned/image-based PDF with no text layer | Re-export from the original source document as text-based PDF/DOCX |
| Extracted text is present but garbled/out of order | Multi-column layout or text boxes | Convert to single-column, linear layout |
| Skills section keywords don't show up in extracted text | Skills rendered as a graphic/icon bar (e.g., star ratings) | Replace with plain-text skill list |
| Contact info missing from extracted text | Info placed in header/footer | Move name, phone, email, location into the main document body |
| Dates missing or inconsistent | Non-standard date formatting or omitted end dates | Standardize to "Mon YYYY – Mon YYYY" throughout |

## What ATS Optimization Is Not

Optimizing for ATS does not mean sacrificing readability for a human reviewer, and it does not mean keyword-stuffing. Every recruiter still reads the resume after it clears the ATS filter — a resume that's ATS-parseable but full of jargon-stuffed, unreadable bullets will simply fail at the next stage instead. Treat ATS compatibility as a floor (don't get filtered out on structure) not a ceiling (don't optimize purely for keyword count at the expense of clarity).
