# Rafid — Handoff

**Written:** 2026-08-17 · **Purpose:** everything needed to resume in a fresh session.

> Supersedes `Some-important-files/HANDOFF.md`, which describes the pre-build state and the old name.

---

## Where things stand

**The capstone is finished and working.** Five days done, all reports written, feature-complete against the agreed v1 scope.

| | |
|---|---|
| **Only thing left** | record the demo, then present it |
| **Everything else** | built, tested, measured, documented |

### The headline number

> **A CV went from 42/100 to 73/100.** A professionally written version of the same person scored **75**.
> Pitches cite the candidate's real past projects **91%** of the time, against **0%** in Week 6.

---

## The project

**Rafid** (رافد — *a tributary that feeds a larger river; one who supports*). **Renamed from "Sanad" on 2026-08-17.**

A Discord DM bot that:
1. Reviews your CV → summary in chat + full report PDF
2. Rewrites it → optimised CV + change report, both PDF
3. Matches it against live freelance projects, with a pitch per job
4. Remembers your CV between sessions
5. **Sends one gig every morning at 08:00, unprompted**

---

## Architecture in one box

```
Discord DM ──poll 15s──► n8n (self-hosted)
                           ├─ HTTP ─► rafid_bridge.py ─► Claude Code CLI + 2 skills
                           ├──────► Freelancer.com API
                           ├──────► Gemini / DeepSeek / Groq
                           └──────► Google Sheets (Jobs · Matches)
```

**Two rules that explain most decisions:**
- **No inbound networking.** Discord is polled, never pushed to.
- **The bridge owns every side effect.** n8n speaks nothing but HTTP. It cannot touch files, and it cannot hold a lock during slow work — so it does neither.

**Three workflows**, split by trigger: `Rafid - Poll Loop` (15s, 31 nodes) · `Rafid - Job Matching` (sub-workflow, 25 nodes) · `Rafid - Daily Digest` (08:00, 9 nodes).

---

## Repo layout

```
Week-7-Capstone-Project/
├── INSTALL.md            ← how to run it from scratch
├── WEEK7-README.md       ← the week write-up
├── HANDOFF.md            ← this file
├── rafid/                ← THE APPLICATION
│   ├── bridge/           rafid_bridge.py (9 endpoints) · md2pdf.py
│   ├── skills/           cv-reviewer · cv-optimizer
│   ├── workflows/        the 3 live workflows  ← import these
│   ├── fixtures/         synthetic-cv-messy.pdf · synthetic-cv-polished.pdf
│   ├── scripts/          start-rafid.bat · stop-rafid.bat
│   ├── brand/            icon.png · banner.svg · logo.svg
│   └── workspace/        runtime scratch — GITIGNORED
├── Day-1 … Day-5/        reports and per-day artefacts
└── Some-important-files/ old handoff + superseded scaffolding — GITIGNORED
```

> **Days 1–4 still say "Sanad" and still contain `sanad-*.json` copies.** Deliberate — they are a dated record and the rename happened on Day 5. Do not "fix" them; the user decided this explicitly.

---

## To bring it back up

```
rafid\scripts\start-rafid.bat
```

Then **wait 3–4 minutes.** The port opens long before n8n is usable — it goes `503 → timeouts → 404 → 200`. An open port means nothing.

Check `http://127.0.0.1:8900/health` → `{"ok": true, ...}` and `http://localhost:5678`.

**Before demoing:** send `reset` in Discord, then `hi`.

---

## Traps that cost real time — do not rediscover these

| Trap | What actually happens |
|---|---|
| **n8n port opens ~3 min before the UI works** | 503, then 404, then 200. Be patient |
| **Resource-locator dropdowns lie** | They store `{value: id, cachedResultName: label}` and **render the label**. A node can display "Rafid - Job Matching" while pointing at a deleted workflow. Re-selecting the shown value changes nothing — switch the selector to **By ID** and paste the id |
| **Sub-workflows must be published** | n8n 2.x refuses to publish a parent whose sub-workflow is unpublished. Order: Job Matching → Poll Loop → Daily Digest |
| **n8n cannot be closed gracefully** | It runs windowless and ignores close requests. Always kill it, then **checkpoint the database** — that is what `stop-rafid.bat` now does. Skipping this causes `503 Database is not ready!` |
| **Execution history bloats the DB** | It reached 91 MB and boot started timing out. Pruned to 2 MB. Prune again if boot gets slow |
| **Groq counts `prompt + max_tokens`** | Not actual output. Raising the ceiling makes the request fail *before* generating. Keep `maxTokensToSample` at 2000 |
| **Claude Code sandboxes file reads to its cwd** | The bridge passes `cwd` and defaults to the workspace |
| **HTTP nodes overwrite `$json`** | Anything downstream must use `$('Node Name')`. Side-effect calls go on a side branch |

---

## Current live IDs

| | |
|---|---|
| Discord DM channel | `1536751197627617401` |
| Google Sheet | `1GRaUUEDghekkY3bHRCLs5Yoy5PWJKC-jSyQ6Rdfdij4` (tabs `Jobs`, `Matches`) |
| n8n workflow IDs | Job Matching `2jspdtBsP7zypdHU` · Poll Loop `LOQrmt5MGsHOvppF` · Digest `4KIV2dbNFYoETpyO` |
| Bot | `Sanad-AI` — **still needs renaming to Rafid** in the Discord developer portal |

Credentials in n8n: Discord Bot, Google Sheets (service account), Gemini, Groq, OpenRouter. All present and working.

---

## Known limitations — measured, stated in the docs, not hidden

- **Score compression.** 55% of matches score exactly 80. Ranking within the top five is close to arbitrary. Cause: the prompt offers four bands and the model anchors to boundaries. Fix identified, not built.
- **~9% of pitches overstate experience.** The flag reports it; the prompt does not stop it.
- **Currencies not normalised** — CAD/USD/AUD/INR side by side.
- **Non-PDF attachments** report as "no attachment". Fix was written and **deliberately reverted** so the repo matches what was tested.
- **Job-ranking determinism unmeasured** — needs a frozen job pool, which a live API cannot give.
- **Sample sizes are small** — 11 matches, 4 scoring runs.

---

## Open items

1. **Record the demo** — the highest-impact remaining task. Six services must be healthy simultaneously; a recording removes that risk
2. **Rename the Discord bot** to Rafid, upload `rafid/brand/icon.png` as the avatar
3. **Export `banner.svg` to PNG from a browser** — CLI converters mangle the Arabic
4. **Commit** — the rename and brand work is uncommitted
5. *(optional)* Replace the hardcoded channel/sheet/path values with placeholders. **The user declined this** — do not do it unasked

---

## How the user works — read this before doing anything

| | |
|---|---|
| **Ask before creating or editing any file.** | Including inside Week 7 |
| **Weeks 1–6 are read-only** | |
| **The user makes every git commit** | Never run `git commit` or `git push` |
| **Day by day** | Do not start the next day's work unprompted |
| **Be brief** | *"you yap a lot"* — direct answers, no preamble, no restating the plan |
| **The ref ques** | End of each day, in chat only, first person, in the user's voice: *what happened today*, **Daily Task Completed**, **What I Learned**, **Challenges Faced**, **How I Solved Them**. **Target ~200 words total.** There is also a weekly set: most valuable thing learned · biggest challenge · what to practise · additional notes |
| **Check status by testing, not by reasoning** | Twice this session a schema-based diagnosis was wrong and a simple "is it executing?" query gave the answer immediately |

---

## The one thing worth remembering about this build

**Nearly every serious bug was something that worked for a reason nobody had checked.**

The review ran because Claude Code found the file by name after a malformed path. The pitches were generic because the profile schema omitted projects. The CV rendered flat because the model emitted no Markdown. The intake was shallow because the orchestration prompt overrode the skill. The scores clustered at 80 because the prompt offered bands.

In every case the fix only became obvious after establishing **why** it worked, rather than **that** it worked.
