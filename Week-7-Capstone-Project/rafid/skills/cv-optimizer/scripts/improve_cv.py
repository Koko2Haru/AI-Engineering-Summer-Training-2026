#!/usr/bin/env python3
"""
End-to-end gap-scan orchestrator for the CV Optimizer skill.

Ties rewrite_bullets.py + ats_optimizer.py + formatting_helper.py (and,
optionally, optimize_keywords.py when a job description is supplied)
into one mechanical pass over a resume, then ranks the findings using
the severity weights in assets/improvement-priorities.json.

This exists for the case described in SKILL.md step 3 / Input Expectations:
when no cv-reviewer output is available, this script produces the priority
queue that review output would otherwise have supplied. It is a mechanical
first pass, not a substitute for the judgment-driven rewrite itself -
several things (whether a rewrite crosses the fabrication line, what a
clarifying question should ask, whether a placeholder is warranted) still
require the reasoning in references/rewriting-guidelines.md.

Usage:
    python3 improve_cv.py <path/to/extracted_text.txt> [--jd <path/to/job_description.txt>]

Output: a JSON object with mechanical findings and a severity-ranked issue
list, intended to be read by Claude as an input to the rewrite workflow -
not printed directly to the end user as the final output.
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import rewrite_bullets  # noqa: E402
import ats_optimizer  # noqa: E402
import formatting_helper  # noqa: E402


def load_priorities() -> dict:
    path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "assets", "improvement-priorities.json"
    )
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_issue_queue(bullets: dict, ats: dict, formatting: dict, priorities: dict) -> list:
    """
    Flattens findings from every mechanical check into one list of
    {issue_type, severity, detail} entries, ordered by severity weight
    from assets/improvement-priorities.json. Ties are broken by the order
    issues were discovered (bullets -> ATS -> formatting), which is also
    roughly the rewrite-pass order in references/rewriting-guidelines.md.
    """
    severity_rank = {item["key"]: item["rank"] for item in priorities["severity_levels"]}
    issue_severity = {item["issue_type"]: item["severity"] for item in priorities["issue_types"]}

    issues = []

    if ats["sections_missing"]:
        issues.append({
            "issue_type": "missing_standard_section",
            "severity": issue_severity.get("missing_standard_section", "high"),
            "detail": f"Missing section(s): {', '.join(ats['sections_missing'])}",
        })

    if ats["non_standard_headers"]:
        issues.append({
            "issue_type": "non_standard_section_header",
            "severity": issue_severity.get("non_standard_section_header", "medium"),
            "detail": ats["non_standard_headers"],
        })

    if ats["contact_info"]["flag"]:
        issues.append({
            "issue_type": "contact_info_placement",
            "severity": issue_severity.get("contact_info_placement", "critical"),
            "detail": ats["contact_info"]["flag"],
        })

    if ats["date_format_consistency"]["inconsistent"]:
        issues.append({
            "issue_type": "inconsistent_date_format",
            "severity": issue_severity.get("inconsistent_date_format", "medium"),
            "detail": ats["date_format_consistency"]["formats_in_use"],
        })

    if bullets["bullets_needing_work"]:
        issues.append({
            "issue_type": "weak_or_unquantified_bullets",
            "severity": issue_severity.get("weak_or_unquantified_bullets", "high"),
            "detail": f"{bullets['bullets_needing_work']} of {bullets['bullet_count']} "
                      f"bullets flagged (weak phrasing, no quantification, passive voice, "
                      f"or unsupported intensifiers).",
        })

    if bullets["repeated_opening_verbs"]:
        issues.append({
            "issue_type": "repetitive_verbs",
            "severity": issue_severity.get("repetitive_verbs", "medium"),
            "detail": bullets["repeated_opening_verbs"],
        })

    if formatting["bullet_chars"]["inconsistent"]:
        issues.append({
            "issue_type": "inconsistent_bullet_characters",
            "severity": issue_severity.get("inconsistent_bullet_characters", "low"),
            "detail": formatting["bullet_chars"]["bullet_char_counts"],
        })

    if formatting["spacing"]["inconsistent"]:
        issues.append({
            "issue_type": "inconsistent_spacing",
            "severity": issue_severity.get("inconsistent_spacing", "low"),
            "detail": formatting["spacing"]["blank_line_run_counts"],
        })

    issues.sort(key=lambda i: severity_rank.get(i["severity"], 99))
    return issues


def build_report(resume_path: str, jd_path: str = None) -> dict:
    with open(resume_path, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()

    priorities = load_priorities()
    bullets = rewrite_bullets.analyze(text)
    ats = ats_optimizer.analyze(text)
    formatting = formatting_helper.analyze(text)

    report = {
        "bullet_analysis": bullets,
        "ats_analysis": ats,
        "formatting_analysis": formatting,
        "priority_queue": build_issue_queue(bullets, ats, formatting, priorities),
    }

    if jd_path:
        import optimize_keywords  # noqa: E402
        with open(jd_path, "r", encoding="utf-8", errors="replace") as f:
            jd_text = f.read()
        keywords = optimize_keywords.extract_candidate_terms(jd_text)
        report["keyword_analysis"] = {
            "candidate_keywords": keywords,
            "coverage": optimize_keywords.coverage(text, keywords),
        }

    return report


def main():
    args = sys.argv[1:]
    if not args:
        print(
            "Usage: python3 improve_cv.py <path/to/extracted_text.txt> [--jd <path/to/job_description.txt>]",
            file=sys.stderr,
        )
        sys.exit(1)

    resume_path = args[0]
    jd_path = None
    if "--jd" in args:
        jd_index = args.index("--jd")
        if jd_index + 1 >= len(args):
            print("Missing path after --jd", file=sys.stderr)
            sys.exit(1)
        jd_path = args[jd_index + 1]

    try:
        report = build_report(resume_path, jd_path)
    except (FileNotFoundError, ValueError, RuntimeError) as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
