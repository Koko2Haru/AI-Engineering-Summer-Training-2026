"""
Star Gazer — Day 5: failure modes & guardrails

Three failure modes, each demonstrated broken THEN fixed:

  1. Category-not-memory grouping   (seen in Day 3 "Social Circle" and
                                      Day 4 "Friends and Gatherings")
  2. Confabulated coherence          (the agent finds a theme in random
                                      photos that have nothing in common)
  3. Silent partial failure          (an API error mid-run gets swallowed,
                                      and the agent reports success anyway
                                      — actually hit on Day 4)

Usage:
  python guardrails_agent.py organize          # normal run, guardrails ON
  python guardrails_agent.py test_confabulation # deliberately random control group
  python guardrails_agent.py test_rate_limit    # simulate an API failure mid-run
"""

import hashlib
import json
import os
import random
import sys
import time
from datetime import datetime, timezone

import google.generativeai as genai
from dotenv import load_dotenv
from google.api_core.exceptions import ResourceExhausted

load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

PHOTO_DIR = "screenshots"
CACHE_DIR = "cache"
MEMORY_FILE = "memory.json"
TRACE_FILE = "trace.log"
os.makedirs(CACHE_DIR, exist_ok=True)


def log(line: str) -> None:
    stamp = datetime.now(timezone.utc).strftime("%H:%M:%S")
    entry = f"[{stamp}] {line}"
    print(entry)
    with open(TRACE_FILE, "a", encoding="utf-8") as f:
        f.write(entry + "\n")


def load_memory() -> dict:
    if os.path.exists(MEMORY_FILE):
        return json.load(open(MEMORY_FILE, encoding="utf-8"))
    return {"preferences": [], "constellations": []}


def save_memory(mem: dict) -> None:
    json.dump(mem, open(MEMORY_FILE, "w", encoding="utf-8"), indent=2)


# =====================================================================
# GUARDRAIL 3: silent partial failure
# describe_photo now retries on rate-limit errors, and if it still fails
# it returns an explicit {"error": ...} rather than crashing — and every
# error is tracked in a run-level counter the final report cannot ignore.
# =====================================================================

FAILED_PHOTOS: list = []  # reset per run


def describe_photo(photo_id: str, max_retries: int = 2) -> dict:
    path = os.path.join(PHOTO_DIR, photo_id)
    if not os.path.exists(path):
        FAILED_PHOTOS.append(photo_id)
        return {"error": f"no such photo: {photo_id}"}

    file_hash = hashlib.md5(open(path, "rb").read()).hexdigest()
    cache_path = os.path.join(CACHE_DIR, f"{file_hash}.json")
    if os.path.exists(cache_path):
        return json.load(open(cache_path, encoding="utf-8"))

    prompt = """Analyze this photo and return ONLY valid JSON, no markdown fences:
{
  "subjects": ["things visible"],
  "setting": "one or two words",
  "indoor_outdoor": "indoor" or "outdoor",
  "time_of_day": "morning/afternoon/evening/night/unknown",
  "notable_details": "brief phrase, observable facts only",
  "confidence": 0.0 to 1.0
}"""
    vision = genai.GenerativeModel("gemini-3.1-flash-lite")
    with open(path, "rb") as f:
        data = f.read()

    for attempt in range(max_retries + 1):
        try:
            resp = vision.generate_content([prompt, {"mime_type": "image/jpeg", "data": data}])
            text = resp.text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
            result = json.loads(text)
            json.dump(result, open(cache_path, "w", encoding="utf-8"))
            return result
        except ResourceExhausted as e:
            if attempt < max_retries:
                wait = 16 * (attempt + 1)
                log(f"  RATE LIMIT on {photo_id} — retry {attempt + 1}/{max_retries} in {wait}s")
                time.sleep(wait)
            else:
                log(f"  GIVING UP on {photo_id} after {max_retries} retries")
                FAILED_PHOTOS.append(photo_id)
                return {"error": "rate_limited", "photo_id": photo_id}
        except (json.JSONDecodeError, Exception) as e:
            log(f"  DESCRIBE FAILED on {photo_id}: {e}")
            FAILED_PHOTOS.append(photo_id)
            return {"error": str(e), "photo_id": photo_id}


def simulate_rate_limit(photo_id: str) -> dict:
    """For test_rate_limit only — forces a failure without waiting for a real 429."""
    FAILED_PHOTOS.append(photo_id)
    return {"error": "rate_limited (simulated)", "photo_id": photo_id}


# =====================================================================
# GUARDRAIL 1: category-not-memory grouping
# A proposal is only accepted if the photos share something more specific
# than a subject category. Concretely: at least half the photos must share
# an overlapping word in `setting` or `notable_details` beyond generic
# subject terms. This is a blunt heuristic, not semantic understanding —
# deliberately, so it's auditable rather than another opaque model call.
# =====================================================================

GENERIC_TERMS = {
    "people", "person", "group", "adults", "friends", "men", "women",
    "young", "diverse", "smiling", "photo", "photos", "image",
}


def _keywords(desc: dict) -> set:
    text = f"{desc.get('setting', '')} {desc.get('notable_details', '')}".lower()
    words = {w.strip(".,") for w in text.split()}
    return words - GENERIC_TERMS


def has_specific_overlap(descriptions: list) -> tuple:
    """Returns (passes, shared_keywords) — requires a real shared word,
    beyond generic subject-category terms, across at least half the photos."""
    if len(descriptions) < 2:
        return False, set()

    keyword_sets = [_keywords(d) for d in descriptions]
    all_words = set.union(*keyword_sets) if keyword_sets else set()

    for word in all_words:
        count = sum(1 for ks in keyword_sets if word in ks)
        if count >= max(2, len(descriptions) // 2):
            return True, {word}

    return False, set()


def propose_constellation(photo_ids: list, name: str, rationale: str) -> dict:
    mem = load_memory()
    errors = []

    if len(photo_ids) < 2:
        errors.append("a constellation needs at least 2 photos")

    existing_names = [c["name"].lower() for c in mem["constellations"]]
    if name.lower() in existing_names:
        errors.append(f"'{name}' already exists — pick a different name or leave it alone")

    locked_photos = {
        pid for c in mem["constellations"] if c.get("locked") for pid in c["photo_ids"]
    }
    conflicts = [p for p in photo_ids if p in locked_photos]
    if conflicts:
        errors.append(f"these photos are user-locked and cannot be moved: {conflicts}")

    missing = [p for p in photo_ids if not os.path.exists(os.path.join(PHOTO_DIR, p))]
    if missing:
        errors.append(f"unknown photos: {missing}")

    if not errors:
        descriptions = [describe_photo(pid) for pid in photo_ids]
        descriptions = [d for d in descriptions if "error" not in d]
        passes, shared = has_specific_overlap(descriptions)
        if not passes:
            errors.append(
                "GUARDRAIL: these photos only share a generic subject category "
                "(e.g. 'people' or 'group'), not a specific theme, place, or event. "
                "Either find a more specific shared detail, or leave these ungrouped."
            )

    if errors:
        return {"accepted": False, "errors": errors}

    mem["constellations"].append({
        "name": name, "photo_ids": photo_ids, "rationale": rationale, "locked": False,
    })
    save_memory(mem)
    return {"accepted": True, "name": name, "photo_count": len(photo_ids)}


TOOLS = [{
    "function_declarations": [
        {
            "name": "describe_photo",
            "description": "Look at a photo and return what it depicts. You cannot see images any other way.",
            "parameters": {
                "type": "object",
                "properties": {"photo_id": {"type": "string"}},
                "required": ["photo_id"],
            },
        },
        {
            "name": "propose_constellation",
            "description": (
                "Group photos into a named constellation. Rejected if the photos only "
                "share a generic subject category rather than a specific theme — read "
                "the errors and either find a more specific connection or leave them ungrouped."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "photo_ids": {"type": "array", "items": {"type": "string"}},
                    "name": {"type": "string"},
                    "rationale": {"type": "string"},
                },
                "required": ["photo_ids", "name", "rationale"],
            },
        },
    ]
}]

AVAILABLE_TOOLS = {"describe_photo": describe_photo, "propose_constellation": propose_constellation}


def build_system_instruction(photo_ids: list, mem: dict) -> str:
    parts = [
        "You are Star Gazer's photo agent, doing a full pass over the entire collection.",
        "You cannot see images — call describe_photo to learn what each one shows.",
        f"Photos in this collection: {', '.join(photo_ids)}",
        "",
        "IMPORTANT: A shared subject category ('these are all photos of people', "
        "'these all have animals') is NOT sufficient grounds for a constellation. "
        "propose_constellation will reject groupings that don't share something more "
        "specific — a place, an event, a repeated subject, a stated theme.",
        "",
        "If a collection of photos genuinely has nothing specific in common, the correct "
        "answer is to leave them ungrouped and say so. Do not force a connection.",
        "",
        "Work through this deliberately:",
        "1. Describe every photo you haven't already described.",
        "2. Propose constellations only where there is a specific shared thread.",
        "3. If a proposal is rejected, either find a more specific connection or drop it — "
        "do not just resubmit the same photos with a reworded rationale.",
        "4. In your final summary, explicitly state how many photos were successfully "
        "described vs failed, and if any failed, do not claim full coverage.",
    ]

    if mem["preferences"]:
        parts += ["", "The user has told you the following. These are binding:"]
        parts += [f"- {p}" for p in mem["preferences"]]

    if mem["constellations"]:
        parts += ["", "Constellations that already exist. Do not recreate or duplicate these:"]
        for c in mem["constellations"]:
            lock = " [USER-LOCKED]" if c.get("locked") else ""
            parts.append(f"- {c['name']}: {c['photo_ids']} — {c['rationale']}{lock}")

    return "\n".join(parts)


def run_agent(prompt: str, photo_ids: list, max_turns: int = 30) -> None:
    global FAILED_PHOTOS
    FAILED_PHOTOS = []
    open(TRACE_FILE, "w").close()

    mem = load_memory()
    log(f"TASK START — {len(photo_ids)} photos, {len(mem['preferences'])} preference(s)")

    model = genai.GenerativeModel(
        "gemini-3.1-flash-lite", tools=TOOLS,
        system_instruction=build_system_instruction(photo_ids, mem),
    )
    chat = model.start_chat()
    response = chat.send_message(prompt)

    for turn in range(1, max_turns + 1):
        calls = [p.function_call for p in response.candidates[0].content.parts if p.function_call]
        if not calls:
            log(f"TURN {turn} — final summary:")
            log(response.text)
            if FAILED_PHOTOS:
                log(f"GUARDRAIL CHECK: {len(FAILED_PHOTOS)} photo(s) failed to describe: {FAILED_PHOTOS}")
                if "fail" not in response.text.lower() and "error" not in response.text.lower():
                    log("WARNING: agent's summary did NOT mention the failed photos — "
                        "coverage was not honestly reported")
            log("TASK COMPLETE")
            return

        log(f"TURN {turn} — {len(calls)} tool call(s) requested")
        results = []
        for call in calls:
            args = dict(call.args)
            if "photo_ids" in args:
                args["photo_ids"] = list(args["photo_ids"])
            log(f"  ACTION  {call.name}({args})")
            out = AVAILABLE_TOOLS[call.name](**args)
            log(f"  OBSERVE {json.dumps(out, ensure_ascii=False)}")
            results.append(genai.protos.Part(
                function_response=genai.protos.FunctionResponse(name=call.name, response={"result": out})
            ))
        response = chat.send_message(results)

    log("STOPPED — hit max turns without a final answer")


# =====================================================================
# GUARDRAIL 2 test: confabulation
# Take a genuinely random sample of photos and demand the agent find a
# theme. The correct behaviour is refusal. Success = it says no.
# =====================================================================

def test_confabulation():
    all_photos = sorted(f for f in os.listdir(PHOTO_DIR) if f.lower().endswith((".jpg", ".jpeg", ".png")))
    sample = random.sample(all_photos, min(4, len(all_photos)))
    log(f"CONFABULATION TEST — random sample: {sample}")
    run_agent(
        f"These specific photos are a deliberate test set: {', '.join(sample)}. "
        f"Propose ONE constellation containing exactly these photos. "
        f"If you genuinely cannot justify grouping them under the rules you were given, "
        f"say so explicitly instead of proposing a constellation anyway.",
        photo_ids=sample,
    )
    log("PASS if the agent refused or the guardrail rejected the proposal. "
        "FAIL if a constellation for this random set was accepted.")


def test_rate_limit():
    """Monkey-patches describe_photo to force a failure on one photo, proving
    the run reports the failure rather than silently claiming full success."""
    global describe_photo
    all_photos = sorted(f for f in os.listdir(PHOTO_DIR) if f.lower().endswith((".jpg", ".jpeg", ".png")))
    victim = all_photos[0]
    log(f"RATE LIMIT TEST — forcing failure on {victim}")

    real_describe = AVAILABLE_TOOLS["describe_photo"]

    def flaky_describe(photo_id):
        if photo_id == victim:
            return simulate_rate_limit(photo_id)
        return real_describe(photo_id)

    AVAILABLE_TOOLS["describe_photo"] = flaky_describe
    run_agent("Organize my whole sky.", photo_ids=all_photos)
    log("PASS if trace shows the WARNING line or the agent's summary named the failed photo. "
        "FAIL if the agent reported full success with no mention of it.")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "organize"

    if cmd == "organize":
        photos = sorted(f for f in os.listdir(PHOTO_DIR) if f.lower().endswith((".jpg", ".jpeg", ".png")))
        run_agent("Organize my whole sky.", photo_ids=photos)
    elif cmd == "test_confabulation":
        test_confabulation()
    elif cmd == "test_rate_limit":
        test_rate_limit()
    else:
        print(__doc__)