# ⚠️ Sanad — Risk Register & Carry-Over Fixes

**Date:** 2026-08-11 (Day 1) · **Open technical unknowns:** ~~1~~ → **0** *(R-1 closed on Day 2, 2026-08-12)*

> Parent documents: [../PROJECT-PLAN.md](../PROJECT-PLAN.md) · [../REQUIREMENTS.md](../REQUIREMENTS.md) · [ARCHITECTURE.md](ARCHITECTURE.md)

---

## 1. ✅ The one open unknown — now closed

Every other component of the architecture had been tested end to end. Exactly one link had not. **It was tested first thing on Day 2 and passed.**

### R-1 — n8n's HTTP Request node → `sanad_bridge.py`

> ### ✅ **RESOLVED — 2026-08-12, first task of Day 2**
>
> Workflow: [`Day-2-Build-Core/Core-Loop/r1-bridge-check.json`](../../../Day-2-Build-Core/Core-Loop/r1-bridge-check.json)
> Session: `5e4523b5-f981-47ad-892b-9cc54aa1a97f`
>
> | Check | Result | Proves |
> |---|:-:|---|
> | Turn 1 returns `ok:true` | ✅ | the HTTP Request node reaches the bridge — **R-1 itself** |
> | Turn 1 returns `resumed:false` | ✅ | the bridge created a new session |
> | Turn 2 returns `resumed:true` | ✅ | the bridge correctly chose `--resume` over `--session-id` |
> | Turn 2's output contains `7` | ✅ | **session continuity survives two separate n8n HTTP calls** |
>
> `R1_RESULT: PASS`
>
> The test deliberately proved more than R-1 required. Connectivity alone would have left the *actual* dependency untested: `cv-reviewer` asks intake questions across separate Discord messages, and every poll is a separate n8n execution. Turn 2 recalling turn 1's number is the evidence that the intake conversation can work at all. A fresh UUID is generated per run, so a stale session cannot produce a false pass.
>
> **The fallback was not needed. No unknowns remain in the architecture.**

| | |
|---|---|
| **Status** | ✅ **Verified 2026-08-12** |
| **Likelihood of failure** | Low |
| **Impact if it fails** | **Critical** — no CV review, no rewrite. Half the product |
| **Why the risk is low** | The bridge is proven standalone: `/health` responds, and a two-turn conversation over HTTP kept its session memory across separate processes. n8n's HTTP Request node is one of the most-used nodes in the product. No shell, no `PATH`, no spawning is involved — the exact three things that broke Execute Command |
| **Cost to test** | ~30 seconds |
| **When** | **First task of Day 2, before anything else is built** — done |
| **Fallback if it fails** | ~~Have n8n write the prompt to a watched file and poll for the response file~~ — not needed |

Testing it first was the single highest-value thing Day 2 could do. It passed, so the file-drop fallback was never built and the Day 2 plan proceeded unchanged.

---

## 2. 📊 Risk register

Ordered by expected damage.

| ID | Risk | Likelihood | Impact | Mitigation | When |
|:-:|---|:-:|:-:|---|:-:|
| ~~**R-1**~~ | ~~n8n cannot reach the bridge over HTTP~~ | — | — | ✅ **Closed 2026-08-12** — passed, plus session continuity through n8n | Day 2 |
| **R-2** | **Claude Code usage limits** hit during Days 2–3 testing | **Medium** | 🟠 High | **Pin skill outputs in n8n** and test everything downstream against pinned data instead of re-running the skill. Use the shorter fixture where the full report isn't needed | Days 2–3 |
| **R-3** | Demo-day failure — laptop, Discord, Claude Code, Freelancer API and two LLM providers must all work simultaneously, live, in front of supervisors | **Medium** | 🔴 Critical | **Record a full working demo the night before Day 5.** Non-negotiable. Also prepare pinned execution data so the workflow can be walked through even if a service is down | Day 4 |
| **R-4** | **LLM ranking is not deterministic** — Week 6 saw two of five matches change between identical runs on identical data | **High** | 🟡 Medium | Pin temperature to 0, score in fixed batches, and **state the limitation in the write-up** rather than pretending it's solved. Accept it; don't hide it | Day 3 |
| **R-5** | An LLM returns HTTP 200 with **truncated but valid-looking JSON**. Week 6 hit this at exactly `completionTokens: 4096` — nothing errored | Medium | 🟠 High | A validating Code node after **every** LLM call. Cap `maxTokens` explicitly. Never trust a green execution | Day 3 |
| **R-6** | The daily digest repeats a job, or goes silent when there's nothing new | Medium | 🟡 Medium | Check the `Matches` sheet *before* scoring, not after. Send an explicit "nothing new today". Test by forcing an empty result set | Day 3 |
| **R-7** | Discord rate-limits the 15-second poll | Low | 🟡 Medium | ⚠️ **Mitigation revised on Day 2.** The original plan — "advance the cursor only on a successful reply" — is incompatible with the fix for R-16, which must claim the cursor *before* the slow work. See **R-20** for the trade-off this creates | Day 2 |
| ~~**R-8**~~ | ~~Duplicate replies — a 15-second poll answering the same message repeatedly~~ | — | — | ✅ **Closed 2026-08-12.** Cursor + `author.bot` filter. Held for fast messages; the slow-message variant is **R-16** | Day 2 |
| **R-9** | **Imported workflow JSON silently drops fields** — parameter names differ between n8n versions, and resource-locator values import as cached labels with no underlying ID | **High** | 🟡 Medium | After **any** import, re-select every dropdown by hand rather than trusting the text displayed in it | Days 2–3 |
| **R-10** | Google Sheets `Map Automatically` restructures the sheet on a header mismatch — Week 6 had it append new empty columns and report success | Medium | 🟡 Medium | After any schema change, verify column **fill counts**. A green execution is not evidence | Day 3 |
| **R-11** | A free-tier LLM turns out not to be free — DeepSeek's advertised free tokens did not exist for a new account | Medium | 🟡 Medium | Verify quota in the provider console, never from a blog post. Three providers already validated in Week 6 | Day 3 |
| **R-12** | Scope creep into v1.5 / v2 before v1 is finished | Medium | 🟠 High | The scope table in [PROJECT-PLAN.md](../PROJECT-PLAN.md) §4 is fixed. v1.5 is unlocked only when Day 3's definition of done is met | All |
| **R-13** | n8n `503 Database is not ready` — SQLite WAL not checkpointed after an unclean shutdown | Low | 🟢 Low | Always stop with `Ctrl+C` and let it exit. If it persists: rename `~/.n8n/database.sqlite`, delete the `-wal` / `-shm` files, let n8n rebuild. Originally caused by killing `n8n execute` CLI runs mid-flight | All |
| **R-14** | Error workflows only fire on **production** executions, never on manual "Execute Workflow" runs — and running an Error Trigger manually injects n8n's placeholder data, which looks exactly like a real pass | Medium | 🟢 Low | Verify all error handling via a published trigger only | Day 4 |
| **R-15** | The cv-optimizer invents facts not in the source CV | Low | 🟠 High | Manual diff on Day 4 (FR-14). The skill is already written to forbid it; the check confirms it |
| ~~**R-16**~~ | ~~**Overlapping executions reprocess the same message** — the work is slower than the poll interval~~ | — | — | ✅ **Closed 2026-08-12.** Cursor claimed on the bridge *before* the slow work, under a lock. **See §2b** | Day 2 |
| ~~**R-17**~~ | ~~n8n 2.x blocks its own nodes from arbitrary filesystem paths — `Access to the file is not allowed`~~ | — | — | ✅ **Closed 2026-08-12.** The bridge owns all file I/O via `/fetch` and `/file`; n8n speaks only HTTP. Rejected `N8N_RESTRICT_FILE_ACCESS_TO` — it pushes an env var onto every user of the repo | Day 2 |
| ~~**R-18**~~ | ~~Claude Code sandboxes file reads to its working directory, so it cannot read a CV outside it~~ | — | — | ✅ **Closed 2026-08-12.** n8n passes `cwd` explicitly *and* the bridge defaults to the workspace — belt and braces, so it cannot regress on how the bridge is launched | Day 2 |
| ~~**R-19**~~ | ~~An n8n HTTP node overwrites `$json` with its own response, silently breaking every downstream expression~~ | — | — | ✅ **Closed 2026-08-12.** Rule for the rest of the build: **anything downstream of an HTTP node must reference `$('Node Name')`, never `$json`.** Side-effect calls go on a side branch, not in the chain | Days 2–4 |
| **R-20** | **A crash between claiming a message and replying to it loses that message permanently.** Introduced by the R-16 fix: the claim is deliberately written *before* the work, so a failure mid-flight is never retried | Low | 🟡 Medium | Accepted for v1 — the user simply resends. A proper fix is a two-phase claim (`claimed` → `completed`, with stale claims released on a timeout). **Designed, not built. Document it in the write-up.** | v2 |

---

## 2b. 🔬 R-16 in detail — the failure that only appears when the work is slow

Worth writing up properly, because it passed every test until the work got slow enough to overlap.

**What was seen:** one CV upload produced **five** acknowledgements, **five different** intake questions, and one complete review that arrived before the others.

**Why:** the cursor lived in n8n's **workflow static data**, which is only written when an execution *finishes*. A CV review takes **1–3 minutes**; the poll fires every **15 seconds**. While run #1 sat inside `Call Claude`, roughly a dozen more polls started, each read a cursor that had not moved yet, and each concluded the message was new.

**Why n8n cannot fix this itself:** the state only becomes durable *after* the slow work completes. Any lock stored there is worthless, because the whole point of a lock is to exist *during* the work.

**The fix:** the cursor moved to the bridge, which writes it synchronously under a `threading.Lock` before anything slow starts.

```
POST /claim {message_id}
  → {"claimed": true}    exactly one caller ever wins
  → {"claimed": false}   every overlapping poll stops dead
```

Verified directly: the same ID claimed three times → first wins, other two rejected; an older ID → rejected; a newer ID → accepted.

**Two things it fixed for free:** the Claude session ID moved to the same store, so multi-turn conversations became testable *without publishing* (n8n does not persist static data on manual runs either); and the same file is the working mechanism behind **FR-29**, *"remembers the CV between sessions"*.

**The general lesson, which applies to the rest of the build:** *any* polling trigger whose work can outlast its interval has this bug. The daily digest and the job-matching pipeline are both slower than 15 seconds, so both must claim before they work.

---

## 3. 🔧 Week 6 carry-over fixes

These were found during Week 6, **logged rather than patched** — each day's rubric was already met, and the capstone is where they get done properly. This is that list, with where each one lands.

| # | Problem found in Week 6 | Fix | Where |
|:-:|---|---|:-:|
| **1** | **Pitches are shallow.** Three of five reused *"deliver a high-quality solution that meets your requirements"*, and none cited the candidate's actual past work. Root cause was a schema flaw, not the model — the profiling step extracted *skills only*, so the pitch step never saw the projects | Add `notable_projects` to the profile schema; require each pitch to cite one specific past project; ban the filler phrasing explicitly | Day 3 · FR-22 |
| **2** | **Imported JSON silently drops fields** — `keyValue` vs `dedupeValue`, resource locators importing as cached labels | Re-select every dropdown after any import | Days 2–3 · R-9 |
| **3** | **Free-tier claims must be verified in the console**, not from blogs. DeepSeek's free tokens didn't exist for a new account; OpenRouter needed `maxTokens` capped at 4096 | Verify quotas before relying on a provider | Day 3 · R-11 |
| **4** | **Sheets `Map Automatically` restructured a sheet** on a header mismatch (`skill` vs `skills`) — appended new empty columns, filled 0/64, and reported success | Verify fill counts after any schema change | Day 3 · R-10 |
| **5** | **Non-English gigs pass through unfiltered** — ~7 of 50 Freelancer projects. The API exposes a reliable `language` field | One filter node | Day 3 · FR-23 |
| **6** | **LLM ranking is non-deterministic** — two of five top matches changed between identical runs | Pin temperature, fix batch sizes, and state the residual limitation | Day 3 · R-4 |
| **7** | **Error workflows only fire on production executions** — a manual run injects placeholder data that looks like a pass | Verify via a published trigger | Day 4 · R-14 |
| **8** | **LLM output-token ceilings** — HTTP 200 with valid-looking truncated JSON at exactly 4096 tokens; only a validating Code node caught it | Validation guard on every LLM output | Day 3 · R-5 |
| **9** | **Arbeitnow is a weak second source** — ~11 contract roles, Germany-skewed, one employer, no budget data | **Decision: drop it.** A second source is v2, and finding a good one is research, not build | v2 |

---

## 4. 📉 Accepted limitations

Not risks to be mitigated — known properties of the design, to be stated plainly in the write-up rather than discovered by a supervisor during the demo.

- **Sanad only runs while the PC is on**, and while both n8n and the bridge are running.
- **Self-hosting is required, not preferred.** n8n Cloud blocks host access and cannot reach a localhost bridge, so the Claude Code integration could not exist there.
- **A Claude Skill cannot be invoked from n8n directly** — no node exists, and the Skills API needs paid API credit. Hence the CLI and the bridge.
- **LLM ranking is not fully deterministic**, even with temperature pinned.
- **Only *money* is objective.** Difficulty, skills-gained and resume-worth are LLM judgments, not fields in any API. This is why full four-axis scoring is v2 — scoring on three invented axes without evaluating them would be dishonest.
- **One user per instance.** No auth, no user table. Each person self-hosts.
- **One job source.** Freelancer.com only.
- **The 15-second poll is a compromise** — it feels live in a demo and costs nothing on a self-hosted instance, but it is polling, not push.
- **Only the newest message per poll is processed.** Two messages sent inside the same 15-second window means the older one is skipped, not queued. Fine for one person typing; a consequence of claiming a single cursor rather than a queue (see R-16).
- **A message claimed but not completed is lost** — see R-20. The user resends; v1 does not retry.
- **The bridge is now a single point of failure.** It owns state, files and the model call. It holds nothing in memory, so restarting it loses nothing, but nothing works while it is down.

---

## 5. 🎬 Demo-day contingency

R-3 is the highest-impact risk in the register, because it is the one that fails in public.

1. **The recorded demo is made the night before Day 5.** Not on the morning of.
2. **Pinned execution data** is saved for every workflow, so each step can be walked through even with a service down.
3. **Both fixtures stay ready** — messy (46/100) and polished (85/100) — so the before/after story survives even if a live run has to be skipped.
4. **The bridge and n8n both start from `tools/start-sanad.bat`**, so the demo environment comes up in one action rather than four.
