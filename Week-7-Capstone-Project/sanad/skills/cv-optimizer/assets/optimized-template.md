# Optimized Resume Template

Skeleton for the rewritten resume Claude produces. `{{double-brace}}` placeholders are filled in per rewrite; `[single-bracket]` items are the visible in-resume placeholder convention from `references/rewriting-guidelines.md` for genuinely missing information — the two bracket styles serve different purposes and should not be confused when generating real output.

The skeleton below renders as normal Markdown (no code fence) so it displays correctly rather than as literal pipe/heading characters. Its headings are nested one level deeper than the real resume uses (`##` here where the real resume uses `#`, etc.) purely so it sits correctly under this file's own title — when generating the real Optimized Resume, start back at `#`/`##`, and do **not** wrap it in a code fence.

---

## {{Candidate Name}}

{{Phone}} | {{Email}} | {{City, State / Remote}} | {{LinkedIn}} | {{GitHub/Portfolio}}

### Summary

{{2-4 line summary: role/specialization, years of relevant experience if it strengthens the read, 1-2 standout areas of real impact — every claim traceable to the source CV or a clarification answer. Omit this whole section if it doesn't add signal at the candidate's career stage.}}

### Experience

**{{Job Title}}** — {{Company Name}}
{{Mon YYYY}} – {{Mon YYYY / Present}} | {{Location, if in source}}
- {{Rewritten bullet: strong verb + what was done + quantified result if available + method if space allows}}
- {{Rewritten bullet}}
- {{Rewritten bullet, or a visible placeholder: [Consider adding a measurable outcome here — e.g., % improvement, users affected, time saved.]}}

**{{Job Title}}** — {{Company Name}}
{{Mon YYYY}} – {{Mon YYYY}}
- {{...same structure...}}

### Projects

**{{Project Name}}** {{— link, if available}}
- {{What it does, technologies used, candidate's specific contribution, and outcome — or a placeholder if the outcome wasn't provided: [Provide the project's outcome if available.]}}

### Education

**{{Degree}}**, {{Institution}} — {{Graduation Date}}
{{GPA/coursework/honors, only if it adds signal at this career stage}}

### Skills

{{Category 1 (e.g. Languages)}}: {{comma-separated list, every item traceable to the source CV}}
{{Category 2 (e.g. Frameworks)}}: {{...}}
{{Category 3 (e.g. Tools/Infrastructure)}}: {{...}}

### Certifications

- {{Certification Name}} — {{Issuing Body}}, {{Date}}

### Awards / Leadership / Volunteer

{{Include only sections that add genuine signal; apply the same bullet formula as Experience — see references/achievement-writing.md}}

---

**Note below the resume, every time:** if any `[bracketed placeholder]` remains in the document above, say so explicitly and point to the Change Report's "Suggestions Requiring User Input" section — never let a placeholder pass silently as if it were finished, submit-ready text.
