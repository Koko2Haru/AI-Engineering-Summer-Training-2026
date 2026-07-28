"""
Star Gazer — Day 3: two tools + persistent memory

Tools:
  1. describe_photo         -> Gemini vision, structured JSON (from Day 2)
  2. propose_constellation  -> groups photos, validated by code, saved to memory

Memory (memory.json), survives between runs:
  - constellations the agent has already created
  - corrections and preferences the user has stated

Usage:
  python memory_agent.py organize
  python memory_agent.py remember "don't group the eye photo, it isn't a memory"
  python memory_agent.py show
  python memory_agent.py reset
"""

import hashlib
import json
import os
import sys

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

PHOTO_DIR = "screenshots"
CACHE_DIR = "cache"
MEMORY_FILE = "memory.json"
os.makedirs(CACHE_DIR, exist_ok=True)


# ---------- Memory ----------

def load_memory() -> dict:
    if os.path.exists(MEMORY_FILE):
        return json.load(open(MEMORY_FILE, encoding="utf-8"))
    return {"preferences": [], "constellations": []}


def save_memory(mem: dict) -> None:
    json.dump(mem, open(MEMORY_FILE, "w", encoding="utf-8"), indent=2)


# ---------- Tool 1: describe_photo (Day 2, unchanged) ----------

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
    """Code validates the agent's proposal. The agent does not get the final say."""
    mem = load_memory()
    errors = []

    if len(photo_ids) < 2:
        errors.append("a constellation needs at least 2 photos")

    existing_names = [c["name"].lower() for c in mem["constellations"]]
    if name.lower() in existing_names:
        errors.append(f"'{name}' already exists — pick a different name or leave it alone")

    locked_photos = {
        pid
        for c in mem["constellations"]
        if c.get("locked")
        for pid in c["photo_ids"]
    }
    conflicts = [p for p in photo_ids if p in locked_photos]
    if conflicts:
        errors.append(f"these photos are in a user-locked constellation and cannot be moved: {conflicts}")

    missing = [p for p in photo_ids if not os.path.exists(os.path.join(PHOTO_DIR, p))]
    if missing:
        errors.append(f"unknown photos: {missing}")

    if errors:
        return {"accepted": False, "errors": errors}

    mem["constellations"].append({
        "name": name,
        "photo_ids": photo_ids,
        "rationale": rationale,
        "locked": False,
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
                "properties": {"photo_id": {"type": "string", "description": "Filename, e.g. 1.jpg"}},
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
                    "name": {"type": "string", "description": "Short evocative name"},
                    "rationale": {"type": "string", "description": "What these photos share"},
                },
                "required": ["photo_ids", "name", "rationale"],
            },
        },
    ]
}]

AVAILABLE_TOOLS = {
    "describe_photo": describe_photo,
    "propose_constellation": propose_constellation,
}


# ---------- The loop ----------

def build_system_instruction(photo_ids: list, mem: dict) -> str:
    parts = [
        "You are Star Gazer's photo agent. You arrange photos into a night sky.",
        "You cannot see images — you must call describe_photo to learn what a photo shows.",
        f"Photos available: {', '.join(photo_ids)}",
        "",
        "Rules:",
        "- Only group photos that genuinely share a memory. If photos have nothing in common, say so and do not force a group.",
        "- Refusing to group is a valid and correct outcome.",
    ]

    if mem["preferences"]:
        parts += ["", "The user has told you the following. These are binding:"]
        parts += [f"- {p}" for p in mem["preferences"]]

    if mem["constellations"]:
        parts += ["", "Constellations that already exist. Do not recreate or duplicate these:"]
        for c in mem["constellations"]:
            lock = " [USER-LOCKED, cannot be changed]" if c.get("locked") else ""
            parts.append(f"- {c['name']}: {c['photo_ids']} — {c['rationale']}{lock}")

    return "\n".join(parts)


def run_agent(user_prompt: str, max_turns: int = 12) -> None:
    photo_ids = sorted(
        f for f in os.listdir(PHOTO_DIR) if f.lower().endswith((".jpg", ".jpeg", ".png"))
    )
    mem = load_memory()

    print(f"Photos: {photo_ids}")
    print(f"Memory: {len(mem['preferences'])} preference(s), {len(mem['constellations'])} constellation(s)\n")

    model = genai.GenerativeModel(
        "gemini-3.1-flash-lite",
        tools=TOOLS,
        system_instruction=build_system_instruction(photo_ids, mem),
    )
    chat = model.start_chat()
    response = chat.send_message(user_prompt)

    for turn in range(1, max_turns + 1):
        calls = [p.function_call for p in response.candidates[0].content.parts if p.function_call]

        if not calls:
            print(f"[Turn {turn}] Final answer:\n{response.text}")
            return

        print(f"[Turn {turn}] {len(calls)} tool call(s)")
        results = []
        for call in calls:
            args = dict(call.args)
            if "photo_ids" in args:
                args["photo_ids"] = list(args["photo_ids"])
            print(f"  -> {call.name}({args})")
            out = AVAILABLE_TOOLS[call.name](**args)
            print(f"  <- {json.dumps(out, ensure_ascii=False)}")
            results.append(genai.protos.Part(
                function_response=genai.protos.FunctionResponse(
                    name=call.name, response={"result": out}
                )
            ))
        response = chat.send_message(results)

    print("Hit max turns without finishing — possible loop.")


# ---------- CLI ----------

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "organize"

    if cmd == "organize":
        run_agent("Organise my sky. Group photos into constellations where they genuinely belong together.")

    elif cmd == "remember":
        note = " ".join(sys.argv[2:])
        mem = load_memory()
        mem["preferences"].append(note)
        save_memory(mem)
        print(f"Saved: {note}")

    elif cmd == "lock":
        name = " ".join(sys.argv[2:])
        mem = load_memory()
        for c in mem["constellations"]:
            if c["name"].lower() == name.lower():
                c["locked"] = True
                save_memory(mem)
                print(f"Locked: {c['name']}")
                break
        else:
            print(f"No constellation named '{name}'")

    elif cmd == "show":
        mem = load_memory()
        print(json.dumps(mem, indent=2, ensure_ascii=False))

    elif cmd == "reset":
        if os.path.exists(MEMORY_FILE):
            os.remove(MEMORY_FILE)
        print("Memory cleared (photo description cache kept).")

    else:
        print(__doc__)