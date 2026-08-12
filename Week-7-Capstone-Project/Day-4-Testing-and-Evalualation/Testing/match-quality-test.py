"""Measure match quality across every Job Matching run so far.

Yesterday produced single observations - "4 of 5 scored 80", "1 of 5 invented".
One observation is not a rate. This walks every successful execution in n8n's
database and turns them into counts.
"""
import json
import os
import sqlite3
from collections import Counter

db = os.path.join(os.path.expanduser("~"), ".n8n", "database.sqlite")
con = sqlite3.connect("file:" + db.replace(os.sep, "/") + "?mode=ro", uri=True)

wf = con.execute("select id from workflow_entity where name like '%Job Matching%'").fetchone()
rows = con.execute(
    """select e.id, e.status, d.data
       from execution_entity e join execution_data d on d.executionId = e.id
       where e.workflowId = ? order by e.id""", (wf[0],)).fetchall()
con.close()

all_scores = []
runs = []

for eid, status, data in rows:
    try:
        arr = json.loads(data)
    except Exception:
        continue

    seen = {}
    for el in arr:
        if isinstance(el, dict) and "cites_project" in el and "rank" in el:
            r = {k: (arr[int(v)] if isinstance(v, str) and v.isdigit() and int(v) < len(arr) else v)
                 for k, v in el.items()}
            key = (r.get("rank"), r.get("job_id"))
            if key not in seen:
                seen[key] = r

    if not seen:
        continue

    matches = sorted(seen.values(), key=lambda x: x.get("rank") or 0)
    scores = [m.get("score") for m in matches if isinstance(m.get("score"), (int, float))]
    cites = sum(1 for m in matches if m.get("cites_project") is True)
    banned = sum(1 for m in matches if m.get("has_banned_phrase") is True)
    missing = sum(1 for m in matches if m.get("pitch_missing") is True)
    trunc = any(m.get("response_was_truncated") is True for m in matches)

    all_scores += scores
    runs.append({
        "exec": eid, "status": status, "n": len(matches), "scores": scores,
        "cites": cites, "banned": banned, "missing": missing, "truncated": trunc,
    })

print("=" * 68)
print("MATCH QUALITY ACROSS %d RUNS" % len(runs))
print("=" * 68)
for r in runs:
    print("exec %-5s n=%d  scores=%-22s cites=%d/%d  banned=%d  missing=%d%s"
          % (r["exec"], r["n"], str(r["scores"]), r["cites"], r["n"],
             r["banned"], r["missing"], "  TRUNCATED" if r["truncated"] else ""))

tot = sum(r["n"] for r in runs)
if tot:
    print()
    print("-" * 68)
    print("TOTALS over %d matches in %d runs" % (tot, len(runs)))
    print("-" * 68)
    print("  pitches citing a real project : %d/%d  (%.0f%%)"
          % (sum(r["cites"] for r in runs), tot, 100 * sum(r["cites"] for r in runs) / tot))
    print("  pitches with banned filler    : %d/%d" % (sum(r["banned"] for r in runs), tot))
    print("  pitches missing entirely      : %d/%d" % (sum(r["missing"] for r in runs), tot))
    print()
    c = Counter(all_scores)
    print("  score distribution:")
    for s in sorted(c, reverse=True):
        print("     %3s : %s (%d)" % (s, "#" * c[s], c[s]))
    uniq = len(c)
    print()
    print("  distinct score values: %d across %d matches" % (uniq, len(all_scores)))
    if all_scores:
        top = c.most_common(1)[0]
        print("  most common score    : %s appears %d times (%.0f%% of all matches)"
              % (top[0], top[1], 100 * top[1] / len(all_scores)))
