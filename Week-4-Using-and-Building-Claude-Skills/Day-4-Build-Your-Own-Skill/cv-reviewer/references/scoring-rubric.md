# Resume Scoring Rubric

Canonical criteria for every score the CV Reviewer skill produces. Consult this file every time a score is assigned so scoring stays consistent across reviews and reviewers (human or model).

## Score Bands (apply to all categories)

| Band | Range | Meaning |
|---|---|---|
| Excellent | 90-100 | Meets or exceeds professional/recruiter expectations with no notable gaps |
| Strong | 75-89 | Solid; minor polish would help |
| Adequate | 60-74 | Functional but has clear, fixable gaps |
| Weak | 40-59 | Multiple significant issues that will likely cost interviews |
| Poor | 0-39 | Fundamental problems likely to cause ATS failure or outright rejection |

Within a band, move up or down based on how many of that category's criteria are fully met (upper half of the band) vs. partially met (lower half).

## Overall Score Weights

| Category | Weight |
|---|---|
| ATS Compatibility | 20% |
| Content Quality | 20% |
| Impact | 15% |
| Grammar & Spelling | 15% |
| Readability | 10% |
| Visual / Layout | 10% |
| Professionalism | 10% |

`Overall = round(Σ category_score × weight)`. These weights and bands are also encoded machine-readably in `../assets/scoring-matrix.json`.

---

## 1. ATS Compatibility (20%)

Checks whether an applicant tracking system can correctly parse the document into structured fields (name, contact, dates, titles, skills).

**Criteria:**
- [ ] Standard, literal section headers used (e.g., "Experience," "Education," "Skills") — not creative renames like "My Journey"
- [ ] No critical information locked inside tables, text boxes, columns, headers/footers, or images
- [ ] Contact info in the document body, not header/footer only
- [ ] Standard, widely-installed fonts (no icon fonts or symbol substitutions for text)
- [ ] Dates in a consistent, parseable format (e.g., "Jan 2022 - Mar 2024")
- [ ] File is a real text-based document, not a scanned image or flattened graphic
- [ ] Reverse-chronological order within each section (ATS and recruiters both expect this)
- [ ] No graphics/icons used to convey information that isn't also present as text (e.g., a phone icon next to a number is fine; a skill-level graphic bar with no text equivalent is not)

Score in the 0-39 range if the document is image-based/unparseable. Score in the 90+ range only if every criterion is cleanly met with zero exceptions.

## 2. Content Quality (20%)

Checks relevance, specificity, and evidence of real scope and ownership.

**Criteria:**
- [ ] Bullet points describe outcomes and scope, not just duties ("owned," "led," "delivered" vs. "responsible for")
- [ ] Content is tailored/relevant to the target role, not a generic list of every task ever performed
- [ ] Specific technologies, methods, or domains are named rather than vague generalities ("built internal tooling in Python and Go" vs. "worked with various technologies")
- [ ] Each experience entry has enough bullets to convey real substance (2-3 minimum for anything beyond a short stint) without padding
- [ ] No irrelevant or outdated content crowding out relevant material (e.g., a 15-year-old unrelated job taking equal space to the most recent, relevant role)

## 3. Impact (15%)

Checks how much of the resume demonstrates measurable results rather than described activity.

**Criteria:**
- [ ] Majority of bullets include a quantified outcome: a number, percentage, dollar amount, time saved, or scale indicator
- [ ] Where a hard number truly isn't available, scope is still conveyed (team size led, users affected, systems touched)
- [ ] Bullets follow a result-first or STAR/XYZ structure ("Reduced page load time by 40% by...") rather than duty-first ("Was in charge of...")
- [ ] Achievements are distinguishable from routine responsibilities — the reader can tell what was exceptional vs. expected

Score below 40 if quantification is essentially absent across the whole document. Score 90+ only if the large majority of bullets (not just one or two standout lines) are quantified.

## 4. Grammar & Spelling (15%)

**Criteria:**
- [ ] No spelling errors
- [ ] Consistent verb tense within each entry (past tense for past roles, present tense only for the current role)
- [ ] Consistent punctuation style across bullets (e.g., either all bullets end with periods or none do)
- [ ] Correct subject-verb agreement and article usage
- [ ] No sentence fragments that read as errors rather than intentional style (bullet fragments starting with a verb are fine and expected; broken grammar is not)

A single typo caps the score at "Strong" (89) at most, not "Excellent." Multiple typos or tense inconsistencies push into "Adequate" or below.

## 5. Readability (10%)

**Criteria:**
- [ ] Bullets are concise — roughly one line to two lines each, not dense paragraphs
- [ ] Sentences avoid unnecessary jargon or unexplained acronyms outside the candidate's own field
- [ ] Information is grouped logically (skills grouped by category, not one long unsorted list)
- [ ] Active voice is used throughout
- [ ] A reader can understand what the candidate actually did without needing outside context

## 6. Visual / Layout (10%)

**Criteria:**
- [ ] Consistent formatting: one font family, consistent sizing hierarchy, consistent bullet character/style
- [ ] Balanced whitespace — not cramped, not sparse
- [ ] Length appropriate to seniority (see length norms in `resume-writing-guide.md`)
- [ ] Clear visual hierarchy so section boundaries and job titles/dates are easy to scan
- [ ] No orphaned single lines or awkward page breaks (when a page count is knowable)

## 7. Professionalism (10%)

**Criteria:**
- [ ] No first-person pronouns ("I," "my") in bullets
- [ ] Professional email address (not a nickname, number-heavy, or outdated domain handle)
- [ ] No irrelevant personal information (age, marital status, photo, full home address) unless standard for the candidate's region/industry
- [ ] Consistent, professional tone throughout — no slang, excessive exclamation, or informal phrasing
- [ ] No unexplained employment gaps presented in a way that looks evasive (a gap itself isn't unprofessional; how it's handled can be)

---

## Applying the Rubric: Worked Example

A bullet like:

> "Responsible for helping the team with various backend tasks and projects."

- Impact: fails quantification and outcome criteria → contributes to a low Impact score.
- Content Quality: "various" and "helping" are vague, non-specific → contributes to a low Content Quality score.
- Professionalism/Grammar: no issues here specifically.

Rewritten:

> "Rebuilt the order-processing service's retry logic, cutting failed-payment incidents by 35% and reducing on-call pages by half."

This single change would move both the Impact and Content Quality scores up for that entry — always show this kind of before/after when critiquing a bullet, not just the score impact in the abstract.
