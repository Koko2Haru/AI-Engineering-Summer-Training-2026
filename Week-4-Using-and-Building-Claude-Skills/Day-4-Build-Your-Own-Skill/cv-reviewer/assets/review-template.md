# CV Review Report Template

Skeleton for the final report Claude produces. `{{double-brace}}` placeholders are filled in per review; section order and headers should not be reordered or renamed. See `report-example.md` for a fully worked version at the expected depth and tone.

The skeleton below renders as normal Markdown (no code fence) so its table structure displays correctly rather than as literal pipe characters. Its headings are nested one level deeper than the real report uses (`##` here where the real report uses `#`, etc.) purely so they sit correctly under this file's own title — when generating a real report, start back at `#`/`##`.

---

## CV Review: {{candidate_name_or_"Candidate"}}

**Overall Score: {{overall_score}}/100 — {{band_label}}**
**Reviewed as:** {{assumed_target_role_and_level}}
**One-line verdict:** {{one_sentence_verdict}}

### Score Summary

| Category | Score | Band |
|---|---|---|
| ATS Compatibility | {{score}}/100 | {{band}} |
| Content Quality | {{score}}/100 | {{band}} |
| Impact | {{score}}/100 | {{band}} |
| Grammar & Spelling | {{score}}/100 | {{band}} |
| Readability | {{score}}/100 | {{band}} |
| Visual / Layout | {{score}}/100 | {{band}} |
| Professionalism | {{score}}/100 | {{band}} |
| **Overall** | **{{overall_score}}/100** | **{{band}}** |

---

### Category Breakdown

#### ATS Compatibility — {{score}}/100
{{explanation}}

**Working well:** {{bullets}}
**Needs improvement:** {{bullets}}
**Evidence:** {{quoted excerpts}}

#### Content Quality — {{score}}/100
{{...same structure...}}

#### Impact — {{score}}/100
{{...same structure...}}

#### Grammar & Spelling — {{score}}/100
{{...same structure...}}

#### Readability — {{score}}/100
{{...same structure...}}

#### Visual / Layout — {{score}}/100
{{...same structure...}}

#### Professionalism — {{score}}/100
{{...same structure...}}

---

### Deep-Dive Analysis

#### Technical Skills Evaluation
{{assessment of breadth, depth, relevance, and currency of listed technical skills}}

#### Soft Skills Evaluation
{{assessment of evidence for communication, leadership, collaboration — should be evidence-based, not inferred from a "Soft Skills" list alone}}

#### Project Quality Analysis
{{assessment of any listed projects: complexity, relevance, ownership, outcomes}}

#### Experience Evaluation
{{assessment of career progression, scope growth, relevance to target role}}

#### Education Evaluation
{{assessment of relevance, completeness, and appropriate emphasis given career stage}}

#### Achievement Evaluation
{{assessment of awards/recognitions listed, or their notable absence}}

#### Keyword Optimization
{{if a job description was provided: table of required keywords vs. present/missing. If not: assessment against general industry norms for the target role}}

| Keyword | Present? | Notes |
|---|---|---|
| {{keyword}} | {{Yes/No}} | {{note}} |

#### Missing Sections
{{list of standard sections absent, with recommendation on whether to add them}}

#### Weak Bullet Points

| Original | Issue | Suggested Rewrite |
|---|---|---|
| {{quoted bullet}} | {{issue}} | {{rewrite}} |

#### Strong Bullet Points
{{quoted examples of what's already working well, and why}}

#### Repetitive Wording
{{words/phrases overused across the document, with counts}}

#### Action Verb Analysis
{{assessment of verb strength/variety; list of weak verbs/phrases found with locations}}

#### Quantification Analysis
{{proportion of bullets with numbers/metrics; which entries most need quantification added}}

---

### Recruiter & Hiring Manager Perspective

#### Recruiter First-Impression (6-Second Scan)
{{what a recruiter would notice/conclude in a first quick scan}}

#### Hiring Manager Read
{{would this resume earn a phone screen? why or why not?}}

#### Junior vs. Senior Appropriateness
{{does the level of language/scope match the candidate's actual career stage and the target role's level?}}

---

### Synthesis

#### Biggest Strengths
1. {{strength}}
2. {{strength}}
3. {{strength}}

#### Biggest Weaknesses
1. {{weakness}}
2. {{weakness}}
3. {{weakness}}

#### Top 10 Improvements (ordered by impact)
1. {{improvement}}
2. {{improvement}}
...
10. {{improvement}}

#### Quick Wins (high impact, low effort)
- {{quick win}}
- {{quick win}}
- {{quick win}}

#### Final Summary
{{2-4 sentence closing synthesis: overall hireability, what fixing the top issues would realistically do to the resume's performance}}
