# Rafid — Architecture

*Source document 2 of 7. Self-contained: assumes no knowledge of the other files.*

Rafid is a Discord bot that reviews and rewrites CVs, then matches them against live freelance projects. This document describes how it is built.

---

## The whole system

```
Discord DM  ──poll every 15s──►  n8n (self-hosted, native npm)
                                   │
                                   ├─ HTTP ──►  rafid_bridge.py  ──►  Claude Code CLI
                                   │            (127.0.0.1:8900)      + two Claude Skills
                                   │
                                   ├──────────►  Freelancer.com API
                                   ├──────────►  Gemini / DeepSeek / Groq
                                   └──────────►  Google Sheets (Jobs · Matches)
```

Everything runs on one PC. There is no server, no domain, no deployment.

---

## The two rules that shape everything

### 1. No inbound networking

Discord is **polled**, never pushed to. Every connection is outbound from the PC. That removes the public URL, the tunnel, the VPS, the TLS certificate and the entire class of problems that come with exposing a service.

The cost is latency: a message is noticed within 15 seconds rather than instantly. On a self-hosted instance the executions are unlimited and free, so 15 seconds costs nothing.

### 2. The bridge owns every side effect

`rafid_bridge.py` is the only component that touches the filesystem, holds durable state, or invokes a language model outside of n8n's own nodes. n8n polls, branches and formats. **n8n speaks nothing but HTTP.**

This was not the Day 1 design. It was forced by two discoveries during the build, and the architecture is better for it — see §5.

---

## Components and what each owns

| Component | Owns | Deliberately does not own |
|---|---|---|
| **Discord** | the interface — messages, attachments, delivery | any logic |
| **n8n** | polling, branching, formatting, scheduling, the job pipeline | the conversation |
| **LLM classifier** | deciding what each message *means* | doing the work |
| **`rafid_bridge.py`** | files, durable state, invoking Claude Code, rendering PDFs | any Rafid-specific logic |
| **Claude Code + skills** | the CV conversation: intake, review, rewrite | Discord, job matching, storage |
| **Google Sheets** | the job pool and the record of what was sent | logic |
| **Gemini / DeepSeek / Groq** | routing, profiling, scoring, pitch writing | conversation state |

---

## The three workflows

Split by **trigger**, not by feature — the only thing that genuinely cannot be shared.

| Workflow | Trigger | Nodes | Role |
|---|---|:-:|---|
| **Rafid - Poll Loop** | schedule, every 15s | 31 | the conversation |
| **Rafid - Job Matching** | called by the other two | 25 | fetch, score, rank, pitch |
| **Rafid - Daily Digest** | schedule, 08:00 daily | 9 | one gig, unprompted |

Matching is called by both the conversation and the digest, so it became a **sub-workflow** rather than being written twice. The digest differs from "find me work" only in shape: one job instead of five, and rows tagged `source: daily`.

---

## The bridge API

Python standard library only, plus `reportlab` for PDF rendering. Listening on `127.0.0.1:8900`.

| Method | Route | Purpose |
|---|---|---|
| `GET` | `/health` | is Claude Code reachable, and what version |
| `GET` | `/file?name=` | serve a generated PDF back to n8n |
| `GET` | `/state` | read durable state |
| `POST` | `/claude` | run Claude Code with a prompt, in a named session |
| `POST` | `/md2pdf` | render Markdown to PDF, in `report` or `resume` style |
| `POST` | `/fetch` | download a Discord attachment straight to the workspace |
| `POST` | `/claim` | atomically claim a message ID — the concurrency lock |
| `POST` | `/state` | merge a patch into durable state |
| `POST` | `/reset` | forget the session and greeting, keep the cursor |

### Three design decisions inside it

**The prompt is piped on stdin, never placed on a command line.** `subprocess.run(..., shell=False)` — so no shell ever parses it. This is the specific problem that made n8n's Execute Command node unusable, and the reason the bridge exists at all.

**The executable is located, not assumed.** `shutil.which("claude")` first, then known install paths. Child processes spawned by n8n do not reliably inherit the user's `PATH`.

**Session existence is detected, not tracked.** Claude Code writes each transcript to `~/.claude/projects/**/<session-id>.jsonl`. The bridge checks whether that file exists and chooses `--session-id` (create) or `--resume` (continue). It stores nothing itself, so restarting it loses nothing.

---

## Session continuity — the detail everything depends on

Every 15-second poll is a **brand-new n8n execution** with no memory of the previous one. But the CV review is inherently multi-turn: it asks questions and waits for answers.

```
Message 1  ──►  session_id = <uuid>  ──►  --session-id <uuid>  ──►  new session
Message 2  ──►  session_id = <uuid>  ──►  --resume <uuid>      ──►  full history
Message 3  ──►  session_id = <uuid>  ──►  --resume <uuid>      ──►  full history
```

n8n generates the UUID once and stores it via the bridge. Claude Code keeps the actual transcript on disk.

**n8n stores a pointer; Claude Code stores the conversation.**

Verified across genuinely separate processes before any of the rest was built: a two-turn conversation over HTTP kept its memory, including recalling a number given in the first turn.

---

## Concurrency — the hardest problem in the build

A CV review takes **1–3 minutes**. The poll fires every **15 seconds**. So while one review is in flight, roughly a dozen more polls start.

The first implementation kept the "last seen message" cursor in n8n's **workflow static data**, which is only written when an execution *finishes*. Every overlapping poll read a cursor that had not moved yet and concluded the same CV was new. One upload produced **five acknowledgements and five different intake questions.**

n8n cannot fix this itself: the state only becomes durable *after* the slow work. Any lock stored there is worthless, because the entire point of a lock is to exist *during* the work.

**The fix:** the cursor moved to the bridge, which writes it synchronously under a `threading.Lock` **before** anything slow starts.

```
POST /claim {message_id}
  → {"claimed": true}    exactly one caller ever wins
  → {"claimed": false}   every overlapping poll stops dead
```

**The general lesson:** any polling trigger whose work can outlast its interval has this bug. Both the digest and the matching pipeline are slower than 15 seconds.

**The trade-off it introduces:** the claim is written before the work, so a crash mid-flight means that message is never retried. Accepted for v1 — the user resends. A two-phase claim (`claimed` → `completed`, with stale claims released on a timeout) is designed but not built.

---

## Flow A — a CV arrives

```
every 15s
   │
   ▼
Poll Discord ── GET /channels/{id}/messages
   │
   ├─ no new messages ──► stop
   ▼
Claim the message via the bridge  ── loses? stop
   │
   ├─ first ever contact, no file? ──► canned welcome, no model call
   ▼
Has a PDF attached?
   ├─ yes ─► bridge downloads it ─► new Claude session ─► "reading it now"
   └─ no  ─► LLM classifier: job request, or conversation?
                    ├─ job request ──► Flow B
                    └─ conversation ─► resume the existing Claude session
   │
   ▼
Claude Code runs the skill
   │
   ▼
Output contains ===FILE:name=== markers?
   ├─ yes ─► render each to PDF ─► attach to Discord
   └─ no  ─► send as a normal chat message
```

### The document contract

Claude Code signals "I am finished, here are documents" with delimiters:

```
===SUMMARY===              the chat message
===FILE:rafid-review===    the full review
===FILE:rafid-cv===        the optimised CV
===FILE:rafid-changes===   what changed and why
```

Any number of `===FILE:name===` blocks fan out into one PDF each. The review sends one, the rewrite sends two, and the same four nodes handle both. **Adding a document type needs no new nodes.**

Two guards: a marker with a body under 40 characters is treated as chat rather than shipping an empty PDF, and an unknown document name falls back to a default style instead of failing.

---

## Flow B — job matching

```
Load the CV from the bridge — the OPTIMISED one if a rewrite exists
   ▼
Extract its text ─► profile it (Gemini) ─► validate the JSON
   ▼
Fetch 50 live projects from Freelancer.com
   ▼
Filter: language == English
   ▼
Drop anything already in the Matches sheet      ← this is what stops repeats
   ▼
   ├─ nothing left ──► return an explicit empty result
   ▼
Save to the Jobs sheet (upsert on job_id)
   ▼
Score every project 0-100 (DeepSeek, temperature 0)
   ▼
Validate ─► rank ─► take top K
   ▼
Write a pitch per job (Groq) — must cite a real past project
   ▼
Validate, salvaging partial output if truncated
   ▼
Save to Matches ─► return to the caller
```

It matches the **optimised** CV, falling back to the original only if no rewrite exists. That is the entire reason review and rewrite sit in front of matching.

---

## Flow C — the daily digest

```
08:00 ─► read state ─► is there a CV?
                        ├─ no  ──► stay silent, never nag
                        └─ yes ──► matching with top_k=1, mode='daily'
                                     ├─ a job ──► send it
                                     └─ none  ──► "Nothing new today"
```

Two deliberate behaviours. **No CV means silence** — a bot that nags every morning about a CV you never sent is worse than no bot. **Nothing new is still said out loud** — a digest that goes quiet is indistinguishable from a digest that has crashed.

---

## Data model

### Durable state — `workspace/state.json`, owned by the bridge

| Key | Purpose |
|---|---|
| `last_seen_message_id` | the polling cursor, and the concurrency lock |
| `greeted` | has the welcome been sent |
| `session_id` | the Claude Code conversation UUID |
| `cv_name`, `cv_path` | the uploaded CV |
| `cv_optimised_name` | the rewritten CV, used for matching |

Written synchronously under a lock, via atomic file replacement. Survives restarts of both n8n and the bridge — this is the mechanism behind "remembers your CV between sessions".

### Google Sheets — two tabs

**`Jobs`** — the pool. `job_id · title · description · budget_min · budget_max · currency · skills · url · language · fetched_at`. Written with **upsert on `job_id`**, so re-running does not duplicate rows.

**`Matches`** — what has been sent. `job_id · title · url · score · reason · pitch · source · sent_at`. Written with plain **append**, deliberately: a duplicate here would mean a real bug worth seeing rather than silently absorbing.

> Day 1 specified a third `CVs` sheet. It was dropped: the bridge's state file already persists the CV durably, and a second copy in Sheets would only ever be the stale one.

---

## PDF rendering

`md2pdf.py` converts Markdown to PDF using `reportlab` alone. Two style profiles:

| | `report` | `resume` |
|---|---|---|
| Used for | review, change report | the optimised CV |
| Name/heading | 16pt navy | **19pt, owns the top of the page** |
| Sections | navy headings | bold with a hairline rule |
| Body | 9.5pt / 13 leading | 9pt / 11.6 — density matters at one page |

The bridge also writes the **source Markdown next to every PDF**. When output looks wrong, that turns an hour of guessing into a two-second check — added after exactly that hour was lost.

---

## Why self-hosting is required, not preferred

n8n Cloud cannot reach a process on your laptop. The Claude Code integration — which is what makes the CV review possible at zero cost — could not exist there.

The bill for that choice: n8n Cloud ships its own registered Google OAuth application, so connecting Google Sheets is one click. Self-hosted n8n has no such app, and Google requires whoever runs the instance to register their own. That turned a one-click step into a service-account setup.

---

## Failure behaviour

| If this breaks | What happens | Why it is survivable |
|---|---|---|
| Claude Code hits a usage limit | CV review stops | job matching runs on other providers and is unaffected |
| The bridge crashes | everything stops | it holds nothing in memory — restart and sessions resume from disk |
| n8n restarts | the current turn is lost | state lives in the bridge, not in n8n |
| An LLM returns truncated JSON | the guard catches it | complete items are salvaged; the rest is flagged, not silently dropped |
| Freelancer returns nothing | explicit empty result | "nothing new today" rather than silence |
| n8n moves to Docker-only | nothing | the bridge is reached over HTTP; only the hostname changes |
