"""FR-15: does the optimised CV actually score higher than the original?

Never measured. Ad-hoc runs so far varied the target role and the intake answers
between runs, so their scores (46, 49, 40) are not comparable to each other.

This holds everything constant except the document:
  - same reviewer skill
  - same stated target role and seniority
  - no intake questions (proceed on stated assumptions)
  - score only, so the output is short and cheap

Three documents:
  messy      the original fixture               (documented baseline 46)
  optimised  what Sanad produced from it
  polished   the Week 6 well-written fixture    (documented baseline 85)

The messy one runs twice, to separate "the rewrite helped" from "the reviewer
is noisy".
"""
import json
import os
import time
import urllib.request
import uuid

WS = r"C:\Users\aliah\Desktop\AI-Engineering-Summer-Training-2026\Week-7-Capstone-Project\sanad\workspace"
FIX = r"C:\Users\aliah\Desktop\AI-Engineering-Summer-Training-2026\Week-7-Capstone-Project\sanad\fixtures"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fr15_results.json")

DOCS = [
    ("messy-run1", os.path.join(FIX, "synthetic-cv-messy.pdf")),
    ("optimised", os.path.join(WS, "sanad-cv-1536906890473381978.pdf")),
    ("polished", os.path.join(FIX, "synthetic-cv-polished.pdf")),
    ("messy-run2", os.path.join(FIX, "synthetic-cv-messy.pdf")),
]

PROMPT = """Use the cv-reviewer skill to review the CV at this path:
{path}

Hold these constant - do NOT ask me anything, proceed on these assumptions:
- Target role: Full-Stack Web Developer
- Target seniority: junior to mid level
- Target: a full-time in-house position, going through an ATS
- The candidate is not available for intake questions; state assumptions and continue.

When you are done, reply with ONLY this, nothing else:
SCORE: <overall score out of 100>
BAND: <the band word>
TOP3: <the three biggest problems, one short line each, semicolon separated>
"""


def call(path):
    body = json.dumps({
        "session_id": str(uuid.uuid4()),
        "prompt": PROMPT.format(path=path),
        "cwd": WS,
    }).encode()
    req = urllib.request.Request(
        "http://127.0.0.1:8900/claude", data=body,
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=900) as r:
        return json.load(r)


results = []
for label, path in DOCS:
    if not os.path.isfile(path):
        results.append({"label": label, "error": "missing file: " + path})
        continue
    t0 = time.time()
    try:
        res = call(path)
        out = res.get("output", "") if res.get("ok") else res.get("error", "")
    except Exception as exc:  # noqa: BLE001
        out = "CALL FAILED: %s" % exc
    results.append({
        "label": label,
        "file": os.path.basename(path),
        "seconds": round(time.time() - t0, 1),
        "output": out,
    })
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2)
    print("done:", label, "in", results[-1]["seconds"], "s", flush=True)

print("ALL DONE ->", OUT)
