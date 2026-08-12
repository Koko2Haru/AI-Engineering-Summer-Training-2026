# 📘 Day 3 Report — Build Integration

**🎯 Focus:** Everything else in v1 — the rewrite, job matching, the agent layer, and the daily digest

**📝 Assigned task:** *Integrate the pieces into the complete application.*

**📅 Date:** 2026-08-12

**✅ Status:** Completed — all five planned items landed, and v1 is feature-complete

---

## 🗂️ Folder structure

```
📁 Day-3-Build-Integration/
├── 📄 DAY3-REPORT.md                    ← this report
└── 📁 Integration/
    ├── 📄 sanad-poll-loop.json          the conversation — 31 nodes
    ├── 📄 sanad-job-matching.json       the matching pipeline — 25 nodes
    └── 📄 sanad-daily-digest.json       08:00, unprompted — 9 nodes
```

Three workflows, split by **trigger** rather than by feature: the conversation is reactive, the digest is scheduled, and matching is called by both — so it became a sub-workflow instead of being written twice.

---

## 🎯 Objective

Day 2 proved one round trip: a CV in, a review PDF back. Day 3 had to turn that into the whole product — the rewrite, live job matching, an agent deciding what each message means, and a gig arriving every morning without being asked.

All five items landed. Along the way the day produced something more useful than a feature list: **three separate bugs that only appear when a system meets reality**, and a quality problem in the skill's own behaviour that only showed up once a human looked at the output properly.

---

## ✍️ 1. The rewrite — one parser, any number of documents

`cv-reviewer` returns one document. `cv-optimizer` returns two — the optimised CV and a change report. The Day 2 parser looked for a single fixed `===REPORT===` marker, so it could not carry both.

Rather than special-casing the optimizer, the contract was generalised:

```
===SUMMARY===              the chat message
===FILE:sanad-review===    the full review
===FILE:sanad-cv===        the optimised CV
===FILE:sanad-changes===   what changed and why
```

Any number of `===FILE:name===` blocks now fan out into one PDF each. The review sends one, the optimizer sends two, and the same four nodes handle both. **Adding a document type later needs no new nodes.**

Tested offline against five cases *before* it went near n8n:

| Case | Result |
|---|---|
| Optimizer — two documents | ✅ both parsed, correct titles and captions |
| Reviewer — one document | ✅ |
| Plain chat, no markers | ✅ treated as chat, no PDF produced |
| Marker present, body too short | ✅ **guard held** — chat, not an empty PDF |
| Unknown document name | ✅ falls back instead of throwing |

The last two matter most: without them a malformed response either ships a blank PDF or kills the execution.

---

## 🔍 2. The invention problem — found, diagnosed, fixed at the source

The first rewrite worked. Read against the source CV line by line, it had **invented three things**:

| Optimised CV said | What was actually said | The move |
|---|---|---|
| *"saving 2–10 hours **per week**"* | *"saved between 2-10 hrs"* | **added a rate** |
| *"a **client base of 100+**"* | *"**used by** 100+ clients"* — about a tool | **re-attributed a number** |
| *"**majority** repeat-and-referral"* | *"**many** happy clients"* | **strengthened a quantifier** |

None is a hallucination. The model didn't make anything up — it **resolved ambiguity in the candidate's favour**, three times. That is subtler and far more dangerous: *"2–10 hours per week"* is the kind of claim an interviewer probes and the candidate cannot defend.

**The instruction "never invent facts" was already in the prompt and prevented none of them**, because none of them felt like inventing a fact. A rule only works if it names the actual move:

> - Adding a rate they did not say. If they said *"saved 2-10 hours"*, you may NOT write *"2-10 hours per week"*.
> - Re-attributing a number. *"a tool used by 100+ clients"* is a fact about the **tool**.
> - Strengthening a vague quantifier. *"many clients come back"* must not become *"a majority"*.
> - If an answer is ambiguous, **do not pick the more impressive reading.**

**Re-tested with the same ambiguous phrasing.** All three violations gone: *"5-10 hours/week"* because the intake asked for the unit, *"~25 clients"* and *"2,000-5,000 products"* kept as separate facts about separate things.

Two smaller drifts remain and are logged rather than chased: *"around 35"* → *"35+"*, *"approximately 12"* → *"12"*. One dropped hedge each. Tightening further starts producing stilted output.

---

## 🗣️ 3. The intake was shallow, and it was my fault

The first working run asked **three questions**, one at a time, and took four Claude Code invocations to get to a review. Reading the skill afterwards:

| | |
|---|---|
| **The skill's `intake-questions.md`** | *"Ask all at once or in themed batches. **Don't drip-feed one question at a time when several are needed.**"* |
| **The Sanad prompt** | *"Ask your intake questions **ONE at a time**… **Three questions maximum.**"* |

**The orchestration prompt overrode the skill and made it worse.** The same was true of length: `resume-writing-best-practices.md` already said *"Mid-level (3-8 yrs): 1 page"* — the rule was right and simply wasn't carried through.

Rewritten so the prompt serves the skill instead of fighting it:

- **One numbered message**, 8–15 questions, one per unquantified claim in the CV
- **Every question names the unit it wants** — not *"how much time did it save?"* but *"how many hours, and over what period — per week, per month, or one-off?"*
- **Ambiguous answers get one clarifying round**, then a placeholder. Never an estimate
- **The optimised CV is capped** so it fits one page

The result asked **14 questions in one message**, then pushed back on three answers:

> *"the 20% sales increase: compared to what baseline, and measured over what window?"*
> *"'several thousand products' — do you have an actual number or range?"*
> *"the '1,000+ bookings' — over what period? Total since launch, or per year?"*

All three are precise on the final CV. Without that round they would have been vague — or invented.

**One genuine gap in the skill** was found and fixed in both the repo copy and the installed one: its questions covered *"for every number already on the CV, how confident are you?"* but nothing said *"where there is no number, go get one."* That is the rule that catches *"many happy clients"*. Added as Q16–18, along with a note that Q16 should **expand** the question list to fit the document rather than capping it.

---

## 🎨 4. "This is ugly" — two problems wearing one coat

The optimised CV rendered as flat grey text with no hierarchy. Two independent causes, and the obvious suspect was innocent:

**The renderer was fine.** Pushing the same content through `md2pdf.py` *with* `#` and `##` headings produced correct hierarchy immediately. **The model had emitted no Markdown at all** — just plain lines. Fixed by specifying the exact skeleton in the prompt: `#` for the name, `##` per section, `###` per role, `-` for bullets, plus an explicit warning that plain lines render broken.

**But the renderer was still wrong for a CV.** `md2pdf.py` had one look — navy headings, roomy spacing — built for reports. A resume needs the opposite. Added a second style profile:

| | report | resume |
|---|---|---|
| Name | 16pt navy | **19pt, owns the top of the page** |
| Sections | navy headings | bold + hairline rule |
| Body | 9.5pt / 13 leading | 9pt / 11.6 — density matters at one page |
| Contact line | — | small, grey, under the name |

**A bug fixed for both:** `ListFlowable` was rendering bullets as tiny raised specks that looked like artefacts. Replaced with paragraph-level `<bullet>` and a proper hanging indent.

**The lasting fix was neither of those.** The bridge now writes the source `.md` next to every PDF. What cost an hour of guessing is now a two-second check — the next time output looks wrong, the answer is on disk.

---

## 🔗 5. Job matching — the Week 6 port

25 nodes, called as a sub-workflow by both the conversation and the digest.

```
get CV from bridge → extract text → profile it (Gemini)
  → fetch 50 live projects → drop non-English → drop already-sent
  → save to Jobs → score all (DeepSeek) → rank top K
  → write pitches (Groq) → save to Matches → return
```

It matches the **optimised** CV, falling back to the original only if no rewrite exists — which is the entire reason review and rewrite sit in front of matching.

### The four carry-over fixes, verified in one run

| Fix | Week 6 problem | Result |
|:-:|---|---|
| **#1** | pitches generic; three of five reused *"deliver a high-quality solution that meets your requirements"*, none cited past work | `notable_projects` added to the profile schema; each pitch must cite one by name; filler banned. **5/5 cited a real project** |
| **#5** | ~7 of 50 projects came back in other languages | `language !== 'en'` filtered |
| **#6** | two of five matches changed between identical runs | scoring temperature pinned to **0** |
| **#8** | HTTP 200 carrying JSON truncated at 4096 tokens | `maxTokens` capped and every LLM output validated |

Fix #1 was the one worth proving. Week 6's pitches said nothing; these say:

> *"I've successfully implemented e-commerce solutions like **Homeware E-Commerce Shop**, which saw a 20% increase in sales…"*
> *"as seen in the **Supplier Price-Tracking Tool** project, which automated price tracking across 10 supplier websites…"*

The diagnosis was right: it was never the model, it was the schema. The profile extracted skills only, so the pitch step could not cite what it could not see.

The scoring is honest too, which matters as much:

> *"Weak overlap, freelancer knows Python but lacks robotics/electronics expertise"*

---

## 🐛 6. Three bugs that only appear in contact with reality

### 6.1 Truncated pitches — the guard doing its job

The pitch step returned JSON cut off mid-sentence and the validating node refused it. That is carry-over #8 working exactly as designed — Week 6 had the same failure slip through as a valid-looking HTTP 200.

**The instinctive fix was wrong.** Raising `maxTokensToSample` from 4096 to 8192 produced:

```
Request too large ... TPM limit 6000, Requested 9453
```

**Groq's free tier counts `prompt + max_tokens`, not actual output.** Giving the model room made the request fail *before* it generated anything. The real fix was shortening the pitches, not raising the ceiling — 2000 tokens, request ~3260 against a 6000 limit.

The durable fix was neither: `Parse Pitches` now **salvages complete objects from a truncated response** instead of losing all five because the last was clipped. Proven against the exact failure — two pitches survive, the clipped one is flagged `pitch_missing`, and `response_was_truncated` is recorded in the output.

> Third distinct free-tier gotcha in this project, after DeepSeek's non-existent free tokens and OpenRouter's 65536 default. The lesson has sharpened: it is not enough to know the limit — you have to know **what the provider is counting.**

### 6.2 Duplicate rows in the Jobs sheet

Spotted by eye in the spreadsheet: 135 rows, most appearing three times.

`Drop Already Sent` filters against **Matches** — what has been *sent* — which is what protects FR-31, and it worked. But `Save Jobs` blindly appended whatever the fetch returned, and the API returns the same active projects every run.

Fixed with `appendOrUpdate` keyed on `job_id`: an existing project has its row updated, only genuinely new ones add rows. **`Save Matches` deliberately stays a plain append** — it is a log of what was sent, and a duplicate there would be a real FR-31 failure worth seeing rather than silently absorbing.

> The run-to-run overlap is near total, which makes `Drop Already Sent` load-bearing for the digest rather than incidental. Without it, day two sends day one's job again.

### 6.3 The empty case would have been scored as a job

Found while wiring the digest, not by a failing run. When every fetched project had already been sent, `Drop Already Sent` emitted a marker row that would have flowed on and been **scored as though it were a project**.

Now routed to a clean empty result. It only became reachable because the `Matches` sheet was cleared — the bug had been sitting there the whole time, unreachable and undetected.

---

## 🤖 7. The agent layer

FR-5: *"an agent decides what each message means and routes accordingly, **with no keyword matching in the routing**."*

Every non-CV message goes to an LLM classifier which returns `find_work` or `cv_chat`, and n8n branches on the result. Nothing in the routing greps for "find" or "work" — Gemini reads the message and decides.

**A design decision worth defending.** Day 2's plan said "AI Agent node". An Agent node holding the matching workflow as a *tool* returns the model's **narration** of the result, not the structured data — and Discord formatting needs `rank`, `score`, `budget` and `url` intact. Routing with a classifier keeps the decision genuinely model-made and the data structured. Using the Agent node here would have traded working structure for a node name, which is the same "routing with one exit is theatre" argument that deferred it from Day 2.

**One safety behaviour:** an unparseable router response defaults to **chat**, never to job search. The chat path can ask a follow-up; the search cannot.

---

## ☀️ 8. The daily digest

The feature that makes Sanad an automation rather than a chatbot.

```
08:00 → get state → has a CV?
                     ├── no  → stay silent, never nag
                     └── yes → top_k=1, mode='daily' → Job Matching
                                → one job, or "nothing new today" → Discord
```

It **inherits** rather than reimplements: same sub-workflow, so FR-31, the English filter, the pinned temperature and the truncation salvage all come for free. Only the shape differs — one job instead of five, and rows tagged `source: daily` so the write-up can distinguish what was requested from what arrived unprompted.

Two deliberate behaviours:

- **No CV → silence.** A bot that nags every morning about a CV you never sent is worse than no bot.
- **Nothing new → it says so** (FR-32). A digest that goes quiet is indistinguishable from a digest that has crashed.

---

## ✅ 9. Requirements cleared today

| ID | Requirement | Evidence |
|---|---|---|
| **FR-5** | an agent routes each message, no keyword matching | `find me work` reached matching; everything else reached Claude Code |
| **FR-12** | offers to fix, runs optimizer on acceptance | `yes` → rewrite ran |
| **FR-13** | optimised CV + change report, both PDF | 1-page CV + 3-page change report |
| **FR-14** | invents no facts | 3 violations found, fixed at the source, re-verified |
| **FR-18** | offers to find work | ✅ |
| **FR-19** | live projects fetched | 50 per run from Freelancer |
| **FR-20** | scored and ranked | ✅ |
| **FR-21** | top 5 with pitches | ✅ |
| **FR-22** | pitches cite a real project, no filler | **5/5 cited**, 0 banned phrases |
| **FR-23** | non-English filtered | ✅ |
| **FR-29** | CV persists between sessions | `find me work` matched against the stored CV with **no re-upload** |
| **FR-30** | one unseen gig, unprompted | digest ran and delivered |
| **FR-32** | says so when there's nothing | empty branch built and reachable |

---

## ⚠️ 10. Known limitations

Found today, logged rather than patched — Day 4 is where these get measured.

- **Score compression.** Four of five matches scored **exactly 80/100**. Ranking among them is close to arbitrary, which undercuts the whole idea of a ranked list.
- **Currencies are not normalised.** 8–15 CAD, 250–750 USD, 750–1500 AUD, 12500–37500 INR in one result set. Week 6 normalised to USD; the port dropped it. This also undercuts *money* as the one genuinely objective axis.
- **Pitch invention.** One of five pitches opened *"Having replicated an existing business website…"* — a claim absent from the CV, and it cited no named project. The same failure mode as §2, in a different component. The flag caught it; the prompt did not prevent it.
- **The scorer is generous.** A *job-description writing* task scored 80/100 against a web developer's CV.
- **Two small hedge drops** in the rewrite: *"around 35"* → *"35+"*, *"approximately 12"* → *"12"*.
- **The `CVs` sheet was dropped.** Day 1 specified three sheets; the bridge's `state.json` already persists the CV durably, and a second copy in Sheets would only be the stale one. Two sheets, deliberately.
- **Google Sheets needed a credential Week 6 never had to create.** n8n Cloud ships its own registered OAuth app; self-hosted does not. Self-hosting is what makes the Claude Code integration possible — this is the bill for it.

---

## 📦 11. Deliverables

1. **`Integration/sanad-poll-loop.json`** — the conversation, now 31 nodes with the agent layer
2. **`Integration/sanad-job-matching.json`** — 25 nodes, the Week 6 port with four carry-over fixes
3. **`Integration/sanad-daily-digest.json`** — 9 nodes, 08:00, unprompted
4. **`md2pdf.py`** — a second style profile, plus the bullet-rendering fix
5. **`sanad_bridge.py`** — `/reset`, permission-mode handling, and markdown sidecars
6. **`cv-reviewer/references/intake-questions.md`** — Q16–18 added, synced to the installed copy

---

## 🚀 12. What Day 4 opens with

**v1 is feature-complete.** Day 4 is measurement, not building.

1. **FR-15** — does the optimised CV actually score higher? Re-review the rewrite; report both numbers honestly. Never been measured
2. Both fixtures end to end — messy (46) and polished (85)
3. Failure paths — no attachment, wrong file type, bridge down, empty results, malformed JSON
4. Determinism — same CV matched twice, differences recorded rather than hidden
5. The §10 limitations, measured properly: how compressed are the scores, how often does a pitch invent
6. **Record the demo** (R-3) — non-negotiable, the night before Day 5
