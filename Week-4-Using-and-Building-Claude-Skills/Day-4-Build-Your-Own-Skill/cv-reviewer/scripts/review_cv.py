#!/usr/bin/env python3
"""
End-to-end orchestrator for the CV Reviewer skill.

Ties extract_text.py + helpers.py + assets/scoring-matrix.json together into
a single JSON pass over a resume file. This is a mechanical first pass, not
a replacement for the narrative review described in SKILL.md - several
categories (Content Quality, Visual/Layout, most of Professionalism) need
human/model judgment that plain regex heuristics can't reliably produce.
Those are emitted with a "requires_manual_review" flag and supporting
evidence rather than a guessed number, so the numbers this script *does*
produce stay trustworthy.

Usage:
    python3 review_cv.py <path/to/resume.(pdf|docx|txt)>

Output: a JSON object with mechanically-derived signals and partial scores,
intended to be read by Claude and combined with the qualitative analysis
described in SKILL.md - not printed directly to the end user as the final
report.
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import extract_text  # noqa: E402
import helpers  # noqa: E402


def load_scoring_matrix() -> dict:
    path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "assets", "scoring-matrix.json"
    )
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def band_for(score: float, matrix: dict) -> str:
    for band in matrix["score_bands"]:
        if band["min"] <= score <= band["max"]:
            return band["band"]
    return "Unknown"


def score_ats_compatibility(text: str, analysis: dict, extraction_warnings: list) -> dict:
    """Mechanical proxy for ATS Compatibility. Heavy penalty for extraction warnings
    (near-empty text = likely scanned/image PDF, the single most severe ATS failure)."""
    score = 90
    notes = []

    if extraction_warnings:
        score = 20
        notes.append("Extraction warnings present - likely image-based/unparseable document.")

    if "experience" not in analysis["sections_found"]:
        score -= 20
        notes.append("No 'Experience'-style section header detected.")

    if "skills" not in analysis["sections_found"]:
        score -= 10
        notes.append("No 'Skills'-style section header detected.")

    if not analysis["contact_info"]["has_email"]:
        score -= 15
        notes.append("No email address detected in document body.")

    score = max(0, min(100, score))
    return {"score": score, "notes": notes}


def score_impact(analysis: dict) -> dict:
    """Mechanical proxy for Impact, driven directly off quantification rate."""
    rate = analysis["quantification_rate"]
    score = round(rate * 100)
    notes = [f"{round(rate * 100)}% of detected bullets contain a quantified signal."]
    if rate < 0.3:
        notes.append("Most bullets describe activity without a measurable outcome.")
    return {"score": score, "notes": notes}


def score_professionalism_signals(analysis: dict) -> dict:
    """Partial signal only - full Professionalism score also needs a judgment
    pass on tone, personal info, and email quality that this script can't do reliably."""
    first_person_count = len(analysis["first_person_bullets"])
    notes = []
    penalty = 0
    if first_person_count:
        penalty += min(30, first_person_count * 10)
        notes.append(
            f"{first_person_count} bullet(s) use first-person pronouns "
            f"(e.g. {analysis['first_person_bullets'][0]!r})."
        )
    return {"partial_score": max(0, 100 - penalty), "notes": notes, "requires_manual_review": True}


def build_report(path: str) -> dict:
    extraction = extract_text.extract(path)
    text = extraction["text"]
    analysis = helpers.analyze(text)
    matrix = load_scoring_matrix()

    ats = score_ats_compatibility(text, analysis, extraction["warnings"])
    impact = score_impact(analysis)
    professionalism = score_professionalism_signals(analysis)

    return {
        "file_format": extraction["format"],
        "extraction_warnings": extraction["warnings"],
        "mechanical_analysis": analysis,
        "scores": {
            "ats_compatibility": {**ats, "band": band_for(ats["score"], matrix)},
            "impact": {**impact, "band": band_for(impact["score"], matrix)},
            "professionalism": professionalism,
            "content_quality": {"requires_manual_review": True,
                                 "note": "Needs qualitative judgment - see references/scoring-rubric.md #2"},
            "grammar_spelling": {"requires_manual_review": True,
                                  "note": "Needs qualitative judgment - see references/scoring-rubric.md #4"},
            "readability": {"requires_manual_review": True,
                             "note": "Needs qualitative judgment - see references/scoring-rubric.md #5"},
            "visual_layout": {"requires_manual_review": True,
                               "note": "Needs qualitative judgment - see references/scoring-rubric.md #6"},
        },
        "flags": {
            "weak_phrase_bullets": analysis["weak_phrase_bullets"],
            "repeated_opening_verbs": analysis["repeated_opening_verbs"],
            "missing_sections": analysis["sections_missing"],
        },
    }


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 review_cv.py <path/to/resume.(pdf|docx|txt)>", file=sys.stderr)
        sys.exit(1)

    try:
        report = build_report(sys.argv[1])
    except (FileNotFoundError, ValueError, RuntimeError) as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
