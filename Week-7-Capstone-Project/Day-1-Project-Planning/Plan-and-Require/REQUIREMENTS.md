# 📋 Sanad — Requirements

**Date:** 2026-08-11 (Day 1) · **Status:** Locked for v1

> Companion documents: [PROJECT-PLAN.md](PROJECT-PLAN.md) · [Additional-Info/ARCHITECTURE.md](Additional-Info/ARCHITECTURE.md) · [Additional-Info/RISKS.md](Additional-Info/RISKS.md)

Each requirement has an ID, a priority, and an **acceptance test** — the thing that has to be demonstrated for it to count as done. Day 4 works through this list.

**Priority key:** 🟢 v1 (must build) · 🟠 v1.5 (if time) · 🔴 v2 (documented, not built)

---

## 1. 💬 Functional — the conversation

| ID | Requirement | Pri | Acceptance test |
|---|---|:-:|---|
| **FR-1** | Sanad receives direct messages sent to it on Discord | 🟢 | A DM sent from the phone appears in an n8n execution within 15 s |
| **FR-2** | Sanad replies in the same DM channel | 🟢 | A reply arrives in Discord, visibly from `Sanad-AI#1718` |
| **FR-3** | First-ever contact gets a welcome message explaining what Sanad does and how to start | 🟢 | Sending `hi` to a fresh instance returns the welcome, not a generic answer |
| **FR-4** | Each message is processed exactly once | 🟢 | Two polls over the same message produce one reply, not two |
| **FR-5** | An **agent** decides what each message means — CV upload, approval, job request, parameter change, or plain question — and routes accordingly | 🟢 | Five messages of the five different kinds each reach the correct branch, with no keyword matching in the routing |
| **FR-6** | Sanad answers general questions about itself without derailing an in-progress flow | 🟢 | Asking *"what can you do?"* mid-intake answers, then returns to the intake question |
| **FR-7** | Conversation state survives across separate messages | 🟢 | An intake question asked in message 3 is answered in message 4 and the review completes — despite each poll being a separate n8n execution |

## 2. 📄 Functional — CV review and rewrite

| ID | Requirement | Pri | Acceptance test |
|---|---|:-:|---|
| **FR-8** | A PDF CV attached to a DM is downloaded and its text extracted | 🟢 | Attaching `synthetic-cv-messy.pdf` yields readable text in the execution data |
| **FR-9** | `cv-reviewer` runs on the extracted CV | 🟢 | The run produces a score and category breakdown; the messy fixture scores ≈46/100 |
| **FR-10** | Intake questions are asked **in the Discord DM** and the answers feed the review | 🟢 | Sanad asks at least one question, waits, and the answer changes the report |
| **FR-11** | The review is returned as a **short summary in chat** *plus* the **full report as a PDF attachment** | 🟢 | Both arrive; the PDF opens and its text extracts cleanly |
| **FR-12** | Sanad offers to fix the CV, and runs `cv-optimizer` on acceptance | 🟢 | Replying *"yes"* starts the rewrite without further instruction |
| **FR-13** | The rewrite returns the **optimised CV** and a **change report**, both as PDFs | 🟢 | Two PDFs arrive in the DM |
| **FR-14** | The rewrite invents no facts not present in the original CV or the intake answers | 🟢 | Manual diff of the optimised CV against the source: every claim traceable |
| **FR-15** | The optimised CV measurably outscores the original | 🟢 | Re-reviewing the rewrite gives a higher score; both numbers reported honestly |
| **FR-16** | *"Add this new project to my CV"* → updated CV → new PDF | 🟠 | A project described in chat appears, well-written, in a regenerated CV |
| **FR-17** | Revision loop — *"any changes?"* → user asks → CV revised | 🔴 | — not built |

## 3. 🔍 Functional — job matching

| ID | Requirement | Pri | Acceptance test |
|---|---|:-:|---|
| **FR-18** | Sanad offers to find freelance work once the CV is ready | 🟢 | The offer appears unprompted after the rewrite |
| **FR-19** | Live projects are fetched from the Freelancer.com API | 🟢 | The `Jobs` sheet fills with projects dated today |
| **FR-20** | Projects are scored against the CV profile and ranked | 🟢 | Scores present for every fetched job; ranking is by score |
| **FR-21** | The **top 5** are returned with a **pitch for each** | 🟢 | Five jobs in the DM, each with a link and a pitch |
| **FR-22** | Each pitch cites a **specific past project** from the CV and avoids filler phrasing | 🟢 | 5/5 pitches name a real project; none contain the banned phrases (Week 6 carry-over §1) |
| **FR-23** | Non-English projects are filtered out | 🟢 | No non-English titles in the returned set (Week 6 carry-over §5) |
| **FR-24** | The user can set matching parameters in chat | 🟢 | Saying *"only jobs over $500"* changes the result set |
| **FR-25** | **One job per parameter** — the money one, the learning one, the portfolio one | 🟠 | Three jobs returned, each labelled with the axis it won on |
| **FR-26** | Keep / drop / refresh, with replacements offered for drops | 🔴 | — not built |
| **FR-27** | Full four-axis scoring — difficulty, skills gained, resume worth | 🔴 | — not built; only *money* is real API data, the rest are LLM judgments |
| **FR-28** | A second job source | 🔴 | — not built; Week 6 proved the available alternatives are poor |

## 4. 🧠 Functional — memory and initiative

| ID | Requirement | Pri | Acceptance test |
|---|---|:-:|---|
| **FR-29** | The CV persists between sessions | 🟢 | Restart n8n and the bridge, send *"find me work"* — it matches without asking for the CV again |
| **FR-30** | **Every morning at 08:00, exactly one unseen gig is sent, unprompted** | 🟢 | A message arrives with no user action; it contains one job, not five |
| **FR-31** | A job already sent is never sent again | 🟢 | Two consecutive daily runs produce two different jobs |
| **FR-32** | When there is nothing new, Sanad says so rather than repeating or going silent | 🟢 | Forcing an empty result set produces *"nothing new today"* |

## 5. 🛡️ Non-functional

| ID | Requirement | Target | How it's met |
|---|---|---|---|
| **NFR-1** | **Cost** | **$0** | Free-tier LLMs (Gemini / Groq / OpenRouter), Claude Code on the existing subscription, self-hosted n8n. The Anthropic **API** is unavailable — the account balance is product credit, not API credit |
| **NFR-2** | **No inbound networking** | none | Discord is *polled*. No public URL, no tunnel, no VPS, no port forwarding |
| **NFR-3** | **Responsiveness** | ≤ 15 s to acknowledge | 15-second poll interval; long operations send an "on it" message first |
| **NFR-4** | **Privacy** | no real personal data leaves the machine unnecessarily | Only the synthetic CV is used in testing; personal details stripped before any third-party LLM call; PDFs written locally |
| **NFR-5** | **No secrets in the repo** | zero | All keys are `PASTE_YOUR_..._HERE` placeholders, same as Week 6 |
| **NFR-6** | **Portability** | a classmate can run it | Ships with a Gemini + Code-node default path for anyone without a Claude subscription |
| **NFR-7** | **Robustness** | no silent failures | Every LLM output passes a validating Code node before use — Week 6 saw an HTTP 200 carrying truncated JSON at exactly 4096 completion tokens |
| **NFR-8** | **Determinism** | best-effort, honestly reported | Temperature pinned and batch sizes fixed for ranking. LLM ranking is *not* fully deterministic and the write-up says so |
| **NFR-9** | **Recoverability** | a crash loses no CV | The CV lives in Google Sheets, not in n8n memory |
| **NFR-10** | **Setup** | reproducible from one document | `SETUP.md` on Day 5, written from the steps in §7 below |

## 6. 🚫 Explicitly out of scope

Stating these prevents scope creep mid-build and makes the demo honest.

- **Multiple users.** One instance, one person. No user table, no auth, no per-user state.
- **Hosting.** Sanad runs only while the PC is on and both n8n and the bridge are running.
- **A web UI.** Discord *is* the interface.
- **DOCX / image CVs.** PDF and plain text only.
- **Applying to jobs.** Sanad finds and pitches; the human sends.
- **Non-Discord channels.** WhatsApp was evaluated and rejected — its 24-hour messaging window makes an unprompted daily digest a paid, pre-approved template message.
- **Upwork.** No public API; partner-gated; scraping breaks its ToS.

## 7. 🖥️ System requirements

### Software

| Component | Version / command | Notes |
|---|---|---|
| **Node.js + npm** | current LTS | needed for both n8n and Claude Code |
| **n8n** | 2.33.7, **self-hosted natively** | `npm install -g n8n` → `n8n start` → `http://localhost:5678`. Data in `~/.n8n`. Terminal must stay open |
| **Claude Code CLI** | v2.1.226 | `npm install -g @anthropic-ai/claude-code`, then run `claude` once to log in |
| **Python** | 3.x | for the bridge and the PDF writer |
| **Python packages** | `reportlab`, `pypdf` | `pip install reportlab pypdf` — the bridge itself is stdlib-only |
| **Skills** | `cv-reviewer`, `cv-optimizer` | copied into `~/.claude/skills/` |

### Accounts and keys — all free tier

| Service | Used for |
|---|---|
| **Discord** | bot token, a private server, the DM channel ID |
| **Google** | OAuth for Sheets (`Jobs`, `CVs`, `Matches`) |
| **Gemini** | CV profiling and summarisation |
| **Groq** | pitch writing |
| **OpenRouter** | job scoring — cap `maxTokens` at 4096; the 65536 default exceeds the free credit reservation |
| **Freelancer.com** | live project search |
| **Claude subscription** | runs the two skills through Claude Code |

### Discord setup — the non-obvious parts

These cost real time to discover; they are recorded so they cost nobody else any.

1. **A shared server is required.** A bot cannot DM you unless you and it are both in the same server. Undocumented, but confirmed empirically — Discord shows "1 Mutual Server". Create a private server and invite the bot.
2. **The user ID is a numeric snowflake** (17–19 digits), *not* the username. Settings → Advanced → Developer Mode, then right-click your own name → Copy User ID. Passing the username returns `Invalid Form Body`.
3. **The DM channel is created once** via `POST /users/@me/channels`, and the returned channel ID is then hardcoded into every polling workflow. Current instance: `1536751197627617401`.

### Known environment gotchas

- **`503 Database is not ready`** from n8n — the SQLite write-ahead log did not checkpoint after an unclean shutdown. Stop with `Ctrl+C` and let it exit properly, then restart. If it persists, rename `~/.n8n/database.sqlite` and delete the `-wal` / `-shm` files; n8n rebuilds a fresh one.
- **n8n now warns that running outside Docker is deprecated.** Harmless here — the bridge is reached over HTTP, so a containerised n8n calls `http://host.docker.internal:8900` instead of `127.0.0.1:8900`. This is precisely why the bridge replaced Execute Command, which would not have survived the change.
- **After importing any workflow JSON, re-select every dropdown.** Parameter names differ between n8n versions and resource-locator values import as cached labels with no underlying ID — the field looks right and is empty (Week 6 carry-over §2).
