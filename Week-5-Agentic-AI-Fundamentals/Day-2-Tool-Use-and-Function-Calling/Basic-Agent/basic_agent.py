"""
Star Gazer — Day 2: single-tool agent (function calling)
Tool: describe_photo -> Gemini vision, returns structured JSON
"""

import hashlib
import json
import os
import google.generativeai as genai

from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)

# ---------- The tool itself ----------

def describe_photo(path: str) -> dict:
    """Look at a photo and return a structured description."""
    file_hash = hashlib.md5(open(path, "rb").read()).hexdigest()
    cache_path = f"{CACHE_DIR}/{file_hash}.json"
    if os.path.exists(cache_path):
        return json.load(open(cache_path))

    vision_model = genai.GenerativeModel("gemini-3.1-flash-lite")
    prompt = """Analyze this photo and return ONLY valid JSON, no markdown fences, no other text:
{
  "subjects": ["list", "of", "things", "visible"],
  "setting": "one or two words",
  "indoor_outdoor": "indoor" or "outdoor",
  "time_of_day": "morning/afternoon/evening/night/unknown",
  "notable_details": "brief phrase, observable facts only",
  "confidence": 0.0 to 1.0
}"""
    with open(path, "rb") as f:
        image_data = f.read()
    response = vision_model.generate_content(
        [prompt, {"mime_type": "image/jpeg", "data": image_data}]
    )
    text = response.text.strip().strip("```json").strip("```").strip()
    result = json.loads(text)

    json.dump(result, open(cache_path, "w"))
    return result


# ---------- Tool schema the agent model sees ----------

TOOLS = [
    {
        "function_declarations": [
            {
                "name": "describe_photo",
                "description": "Look at a photo file and return what it depicts: subjects, setting, indoor/outdoor, time of day, notable details, and a confidence score.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "File path to the photo to examine",
                        }
                    },
                    "required": ["path"],
                },
            }
        ]
    }
]

AVAILABLE_TOOLS = {"describe_photo": describe_photo}


# ---------- The ReAct loop ----------

def run_agent(user_prompt: str, photo_paths: list[str], max_turns: int = 10):
    agent_model = genai.GenerativeModel(
        "gemini-3.1-flash-lite",
        tools=TOOLS,
        system_instruction=(
            "You are Star Gazer's photo agent. You can only learn what a photo "
            "shows by calling describe_photo on it — you cannot see images "
            "directly. Available photo paths: " + ", ".join(photo_paths)
        ),
    )
    chat = agent_model.start_chat()
    response = chat.send_message(user_prompt)

    turn = 0
    while turn < max_turns:
        turn += 1
        function_calls = [
            part.function_call
            for part in response.candidates[0].content.parts
            if part.function_call
        ]

        if not function_calls:
            print(f"\n[Turn {turn}] Final answer:")
            print(response.text)
            break

        print(f"\n[Turn {turn}] Agent requested {len(function_calls)} tool call(s)")

        tool_results = []
        for call in function_calls:
            tool_name = call.name
            args = dict(call.args)
            print(f"  -> {tool_name}({args})")

            result = AVAILABLE_TOOLS[tool_name](**args)
            print(f"  <- {json.dumps(result)}")

            tool_results.append(
                genai.protos.Part(
                    function_response=genai.protos.FunctionResponse(
                        name=tool_name, response={"result": result}
                    )
                )
            )

        response = chat.send_message(tool_results)
    else:
        print("Hit max turns without a final answer — check for a loop.")


def load_photos_from_folder(folder: str, limit: int = 5) -> list[str]:
    exts = (".jpg", ".jpeg", ".png")
    files = [
        os.path.join(folder, f)
        for f in sorted(os.listdir(folder))
        if f.lower().endswith(exts)
    ]
    return files[:limit]


if __name__ == "__main__":
    photos = load_photos_from_folder("screenshots", limit=5)
    print(f"Found {len(photos)} photos: {photos}")
    run_agent(
        "Look at these photos and tell me what they have in common, if anything.",
        photo_paths=photos,
    )