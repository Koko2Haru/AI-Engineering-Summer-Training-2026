# Rafid — Build Log

*Source document 3 of 7. Self-contained: assumes no knowledge of the other files.*

Rafid is a Discord bot that reviews and rewrites CVs, then matches them against live freelance work. It was built in five days. This document is the story of how, including every bug that mattered.

---

## Before Day 1 — burning down the unknowns

The integration risks were tested **before** the build clock started, so the build days would be assembly rather than discovery. Nine things were verified:

| Verified | Result |
|---|---|
| Claude Code CLI, headless `-p` mode | v2.1.226, subscription auth |
| Skills discovered and triggered headlessly | both, on a real PDF |
| Session continuity across separate processes | `--session-id` then `--resume` |
| The skills chain themselves | the reviewer offered the optimizer unprompted |
| A bridge from HTTP to Claude Code | `/health` fine, two-turn memory over HTTP |
| Markdown to PDF without pandoc | `reportlab` renders headings, tables, bullets |
| Discord DM in and out, with attachments | end to end |
| n8n 2.33.7 self-hosted natively | installed, database initialised |
| A demo fixture with a real before/after | messy 46, polished 85 |

That last finding — **the skills chain themselves** — changed the architecture. The reviewer ended its report by offering the optimizer without being asked. So the orchestrator does not need to manage the CV conversation; Claude Code already does. n8n dropped to being a thin pipe.

---

## Day 1 — planning, no code

The predecessor project (a deterministic CV-to-jobs pipeline) already worked. The temptation was to open the editor and bolt features on. The reason not to: **a pipeline is not an agent**, and getting from one to the other is a design change, not a feature.

Deliverables: a project plan, 32 functional and 10 non-functional requirements each with an **acceptance test**, an architecture document, and a 15-item risk register.

Three decisions worth recording:

**Acceptance tests are what make requirements real.** *"The bot replies to messages"* is a wish. *"Two polls over the same message produce one reply, not two"* is something that can fail.

**Multi-user was cut.** One instance per person, self-hosted. This is what made the rest fit in three days.

**Four-axis job scoring was cut.** The original vision ranked jobs on money, difficulty, skills gained and resume worth. Only **money** is real data; the other three are model judgements with no field behind them in any API. Shipping three invented axes would look impressive and mean nothing.

The day's most valuable hour was auditing the nine verified items against the architecture, which surfaced exactly one untested link: **could n8n's HTTP Request node actually reach the bridge?** Everything else was proven. That became Day 2's first task.

---

## Day 2 — the core loop

### The unknown, closed first

The test was designed to prove more than it needed to. Connectivity alone would leave the real dependency untested — the CV review asks questions across separate Discord messages, and every poll is a separate n8n execution. So it ran two turns: *"remember the number 7"*, then *"what number did I ask you to remember?"*

All four checks passed, including turn 2 recalling `7`. **Session memory survives separate n8n executions.** The fallback plan was never built.

### Then four bugs, each teaching something

**1. n8n will not touch the filesystem.** `Access to the file is not allowed` — n8n 2.x blocks its own file nodes from arbitrary paths. The alternative was an environment variable every user of the repo would also need. Instead, **the bridge took over all file I/O**. n8n now speaks only HTTP. Same reasoning that killed Execute Command, and it survives n8n moving into Docker.

**2. An HTTP node overwrites `$json`.** A "sending acknowledgement" node sat between two others, so Discord's response arrived where the workflow's own data should have been and a URL evaluated to a bare `/claude`. Fix: the acknowledgement became a **side branch**. General rule adopted for the rest of the build — *anything downstream of an HTTP node must reference the source node by name, never `$json`*.

**3. Claude Code is sandboxed to its working directory.** It replied, in chat, that it could not read the CV because the file was outside its scope. A clear error from the model rather than a stack trace. Fixed in two layers so it cannot regress.

**4. Overlapping executions.** The important one. One CV upload produced **five acknowledgements and five different intake questions**. Cause: the polling cursor lived in n8n's workflow static data, which is only written when an execution *finishes*. A review takes 1–3 minutes; the poll fires every 15 seconds; a dozen overlapping polls all read a stale cursor.

n8n cannot fix this — the state only becomes durable *after* the slow work. The cursor moved to the bridge, which writes it under a lock **before** anything slow starts. First caller wins, everyone else stops dead.

### And a fifth, found by reading state rather than output

After a successful run, the state file showed a path with a missing separator: `...workspacecv-1536830640287260835.pdf`. The review had **only worked by luck**, because Claude Code happened to be working in that directory and found the file by name.

> **A green run is not proof of correctness.** This bug passed its own test and was caught only by reading state nothing was asserting on.

**End of Day 2:** a CV sent in Discord came back as a summary plus a five-page PDF, scoring 46/100 — matching the documented fixture baseline.

---

## Day 3 — everything else

### The rewrite

The document contract was generalised from one fixed marker to any number of `===FILE:name===` blocks, tested offline against five cases — including two guards (empty body, unknown name) — before going anywhere near n8n.

### The invention problem

The first rewrite worked, and reading it against the source line by line revealed **three invented claims**:

| The CV said | What was actually said | The move |
|---|---|---|
| *"saving 2–10 hours **per week**"* | *"saved between 2-10 hrs"* | **added a rate** |
| *"a **client base of 100+**"* | *"**used by** 100+ clients"* — about a tool | **re-attributed a number** |
| *"**majority** repeat-and-referral"* | *"**many** happy clients"* | **strengthened a quantifier** |

None is a hallucination. The model invented nothing — it **resolved ambiguity in the candidate's favour**, three times. That is subtler and more dangerous, because *"2–10 hours per week"* is exactly the claim an interviewer probes.

**The instruction "never invent facts" was already in the prompt and prevented none of them**, because none of them felt like inventing a fact. The rule only worked once it named the specific moves: do not add a rate they did not say; do not re-attribute a number; do not strengthen a quantifier; and *if an answer is ambiguous, do not pick the more impressive reading*.

Re-tested with the same ambiguous input: all three gone.

### The intake was shallow, and it was the orchestrator's fault

The first working run asked three questions, one at a time. Reading the skill afterwards:

- **The skill said:** *"Ask all at once or in themed batches. Don't drip-feed one question at a time."*
- **The orchestration prompt said:** *"Ask your intake questions ONE at a time. Three questions maximum."*

The prompt was overriding the skill and making it worse. The same was true of page length — the skill already specified one page for a mid-level CV.

Rewritten, the intake asked **14 questions in a single numbered message**, then pushed back on three vague answers before proceeding. All three became precise on the final CV.

One genuine gap in the skill was also found and fixed: it asked *"for every number already on the CV, how confident are you?"* but nothing said *"where there is no number, go get one."* That is the rule that catches *"many happy clients"*.

### "This is ugly"

The optimised CV rendered as flat grey text. Two independent causes, and the obvious suspect was innocent:

- **The renderer was fine.** The same content with proper Markdown headings rendered correctly. **The model had emitted no Markdown at all.** Fixed by specifying the exact document skeleton in the prompt.
- **But the renderer was still wrong for a CV.** It had one look, built for reports. A resume style was added — bigger name, quiet section rules, tighter density.

A bug was fixed for both styles along the way: bullets were rendering as tiny raised specks that looked like artefacts.

**The lasting fix was neither.** The bridge now saves the source Markdown next to every PDF. What cost an hour of guessing is now a two-second check.

### Job matching, and three more bugs

The predecessor pipeline was ported as a 25-node sub-workflow with four carried-over fixes applied. Three new bugs surfaced:

**Truncated pitch output.** The validating guard refused a half-parsed response — working exactly as designed. The instinctive fix, raising the token ceiling, produced a **worse** failure: `Request too large... TPM limit 6000, Requested 9453`. **The free tier counts `prompt + max_tokens`, not actual output** — giving the model room made the request fail before it generated anything. The real fix was shortening the pitches. The durable fix was neither: the parser now **salvages complete objects from a truncated response**.

**Duplicate rows in the Jobs sheet**, spotted by eye in the spreadsheet — 135 rows, most appearing three times. Deduplication was happening against the *Matches* sheet (what had been sent) but nothing deduplicated the *Jobs* pool. Fixed with an upsert on `job_id`.

**The empty case would have been scored as a job.** Found while wiring the digest, not by a failing run. When every fetched project had already been sent, a marker row flowed onward and would have been scored as though it were a project. It only became reachable after the sheets were cleared — the bug had been sitting there undetected.

### The agent layer

Every non-CV message goes to a language model that returns `find_work` or `cv_chat`. Nothing greps for keywords.

**A planned design was rejected here.** The original plan called for an agent node holding the matching pipeline as a *tool*. An agent returns the model's **narration** of a tool result, not the structured data — and the Discord formatting needs rank, score, budget and URL intact. A classifier keeps the decision genuinely model-made and the data structured. Using the agent node would have traded working structure for a node name.

**End of Day 3:** feature-complete.

---

## Day 4 — measurement

Three days of building produced a system that worked every time it was run. That is not the same as knowing it works.

### The headline

Everything was pinned except the document — same skill, same target role, no intake questions:

| Document | Score |
|---|:-:|
| Original messy fixture | **42** |
| Original, second run | **42** |
| **Rafid's rewrite of it** | **73** |
| Hand-written "polished" version | **75** |

**+31 points, and within 2 of a professionally written CV of the same person.**

The two identical 42s also corrected a standing assumption: earlier score variation (46, 49, 40) was **not** model noise, it was different inputs between runs.

### Rates, not anecdotes

Across 11 matches from real executions:

| | Predecessor | Rafid |
|---|:-:|:-:|
| Pitches citing a real past project | 0/5 | **10/11 (91%)** |
| Pitches with banned filler | 3/5 | **0/11** |

And a finding that only appears with a sample size:

```
 90 : #        (1)
 85 : ##       (2)
 80 : ######   (6)   ← 55% of every match ever scored
 70 : ##       (2)
```

**Four distinct values, all multiples of five, more than half at exactly 80.** So "top 5, ranked" is partly an illusion — six of eleven were tied. The cause is a prompt-design flaw: the model is given four bands and anchors to band boundaries. **It is scoring categorically while being asked for a continuous number.**

### A defect found and deliberately not fixed

A `.docx` attachment produced *"I don't see a CV attached — could you send it as a PDF?"* The next action is right, the wording is wrong: a file *was* attached. The fix was written, then **reverted**, so the committed code matches what was actually tested. Logged as a limitation instead.

---

## The pattern across all five days

Nearly every serious bug had the same shape: **something worked, and the reason it worked was not the reason assumed.**

- The review worked because Claude Code found the file by luck, not because the path was right
- The pitches were generic because the profile schema omitted projects, not because the model was lazy
- The CV rendered flat because the model emitted no Markdown, not because the renderer was broken
- The intake was shallow because the orchestrator overrode the skill, not because the skill was weak
- The scores clustered at 80 because the prompt offered bands, not because the model was imprecise

In every case the fix only became obvious after finding out *why* it worked, rather than *that* it worked.
