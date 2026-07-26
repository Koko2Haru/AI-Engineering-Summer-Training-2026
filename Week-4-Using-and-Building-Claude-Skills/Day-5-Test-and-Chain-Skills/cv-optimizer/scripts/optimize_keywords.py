#!/usr/bin/env python3
"""
Keyword coverage comparison for the CV Optimizer skill's keyword pass.

Compares resume text against a target job description (or a plain list of
target keywords) and reports which terms are already present, which are
close-but-differently-phrased, and which are genuinely absent. This script
only *detects* coverage - it never decides to add a keyword to the resume.
Per references/keyword-optimization.md, a keyword may only be added to the
rewrite if the candidate's own content already substantiates it; this tool's
"missing" list is an input to a Change Report note or a clarifying question,
not an instruction to insert the term.

No third-party dependencies - stdlib only, so this always runs.

Usage:
    python3 optimize_keywords.py <resume_text_path> <job_description_path>
    python3 optimize_keywords.py <resume_text_path> --keywords "CI/CD,Kubernetes,SQL"
"""

import re
import sys
import json

STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "to", "in", "on", "for", "with",
    "at", "by", "from", "as", "is", "are", "was", "were", "be", "been",
    "will", "you", "your", "we", "our", "this", "that", "it", "its",
    "into", "using", "across", "over", "than", "who", "have", "has",
    "job", "role", "work", "team", "years", "experience",
}

# Common multi-word technical/role terms worth extracting whole rather than
# splitting into individual stopword-filtered words.
PHRASE_HINTS = [
    "ci/cd", "machine learning", "data pipeline", "data pipelines",
    "cloud infrastructure", "project management", "product management",
    "customer relationship management", "rest api", "rest apis",
    "microservices", "cross-functional", "agile", "scrum",
]


def extract_candidate_terms(jd_text: str, top_n: int = 15) -> list:
    """
    Pull out likely-important terms from a job description: capitalized
    multi-word tech/tool names, known phrase hints, and frequent
    non-stopword unigrams. Heuristic, not exhaustive - Claude should use
    judgment on top of this list, not treat it as final.
    """
    lower = jd_text.lower()
    found_phrases = [p for p in PHRASE_HINTS if p in lower]

    # Capitalized tokens (likely tool/tech/proper nouns): e.g. "Python", "AWS", "React"
    capitalized = re.findall(r"\b[A-Z][A-Za-z0-9+.#]{1,20}\b", jd_text)
    from collections import Counter
    cap_counts = Counter(w for w in capitalized if w.lower() not in STOPWORDS)

    words = re.findall(r"[A-Za-z][A-Za-z0-9+.#/-]{2,}", lower)
    word_counts = Counter(w for w in words if w not in STOPWORDS and len(w) > 2)

    ranked = found_phrases + [w for w, _ in cap_counts.most_common(top_n)]
    for w, _ in word_counts.most_common(top_n):
        if w not in [r.lower() for r in ranked]:
            ranked.append(w)

    # de-duplicate case-insensitively, preserve order
    seen = set()
    deduped = []
    for term in ranked:
        key = term.lower()
        if key not in seen:
            seen.add(key)
            deduped.append(term)
    return deduped[:top_n]


def coverage(resume_text: str, keywords: list) -> dict:
    lower_resume = resume_text.lower()
    present, absent = [], []
    for kw in keywords:
        if kw.lower() in lower_resume:
            present.append(kw)
        else:
            absent.append(kw)
    return {
        "present": present,
        "absent": absent,
        "coverage_rate": round(len(present) / len(keywords), 2) if keywords else 0.0,
    }


def main():
    if len(sys.argv) < 3:
        print(
            "Usage:\n"
            "  python3 optimize_keywords.py <resume_text_path> <job_description_path>\n"
            "  python3 optimize_keywords.py <resume_text_path> --keywords \"kw1,kw2,kw3\"",
            file=sys.stderr,
        )
        sys.exit(1)

    resume_path = sys.argv[1]
    with open(resume_path, "r", encoding="utf-8", errors="replace") as f:
        resume_text = f.read()

    if sys.argv[2] == "--keywords":
        if len(sys.argv) < 4:
            print("Missing keyword list after --keywords", file=sys.stderr)
            sys.exit(1)
        keywords = [k.strip() for k in sys.argv[3].split(",") if k.strip()]
        source = "explicit_keyword_list"
        jd_text = None
    else:
        jd_path = sys.argv[2]
        with open(jd_path, "r", encoding="utf-8", errors="replace") as f:
            jd_text = f.read()
        keywords = extract_candidate_terms(jd_text)
        source = "job_description"

    result = {
        "source": source,
        "candidate_keywords": keywords,
        "coverage": coverage(resume_text, keywords),
        "note": (
            "Terms in 'absent' are NOT automatically added to the resume. "
            "Per references/keyword-optimization.md, only add a term if the "
            "candidate's existing content already substantiates it, or if the "
            "user confirms it during clarification. Otherwise, list it in the "
            "Change Report as a genuine gap."
        ),
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
