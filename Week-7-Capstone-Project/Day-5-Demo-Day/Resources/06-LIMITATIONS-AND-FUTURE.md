# Sanad — Limitations and Future Work

*Source document 7 of 7. Self-contained: assumes no knowledge of the other files.*

Sanad is a Discord bot that reviews and rewrites CVs, then matches them against live freelance work. This document is the honest account of what it cannot do, what is known to be imperfect, and what a next version would fix.

---

## Structural limitations — properties of the design, not bugs

These are consequences of decisions taken deliberately. None is going to be fixed within this version.

### It only runs while the PC is on

Both n8n and the bridge must be running. Close the laptop and the daily digest does not arrive. There is no server anywhere.

This is the direct cost of the "no inbound networking" decision, which is also what removes the need for a public URL, a tunnel, a VPS and a certificate.

### One user per instance

No user table, no authentication, no multi-tenancy. Every person who wants Sanad runs their own copy.

This single cut is what made everything else fit in a three-day build window.

### Self-hosting is required, not preferred

n8n Cloud cannot reach a process on your laptop, so the Claude Code integration — the thing that makes CV review free — could not exist there.

The bill: n8n Cloud ships its own registered Google OAuth application, making Sheets a one-click connection. Self-hosted n8n has none, turning that into a service-account setup with a key file.

### One job source

Freelancer.com only. A second source was evaluated and measured — roughly 11 contract roles, heavily skewed to one country, mostly a single employer, no budget data — and **dropped rather than deferred**.

### Only "money" is objective

The original vision ranked jobs on money, difficulty, skills gained and resume worth. Only money exists as a field in any API. The other three are model judgements, so they were cut rather than invented.

### It finds and pitches; it does not apply

Sanad hands you a link and an opening line. A human sends it.

### PDF and plain text only

DOCX and images are not read.

### The 15-second poll is a compromise

It feels live in a demo and costs nothing on a self-hosted instance, but it is polling, not push. A message is noticed within 15 seconds, not instantly.

---

## Measured defects

These were found by testing and have numbers attached.

### Score compression — the most actionable one

```
 90 : #        (1)
 85 : ##       (2)
 80 : ######   (6)   ← 55% of every match ever scored
 70 : ##       (2)
```

**Four distinct values across 11 matches, all multiples of five, more than half at exactly 80.**

Six of eleven matches were **tied**, so their displayed order came from the sort rather than from any quality difference. *"The top 5, ranked"* is partly an illusion.

**Cause, and it is a prompt-design flaw rather than a model failure:** the scoring prompt offers four bands (80–100, 50–79, 20–49, 0–19). The model picks a band and anchors to its boundary. **It is scoring categorically while being asked for a continuous number.**

**Fix:** either remove the band boundaries so there is nothing to anchor to, or score several sub-criteria separately and sum them — which would also yield a defensible explanation per score.

### Pitch invention, roughly 9%

One pitch in eleven opened *"Having replicated an existing business website…"* — a claim absent from the CV — and cited no named project.

This is the same failure mode as the CV rewrite (see below), in a different component. The self-assessment flag caught and recorded it; the prompt did not prevent it.

### Currencies are not normalised

A single result set contained **CAD, USD, AUD and INR**. Budgets cannot be compared across them, which undermines *money* as the one genuinely objective axis. The predecessor project normalised to USD; the port dropped it.

### The scorer is generous

A *job-description writing* task scored **80/100** against a web developer's CV. The prompt explicitly instructs low scores for weak overlap, and it was not followed.

### Non-PDF attachments report as "no attachment"

Sending a `.docx` produces *"I don't see a CV attached — could you send it as a PDF?"* The next action is correct, but the wording is untrue: a file *was* attached.

Cause: non-PDFs are filtered out upstream, so "wrong type" and "nothing attached" are indistinguishable downstream. **The fix was written and deliberately reverted**, so the committed code matches what was actually tested.

### Small hedge-dropping in rewrites

*"around 35"* became *"35+"*; *"approximately 12"* became *"12"*. One dropped hedge each. Within normal CV-writing latitude, but it is the same directional bias as the invention problem, just milder.

### Only the newest message per poll is processed

Two messages inside the same 15-second window means the older one is skipped, not queued. Fine for one person typing.

### A claimed message that fails is lost

The concurrency fix writes the "seen" marker **before** the slow work, so a crash mid-flight means that message is never retried. Accepted for this version — the user resends.

**Designed but not built:** a two-phase claim (`claimed` → `completed`) with stale claims released on a timeout.

### The bridge is a single point of failure

It owns state, files, PDF rendering and every Claude Code call. It holds nothing in memory and restarts cleanly, but nothing works while it is down.

---

## The invention problem, in full

Worth its own section, because it is the most interesting defect in the project and it was largely fixed.

The first rewrite invented three things:

| The CV said | What was actually said | The move |
|---|---|---|
| *"saving 2–10 hours **per week**"* | *"saved between 2-10 hrs"* | **added a rate** |
| *"a **client base of 100+**"* | *"**used by** 100+ clients"* — about a tool | **re-attributed a number** |
| *"**majority** repeat-and-referral"* | *"**many** happy clients"* | **strengthened a quantifier** |

**None is a hallucination.** The model invented nothing. It **resolved ambiguity in the candidate's favour**, three times — which is subtler and more dangerous, because *"2–10 hours per week"* is exactly the claim an interviewer probes.

**The instruction "never invent facts" was already present and prevented all three**, because none of them felt like inventing a fact.

The rule only worked once it named the moves explicitly, and added: *if an answer is ambiguous, do not pick the more impressive reading; use a placeholder.*

**Re-tested with the same ambiguous input: all three gone.** The intake now asks for the unit alongside every number and re-asks once when an answer is unclear.

**Residual risk:** roughly 9% in pitches, and mild hedge-dropping in rewrites. The mechanism is understood but not eliminated.

---

## What was not tested

Stating this is part of the result.

**Job-ranking determinism.** **Methodologically blocked** — the pipeline drops previously-sent jobs and the live pool changes between calls, so two runs never see the same input. A real test needs a frozen job pool.

**Error handling on a published trigger.** Manual runs inject placeholder data that looks like a pass, so a genuine test requires a deliberate production failure.

**Bridge failure mid-review.** Requires killing an in-flight run.

**The polished fixture end to end through Discord.** Scored directly, never sent as a full conversation.

**Sample sizes are small.** 11 matches, 4 CV scoring runs, one run per failure path. The 91% citation rate is 10 of 11 — one more failure would make it 83%. The defensible claim is directional: *citation went from none to nearly all; filler from most to none.*

---

## Version 2 — designed, not built

Ordered by value.

### 1. Fix score compression
Remove the band boundaries, or score sub-criteria and sum them. Would make ranking mean something and produce an explanation per score.

### 2. Normalise currencies
Convert every budget to one currency at fetch time. Restores *money* as a usable axis and makes "the highest-paying one" answerable.

### 3. Two-phase claim
`claimed` → `completed`, with stale claims released on a timeout. Removes the "crash loses the message" trade-off.

### 4. One job per parameter
*"The money one, the learning one, the portfolio one."* Cheap to add and the best-demonstrating feature not built.

### 5. "Add this new project to my CV"
Closes the loop and proves the CV is genuinely persistent state rather than a cache.

### 6. A revision loop on the rewrite
*"Anything you'd like changed?"* Needs multi-turn editing state.

### 7. Keep / drop / refresh on matches
With replacements offered for anything dropped. Needs per-match state and a re-query path.

### 8. Four-axis scoring, honestly
Only worth building alongside a way to evaluate whether the three subjective axes mean anything.

### 9. A second job source
Only if a genuinely good one is found. The one evaluated was worse than nothing.

### 10. Move state to a real database
The JSON file works and is atomic, but it is one user's worth of state by design.

---

## The honest summary

**What works, with evidence:** a CV goes from 42/100 to 73/100 — two points off a professionally written version of the same person. Pitches cite real past projects 91% of the time, against 0% before. A gig arrives every morning without being asked. Everything runs at zero marginal cost on one laptop.

**What does not:** ranking within the top five is close to meaningless because most scores are tied. About one pitch in eleven overstates experience. Budgets are not comparable across currencies. It stops entirely when the laptop sleeps.

**What is unknown:** whether job ranking is reproducible, because it could not be measured against a live pool.
