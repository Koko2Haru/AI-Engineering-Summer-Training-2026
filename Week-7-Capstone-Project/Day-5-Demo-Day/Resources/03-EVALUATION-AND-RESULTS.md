# Rafid — Evaluation and Results

*Source document 4 of 7. Self-contained: assumes no knowledge of the other files.*

Rafid is a Discord bot that reviews and rewrites CVs, then matches them against live freelance work. This document contains every measurement taken, the method behind each, and what was deliberately left unmeasured.

---

## The headline result

### Does the rewrite actually make the CV better?

This is the claim the entire project rests on, and for three days it was an assumption.

**Method.** Earlier runs produced scores of 46, 49 and 40 — but they were **not comparable**, because each used a different target role and different intake answers. To isolate the document as the only variable, everything else was pinned:

- the same reviewer skill
- the same stated target: *full-stack web developer, junior-to-mid, in-house, screened by an ATS*
- **no intake questions** — proceed on stated assumptions
- score-only output, so the runs stay short

**Results.**

| Document | Score | Band |
|---|:-:|---|
| Original messy fixture | **42** | Weak |
| Original messy fixture *(re-run)* | **42** | Weak |
| **Rafid's rewrite of it** | **73** | Adequate |
| Hand-written "polished" version | **75** | Strong |

### **+31 points. Two points short of a professionally written CV of the same person.**

Same facts, same person, same reviewer. The only thing that changed is that Rafid rewrote it.

---

## Three findings underneath that number

### 1. The CV reviewer is deterministic

**42 twice, identical.** This corrected a standing assumption. The earlier 46 / 49 / 40 spread was **not** model noise — it was different target roles and different intake answers between runs. Hold the inputs constant and the score does not move.

This matters for how results are reported: non-determinism applies to **job ranking**, not to CV scoring, and the two should not be described in the same breath.

### 2. The reviewer scores against the stated target, not against polish

The polished fixture scored **75** here, against a documented baseline of **85** elsewhere. That is the reviewer working correctly, not a regression.

This run forced the target to *junior-mid in-house full-stack*. That CV is a **freelance e-commerce specialist's** CV. The mismatch cost it ten points.

> **Consequence:** any score quoted without its target role is meaningless.

### 3. The nature of the remaining problems changed

| The original's top 3 issues | The rewrite's top 3 issues |
|---|---|
| zero quantification anywhere | unfilled `[Add phone number]` placeholders |
| non-standard headers, ATS mis-parse risk | thin evidence of *custom* full-stack work |
| age / marital status / unprofessional email | inconsistent date formatting |

The original's problems were **presentation**. The rewrite's are **substance and unfinished fields** — things no rewrite could honestly fix without the candidate supplying a phone number or actually having backend experience.

That is the correct place for a rewrite to stop, and it is what a working "never invent" rule looks like from the outside.

---

## Match quality

**Method.** Rather than burning new runs, every Job Matching execution stored in n8n's database was parsed and counted. Each match carries three self-assessment flags written at generation time: does the pitch cite a real past project, does it contain banned filler phrasing, is the pitch missing.

**Sample: 11 matches across 3 runs.**

| Metric | Predecessor project | Rafid |
|---|:-:|:-:|
| Pitches citing a **real past project** | **0 / 5** | **10 / 11 (91%)** |
| Pitches containing banned filler | **3 / 5 (60%)** | **0 / 11** |
| Pitches missing entirely | — | **0 / 11** |

**What changed.** The predecessor's profile schema extracted *skills only*, so the pitch step never saw the candidate's projects and literally could not cite them. Three of five pitches reused *"deliver a high-quality solution that meets your requirements"*.

Adding a `notable_projects` field to the profile — plus a requirement to cite one by name and an explicit ban list — took citation from **0% to 91%** and filler from **60% to 0%**.

> The diagnosis matters as much as the fix: it was never the model, it was the schema.

**Example of the output now:**

> *"I've built scalable e-commerce platforms like **Homeware E-Commerce Shop**, which saw a 20% increase in sales. I'd leverage my PHP expertise to create a robust backend. First, I'd design a database schema to efficiently store user financial data."*

---

## The score compression problem

The most actionable negative finding.

```
 90 : #        (1)
 85 : ##       (2)
 80 : ######   (6)   ← 55% of every match ever scored
 70 : ##       (2)
```

**Four distinct values across 11 matches. All multiples of five. More than half at exactly 80.**

So "the top 5, ranked" is partly an illusion: **six of eleven matches were tied**, and their displayed order came from the sort, not from any real quality difference.

**The cause is visible in the prompt.** It gives the model four bands:

```
80-100: squarely in their core skills
50-79:  adjacent, could do it with some stretch
20-49:  weak overlap
0-19:   wrong field entirely
```

The model picks a band and anchors to its boundary. **It is scoring categorically while being asked for a continuous number.** That is a prompt-design flaw, not a model failure.

**Fix identified, not implemented:** either remove the band boundaries so there is nothing to anchor to, or score several sub-criteria separately and compute the total — which would also produce a defensible explanation of each score.

---

## Scoring honesty

Two behaviours worth recording, because they cut in opposite directions.

**It declines to inflate weak matches.** Reasons attached to low scores included:

> *"Weak overlap, freelancer knows Python but lacks robotics/electronics expertise"*
> *"Adjacent, freelancer has PHP but lacks mobile app development expertise"*

**But it is still generous.** A *job-description writing* task scored **80/100** against a web developer's CV. The prompt explicitly instructs low scores for weak overlap; it was not followed here.

---

## Robustness

### The salvage path proved itself in production

One execution carries `response_was_truncated: true` and still returned **5/5 pitches citing projects, 0 missing**.

The pitch model's output was cut off mid-JSON in a real run. The parser recovered every complete pitch rather than losing all five because the last was clipped. That path was written and unit-tested offline; this is it working unprompted on live data.

### Failure paths tested

| Input | Behaviour | Verdict |
|---|---|---|
| Off-topic message (`I like banana`) | routed to conversation, not job search; answered with a joke, then steered back | **pass** |
| A `.docx` attachment | *"I don't see a CV attached — could you send it as a PDF?"* No crash, no silent drop | **pass, with a wording flaw** |
| Every project already sent | explicit empty result, *"nothing new today"* | **pass** |
| Truncated model output | complete items salvaged, remainder flagged | **pass** |
| Same message polled repeatedly during a 3-minute job | claimed once, all other polls stop | **pass** |

The `.docx` case degrades usefully — the user re-exports as PDF — but the message is inaccurate: a file *was* attached, just not a readable one. The cause is that non-PDFs are filtered upstream, making "wrong type" indistinguishable from "nothing attached". **The fix was written and deliberately reverted**, so the committed code matches what was actually tested.

---

## What was NOT measured, and why

Stating this plainly is part of the result.

**Job-ranking determinism.** The prediction was that two of five matches would move between identical runs. **Methodologically blocked:** the pipeline drops previously-sent jobs, and the live project pool changes between calls, so two consecutive runs never see the same input. A real test needs a frozen job pool. Recorded as **unmeasured**, not guessed.

**Error handling on a published trigger.** Not attempted. Manual runs inject placeholder data that looks like a pass, so a genuine test requires a deliberate production failure.

**Bridge failure mid-review.** Requires killing an in-flight run. Skipped by choice.

**The polished fixture end to end.** It was scored directly, but never sent through Discord as a full conversation.

---

## Sample sizes, stated honestly

| Measurement | n |
|---|:-:|
| CV score comparison | 4 runs |
| Match quality rates | 11 matches, 3 runs |
| Score distribution | 11 matches |
| Failure paths | 1 run each |

**These are small.** The citation rate of 91% is 10 of 11 — one more failure would make it 83%. The claim that survives scrutiny is directional, not precise: *citation went from none to nearly all, and filler from most to none.*

The CV score comparison is the strongest result, because the effect is large (+31) and the confound (input variation) was explicitly controlled for and then verified by the identical repeat.

---

## Summary

| Claim | Evidence | Confidence |
|---|---|---|
| The rewrite substantially improves the CV | 42 → 73, controlled | **High** |
| The rewrite approaches hand-written quality | 73 vs 75 | **Moderate** — one document |
| Pitches now cite real work | 10/11 vs 0/5 before | **High** — large effect |
| Filler phrasing is eliminated | 0/11 vs 3/5 before | **High** |
| Ranking within the top five is meaningful | **contradicted** — 55% tied | **Refuted** |
| The reviewer is deterministic | 42 twice, inputs pinned | **Moderate** — one pair |
| Job ranking is deterministic | not measurable with a live pool | **Unknown** |
