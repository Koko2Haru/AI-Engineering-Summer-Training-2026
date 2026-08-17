# Installing Rafid

**Rafid** is a Discord bot that reviews and rewrites your CV, then finds live freelance work that fits it — and sends you one job every morning without being asked.

This is the practical guide: what to take from this repo, and how to get it running on your own machine.

**Time: 45–60 minutes**, most of it waiting on account signups.
**Cost: $0** — free tiers throughout, plus a Claude subscription you probably already have.

---

## 1. What to take from this repo

**One folder: `rafid/`.** That's the whole application.

```
rafid/
├── bridge/      rafid_bridge.py · md2pdf.py
├── skills/      cv-reviewer · cv-optimizer
├── workflows/   the three n8n workflows
├── fixtures/    two demo CVs, for testing the install
└── scripts/     start-rafid.bat · stop-rafid.bat
```

Plus **this file** for the instructions.

> The `Day-1` … `Day-5` folders are the coursework write-up — daily reports, planning documents, test results. They also contain **older copies of the workflows** under their original name, kept as a dated record. Don't import those; use `rafid/workflows/`.

---

## 2. What you need first

| | Why |
|---|---|
| **Node.js LTS + npm** | runs n8n and Claude Code |
| **Python 3.9+** | runs the bridge and the PDF renderer |
| **A Claude subscription** | runs the two CV skills |
| **A Google account** | Google Sheets |
| **A Discord account** | the interface |

> **Your Claude subscription is enough — you do not need API credit.** They are separate products. A direct API call fails with `credit balance is too low` even with product credit on the account. Rafid runs the Claude Code CLI, which uses the subscription.

---

## 3. Install

### 3.1 Claude Code

```bash
npm install -g @anthropic-ai/claude-code
claude
```

Run `claude` once and log in. Built against **v2.1.226**.

### 3.2 The skills

```bash
cp -r rafid/skills/cv-reviewer   ~/.claude/skills/
cp -r rafid/skills/cv-optimizer  ~/.claude/skills/
```

Windows: `C:\Users\<you>\.claude\skills\`. Delete any `__pycache__` folders that came along.

### 3.3 Python packages

```bash
pip install reportlab pypdf
```

### 3.4 n8n

```bash
npm install -g n8n
n8n start
```

Open `http://localhost:5678`, create a local owner account. **Always stop n8n with `Ctrl+C`** — closing the window leaves the database in a state that returns `503 Database is not ready` on next start.

---

## 4. Accounts and keys

### 4.1 Discord

1. **discord.com/developers** → New Application → Bot → copy the **token**
2. Create a **private server** and invite your bot to it
3. Settings → Advanced → **enable Developer Mode**
4. Right-click **your own name** → **Copy User ID**
5. Create the DM channel, once:

```bash
curl -X POST "https://discord.com/api/v10/users/@me/channels" \
  -H "Authorization: Bot YOUR_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"recipient_id":"YOUR_NUMERIC_USER_ID"}'
```

**Save the `id` from the response.** That's your DM channel ID — you need it in step 6.

> **A shared server is required.** A bot cannot DM you unless you're both in the same server. Undocumented, but real — that's why step 2 exists.
>
> **The user ID is a number**, 17–19 digits, not your username. A username returns `Invalid Form Body`.

### 4.2 Google Sheets

Create a spreadsheet called `Rafid` with **two tabs**. Row 1 of each, exactly:

**`Jobs`**
```
job_id  title  description  budget_min  budget_max  currency  skills  url  language  fetched_at
```

**`Matches`**
```
job_id  title  url  score  reason  pitch  source  sent_at
```

> Headers must match exactly. A mismatch doesn't error — n8n silently appends new empty columns and reports success.

**Connect it with a service account**, not OAuth. Self-hosted n8n has no registered Google app, so OAuth means building one; a service account skips the consent screen entirely.

1. **console.cloud.google.com** → new project
2. **APIs & Services → Library** → enable **Google Sheets API** *and* **Google Drive API**
3. **Credentials → Create Credentials → Service account** → name it → Done
4. Open it → **Keys → Add key → Create new key → JSON** → a file downloads
5. In n8n: new Google Sheets credential → **Service Account** auth → paste `client_email` and `private_key` from that file
6. **Share your `Rafid` sheet with that `client_email`, as Editor**

Step 6 is the one people forget. Without it you get a confusing permissions error — a service account is a separate identity and only sees what's shared with it.

### 4.3 Model providers

Free tier on all three. Create an n8n credential for each.

| Provider | Used for | Watch out |
|---|---|---|
| **Google Gemini** | routing, CV profiling | — |
| **OpenRouter** | scoring jobs | cap `maxTokens` at 4096 — the 65536 default exceeds the free credit reservation |
| **Groq** | writing pitches | free tier is **6000 tokens/minute**, counted as `prompt + max_tokens`, **not** actual output |

> That Groq behaviour is counterintuitive enough to cost you an hour. Raising the token ceiling to give the model room makes the request fail **before it generates anything**. Leave `maxTokensToSample` at 2000.

---

## 5. Import the workflows

In n8n: **Create Workflow → ⋮ → Import from File**, once per file.

```
1. rafid-job-matching.json     ← import FIRST, the others reference it
2. rafid-poll-loop.json
3. rafid-daily-digest.json
```

### Re-select every credential after importing

Credential references do not survive an import. Resource-locator fields import as cached labels with **no underlying value** — the field looks filled and is empty.

| Workflow | Select credentials on |
|---|---|
| **Job Matching** | `Read Sent Matches`, `Save Jobs`, `Save Matches` (Sheets) · `Gemini Flash` · `OpenRouter DeepSeek` · `Groq Llama` |
| **Poll Loop** | 9 Discord nodes (`Get Messages`, `Send Welcome`, `Send Ack`, `Send Summary`, `Send Document`, `Send Chat Reply`, `Send Searching`, `Send Matches`, `Send Reset Confirm`) · `Router Gemini` |
| **Daily Digest** | `Send Digest` (Discord) |

---

## 6. Change these four values to your own

The workflows ship with the author's values. Replace all four.

| # | What | Where |
|:-:|---|---|
| 1 | **DM channel ID** | `Config` node → `dm_channel_id`, in **Poll Loop** *and* **Daily Digest** |
| 2 | **Workspace path** | `Config` node → `workspace`, in **Poll Loop**. Set it to your own `rafid/workspace` folder |
| 3 | **Spreadsheet ID** | the three Sheets nodes in **Job Matching** — the long string from your sheet's URL |
| 4 | **Job Matching reference** | `Run Job Matching` node in **Poll Loop** *and* **Daily Digest** — re-select your imported copy from the dropdown |

Miss #4 and the job search silently does nothing. Miss #2 and Claude Code can't read your CV, because it sandboxes file access to its working directory.

---

## 7. Start it

```bash
rafid/scripts/start-rafid.bat
```

Launches n8n and the bridge in two minimised windows. n8n takes 20–30 seconds.

Or by hand:

```bash
n8n start
python rafid/bridge/rafid_bridge.py
```

**Check the bridge:** open `http://127.0.0.1:8900/health` — you want `{"ok": true, ...}` and the path to your Claude Code executable.

The bridge's terminal sits there doing nothing after printing its routes. That's correct — it's a server.

---

## 8. Publish

**Publish all three, and publish `Rafid - Job Matching` FIRST.**

n8n 2.x refuses to publish a workflow whose sub-workflows are not published:

```
Cannot publish workflow: Node "Run Job Matching" references workflow
<id> which is not published. Please publish all referenced sub-workflows first.
```

So the order is:

1. **`Rafid - Job Matching`** — publish it
2. **`Rafid - Poll Loop`** — publish
3. **`Rafid - Daily Digest`** — publish

> If you get that error and Job Matching *is* published, the `Run Job Matching`
> node is pointing at a different copy.
>
> **Do not trust the dropdown.** n8n stores that field as an ID plus a cached
> label, and it renders the *label*. A node can display **"Rafid - Job Matching"**
> while pointing at a workflow that no longer exists — so "re-selecting" the value
> already shown changes nothing.
>
> **Set it by ID instead:** open the node, switch the Workflow selector from
> `From list` to `By ID`, and paste the id from the workflow's URL
> (`/workflow/<id>`). Do this in **both** Poll Loop and Daily Digest.
>
> The shipped files leave this field **empty on purpose**, so it fails loudly
> rather than looking correct.

> "Publish" is what older n8n called "Active". Unpublished workflows don't run on their schedule.

---

## 9. Check it works

Message your bot in Discord:

| Send | Expect |
|---|---|
| `hi` | the welcome, within 15 seconds |
| a CV as a **PDF** | acknowledgement, then ~14 numbered questions |
| your answers | maybe one clarifying question, then a review + PDF |
| `yes` | optimised CV and change report, both PDFs |
| `find me work` | five live projects with pitches, ~1 minute |

Then wait for **08:00** — one job arrives without you asking.

`reset` clears the conversation and starts fresh, without touching n8n. Useful when demoing.

---

## 10. When it breaks

| Symptom | Cause |
|---|---|
| Bot never replies | workflow isn't **published**, or the bridge is down |
| Replies arrive several times | n8n can't reach the bridge, so the message lock isn't working |
| *"I don't see a CV attached"* after sending a file | you sent a non-PDF. Only PDFs are read |
| *"I need permission to run…"* in chat | Claude Code permissions are per working directory — check value #2 |
| Sheets permission error | the sheet was never **shared with the service account email** |
| `Request too large … TPM` | a token ceiling was raised above the free-tier per-minute limit |
| Sheet grows empty columns | a header doesn't match the workflow's column names exactly |
| Bot replies to an old message right after publishing | expected — it claims the newest existing message. Send `reset` first |
| n8n won't start, `503 Database is not ready` | it was killed rather than stopped. `Ctrl+C` next time. If stuck, rename `~/.n8n/database.sqlite`, delete the `-wal`/`-shm` files |

---

## Before you rely on it

- **It only runs while your PC is on**, with both n8n and the bridge running
- **One person per installation.** No accounts, no multi-user — everyone self-hosts
- **PDF and plain text CVs only**
- **Ranking within the top five is weak** — about half of all scores land on exactly 80
- **Roughly 1 pitch in 11 overstates your experience.** Read them before sending
- **Budgets aren't converted** — you'll see CAD, USD, AUD and INR side by side

Fuller detail, with a fix identified for each, in
[`Day-5-Demo-Day/Resources/06-LIMITATIONS-AND-FUTURE.md`](Day-5-Demo-Day/Resources/06-LIMITATIONS-AND-FUTURE.md).

---

## Where to read more

| | |
|---|---|
| What Rafid is and why | [`Resources/00-WHAT-IS-RAFID.md`](Day-5-Demo-Day/Resources/00-WHAT-IS-RAFID.md) |
| How it's built | [`Resources/01-ARCHITECTURE.md`](Day-5-Demo-Day/Resources/01-ARCHITECTURE.md) |
| Does it actually work | [`Resources/03-EVALUATION-AND-RESULTS.md`](Day-5-Demo-Day/Resources/03-EVALUATION-AND-RESULTS.md) |
| Why these choices | [`Resources/05-DECISIONS-AND-REJECTED.md`](Day-5-Demo-Day/Resources/05-DECISIONS-AND-REJECTED.md) |
