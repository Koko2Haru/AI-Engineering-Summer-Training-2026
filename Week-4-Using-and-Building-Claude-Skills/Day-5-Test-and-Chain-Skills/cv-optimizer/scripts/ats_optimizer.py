#!/usr/bin/env python3
"""
Structural ATS issue detector for the CV Optimizer skill's ATS pass.

Checks extracted resume text against the structural rules in
references/ats-optimization.md: standard section headers, contact info
presence in the main body, date-format consistency, and non-standard
header names. Emits a list of fixes to apply, each mapped to a concrete
action from that reference - this script flags issues, it does not itself
decide wording, since the fix action is deterministic once the issue type
is known.

No third-party dependencies - stdlib only, so this always runs.

Usage:
    python3 ats_optimizer.py <path/to/extracted_text.txt>
"""

import re
import sys
import json

STANDARD_SECTION_PATTERNS = {
    "experience": [r"experience", r"employment history", r"work history"],
    "education": [r"education"],
    "skills": [r"skills?", r"technical skills", r"core competencies"],
    "summary": [r"summary", r"objective", r"profile"],
    "projects": [r"projects?"],
    "certifications": [r"certifications?", r"licenses?"],
}

NON_STANDARD_HEADER_MAP = {
    r"my journey": "Experience",
    r"career story": "Experience",
    r"where i.?ve been": "Experience",
    r"what i bring": "Skills",
    r"superpowers": "Skills",
    r"learning": "Education",
}

EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE_RE = re.compile(r"(\+?\d{1,2}[\s.-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}")

DATE_FORMAT_PATTERNS = {
    "mon_yyyy": re.compile(r"\b[A-Z][a-z]{2}\.?\s+\d{4}\b"),
    "mm_yyyy_slash": re.compile(r"\b\d{1,2}/\d{4}\b"),
    "full_month_yyyy": re.compile(r"\b(January|February|March|April|May|June|July|"
                                   r"August|September|October|November|December)\s+\d{4}\b"),
    "yyyy_only": re.compile(r"(?<!\d)\d{4}(?!\d)"),
}


def detect_sections(text: str) -> dict:
    found = {}
    for i, line in enumerate(text.splitlines()):
        stripped = line.strip()
        if not stripped or len(stripped) > 40:
            continue
        normalized = stripped.lower().strip(":")
        for section, patterns in STANDARD_SECTION_PATTERNS.items():
            if section in found:
                continue
            for pattern in patterns:
                if re.fullmatch(pattern, normalized) or re.match(rf"^{pattern}\b", normalized):
                    found[section] = i
    return found


def find_non_standard_headers(text: str) -> list:
    hits = []
    for i, line in enumerate(text.splitlines()):
        stripped = line.strip()
        if not stripped or len(stripped) > 40:
            continue
        for pattern, replacement in NON_STANDARD_HEADER_MAP.items():
            if re.search(pattern, stripped, re.IGNORECASE):
                hits.append({
                    "line_number": i,
                    "original": stripped,
                    "suggested_replacement": replacement,
                })
    return hits


def date_format_consistency(text: str) -> dict:
    counts = {name: len(pattern.findall(text)) for name, pattern in DATE_FORMAT_PATTERNS.items()}
    formats_in_use = [name for name, count in counts.items() if count > 0]
    return {
        "format_counts": counts,
        "inconsistent": len(formats_in_use) > 1,
        "formats_in_use": formats_in_use,
    }


def contact_info_check(text: str) -> dict:
    lines = text.splitlines()
    top_block = "\n".join(lines[:8])
    has_email_top = bool(EMAIL_RE.search(top_block))
    has_email_anywhere = bool(EMAIL_RE.search(text))
    return {
        "has_email_anywhere": has_email_anywhere,
        "has_email_in_top_block": has_email_top,
        "has_phone_anywhere": bool(PHONE_RE.search(text)),
        "flag": (
            "Email detected but not near the top of the document - may be in a "
            "header/footer or buried; move contact info to the main body under "
            "the candidate's name."
            if has_email_anywhere and not has_email_top
            else None
        ),
    }


def analyze(text: str) -> dict:
    sections = detect_sections(text)
    missing = [s for s in ("experience", "education", "skills") if s not in sections]
    return {
        "sections_found": list(sections.keys()),
        "sections_missing": missing,
        "non_standard_headers": find_non_standard_headers(text),
        "date_format_consistency": date_format_consistency(text),
        "contact_info": contact_info_check(text),
    }


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 ats_optimizer.py <path/to/extracted_text.txt>", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1], "r", encoding="utf-8", errors="replace") as f:
        text = f.read()

    print(json.dumps(analyze(text), indent=2))


if __name__ == "__main__":
    main()
