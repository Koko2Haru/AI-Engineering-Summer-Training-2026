# Week 6 — Automation & Orchestration with n8n ⚙️🤖

> **Instructor:** Abdullah Barghash
> **Theme:** one automation, built a layer at a time — a scheduled workflow that
> collects data, a second and third API feeding each other, three chained LLM steps
> that turn a CV into ranked freelance work, error handling and a human approval
> checkpoint in front of the irreversible step, and finally a public form that lets
> the whole thing run without me.

**AI Engineering Summer Training 2026**
Student: **Ali** ([koko2haru](https://github.com/Koko2Haru))

---

## 🎯 The Week's Project: FreelanceScout

**FreelanceScout** takes a CV and returns the freelance projects that actually match
the skills in it — summarised, scored, ranked, and delivered with a tailored pitch
for each one.

The problem is real and personal: freelance job boards are enormous, mostly
irrelevant to any given person, and searching them by keyword surfaces the wrong
things. A CV already contains everything needed to filter that noise — it just isn't
in a form a job board can use.

Every day added one layer to the *same* workflow rather than starting a new exercise:
scheduled collection → multiple APIs exchanging data → chained LLM reasoning →
resilience and human oversight → a front door anyone can use. By Friday it was a
single automation someone could hand a CV to.

This is also deliberately the **seed of the Week 7 capstone**, which extends it with
CV review and optimisation, and swaps the form and email for a WhatsApp bot. That's
why every stage was kept separable from Day 1 — the capstone should be node changes,
not a rebuild.

---

## 🗓️ Day by Day

| Day | Focus | Deliverables | Report |
|---|---|---|---|
| 1 | Automation foundations & intro to n8n | [`scheduled-job-fetch.json`](Day-1-Automation-Foundations-and-Intro-to-n8n/Introduction-to-n8n/scheduled-job-fetch.json) — scheduled 5-node workflow, live jobs → Google Sheets | [Day 1](Day-1-Automation-Foundations-and-Intro-to-n8n/DAY1-REPORT.md) |
| 2 | Connecting tools & APIs | [`multi-api-job-pipeline.json`](Day-2-Connecting-Tools-and-APIs-in-n8n/Multiple-Connections/multi-api-job-pipeline.json) — 3 APIs + 2 tools, currency conversion, deduplication | [Day 2](Day-2-Connecting-Tools-and-APIs-in-n8n/DAY2-REPORT.md) |
| 3 | AI workflows & chaining agents | [`cv-matching-chain.json`](Day-3-AI-Workflows-and-Chaining-Agents/Multiple-LLMs/cv-matching-chain.json) — 3 chained LLM steps across 3 different models | [Day 3](Day-3-AI-Workflows-and-Chaining-Agents/DAY3-REPORT.md) |
| 4 | Error handling & human-in-the-loop | [`resilient-cv-matching-hitl.json`](Day-4-Error-Handling-and-Human-in-The-Loop/Error-Handling/resilient-cv-matching-hitl.json) + [`error-handler.json`](Day-4-Error-Handling-and-Human-in-The-Loop/Error-Handling/error-handler.json) — 3 protection layers, approval gate, 4 tests | [Day 4](Day-4-Error-Handling-and-Human-in-The-Loop/DAY4-REPORT.md) |
| 5 | Build an automation | [`freelancescout-end-to-end.json`](Day-5-Build-an-Automation/Automatication/freelancescout-end-to-end.json) — 23 nodes, public upload form to notification | [Day 5](Day-5-Build-an-Automation/DAY5-REPORT.md) |

---

## 📅 Day 1 — Automation Foundations & Intro to n8n

**Focus:** nodes, triggers, scheduling — and how data actually moves between steps.
**Task:** build an n8n workflow that runs automatically on a schedule and performs at
least two connected actions.

Five nodes, four connected actions: a schedule trigger, an HTTP request to a live job
API, a Split Out, field normalisation, and an append to Google Sheets. Proven
*scheduled* rather than merely working — published and left alone until it fired three
times unattended, sixty seconds apart.

Two things went wrong and both were worth more than the build. The first source,
**Remotive**, turned out to be a *remote* job board rather than a freelance one — only
**5 of 31** results qualified, which broke the premise of the project. Swapped to the
**Freelancer.com** API where 50 of 50 qualify. The second: bid counts silently rendered
in Sheets as dates from 1899, caused by stale column formatting combined with
`USER_ENTERED` mode. n8n sent correct integers the whole time; the destination
corrupted them on arrival and nothing errored.

📄 **[`jobs-output.csv`](Day-1-Automation-Foundations-and-Intro-to-n8n/Introduction-to-n8n/jobs-output.csv)** —
the real output, duplicates and all, kept as evidence for Day 2's problem.

---

## 📅 Day 2 — Connecting Tools & APIs

**Focus:** the difference between calling APIs and making them *exchange* data.
**Task:** connect two external APIs inside n8n and exchange data between them
successfully.

Three APIs and two tools, not two: **Freelancer.com** and **Arbeitnow** as sources, an
**exchange-rate API** as enrichment, then **Google Sheets** and **Gmail** as tools.

The rubric's phrase *"exchange data between them"* set the design. Three parallel
fetches stapled together would satisfy it on a technicality; instead the job APIs'
output feeds the rate API's data to produce something neither could alone — budgets
arriving in INR, GBP, EUR and USD all converted to one comparable scale. A
₹150,000–250,000 project becomes **$1,573–$2,622**, which is what makes ranking
possible at all on Day 3.

The second source was chosen by testing four candidates against live responses, not by
reading descriptions: RemoteOK returned **0** contract or freelance roles out of 100,
Jobicy **50 of 50** full-time. Arbeitnow made it in with caveats that are stated
honestly in the report.

Also the day's best bug: Arbeitnow returns `job_types` as an **array for 132 records
and an object for 43** — same endpoint, same field, two incompatible types, crashing
only once execution reached item 112.

📄 **[`merged-jobs-output.csv`](Day-2-Connecting-Tools-and-APIs-in-n8n/Multiple-Connections/merged-jobs-output.csv)** —
64 merged, converted and deduplicated rows.

---

## 📅 Day 3 — AI Workflows & Chaining Agents

**Focus:** chained LLM steps where each one genuinely depends on the last.
**Task:** create an AI workflow where multiple LLM steps process data sequentially
before producing a final output.

The day FreelanceScout stopped being a scraper. Three LLM steps across **three
different providers**, each chosen for what its step needs:

| Step | Model | Why |
|---|---|---|
| CV → skill profile | **Gemini 2.0 Flash** | everything downstream depends on clean, schema-correct JSON |
| Score 64 jobs | **DeepSeek** (via OpenRouter) | the heaviest reasoning step |
| Write pitches | **Llama 3.3 70B** (Groq) | pure generation; fastest inference available |

**Result: 5 correct matches out of 5, from 64 candidates.** That was measurable rather
than eyeballed because the test fixture was built to make it so — a fully synthetic CV
for an invented WordPress/Shopify developer, so which gigs *should* rank high and
which *should* score near zero were both predicted in advance.

Privacy drove two decisions: the CV is fictional (a real one can't be committed to a
public repo, and shouldn't be sent to three third-party APIs), and a **PII-stripping
node** removes emails, phones and URLs before any model sees the text — redundant now,
necessary in Week 7.

A deliberate choice worth naming: **the AI Agent node was not used.** An Agent exists to
run a tool-calling loop; none of these three steps have tools to call. Basic LLM Chain
nodes are the correct tool and the report argues why.

**Where it fell short, stated plainly:** the pitches are accurate but generic — three of
five reused the same filler phrase and none cited the candidate's actual projects.
Traced to a design flaw of mine (the profile schema extracts skills but not projects)
and logged for Week 7 rather than patched.

📄 **[`synthetic-cv.pdf`](Day-3-AI-Workflows-and-Chaining-Agents/Multiple-LLMs/synthetic-cv.pdf)** ·
**[`top-5-matches.csv`](Day-3-AI-Workflows-and-Chaining-Agents/Multiple-LLMs/top-5-matches.csv)**

---

## 📅 Day 4 — Error Handling & Human-in-the-Loop

**Focus:** surviving failure, and putting a human in front of the irreversible step.
**Task:** add error handling and a human approval step to an existing workflow, then
test both success and failure scenarios.

Three layers, because one isn't enough:

| Layer | Catches |
|---|---|
| **Retries** (3×) on every network call | transient failures — rate limits, timeouts |
| **Error branches** on 5 nodes | failures at steps I *expected* could fail |
| **A separate Error Trigger workflow** | everything I **didn't** anticipate |

Plus a Gmail **send-and-wait approval gate**: nothing reaches the Matches sheet without
a click. An approval step that writes either way is a notification, not a gate.

All four tests passed — approve, decline, a handled API failure, an unhandled crash.

**The day's most useful finding came before any of them.** The first real run failed
with invalid JSON, and the token usage showed why: `completionTokens: 4096` against a
4096 cap. The scoring output had been truncated mid-array. The API call **succeeded** —
HTTP 200, well-formed response, no node went red. Only a validating Code node caught
it. That's the entire argument for the day's work in one incident.

**And one test almost passed dishonestly.** The error-handler test "worked" — an email
arrived — until reading it revealed n8n's placeholder data (*"Example Workflow"*,
*"Node With Error"*). n8n only triggers error workflows for **production** executions,
never manual ones. Proving it properly meant swapping in a schedule trigger, publishing,
and waiting for a genuine failure. Accepting the first email would have put a false
claim in this repo.

📄 **[`Rejected-sheet.csv`](Day-4-Error-Handling-and-Human-in-The-Loop/Error-Handling/Rejected-sheet.csv)** —
proof the decline branch wrote a rejection and left Matches untouched.

---

## 📅 Day 5 — Build an Automation

**Focus:** removing myself from the loop entirely.
**Task:** build an end-to-end automation that receives a document, summarises it using
AI, stores the result, and sends a notification.

Every clause maps to a node:

| Requirement | Node |
|---|---|
| receives a document | `CV Upload Form` — n8n Form Trigger, public page, PDF upload |
| summarises it using AI | `Summarize and Profile CV` — Gemini |
| stores the result | `Save Matches` — Google Sheets |
| sends a notification | `Send Results` — Gmail |

23 nodes, three LLM providers, two Google services, with Day 4's error handling and
approval gate carried through. Someone uploads a CV on a web page and everything else
happens on its own.

Two design decisions mattered more than they look. **The email address comes from the
form**, not the workflow — which makes it a product rather than a thing wired to one
inbox, and means the workflow file contains no personal data at all. And **the user
chooses how many matches**, clamped 1–10 in code, because trusting a form field to be
sane is how you end up asking an LLM for 900 results.

Final run: **5 matches from 64 live projects, scoring 92 down to 85**, all in the test
CV's actual field.

📄 **[`full-output.csv`](Day-5-Build-an-Automation/Automatication/full-output.csv)** —
the end-to-end result.

---

## 🧵 The Through-Line

- **Day 1's** duplication problem → became **Day 2's** dedupe requirement, and the
  observation that duplicates *weren't identical* (bid counts drifted 150→159 between
  runs) is what proved deduping had to key on `url` rather than compare rows.
- **Day 1's** wrong data source → set the rule for **Day 2's** source selection: test
  four candidates against live responses instead of trusting their descriptions.
- **Day 2's** currency conversion → made **Day 3's** ranking possible, because budgets
  in four currencies can't be compared.
- **Day 3's** `skills` column, collected on Days 1–2 → the field the CV matching
  actually runs against.
- **Day 4's** approval gate → the direct answer to **Week 5's** closing finding, where
  an agent confidently reported work it hadn't done. A human gate doesn't rely on the
  model's self-report.
- **Day 5's** form → the seat WhatsApp takes in the Week 7 capstone.

**Recurring lesson across all five days:** *a green execution means the workflow ran,
not that the data is right.* Bid counts became 1899 dates. A header typo silently
restructured a sheet. A truncated LLM response returned HTTP 200. An error-handler test
passed on placeholder data. Every one of those "succeeded" — and every one was only
caught by reading the actual output.

A second pattern worth naming: **three separate times this week, something appeared
configured but wasn't** — imported dropdowns holding labels with no underlying IDs, an
error workflow that couldn't be selected until published, a form field the PDF
extractor wasn't pointed at. Three times in five days is a pattern, not bad luck.

---

## 🧰 Stack

| Layer | Used |
|---|---|
| Orchestration | n8n (Cloud) |
| LLMs | Google Gemini 2.0 Flash · DeepSeek via OpenRouter · Llama 3.3 70B via Groq |
| Job data | Freelancer.com API · Arbeitnow API |
| Enrichment | open.er-api.com (live exchange rates) |
| Storage | Google Sheets |
| Delivery | Gmail (notification + send-and-wait approval) |
| Input | Google Drive (Days 3–4) → n8n Form Trigger (Day 5) |

Every LLM used is on a genuinely free tier — no credit card on any of the three.

---

## 📂 Structure

```
Week-6-Automation-and-Orchestration-with-n8n/
├── WEEK6-README.md
├── Day-1-Automation-Foundations-and-Intro-to-n8n/
│   ├── DAY1-REPORT.md
│   └── Introduction-to-n8n/
│       ├── scheduled-job-fetch.json
│       ├── jobs-output.csv
│       └── screenshots/
├── Day-2-Connecting-Tools-and-APIs-in-n8n/
│   ├── DAY2-REPORT.md
│   └── Multiple-Connections/
│       ├── multi-api-job-pipeline.json
│       ├── merged-jobs-output.csv
│       └── screenshots/
├── Day-3-AI-Workflows-and-Chaining-Agents/
│   ├── DAY3-REPORT.md
│   └── Multiple-LLMs/
│       ├── cv-matching-chain.json
│       ├── synthetic-cv.pdf
│       ├── top-5-matches.csv
│       └── screenshots/
├── Day-4-Error-Handling-and-Human-in-The-Loop/
│   ├── DAY4-REPORT.md
│   └── Error-Handling/
│       ├── resilient-cv-matching-hitl.json
│       ├── error-handler.json
│       ├── Rejected-sheet.csv
│       └── screenshots/
└── Day-5-Build-an-Automation/
    ├── DAY5-REPORT.md
    └── Automatication/
        ├── freelancescout-end-to-end.json
        ├── full-output.csv
        └── screenshots/
```

---

*Part of [AI-Engineering-Summer-Training-2026](https://github.com/koko2haru/AI-Engineering-Summer-Training-2026).*
