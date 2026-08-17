#!/usr/bin/env python3
"""
Bullet-level flagging for the CV Optimizer skill's bullet pass.

Scans extracted resume text for bullet lines and flags, per bullet: weak
verbs/phrases, first-person pronouns, missing quantification, and passive
voice signals. This is a mechanical *flagging* pass, not a rewriter - it
tells Claude where a bullet needs work and why, per references/rewriting-
guidelines.md and references/achievement-writing.md; the actual rewrite
still requires judgment about what the underlying fact supports, which
this script cannot know.

No third-party dependencies - stdlib only, so this always runs.

Usage:
    python3 rewrite_bullets.py <path/to/extracted_text.txt>
"""

import re
import json
import sys

BULLET_LINE_RE = re.compile(r"^\s*[•\-\*●‣⁃]\s*(.+)$")

WEAK_PHRASES = [
    "responsible for",
    "helped with",
    "assisted with",
    "worked on",
    "involved in",
    "duties included",
    "tasked with",
    "participated in",
]

WEAK_VERBS = [
    "did", "made", "used", "handled", "dealt with",
    "was in charge of", "got", "gave", "took care of",
]

INTENSIFIER_RE = re.compile(
    r"\b(significantly|dramatically|greatly|substantially|considerably|"
    r"vastly|hugely)\b",
    re.IGNORECASE,
)
# Flags "sounds-quantified-but-isn't" filler - see references/achievement-writing.md
# "Common Trap: Confusing Confidence with Fabrication".

QUANTIFICATION_RE = re.compile(
    r"(\d+(\.\d+)?%|\$\d[\d,]*(\.\d+)?[kKmMbB]?|\b\d+(\.\d+)?[xX]\b|"
    r"\b\d[\d,]*\+?\s*(users|customers|engineers|people|team members|"
    r"requests|records|clients|projects|hours|days|weeks|months|years)\b|"
    r"\b\d[\d,]*\+?\b)"
)

FIRST_PERSON_RE = re.compile(r"\b(I|my|me)\b", re.IGNORECASE)

PASSIVE_RE = re.compile(
    r"\b(was|were|is|are|been|being)\s+\w+ed\b", re.IGNORECASE
)


def extract_bullets(text: str) -> list:
    """Pull out lines that look like bullet points."""
    bullets = []
    for i, line in enumerate(text.splitlines()):
        match = BULLET_LINE_RE.match(line)
        if match:
            bullets.append({"line_number": i, "text": match.group(1).strip()})
    return bullets


def opening_verb(bullet: str) -> str:
    words = re.findall(r"[A-Za-z']+", bullet)
    return words[0] if words else ""


def flag_bullet(bullet_text: str) -> dict:
    lower = bullet_text.lower()
    flags = []

    weak_hits = [p for p in WEAK_PHRASES if p in lower]
    if weak_hits:
        flags.append({"type": "weak_phrase", "detail": weak_hits})

    weak_verb_hits = [v for v in WEAK_VERBS if v in lower]
    if weak_verb_hits:
        flags.append({"type": "weak_verb", "detail": weak_verb_hits})

    if not QUANTIFICATION_RE.search(bullet_text):
        flags.append({
            "type": "missing_quantification",
            "detail": "No number/metric detected - candidate for a clarifying "
                       "question or a bracketed placeholder per "
                       "references/rewriting-guidelines.md.",
        })

    if FIRST_PERSON_RE.search(bullet_text):
        flags.append({"type": "first_person", "detail": "Drop the implied first-person pronoun."})

    if PASSIVE_RE.search(bullet_text):
        flags.append({"type": "possible_passive_voice", "detail": "Consider active voice."})

    if INTENSIFIER_RE.search(bullet_text):
        flags.append({
            "type": "unsupported_intensifier",
            "detail": "Vague intensifier with no real number behind it - "
                       "replace with an actual metric or a concrete outcome.",
        })

    return {"text": bullet_text, "flags": flags, "opening_verb": opening_verb(bullet_text)}


def repeated_opening_verbs(flagged_bullets: list, min_count: int = 3) -> dict:
    from collections import Counter
    verbs = [b["opening_verb"].lower() for b in flagged_bullets if b["opening_verb"]]
    counts = Counter(verbs)
    return {v: c for v, c in counts.items() if c >= min_count}


def analyze(text: str) -> dict:
    bullets = extract_bullets(text)
    flagged = [flag_bullet(b["text"]) for b in bullets]
    needs_work = [b for b in flagged if b["flags"]]
    return {
        "bullet_count": len(bullets),
        "bullets_needing_work": len(needs_work),
        "flagged_bullets": needs_work,
        "repeated_opening_verbs": repeated_opening_verbs(flagged),
    }


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 rewrite_bullets.py <path/to/extracted_text.txt>", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1], "r", encoding="utf-8", errors="replace") as f:
        text = f.read()

    print(json.dumps(analyze(text), indent=2))


if __name__ == "__main__":
    main()
