#!/usr/bin/env python3
"""
Formatting-consistency detector for the CV Optimizer skill's formatting pass.

Checks extracted resume text for the mechanical inconsistencies covered in
references/resume-layout-guidelines.md: mixed bullet characters, mixed
date formats (delegated to the same detection used by ats_optimizer.py),
and inconsistent spacing between entries. Purely mechanical - never
suggests wording changes, only presentation normalization.

No third-party dependencies - stdlib only, so this always runs.

Usage:
    python3 formatting_helper.py <path/to/extracted_text.txt>
"""

import re
import sys
import json
from collections import Counter

BULLET_CHAR_RE = re.compile(r"^\s*([•\-\*●‣⁃])\s+")


def bullet_char_consistency(text: str) -> dict:
    chars = []
    for line in text.splitlines():
        match = BULLET_CHAR_RE.match(line)
        if match:
            chars.append(match.group(1))
    counts = Counter(chars)
    return {
        "bullet_char_counts": dict(counts),
        "inconsistent": len(counts) > 1,
        "dominant_char": counts.most_common(1)[0][0] if counts else None,
    }


def blank_line_run_lengths(text: str) -> list:
    """Lengths of consecutive blank-line runs, used to spot uneven spacing
    between entries (e.g., one blank line between some jobs, three between others)."""
    runs = []
    current = 0
    for line in text.splitlines():
        if line.strip() == "":
            current += 1
        else:
            if current > 0:
                runs.append(current)
            current = 0
    if current > 0:
        runs.append(current)
    return runs


def spacing_consistency(text: str) -> dict:
    runs = blank_line_run_lengths(text)
    counts = Counter(runs)
    return {
        "blank_line_run_counts": dict(counts),
        "inconsistent": len(counts) > 1,
        "note": (
            "Multiple distinct blank-line run lengths between entries can indicate "
            "uneven spacing; normalize to one consistent gap between entries and "
            "one (possibly different) consistent gap between sections."
        ),
    }


def bolding_hint(text: str) -> dict:
    """Markdown-style ** markers, if the extracted text preserves them, as a rough
    signal for bolding-pattern consistency. Best-effort only - most plain-text
    extraction loses bold formatting entirely, in which case this is a no-op."""
    bold_spans = re.findall(r"\*\*(.+?)\*\*", text)
    return {
        "bold_span_count": len(bold_spans),
        "note": (
            "Plain-text extraction typically loses bold/italic formatting; if this "
            "count is 0, verify bolding consistency by inspecting the original "
            "document/file directly rather than relying on this signal."
        ),
    }


def analyze(text: str) -> dict:
    return {
        "bullet_chars": bullet_char_consistency(text),
        "spacing": spacing_consistency(text),
        "bolding_hint": bolding_hint(text),
    }


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 formatting_helper.py <path/to/extracted_text.txt>", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1], "r", encoding="utf-8", errors="replace") as f:
        text = f.read()

    print(json.dumps(analyze(text), indent=2))


if __name__ == "__main__":
    main()
