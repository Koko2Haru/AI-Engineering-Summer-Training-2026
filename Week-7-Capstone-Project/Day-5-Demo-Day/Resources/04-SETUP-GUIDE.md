# Rafid — Setup Guide

*Source document 5 of 7. Self-contained: assumes no knowledge of the other files.*

Rafid is a Discord bot that reviews and rewrites CVs, then matches them against live freelance work. It runs entirely on one PC. This document is how to get it running from nothing.

**Realistic time: 45–60 minutes**, most of it waiting on account setup.

---

## What you are building

```
Discord DM  ──poll every 15s──►  n8n (localhost:5678)
                                   │
                                   ├─ HTTP ──►  rafid_bridge.py (127.0.0.1:8900)
                                   │              └──►  Claude Code CLI + 2 skills
                                   ├──────────►  Freelancer.com API
                                   ├──────────►  Gemini / DeepSeek / Groq
                                   └──────────►  Google Sheets
```

Two processes must be running: **n8n** and **the bridge**. Nothing is exposed to the internet.

---

## Prerequisites

| Thing | Why |
|---|---|
| Node.js LTS + npm | runs both n8n and Claude Code |
| Python 3.9+ | runs the bridge and the PDF renderer |
| A Claude subscription | runs the two CV skills through Claude Code |
| A Google account | Sheets |
| A Discord account | the interface |

---

## 1. Claude Code

```bash
npm install -g @anthropic-ai/claude-code
claude
```

Run `claude` once interactively and log in. Verified working on **v2.1.226**.

> **This uses your Claude subscription, not the API.** A subscription does not grant API access — a direct API call returns `credit balance is too low` even with product credit on the account. Running the CLI is what makes the CV features free.

---

## 2. The skills

Copy both skill folders into your Claude Code skills directory:

```bash
cp -r rafid/skills/cv-reviewer   ~/.claude/skills/
cp -r rafid/skills/cv-optimizer  ~/.claude/skills/
```

On Windows that is `C:\Users\<you>\.claude\skills\`.

Delete any `__pycache__` folders that came along.

---

## 3. Python dependencies

```bash
pip install reportlab pypdf
```

The bridge itself is standard library only. `reportlab` renders PDFs; `pypdf` is used by the skills to read them.

---

## 4. n8n

```bash
npm install -g n8n
n8n start
```

Open `http://localhost:5678` and create a local owner account. Data lives in `~/.n8n`. **The terminal must stay open.**

### Two things that will bite you

**`503 Database is not ready`** — the SQLite write-ahead log did not checkpoint after an unclean shutdown. Stop with `Ctrl+C` and let it exit properly, then start again. If it persists, rename `~/.n8n/database.sqlite` and delete the `-wal` and `-shm` files; n8n rebuilds. **Always stop n8n with `Ctrl+C`**, never by closing the window.

**n8n warns that running outside Docker is deprecated.** Harmless here. The bridge is reached over HTTP, so a containerised n8n simply calls `http://host.docker.internal:8900` instead of `127.0.0.1:8900`.

---

## 5. Discord

1. **discord.com/developers** → New Application → Bot → copy the **token**
2. Create a **private server** and invite the bot to it
3. **Enable Developer Mode**: Settings → Advanced → Developer Mode
4. Right-click **your own name** → **Copy User ID**
5. Create the DM channel once, with your bot token and your user ID:

```bash
curl -X POST "https://discord.com/api/v10/users/@me/channels" \
  -H "Authorization: Bot YOUR_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"recipient_id":"YOUR_NUMERIC_USER_ID"}'
```

Save the `id` from the response — that is your **DM channel ID**, needed by every workflow.

### Three non-obvious things

- **A shared server is required.** A bot cannot DM you unless you are both in the same server. This is undocumented but real — Discord will show "1 Mutual Server". This is why step 2 exists.
- **The user ID is a numeric snowflake** (17–19 digits), *not* your username. Passing a username returns `Invalid Form Body`.
- **The DM channel is created once** and its ID is then fixed forever.

---

## 6. Google Sheets

Create a spreadsheet named `Rafid` with **two tabs**, and put these exact headers in **row 1**:

**`Jobs`**
```
job_id  title  description  budget_min  budget_max  currency  skills  url  language  fetched_at
```

**`Matches`**
```
job_id  title  url  score  reason  pitch  source  sent_at
```

> Headers must match exactly. A mismatch does not error — n8n appends brand-new empty columns and reports success.

### Connecting it — use a service account, not OAuth

**n8n Cloud ships its own registered Google OAuth app, so it is one click there. Self-hosted n8n does not**, and Google requires whoever runs the instance to register their own. A **service account** is roughly half the steps and skips the consent screen entirely.

1. **console.cloud.google.com** → create a project
2. **APIs & Services → Library** → enable **Google Sheets API** *and* **Google Drive API**
3. **Credentials → Create Credentials → Service account** → name it → Done
4. Open it → **Keys → Add key → Create new key → JSON**. A file downloads
5. From that file you need two values: **`client_email`** and **`private_key`**
6. In n8n, create a Google Sheets credential using **Service Account** auth and paste those two in
7. **Open your `Rafid` sheet → Share → paste the `client_email` → give it Editor**

Step 7 is the one everyone forgets. Without it you get a confusing permissions error, because a service account is a separate identity that can only see what is explicitly shared with it.

---

## 7. Free-tier API keys

All three have free tiers. Create a credential in n8n for each.

| Provider | Used for | Watch out for |
|---|---|---|
| **Google Gemini** | intent routing, CV profiling | — |
| **OpenRouter** | scoring jobs | cap `maxTokens` at 4096; the default of 65536 exceeds the free credit reservation |
| **Groq** | writing pitches | free tier is **6000 tokens per minute**, and it counts `prompt + max_tokens`, **not** actual output |

> That Groq behaviour is genuinely counterintuitive. Raising the token ceiling to give the model room makes the request fail **before** it generates anything. Keep `maxTokensToSample` at 2000.

**Verify quotas in the provider's own console, never from a blog post.** One provider's widely-advertised free allowance did not exist for a new account.

---

## 8. Start the services

```bash
rafid/scripts/start-rafid.bat
```

That launches both n8n and the bridge in minimised windows. n8n takes 20–30 seconds to boot.

Or start them by hand:

```bash
n8n start
python rafid/bridge/rafid_bridge.py
```

**Check the bridge:** open `http://127.0.0.1:8900/health`. You should see `{"ok": true, ...}` with the path to your Claude Code executable.

The bridge's terminal will sit there doing nothing after printing its routes. That is correct — it is a server, it never returns to the prompt.

---

## 9. Import the workflows

In n8n, for each of the three files: **Create Workflow → ⋮ → Import from File**.

```
rafid-job-matching.json     import this FIRST - the others reference it
rafid-poll-loop.json
rafid-daily-digest.json
```

### After every import, re-select every credential and dropdown by hand

Credential references do not survive an import, and resource-locator fields import as cached labels with **no underlying value** — the field looks correctly filled and is empty.

| Workflow | Credentials to select |
|---|---|
| **Job Matching** | Google Sheets ×3, Gemini, OpenRouter, Groq |
| **Poll Loop** | Discord ×9, Gemini |
| **Daily Digest** | Discord ×1 |

### Then set your own values

Three things are specific to your installation:

| Where | What to change |
|---|---|
| `Config` node in Poll Loop and Daily Digest | your **DM channel ID** |
| `Config` node in Poll Loop | the **workspace path** on your machine |
| Sheets nodes in Job Matching | your **spreadsheet ID** |
| `Run Job Matching` nodes | re-select the **Job Matching workflow** |

---

## 10. Publish

**Publish all three, and publish Job Matching FIRST.**

Job Matching has no trigger of its own — it is called by the other two — but n8n 2.x still refuses to publish a workflow whose sub-workflows are unpublished:

```
Cannot publish workflow: Node "Run Job Matching" references workflow
<id> which is not published. Please publish all referenced sub-workflows first.
```

Order: **Job Matching → Poll Loop → Daily Digest.**

If that error appears while Job Matching *is* published, the `Run Job Matching` node is pointing at a different copy — open it and re-select the workflow from the dropdown. That reference is stored by ID, so it survives a rename but not a re-import.

> In n8n 2.x, "Publish" is what older versions called "Active". A workflow that is not published will not run on its schedule.

---

## 11. Test it

In Discord, message your bot:

1. `hi` → the welcome message, instantly
2. Send a CV as a **PDF** → an acknowledgement, then ~14 numbered questions
3. Answer them → possibly a clarifying question → then the review plus a PDF
4. `yes` → the optimised CV and a change report, both PDFs
5. `find me work` → five live projects with pitches

If something goes wrong, `reset` clears the conversation and starts fresh without touching n8n.

---

## Troubleshooting

| Symptom | Cause |
|---|---|
| Bot never replies | the workflow is not **published**, or the bridge is down |
| *"Access to the file is not allowed"* | a file node is being used instead of the bridge |
| *"I need permission to run..."* in chat | Claude Code permissions are per working directory; the bridge sets `--permission-mode` for this |
| Replies arrive several times | the cursor is not being claimed — check the bridge is reachable from n8n |
| Sheets error about permissions | the spreadsheet was never **shared with the service account email** |
| `Request too large ... TPM` | a token ceiling was raised above the free-tier per-minute limit |
| Sheet gains empty columns | a header does not match the workflow's column names exactly |
| Bot replies to old messages on first publish | expected — it claims the newest existing message. Send `reset` first |

---

## What it costs

**Nothing.** Claude Code runs on an existing subscription; Gemini, OpenRouter and Groq are used within free tiers; n8n is self-hosted; Google Sheets is free; Discord is free.

The real cost is that **Rafid only runs while the PC is on and both processes are running.**
