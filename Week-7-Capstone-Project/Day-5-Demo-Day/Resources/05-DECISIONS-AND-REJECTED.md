# Rafid — Decisions and Rejected Alternatives

*Source document 6 of 7. Self-contained: assumes no knowledge of the other files.*

Rafid is a Discord bot that reviews and rewrites CVs, then matches them against live freelance work. This document records what was chosen, what was rejected, and why. Recording the rejections is as much a part of the design as the choices.

---

## Locked decisions

| Area | Decision | Reason |
|---|---|---|
| **Interface** | Discord DM | personal use; and unlike WhatsApp it permits unprompted messages |
| **Discord input** | polling every 15 seconds | n8n has no official Discord trigger; polling avoids community nodes entirely |
| **Networking** | none inbound | polling is all outbound — no public URL, no tunnel, no VPS |
| **n8n** | self-hosted natively via npm | needs host access to reach the bridge; Cloud cannot |
| **CV skills** | Claude Code CLI | free on an existing subscription, and runs the skills' own Python |
| **PDF** | `reportlab` via a custom renderer | pandoc needs a multi-gigabyte LaTeX install |
| **State** | a JSON file owned by the bridge | must be writable *during* slow work, which n8n cannot do |
| **Scope** | single user, self-hosted | what made the rest fit in a three-day build |

---

## Rejected alternatives

### The Anthropic API

The account had roughly $100 of credit. It is **product** credit — for Claude Code and claude.ai — **not API credit**. A real API call returns `credit balance is too low`. Scoping to a cheaper model does not help.

> **A subscription never grants API access.** They are separate products with separate billing.

This is why the CV features go through the Claude Code CLI and a local bridge rather than a clean HTTP call.

### Calling a Claude Skill directly from n8n

No node exists for it, and the Skills API requires paid API credit. Hence the CLI.

### n8n's Execute Command node

Disabled by default in n8n 2.x, and broken even when enabled. It spawns with `{shell: true, detached: true}`, which on Windows becomes `cmd.exe /d /s /c "..."` — mangling any argument containing spaces, quotes or newlines. A prompt is nothing but spaces, quotes and newlines.

`echo` worked. No external executable did. A no-argument wrapper script also failed.

**Replaced by an HTTP bridge**, which sidesteps shell quoting, PATH inheritance and detached spawning at once — and is more portable, since a containerised n8n can still reach it.

### n8n's file nodes

`Access to the file is not allowed`. n8n 2.x blocks its own read/write nodes from arbitrary paths.

The documented workaround is an environment variable — rejected, because it pushes a configuration step onto every future user of the repo. Instead **the bridge took over all file I/O**. n8n now speaks nothing but HTTP, which also survives n8n moving to Docker-only.

### n8n Cloud

Cannot reach a process on your laptop. The Claude Code integration could not exist there.

> **Self-hosting is required, not preferred.** The bill for it: n8n Cloud ships a registered Google OAuth app, so connecting Sheets is one click. Self-hosted has none, turning that into a service-account setup.

### n8n's static data as a lock

The obvious place to keep the polling cursor. It is only written when an execution **finishes** — so during a 3-minute CV review, a dozen overlapping 15-second polls all read a stale cursor and reprocessed the same message.

**A lock that only exists after the work is not a lock.** Moved to the bridge, which writes synchronously under a mutex before the slow work starts.

### An AI Agent node holding matching as a tool

The Day 1 plan called for this, and it was rejected during implementation.

An agent returns the model's **narration** of a tool result, not the structured data. The Discord formatting needs rank, score, budget and URL intact.

A classifier plus a branch keeps the routing decision genuinely model-made — no keyword matching anywhere — while the data stays structured. **Using the agent node would have traded working structure for a node name.**

### pandoc

Needs a multi-gigabyte LaTeX distribution to produce PDFs. Replaced with a ~200-line `reportlab` renderer that has no external dependencies and, as a side effect, could be given a purpose-built resume style later.

### WhatsApp

Its 24-hour messaging window turns an unprompted daily digest into a paid, pre-approved template message. **The single most important feature would have been the one that cost money.** Discord has no such restriction.

### Telegram

Would have worked. Discord was chosen so the project differed from what others were building.

### Upwork as a job source

The API is partner-gated with no public access, and scraping breaks its terms of service. Freelancer.com has an open API.

### A second job source

Evaluated and measured: roughly 11 contract roles, heavily skewed to one country, mostly one employer, and no budget data at all. **Dropped rather than deferred** — a bad second source is worse than one good one.

### A `CVs` sheet

Day 1's architecture specified three sheets. The bridge's state file already persists the CV durably and survives restarts of both processes. A second copy in Sheets would only ever be the stale one. **Two sheets, deliberately.**

---

## Scope cuts, and why each was cut

### Multi-user

One instance per person. No user table, no authentication, no per-user state.

This is what made everything else fit in three days. It is stated as a limitation rather than hidden.

### Four-axis job scoring

The original vision ranked jobs on **money, difficulty, skills gained, and resume worth**.

Only **money** is real data. The other three are model judgements with no field behind them in any API. Shipping three invented axes would look impressive in a demo and mean nothing.

> Cut **with the reason recorded**. That is scoping. Deleting it silently would have been hiding.

### The revision loop on the rewrite

*"Any changes you'd like?"* — multi-turn editing state, a day's work on its own.

### Keep / drop / refresh on matches

Needs per-match state and a re-query path.

---

## Decisions that changed during the build

Three plans did not survive contact with reality. Each is more interesting than the original plan.

### n8n was going to orchestrate the CV conversation

**Changed on discovery.** During pre-build testing, the reviewer skill ended its report by offering the optimizer *without being asked*. It already knew how to chain.

Orchestrating that from n8n would have meant re-implementing a conversation that existed for free. n8n dropped to being a thin pipe: it moves text and files, Claude Code owns the conversation.

**This was found, not designed.**

### The bridge was going to be a thin shim

It began as "wrap the CLI in HTTP, about 40 lines". It ended up owning **all** file I/O, **all** durable state, PDF rendering, and the concurrency lock — nine endpoints.

Every expansion was forced by a specific failure: n8n cannot touch files, n8n cannot hold a lock during slow work, n8n cannot run a script. Rather than working around each separately, one component became the place where side effects live.

**The result is a cleaner boundary than the original design:** n8n polls, branches and formats. The bridge does everything with a consequence.

### Intake was capped at three questions

The orchestration prompt said *"ask one at a time, three maximum"* — intended to keep Discord messages short.

The skill it was driving said the opposite: *"don't drip-feed one question at a time"*, with a 20-question bank.

**The prompt was overriding the skill and making it worse.** Removing the cap took the intake from 3 questions to 14, and — because they now arrive in one message — took the conversation from four model invocations to two.

> The lesson: when a component underperforms, check whether something upstream is preventing it from doing its job properly.

---

## Principles that held for the whole build

**Test the unknown first.** Day 2 opened with the one unverified link rather than the interesting part. It passed, so the fallback was never built.

**A green run is not proof.** The worst bug of the build passed its own test — a review worked only because the model happened to find the file by name after being given a malformed path. It was caught by reading state that nothing was asserting on.

**Report, don't fail, on quality.** Every generated pitch is graded at generation time for whether it cites a real project and whether it contains banned filler. Those flags are **recorded, not enforced** — a live run should not die because one pitch was weak, but the rate should be measurable afterwards. That is what made "91% cite a real project" possible to state.

**Name the specific move.** *"Never invent facts"* prevented nothing, because the model was not inventing facts — it was resolving ambiguity favourably. The rule only worked once it forbade the exact moves: adding a rate, re-attributing a number, strengthening a quantifier.

**Write down what you did not test.** Job-ranking determinism is unmeasurable against a live job pool. Recorded as unmeasured rather than guessed at.
