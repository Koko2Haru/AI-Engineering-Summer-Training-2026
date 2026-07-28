"""
Star Gazer — Day 4: full multi-step organize pass, fully logged.

Same two tools as Day 3 (describe_photo, propose_constellation).
The difference is the task: "organize my whole sky" against the entire
photo folder in one run, with every thought/action/observation written
to trace.log as it happens. The trace file IS the Day 4 deliverable —
not the final constellations.

Usage:
  python full_organize.py
"""

import hashlib
import json
import os
from datetime import datetime, timezone

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

PHOTO_DIR = "screenshots"
CACHE_DIR = "cache"
MEMORY_FILE = "memory.json"
TRACE_FILE = "trace.log"
os.makedirs(CACHE_DIR, exist_ok=True)


# ---------- Trace logging ----------

def log(line: str) -> None:
    stamp = datetime.now(timezone.utc).strftime("%H:%M:%S")
    entry = f"[{stamp}] {line}"
    print(entry)
    with open(TRACE_FILE, "a", encoding="utf-8") as f:
        f.write(entry + "\n")


# ---------- Memory ----------

def load_memory() -> dict:
    if os.path.exists(MEMORY_FILE):
        return json.load(open(MEMORY_FILE, encoding="utf-8"))
    return {"preferences": [], "constellations": []}


def save_memory(mem: dict) -> None:
    json.dump(mem, open(MEMORY_FILE, "w", encoding="utf-8"), indent=2)


# ---------- Tool 1: describe_photo ----------

def describe_photo(photo_id: str) -> dict:
    path = os.path.join(PHOTO_DIR, photo_id)
    if not os.path.exists(path):
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
    resp = vision.generate_content([prompt, {"mime_type": "image/jpeg", "data": data}])
    text = resp.text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    result = json.loads(text)

    json.dump(result, open(cache_path, "w", encoding="utf-8"))
    return result


# ---------- Tool 2: propose_constellation ----------

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
            "description": "Group photos into a named constellation. Rejected if invalid — read the errors and revise.",
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


# ---------- The full multi-step pass ----------

def build_system_instruction(photo_ids: list, mem: dict) -> str:
    parts = [
        "You are Star Gazer's photo agent, doing a full pass over the entire collection.",
        "You cannot see images — call describe_photo to learn what each one shows.",
        f"Photos in this collection: {', '.join(photo_ids)}",
        "",
        "This is a multi-step task. Work through it deliberately:",
        "1. Describe every photo you haven't already described.",
        "2. Look for genuine shared threads — same place, same people, same event, a stated theme.",
        "   A shared subject category (e.g. 'photos with people in them') is NOT enough on its own.",
        "3. Propose constellations for groups with real evidence. If a proposal is rejected,",
        "   read the error and revise rather than repeating the same call.",
        "4. Photos with no genuine connection to anything else should be left ungrouped.",
        "   State clearly which photos ended up ungrouped and why.",
        "5. When finished, give a final summary: constellations formed, photos left sparse.",
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


def run_full_organize(max_turns: int = 30) -> None:
    open(TRACE_FILE, "w").close()  # fresh trace each run

    photo_ids = sorted(
        f for f in os.listdir(PHOTO_DIR) if f.lower().endswith((".jpg", ".jpeg", ".png"))
    )
    mem = load_memory()

    log(f"TASK START — {len(photo_ids)} photos, {len(mem['preferences'])} preference(s), "
        f"{len(mem['constellations'])} existing constellation(s)")

    model = genai.GenerativeModel(
        "gemini-3.1-flash-lite",
        tools=TOOLS,
        system_instruction=build_system_instruction(photo_ids, mem),
    )
    chat = model.start_chat()
    response = chat.send_message(
        "Organize my whole sky. Work through the full collection step by step."
    )

    for turn in range(1, max_turns + 1):
        calls = [p.function_call for p in response.candidates[0].content.parts if p.function_call]

        if not calls:
            log(f"TURN {turn} — final summary:")
            log(response.text)
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
                function_response=genai.protos.FunctionResponse(
                    name=call.name, response={"result": out}
                )
            ))
        response = chat.send_message(results)

    log("STOPPED — hit max turns without a final answer, possible loop")


if __name__ == "__main__":
    run_full_organize()