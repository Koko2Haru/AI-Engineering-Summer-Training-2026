#!/usr/bin/env python3
"""
Shared analysis helpers for the CV Reviewer skill.

These formalize the heuristics described in SKILL.md and the references/
directory into reusable functions: section detection, bullet splitting,
quantification detection, weak-phrase/verb detection, and repetition
analysis. review_cv.py composes these into a full report; they're also
useful to run standalone against a large or ambiguous document to get a
quick, mechanical first pass before writing the narrative review.

No third-party dependencies - stdlib only, so this always runs.
"""

import re
from collections import Counter

# ---------------------------------------------------------------------------
# Section detection
# ---------------------------------------------------------------------------

SECTION_HEADER_PATTERNS = {
    "contact_info": [],  # inferred, not header-matched - see detect_contact_info
    "summary": [r"summary", r"objective", r"profile"],
    "experience": [r"experience", r"employment history", r"work history"],
    "projects": [r"projects?"],
    "education": [r"education"],
    "skills": [r"skills?", r"technical skills", r"core competencies"],
    "certifications": [r"certifications?", r"licenses?"],
    "achievements": [r"achievements?", r"awards?", r"honou?rs"],
}

EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE_RE = re.compile(r"(\+?\d{1,2}[\s.-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}")


def detect_sections(text: str) -> dict:
    """
    Scan line-by-line for lines that look like section headers (short,
    title-cased or all-caps, matching a known section keyword).
    Returns {section_key: line_number_found} for sections detected;
    missing sections are simply absent from the returned dict.
    """
    found = {}
    lines = text.splitlines()
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped or len(stripped) > 40:
            continue  # section headers are short lines
        normalized = stripped.lower().strip(":")
        for section, patterns in SECTION_HEADER_PATTERNS.items():
            if section in found:
                continue
            for pattern in patterns:
                if re.fullmatch(pattern, normalized) or re.match(
                    rf"^{pattern}\b", normalized
                ):
                    found[section] = i
                    break
    return found


def detect_contact_info(text: str) -> dict:
    """Best-effort detection of email/phone presence in the document body."""
    return {
        "has_email": bool(EMAIL_RE.search(text)),
        "has_phone": bool(PHONE_RE.search(text)),
        "email_matches": EMAIL_RE.findall(text),
    }


def missing_sections(text: str) -> list:
    """Sections expected on a typical resume but not detected."""
    expected = ["experience", "education", "skills"]
    found = detect_sections(text)
    return [s for s in expected if s not in found]


# ---------------------------------------------------------------------------
# Bullet extraction
# ---------------------------------------------------------------------------

BULLET_LINE_RE = re.compile(r"^\s*[•\-\*•●‣⁃]\s*(.+)$")


def extract_bullets(text: str) -> list:
    """
    Pull out lines that look like bullet points (start with a bullet
    character). Falls back to short standalone lines under an Experience-like
    section if no explicit bullet characters are used, since some resumes
    format bullets as plain line breaks.
    """
    bullets = []
    for line in text.splitlines():
        match = BULLET_LINE_RE.match(line)
        if match:
            bullets.append(match.group(1).strip())
    return bullets


# ---------------------------------------------------------------------------
# Quantification detection
# ---------------------------------------------------------------------------

QUANTIFICATION_RE = re.compile(
    r"(\d+(\.\d+)?%|\$\d[\d,]*(\.\d+)?[kKmMbB]?|\b\d+(\.\d+)?[xX]\b|"
    r"\b\d[\d,]*\+?\s*(users|customers|engineers|people|team members|"
    r"requests|records|clients|projects|hours|days|weeks|months|years)\b|"
    r"\b\d[\d,]*\+?\b)"
)


def is_quantified(bullet: str) -> bool:
    return bool(QUANTIFICATION_RE.search(bullet))


def quantification_rate(bullets: list) -> float:
    """Fraction (0.0-1.0) of bullets containing a quantified signal."""
    if not bullets:
        return 0.0
    return sum(1 for b in bullets if is_quantified(b)) / len(bullets)


# ---------------------------------------------------------------------------
# Weak phrase / weak verb detection
# ---------------------------------------------------------------------------

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

WEAK_VERBS = ["did", "made", "used", "handled", "dealt with", "was in charge of", "got", "gave", "took care of"]

FIRST_PERSON_RE = re.compile(r"\b(I|my|me)\b", re.IGNORECASE)


def find_weak_phrases(bullet: str) -> list:
    lower = bullet.lower()
    return [p for p in WEAK_PHRASES + WEAK_VERBS if p in lower]


def has_first_person(bullet: str) -> bool:
    return bool(FIRST_PERSON_RE.search(bullet))


def opening_verb(bullet: str) -> str:
    """Returns the first word of a bullet, stripped of punctuation - a rough proxy for the 'action verb' used."""
    words = re.findall(r"[A-Za-z']+", bullet)
    return words[0] if words else ""


# ---------------------------------------------------------------------------
# Repetition analysis
# ---------------------------------------------------------------------------

STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "to", "in", "on", "for", "with",
    "at", "by", "from", "as", "is", "was", "were", "be", "been", "that",
    "this", "it", "its", "into", "using", "across", "over", "than",
}


def word_frequencies(text: str, min_length: int = 4, top_n: int = 15) -> list:
    """
    Returns [(word, count), ...] for the most repeated non-trivial words,
    used to flag repetitive wording across the document. Excludes common
    stopwords and words shorter than min_length so results stay meaningful.
    """
    words = re.findall(r"[A-Za-z']+", text.lower())
    filtered = [w for w in words if len(w) >= min_length and w not in STOPWORDS]
    counts = Counter(filtered)
    return counts.most_common(top_n)


def repeated_opening_verbs(bullets: list, min_count: int = 3) -> dict:
    """Flags action verbs used to open 3+ bullets - a sign of low verb variety."""
    verbs = [opening_verb(b).lower() for b in bullets if opening_verb(b)]
    counts = Counter(verbs)
    return {verb: count for verb, count in counts.items() if count >= min_count}


# ---------------------------------------------------------------------------
# CLI: quick mechanical pass over a text file
# ---------------------------------------------------------------------------

def analyze(text: str) -> dict:
    bullets = extract_bullets(text)
    return {
        "sections_found": list(detect_sections(text).keys()),
        "sections_missing": missing_sections(text),
        "contact_info": detect_contact_info(text),
        "bullet_count": len(bullets),
        "quantification_rate": round(quantification_rate(bullets), 2),
        "weak_phrase_bullets": [
            {"bullet": b, "flags": find_weak_phrases(b)}
            for b in bullets
            if find_weak_phrases(b)
        ],
        "first_person_bullets": [b for b in bullets if has_first_person(b)],
        "repeated_opening_verbs": repeated_opening_verbs(bullets),
        "top_repeated_words": word_frequencies(text),
    }


def main():
    import sys
    import json

    if len(sys.argv) != 2:
        print("Usage: python3 helpers.py <path/to/extracted_text.txt>", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1], "r", encoding="utf-8", errors="replace") as f:
        text = f.read()

    print(json.dumps(analyze(text), indent=2))


if __name__ == "__main__":
    main()
