---
name: {{skill-name-kebab-case}}
description: {{One or two sentences: what this skill does, plus the concrete phrases/situations that should trigger it. Description quality IS trigger quality — the model only sees this line before deciding whether to load the rest.}}
---

<!--
ANNOTATION — Progressive disclosure, Level 1:
The frontmatter above (name + description) is the ONLY part of this file loaded
into context by default, for every skill in the project, all the time. It has to
be cheap to keep around and specific enough to match real phrasing. Everything
below this comment is Level 2 — it loads only once this skill is selected. Files
in references/, scripts/, assets/ are Level 3 — they load only when explicitly
needed. Keep that cost gradient in mind for every section that follows: nothing
below should need to be in the frontmatter, and nothing in references/ should
need to be inlined here.
-->

# {{Skill Display Name}}

{{One-sentence tagline: what this skill does and why it's worth having as a packaged skill instead of an ad-hoc prompt.}}

<!--
ANNOTATION — Why this exists at all:
Before writing anything below, answer: what goes wrong without this skill? Inconsistent
scoring across runs? Reinventing the same multi-step process each time? Forgetting a
step under time pressure? If the answer is "nothing, really" — this doesn't need to be
a skill, it can just be a good prompt. Skills earn their overhead by encoding something
that's easy to get wrong or expensive to re-derive from scratch every conversation.
-->

## Purpose

{{2-4 sentences: the problem this skill solves, and what "good" looks like when it works.}}

## When This Skill Should Trigger

<!--
ANNOTATION:
Be concrete, not topical. "Review my resume" / "will this pass ATS" beats a vague
label like "resume-related requests" — the model matches against actual phrasing,
not category names. List situations, not keywords.
-->

- {{Concrete situation #1 — quote realistic phrasing a user might actually type}}
- {{Concrete situation #2}}
- {{Concrete situation #3}}

## When It Should NOT Trigger

<!--
ANNOTATION:
Just as important as the trigger list — this is what stops the skill from firing
on everything adjacent to its topic and producing shallow, over-general answers.
Name the specific nearby request that looks similar but isn't the same task.
-->

- {{A nearby but out-of-scope request — explain what to do instead}}
- {{A narrow single-fact question that doesn't need the full workflow — answer it directly instead}}

## Input Expectations

{{What form(s) can input take? Pasted text, a file path, multiple files, an optional secondary input (e.g. a job description alongside a resume)? What's the minimum needed to proceed, and what should Claude do — ask, or assume and state the assumption — if something's missing?}}

## Output Format

{{What should the final output look like — structure, tone, tables vs. prose? If a template file exists in assets/, point to it here by name rather than repeating its structure inline.}}

<!--
ANNOTATION — learned the hard way on Day 4 (see ../../Day-4-Build-Your-Own-Skill/DAY4-REPORT.md):
If assets/ holds a worked example with tables or headings, do NOT wrap that example in
a code fence unless this file ALSO says explicitly, in plain language, that the fence is
a documentation convention for that reference file — not an instruction to reproduce.
Otherwise the model can plausibly copy the fence into the real output, flattening every
table into literal pipe-delimited text. State rendering intent explicitly; don't assume
it's obvious from context.
-->

## Instructions for Claude

### Workflow

1. {{Step one}}
2. {{Step two}}
3. {{Step three — note if a later step depends on a fact gathered in an earlier one; say so explicitly if order matters}}

### Edge Cases

- {{An input shape that's technically valid but unusual — how should Claude handle it rather than silently guessing?}}
- {{A case where the honest answer is "I don't have enough information" — say what to do instead of forcing an answer}}

### Constraints

- {{Something Claude must never do — e.g., never fabricate data the input doesn't contain}}
- {{A quality bar that must never be skipped even under time pressure}}

## File Usage

<!--
ANNOTATION:
This table is the single biggest lever for progressive disclosure discipline. If Claude
would have to guess when to open a given reference/script/asset file, the file was named
or organized wrong. Name files by what they contain, and state the trigger condition for
opening them explicitly, right here — don't make the model infer it.
-->

| Path | Purpose | When to consult |
|---|---|---|
| `references/{{name}}.md` | {{what knowledge or rules it holds}} | {{the specific moment in the workflow to read it}} |
| `scripts/{{name}}.py` | {{what it computes or extracts}} | {{when to run it, and what to do if it's unavailable}} |
| `assets/{{name}}` | {{template, example, or config it provides}} | {{when to use it}} |

## Best Practices

- {{A habit that consistently produces better output — stated as a rule, not a vague aspiration}}

## Failure Handling

- {{What input/tool failure is most likely, and what Claude should say/do instead of guessing or failing silently}}
