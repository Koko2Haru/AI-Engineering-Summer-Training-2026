# Prompt Logger — Test Plan

Covers every branch in `prompt_logger.py`: menu validation, experiment creation,
typo detection, all four save paths, the parser fixes, and failure handling.

## Before you start

- Every chat prompt must be pasted as **one single line** — `input()` splits on newlines.
- Full reset: with the script closed, delete `saved_responses/` and `prompt_log.csv`.
  Both rebuild automatically on the next launch.
- Seed step (needed for the typo tests): launch once → pick `1` → type `exit`.
  This creates `role_prompting/` so the fuzzy matcher has something to catch.

## Folder name reference

The CSV logs the display name; the folder gets the sanitized slug.

| Menu input | Experiment      | Folder created       |
|------------|-----------------|----------------------|
| Enter      | General         | `general`            |
| 1          | Role Prompting  | `role_prompting`     |
| 2          | Few-Shot        | `few-shot`           |
| 3          | Chain-of-Thought| `chain-of-thought`   |
| 4          | Structured Output| `structured_output` |
| 5          | General         | `general`            |
| 6          | Custom name     | sanitized input      |

---

## Session 1 — Startup gauntlet (input validation)

Launch the script and type these in order. No chatting needed.

- [ ] **1.1** Type `9` → `Invalid choice, try again.`
- [ ] **1.2** Type `x` → rejected again (non-digit path).
- [ ] **1.3** Type `6` → enters custom name mode.
- [ ] **1.4** Press Enter on the empty name → `Name can't be empty.`
- [ ] **1.5** Type `role_promting` (missing p) → `Found a similar experiment "role_prompting". Use it instead? (Y/N)` → answer `Y` → reuses the existing folder, no duplicate created.
- [ ] **1.6** At parameters type `n`, then for Temperature type `0..7` → `Invalid number, keeping 0.7` (old version crashed here).
- [ ] **1.7** Press Enter through every remaining parameter → each keeps its default.
- [ ] **1.8** Type `exit` → `Goodbye!`

---

## Session 2 — Experiment creation (one quick launch each)

Folders appear immediately at startup — pick the option, confirm the folder
exists in the sidebar, type `exit`. No chatting needed except 2.8.

- [ ] **2.1** Press Enter on the menu → `Experiment: General`, folder `general/` appears.
- [ ] **2.2** `6` → type `heist map ideas` → creates `heist_map_ideas/`, no similarity prompt (nothing similar exists), spaces become underscores.
- [ ] **2.3** `6` → type `My Cool Test!!` → folder `my_cool_test/` (punctuation stripped, lowercased).
- [ ] **2.4** `6` → type an Arabic name like `تجربة الأنماط` → folder `تجربة_الأنماط/` (unicode-safe).
- [ ] **2.5** `6` → type `role_promting` again, but answer `N` this time → creates the misspelled `role_promting/` folder. Your choice is respected — the shield suggests, never forces. Delete this folder afterwards.
- [ ] **2.6** `6` → type `general` (exact match to existing) → no "did you mean" prompt at all, silently reuses the folder.
- [ ] **2.7** Pick `1` when `role_prompting/` already exists → no error, folder reused as-is.
- [ ] **2.8** After Session 3 fills `few-shot/` with files 001–004: relaunch, pick `2`, send any save prompt → the new file is `005_...` (numbering scans the folder and continues, per experiment).

---

## Session 3 — Chat and save paths

Launch, pick `2` (Few-Shot), `Y` for default parameters. Paste in order.

### Test A — normal chat (control: no file, one CSV row)

```
What is the difference between a virus and a worm in one short paragraph?
```

- [ ] Reply printed as normal prose, `few-shot/` stays empty.

### Test B — PDF path → expect `001_*.pdf`

```
Summarize the following in 3 sentences and save it as a PDF: Phishing is a social engineering attack where criminals impersonate trusted organizations to steal credentials or money. A typical phishing email creates urgency, such as claiming an account will be suspended, and links to a fake login page that captures whatever the victim types. Spear phishing targets one specific person using details gathered from their social media, which makes it far more convincing than mass campaigns. Warning signs include mismatched sender addresses, generic greetings, unexpected attachments, and links whose real destination differs from the displayed text. Multi-factor authentication limits the damage because a stolen password alone is no longer enough to get into the account.
```

- [ ] `001_*.pdf` created, opens in the VS Code viewer, contains parameters + prompt + response.

### Test C — TXT path → expect `002_*.txt`, no PDF

```
Summarize this in 2 sentences and save it as a text file: Punching power comes mostly from the legs and hips rather than the arms. A powerful cross starts with the rear foot pivoting, transfers rotation through the hips and core, and only ends at the fist, which is why coaches say power travels from the ground up. Heavy bag work builds the ability to deliver force, while medicine ball throws and plyometric push-ups train the explosive speed that turns raw strength into knockout power. Skipping rope and roadwork keep the legs conditioned so power does not fade in the later rounds.
```

- [ ] `002_*.txt` only.

### Test D — "both" path + newline stress → expect a `003_` pdf AND txt pair

Bullet points force real newlines inside the JSON `content` — this is the
`strict=False` parser fix under load.

```
Summarize the following in 3 bullet points and save it as both a PDF and a text file: Few-shot prompting means showing a language model a handful of worked examples inside the prompt before asking it to handle a new case. Instead of describing the task in abstract rules, you demonstrate it: two or three input and output pairs teach the model the pattern, format, and tone you expect. This works because large models are strong pattern completers, so consistent examples constrain the output better than instructions alone. The main risks are that examples eat into the context window, and that a badly chosen example teaches the wrong pattern, which the model will copy faithfully. Zero-shot means no examples, one-shot means one, and few-shot typically means two to five.
```

- [ ] `003_*.pdf` and `003_*.txt` share the same number and sit next to each other.

### Test E — escape() stress → expect `004_*.pdf` (old code crashed here)

```
Summarize this in 2 sentences and save it as a PDF: In HTML, tags like <div> and <span> are used to group content, while a raw & symbol must be written as &amp; to display correctly. Browsers treat <img> and <br> as self-closing tags, and developers generally agree that readability improves when nesting depth stays < 5 levels and more than 90% of tags are properly closed.
```

- [ ] PDF created without a crash and renders cleanly despite `&`, `<`, `>`.

### Test F — false-positive trap (mentions PDF, requests nothing)

```
What does PDF actually stand for and who invented the format?
```

- [ ] Normal answer, zero new files. If llama3.2 outputs save-JSON here, that is a real finding: the system prompt needs tightening.

### Test G — unknown file_type branch

```
Summarize our conversation so far and save it as a Word document
```

- [ ] Likely `"file_type": "docx"` → `[!] Unknown file_type, nothing was saved.`
      Model-dependent: it may defensively pick pdf instead — retry once if so.

### Test H — conversation memory (two messages, sent separately)

```
My favorite hero in Marvel Rivals is Iron Fist, remember that
```

```
Which hero did I tell you is my favorite?
```

- [ ] Second answer says Iron Fist — history is flowing.

### Test I — JSON pollution check (send right after a save)

```
Now explain top_k in one single sentence
```

- [ ] Plain prose answer. The old code sometimes answered this in JSON because raw JSON sat in history; the history-swap fix prevents it.

### Test J — empty input, then quit

- [ ] Press Enter on an empty line → nothing happens: no model call, no CSV row.
- [ ] Type `exit` → `Goodbye!`

### Test K - Arabic prompt

```
أنشئ ملف PDF بعنوان "مقدمة في هندسة الأوامر (Prompt Engineering)".

يجب أن يحتوي على:
- تعريف هندسة الأوامر
- أهمية هندسة الأوامر
- تقنية Few-shot Prompting
- تقنية Role Prompting
- تقنية Chain of Thought
- أفضل الممارسات
- خاتمة قصيرة

استخدم عناوين ونقاط منظمة.
```

---

## Session 4 — Failure paths

- [ ] **4.1** Quit Ollama completely. Run the script, send `hello` → `[!] Could not reach Ollama: ...` and the script keeps running instead of crashing.
- [ ] **4.2** Start Ollama again, send `hello` in the SAME session → works, and the conversation is intact (`messages.pop()` kept history consistent).
- [ ] **4.3** *(optional, destructive)* Open `prompt_log.csv` in Excel and send a message → the script crashes with PermissionError, because Excel locks the file. Known limitation: view the CSV in VS Code during sessions, open Excel only afterwards.

---

## Final scoreboard

- [ ] `few-shot/` contains exactly: `001` (pdf), `002` (txt), `003` (pdf + txt pair), `004` (pdf).
- [ ] `general/`, `role_prompting/`, `heist_map_ideas/`, `my_cool_test/` exist; `role_promting/` deleted after 2.5.
- [ ] `prompt_log.csv` has one row per sent message — including F, G, H, I — and no row for the empty Enter (J).
- [ ] The Experiment column distinguishes rows from different experiments in the one shared CSV.
- [ ] No stray `saved_responses/` reappeared at the project root — the `BASE_DIR` fix is holding.