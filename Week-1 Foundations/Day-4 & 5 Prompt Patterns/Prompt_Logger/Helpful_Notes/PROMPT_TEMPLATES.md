# Four Prompt Templates — Role, Few-Shot, Chain-of-Thought, Structured Output

A reference for the four prompt patterns, one per experiment folder in the
Prompt Logger. Each entry has: what it is, when to use it, the **template**
(placeholders in `{CURLY_CASE}`), a guide to every placeholder, a **filled test**
on a real problem, the **expected output**, and notes.

Placeholder convention: replace everything in `{BRACES}`. Leave the surrounding
structure intact — the structure is what makes the technique work.

How these map to your logger:

| Template | Run under experiment | Menu option |
|----------|---------------------|-------------|
| Role Prompting | Role Prompting | 1 |
| Few-Shot | Few-Shot | 2 |
| Chain-of-Thought | Chain-of-Thought | 3 |
| Structured Output | Structured Output | 4 |

---

## 1. Role Prompting

**What it is:** You assign the model a specific identity, expertise, audience, and
voice before giving the task. The persona shifts vocabulary, depth, assumptions,
and tone — a "senior security engineer explaining to a junior" produces a very
different answer than the same question asked cold.

**Best for:** explanations, reviews, advice, writing in a specific voice, anything
where *who is answering* and *who is listening* changes the ideal response.

**Anatomy:** identity → credentials → audience (and their level) → context → task →
behavioural guidelines → hard constraints → the actual question. Each part narrows
the space of acceptable answers.

### Template

```
You are {ROLE}, a {EXPERTISE_LEVEL} expert in {DOMAIN} with {YEARS} years of
hands-on experience specialising in {SPECIALTY}.

Your background:
- {CREDENTIAL_OR_ACHIEVEMENT_1}
- {CREDENTIAL_OR_ACHIEVEMENT_2}
- You are known for {SIGNATURE_STRENGTH}.

You are speaking to {AUDIENCE}, who {AUDIENCE_KNOWLEDGE_LEVEL}.

Context: {SITUATION_OR_BACKGROUND}

Your task: {TASK}

Guidelines:
- Tone: {TONE}.
- Depth: {DEPTH_LEVEL}.
- Always {DO_THIS}.
- Never {AVOID_THIS}.
- If {EDGE_CASE}, then {HOW_TO_HANDLE_IT}.
- Use {ANALOGY_OR_EXAMPLE_STYLE} to make ideas concrete.

Constraints:
- Keep the response under {WORD_LIMIT} words.
- Write the explanation in {LANGUAGE}.
- {EXTRA_FORMAT_RULE}.

Now respond to: {USER_QUESTION}
```

### Placeholder guide

- `{ROLE}` — the persona, e.g. "a senior application security engineer".
- `{EXPERTISE_LEVEL}` — junior / senior / world-class / veteran.
- `{DOMAIN}` / `{SPECIALTY}` — broad field / narrow focus (e.g. "web security" / "SQL injection defence").
- `{YEARS}` — years of experience; raises perceived authority and depth.
- `{CREDENTIAL_*}` — concrete achievements that bias the model toward practical, experienced answers.
- `{SIGNATURE_STRENGTH}` — what the persona is best at, e.g. "explaining hard ideas simply".
- `{AUDIENCE}` + `{AUDIENCE_KNOWLEDGE_LEVEL}` — the single most powerful lever; sets vocabulary and assumed knowledge.
- `{TONE}` / `{DEPTH_LEVEL}` — patient, blunt, encouraging / overview vs deep-dive.
- `{DO_THIS}` / `{AVOID_THIS}` — positive and negative behaviour, e.g. "define jargon on first use" / "never assume prior knowledge of databases".
- `{EDGE_CASE}` + `{HOW_TO_HANDLE_IT}` — a fallback rule for tricky inputs.
- `{WORD_LIMIT}`, `{LANGUAGE}`, `{EXTRA_FORMAT_RULE}` — hard output constraints.

### Test (filled)

```
You are a senior application security engineer, a veteran expert in web security
with 12 years of hands-on experience specialising in injection attacks.

Your background:
- You have run penetration tests for banks and e-commerce platforms.
- You have fixed hundreds of real SQL injection bugs in production code.
- You are known for explaining hard security ideas in plain language.

You are speaking to a junior backend developer, who can write basic SQL and
Python but has never studied security and does not know what an injection attack is.

Context: The junior just wrote a login query by gluing user input directly into
a SQL string, and asked you why that is dangerous.

Your task: Explain what SQL injection is, why their code is vulnerable, and how to
fix it.

Guidelines:
- Tone: patient and encouraging, never condescending.
- Depth: enough to fully understand the risk and the fix, no more.
- Always define a security term the first time you use it.
- Never assume they know database internals.
- If a real attack string would help, show a simple safe illustrative example.
- Use a concrete everyday analogy to make the core idea click.

Constraints:
- Keep the response under 300 words.
- Write the explanation in English.
- End with a one-line "golden rule" they can remember.

Now respond to: "Why is building my SQL query like
'SELECT * FROM users WHERE name = ' + username dangerous?"
```

### Expected output (shape of a good answer)

> Great question — this is one of the most important things to learn early.
>
> **SQL injection** is when an attacker types database commands into a normal
> input box (like a username field) and your code accidentally runs them.
>
> Think of your query as a sentence you're building: `... WHERE name = ` + whatever
> they typed. You *expect* a name. But nothing stops them typing
> `' OR '1'='1`. Now your sentence becomes `WHERE name = '' OR '1'='1'`, which is
> always true — so the database happily returns **every user**. Worse inputs can
> delete tables or read passwords.
>
> The analogy: it's like a form letter where you paste the reader's reply straight
> into the *instructions* section. If they write "ignore the address and mail this
> to me instead," the mailroom obeys.
>
> **The fix** is to never glue input into the query. Use *parameterised queries*
> (also called prepared statements), where the database treats input strictly as
> data, never as commands:
>
> `cursor.execute("SELECT * FROM users WHERE name = ?", (username,))`
>
> The `?` is a placeholder; the driver fills it in safely. Whatever they type stays
> a value — quotes and all — and can never change the query's meaning.
>
> **Golden rule:** never build a query by string concatenation — always pass user
> input as a parameter.

**Why it works:** the audience line forces beginner vocabulary; the "define jargon"
and "analogy" guidelines produce the form-letter metaphor; the constraints keep it
tight and give the memorable closer.

**Common mistake:** writing a rich persona but a vague audience. The audience is
what actually controls the answer — always specify their knowledge level.

---

## 2. Few-Shot Prompting

**What it is:** You show the model 2–5 worked examples (input → output) so it infers
the pattern, format, and tone, then you give it a fresh input to complete. You teach
by demonstration instead of description.

**Best for:** classification, extraction, consistent formatting, tagging, converting
between formats — any task where "do it like these" beats a paragraph of rules.

**Anatomy:** a one-line task cue → a fixed, repeated format → several examples that
cover the range of cases (including a tricky one) → the real input with the output
line left blank. Consistency across examples is everything: the model copies the
pattern you show, including any accidental sloppiness.

### Template

```
{BRIEF_TASK_INSTRUCTION}

Follow the exact format shown in the examples. Output only the {OUTPUT_LABEL} line.

Example 1:
{INPUT_LABEL}: {EXAMPLE_1_INPUT}
{OUTPUT_LABEL}: {EXAMPLE_1_OUTPUT}

Example 2:
{INPUT_LABEL}: {EXAMPLE_2_INPUT}
{OUTPUT_LABEL}: {EXAMPLE_2_OUTPUT}

Example 3:
{INPUT_LABEL}: {EXAMPLE_3_INPUT}
{OUTPUT_LABEL}: {EXAMPLE_3_OUTPUT}

Now complete the same task for this new input:
{INPUT_LABEL}: {ACTUAL_INPUT}
{OUTPUT_LABEL}:
```

### Placeholder guide

- `{BRIEF_TASK_INSTRUCTION}` — one sentence naming the task. Keep it short; the examples do the teaching.
- `{INPUT_LABEL}` / `{OUTPUT_LABEL}` — the repeated field names (e.g. `Message` / `Verdict`). Must be identical in every example.
- `{EXAMPLE_N_INPUT}` / `{EXAMPLE_N_OUTPUT}` — your demonstrations. Rules that matter:
  - Use **at least 3**, and make one of them a *hard* or *edge* case.
  - Keep the output format byte-for-byte consistent (same separators, same order, same casing).
  - Cover different output classes (don't show only "positive" examples).
- `{ACTUAL_INPUT}` — the real thing you want classified/converted. The blank output line signals the model to produce the same shape.

### Test (filled)

A phishing triage classifier — verdict, one-line reason, recommended action.

```
Classify each message as a phishing risk. Follow the exact format shown. Output
only the Verdict line.

Example 1:
Message: "Your account will be suspended in 24 hours. Verify now: http://paypa1-secure.tk"
Verdict: PHISHING | urgency pressure + lookalike domain (paypa1, .tk) | Do not click; report it

Example 2:
Message: "Hey, are we still on for lunch tomorrow at 1?"
Verdict: SAFE | personal message, no links or requests | No action needed

Example 3:
Message: "Congratulations! You won a $1000 gift card. Enter your card number to claim."
Verdict: PHISHING | too-good-to-be-true reward + asks for card details | Delete; never enter card details

Now complete the same task for this new input:
Message: "Your package could not be delivered. Pay a $2.99 redelivery fee and update your address: http://usps-redelivery.info"
Verdict:
```

### Expected output

```
PHISHING | fake delivery notice + small fee to lower suspicion + non-official domain | Do not pay; check tracking directly with the carrier
```

**Why it works:** three examples fix the `VERDICT | reason | action` shape and show
both classes, so the model reproduces the format exactly and reasons in the same
style. Note the small-fee tactic in the answer — the model generalised the
"manipulation tactic" pattern the examples taught.

**Common mistake:** all examples showing the same class, or inconsistent formatting
between examples. The model will copy whatever inconsistency you show it.

---

## 3. Chain-of-Thought (CoT)

**What it is:** You instruct the model to show its reasoning step by step *before*
the final answer. Forcing intermediate steps dramatically improves accuracy on
anything multi-step, because the model works the problem instead of guessing the
end in one leap.

**Best for:** math, logic, debugging, planning, estimates, security analysis — any
problem where a naive one-shot answer is often wrong.

**Anatomy:** frame the problem → list the givens → *explicitly* ask for numbered
reasoning → provide a step scaffold → demand a sanity check → separate the final
answer from the reasoning so it's easy to read and log.

### Template

```
You are solving a {PROBLEM_TYPE} problem. Work through it carefully and show ALL
of your reasoning before giving the final answer. Do not skip steps.

Problem:
{PROBLEM_STATEMENT}

Known information:
- {GIVEN_1}
- {GIVEN_2}
- {GIVEN_3}

Instructions:
1. Restate the goal in your own words.
2. Identify which information is relevant and note anything missing or assumed.
3. Break the problem into ordered steps.
4. Work through each step, showing every calculation or logical move.
5. Sanity-check the result against {SANITY_CHECK}.
6. State the final answer.

Format your response exactly as:

Reasoning:
<numbered step-by-step working>

Final Answer:
<the answer only, {ANSWER_FORMAT}>

Constraints: {CONSTRAINTS}
```

### Placeholder guide

- `{PROBLEM_TYPE}` — math / logic / estimation / debugging; primes the reasoning style.
- `{PROBLEM_STATEMENT}` — the question, stated fully.
- `{GIVEN_*}` — the known facts, one per line. Pulling them out reduces missed constraints.
- `{SANITY_CHECK}` — how to verify, e.g. "plug the answer back in" or "check the order of magnitude is reasonable". This catches errors.
- `{ANSWER_FORMAT}` — units/rounding for the final line, e.g. "rounded to 1 decimal place, with units".
- `{CONSTRAINTS}` — anything else, e.g. "state assumptions explicitly".

### Test (filled)

A password brute-force time estimate — a classic case where skipping steps gives
a wildly wrong answer.

```
You are solving a math problem. Work through it carefully and show ALL of your
reasoning before giving the final answer. Do not skip steps.

Problem:
Estimate how long it would take an attacker to brute-force a password by trying
every possible combination.

Known information:
- The password is exactly 8 characters long.
- Each character can be a lowercase letter, an uppercase letter, or a digit.
- The attacker can test 1,000,000,000 (one billion) guesses per second.
- Assume the worst case: the attacker must try the entire keyspace.

Instructions:
1. Restate the goal in your own words.
2. Identify which information is relevant and note anything assumed.
3. Break the problem into ordered steps.
4. Work through each step, showing every calculation.
5. Sanity-check the result against a reasonable order of magnitude.
6. State the final answer.

Format your response exactly as:

Reasoning:
<numbered step-by-step working>

Final Answer:
<the answer only, in days, rounded to 1 decimal place>

Constraints: State any assumption you make.
```

### Expected output

> Reasoning:
> 1. Goal: find the time to try every possible 8-character password at a fixed
>    guess rate.
> 2. Relevant: character set size, length, guesses/sec. Assumption: worst case =
>    full keyspace searched.
> 3. Steps: (a) count the characters in the set, (b) raise to the 8th power for the
>    total combinations, (c) divide by guesses/sec for seconds, (d) convert to days.
> 4. Working:
>    (a) 26 lowercase + 26 uppercase + 10 digits = 62 possible characters.
>    (b) Combinations = 62^8 = 218,340,105,584,896 (~2.18 × 10^14).
>    (c) Seconds = 2.18340 × 10^14 ÷ 1 × 10^9 = 218,340 seconds.
>    (d) Days = 218,340 ÷ 86,400 ≈ 2.527 days.
> 5. Sanity check: ~2×10^14 combinations at 10^9/sec ≈ 2×10^5 seconds ≈ a couple of
>    days. Order of magnitude looks right.
>
> Final Answer:
> 2.5 days

**Why it works:** the numbered scaffold makes the model compute `62^8` explicitly
instead of guessing; the sanity-check step catches magnitude errors; separating the
final answer makes it trivial to read and log. (Real attackers average *half* the
keyspace, so expected time ≈ 1.3 days — a natural follow-up prompt.)

**Common mistake:** asking for reasoning but letting the answer come first. Put the
reasoning *before* the final answer, or you lose most of the accuracy benefit.

---

## 4. Structured Output

**What it is:** You force the response into a strict machine-readable schema (JSON
here) so a program can parse it. You define every field, its type, and the rules,
then forbid any prose around it.

**Best for:** anything a program will consume — data extraction, tagging, API-style
responses, and (directly relevant to you) the save-file mechanism in your logger.

**Anatomy:** task → the exact schema with field names, types, and per-field
descriptions → hard rules (valid JSON only, no prose, no code fences, enum
constraints, defaults) → the input to process.

### Template

```
{TASK_DESCRIPTION}

Respond with ONLY a valid JSON object matching the schema below. Output nothing
before or after the JSON. Do not wrap it in markdown code fences.

Schema:
{
  "{FIELD_1}": {TYPE_1},         // {DESCRIPTION_1}
  "{FIELD_2}": {TYPE_2},         // {DESCRIPTION_2}; must be one of: {ENUM_VALUES}
  "{FIELD_3}": [{ITEM_TYPE}],    // {DESCRIPTION_3}; a list
  "{FIELD_4}": {TYPE_4}          // {DESCRIPTION_4}; optional, default {DEFAULT}
}

Rules:
- Output must be valid JSON and parseable as-is.
- All string values must be written in {LANGUAGE}.
- "{FIELD_2}" must be exactly one of the allowed values, lowercase.
- If {CONDITION}, set "{FIELD_X}" to {FALLBACK}.
- Numbers must be {NUMBER_CONSTRAINT}.

Input to analyse:
{INPUT_DATA}
```

### Placeholder guide

- `{TASK_DESCRIPTION}` — what to produce from the input.
- `{FIELD_N}` / `{TYPE_N}` — the key name and its JSON type (string, number, boolean, array).
- `{DESCRIPTION_N}` — a short comment telling the model what goes in each field. This is what makes structured output reliable — describe every field.
- `{ENUM_VALUES}` — the closed set a field may take (e.g. `low, medium, high, critical`). Enums stop free-text drift.
- `{DEFAULT}` / `{CONDITION}` / `{FALLBACK}` — how to handle optional or missing data so the shape is always valid.
- `{NUMBER_CONSTRAINT}` — e.g. "between 0 and 10, one decimal".
- `{INPUT_DATA}` — the raw text to analyse.

### Test (filled)

Turning a plain-language vulnerability description into a structured triage record.

```
You are a security triage assistant. Convert the vulnerability description into a
structured record.

Respond with ONLY a valid JSON object matching the schema below. Output nothing
before or after the JSON. Do not wrap it in markdown code fences.

Schema:
{
  "vulnerability": string,            // short name of the flaw
  "severity": string,                 // one of: low, medium, high, critical
  "category": string,                 // e.g. injection, auth, misconfiguration
  "affected_component": string,       // where the flaw lives
  "cwe_id": string,                   // the CWE identifier if known, else "unknown"
  "remediation": [string],            // concrete fix steps, most important first
  "exploitable_without_auth": boolean // true if no login is needed to exploit
}

Rules:
- Output must be valid JSON and parseable as-is.
- All string values must be written in English.
- "severity" must be exactly one of the allowed values, lowercase.
- If the CWE is unknown, set "cwe_id" to "unknown".

Input to analyse:
A public web login form takes a username and builds its SQL query by string
concatenation: "SELECT * FROM users WHERE name = '" + username + "'". There is no
input validation or escaping, and the endpoint requires no authentication.
```

### Expected output

```json
{
  "vulnerability": "SQL Injection",
  "severity": "critical",
  "category": "injection",
  "affected_component": "public web login form",
  "cwe_id": "CWE-89",
  "remediation": [
    "Replace string concatenation with parameterised queries (prepared statements)",
    "Add server-side input validation",
    "Run the database connection under a least-privilege account"
  ],
  "exploitable_without_auth": true
}
```

**Why it works:** each field has a description, so the model knows exactly what to
put where; the `severity` enum prevents made-up values like "very high"; the "no
fences, no prose" rule makes the output parse on the first try.

**Common mistake:** defining field names but not describing them, or allowing
free-text where an enum belongs. Undescribed fields get filled inconsistently.

---

## Testing these in your logger — one thing to know

Your logger's system prompt tells the model to emit JSON **only when asked to save
a file**, and `parse_json_response()` checks for `"save": true`.

- Templates 1–3 return normal prose → printed and logged as usual.
- **Template 4 returns JSON with no `"save"` key.** So `parse_json_response()` will
  parse it, but `data.get("save")` is falsy → it prints as a normal message and
  writes **no file**. That's correct and expected: you'll see the JSON in the
  terminal and in the CSV, but the folder stays empty. If you *want* Template 4's
  JSON saved as a document, add `"save": true` and `"file_type"` to its schema.

Run each template under its matching experiment folder, try one with `llama3.2`
and one with `qwen2.5:7b`, and your CSV becomes a clean side-by-side record of how
each pattern behaves per model — which is exactly the kind of evidence a Day-4
write-up wants.