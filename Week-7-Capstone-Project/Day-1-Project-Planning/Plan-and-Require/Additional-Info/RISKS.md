# ⚠️ Sanad — Risk Register & Carry-Over Fixes

**Date:** 2026-08-11 (Day 1) · **Open technical unknowns:** 1

> Parent documents: [../PROJECT-PLAN.md](../PROJECT-PLAN.md) · [../REQUIREMENTS.md](../REQUIREMENTS.md) · [ARCHITECTURE.md](ARCHITECTURE.md)

---

## 1. 🔴 The one open unknown

Every other component of the architecture has been tested end to end. Exactly one link has not.

### R-1 — n8n's HTTP Request node → `sanad_bridge.py`

| | |
|---|---|
| **Status** | ⚠️ **Unverified** |
| **Likelihood of failure** | Low |
| **Impact if it fails** | **Critical** — no CV review, no rewrite. Half the product |
| **Why the risk is low** | The bridge is proven standalone: `/health` responds, and a two-turn conversation over HTTP kept its session memory across separate processes. n8n's HTTP Request node is one of the most-used nodes in the product. No shell, no `PATH`, no spawning is involved — the exact three things that broke Execute Command |
| **Cost to test** | ~30 seconds |
| **When** | **First task of Day 2, before anything else is built** |
| **Fallback if it fails** | Have n8n write the prompt to a watched file and poll for the response file. Slower and uglier, but shell-free — which was the whole point of dropping Execute Command |

Testing it first is the single highest-value thing Day 2 can do. If it fails, three days remain to route around it; if it fails on Day 4, the project fails.

**This is the only remaining unknown in the whole architecture.**

---

## 2. 📊 Risk register

Ordered by expected damage.

| ID | Risk | Likelihood | Impact | Mitigation | When |
|:-:|---|:-:|:-:|---|:-:|
| **R-1** | n8n cannot reach the bridge over HTTP | Low | 🔴 Critical | Test first thing on Day 2; file-drop fallback designed | Day 2 |
| **R-2** | **Claude Code usage limits** hit during Days 2–3 testing | **Medium** | 🟠 High | **Pin skill outputs in n8n** and test everything downstream against pinned data instead of re-running the skill. Use the shorter fixture where the full report isn't needed | Days 2–3 |
| **R-3** | Demo-day failure — laptop, Discord, Claude Code, Freelancer API and two LLM providers must all work simultaneously, live, in front of supervisors | **Medium** | 🔴 Critical | **Record a full working demo the night before Day 5.** Non-negotiable. Also prepare pinned execution data so the workflow can be walked through even if a service is down | Day 4 |
| **R-4** | **LLM ranking is not deterministic** — Week 6 saw two of five matches change between identical runs on identical data | **High** | 🟡 Medium | Pin temperature to 0, score in fixed batches, and **state the limitation in the write-up** rather than pretending it's solved. Accept it; don't hide it | Day 3 |
| **R-5** | An LLM returns HTTP 200 with **truncated but valid-looking JSON**. Week 6 hit this at exactly `completionTokens: 4096` — nothing errored | Medium | 🟠 High | A validating Code node after **every** LLM call. Cap `maxTokens` explicitly. Never trust a green execution | Day 3 |
| **R-6** | The daily digest repeats a job, or goes silent when there's nothing new | Medium | 🟡 Medium | Check the `Matches` sheet *before* scoring, not after. Send an explicit "nothing new today". Test by forcing an empty result set | Day 3 |
| **R-7** | Discord rate-limits the 15-second poll | Low | 🟡 Medium | Advance the last-seen cursor only on a successful reply, so a rate-limited poll re-reads rather than skips | Day 2 |
| **R-8** | Duplicate replies — a 15-second poll answering the same message four times a minute | Medium | 🟡 Medium | `after={message_id}` on the Discord read, plus the cursor in the `CVs` sheet. Explicitly tested (FR-4) | Day 2 |
| **R-9** | **Imported workflow JSON silently drops fields** — parameter names differ between n8n versions, and resource-locator values import as cached labels with no underlying ID | **High** | 🟡 Medium | After **any** import, re-select every dropdown by hand rather than trusting the text displayed in it | Days 2–3 |
| **R-10** | Google Sheets `Map Automatically` restructures the sheet on a header mismatch — Week 6 had it append new empty columns and report success | Medium | 🟡 Medium | After any schema change, verify column **fill counts**. A green execution is not evidence | Day 3 |
| **R-11** | A free-tier LLM turns out not to be free — DeepSeek's advertised free tokens did not exist for a new account | Medium | 🟡 Medium | Verify quota in the provider console, never from a blog post. Three providers already validated in Week 6 | Day 3 |
| **R-12** | Scope creep into v1.5 / v2 before v1 is finished | Medium | 🟠 High | The scope table in [PROJECT-PLAN.md](../PROJECT-PLAN.md) §4 is fixed. v1.5 is unlocked only when Day 3's definition of done is met | All |
| **R-13** | n8n `503 Database is not ready` — SQLite WAL not checkpointed after an unclean shutdown | Low | 🟢 Low | Always stop with `Ctrl+C` and let it exit. If it persists: rename `~/.n8n/database.sqlite`, delete the `-wal` / `-shm` files, let n8n rebuild. Originally caused by killing `n8n execute` CLI runs mid-flight | All |
| **R-14** | Error workflows only fire on **production** executions, never on manual "Execute Workflow" runs — and running an Error Trigger manually injects n8n's placeholder data, which looks exactly like a real pass | Medium | 🟢 Low | Verify all error handling via a published trigger only | Day 4 |
| **R-15** | The cv-optimizer invents facts not in the source CV | Low | 🟠 High | Manual diff on Day 4 (FR-14). The skill is already written to forbid it; the check confirms it |

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

---

## 5. 🎬 Demo-day contingency

R-3 is the highest-impact risk in the register, because it is the one that fails in public.

1. **The recorded demo is made the night before Day 5.** Not on the morning of.
2. **Pinned execution data** is saved for every workflow, so each step can be walked through even with a service down.
3. **Both fixtures stay ready** — messy (46/100) and polished (85/100) — so the before/after story survives even if a live run has to be skipped.
4. **The bridge and n8n both start from `tools/start-sanad.bat`**, so the demo environment comes up in one action rather than four.
