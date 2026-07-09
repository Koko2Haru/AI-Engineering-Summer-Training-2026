"""
Prompt Logger
-------------
An Ollama chat application that:
- Logs every prompt/response to CSV
- Tracks experiments (fixed prompt-engineering categories + custom, with typo detection)
- Measures response time
- Automatically generates PDF/TXT documents
- Supports conversation history
"""

from ollama import chat, list as ollama_list

import csv
import difflib
import json
import os
import re
import shutil
import textwrap
import time
from datetime import datetime
from xml.sax.saxutils import escape

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    ARABIC_SUPPORT = True
except ImportError:
    ARABIC_SUPPORT = False


# ==========================================================
# Configuration
# ==========================================================

# Preferred default in the model menu, and the fallback
# suggestion when the Ollama server can't be reached.
DEFAULT_MODEL = "llama3.2"

DEFAULT_OPTIONS = {
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 40,
    "repeat_penalty": 1.1,
    "num_predict": 800,   # 200 was cutting documents off mid-sentence
    "num_ctx": 4096,      # 1024 pushed the system prompt out of context after a few turns
    "seed": 42
}

# Fixed experiment categories.
# The menu adds a "Custom name" option at the end for anything else.
EXPERIMENT_TYPES = [
    "Role Prompting",
    "Few-Shot",
    "Chain-of-Thought",
    "Structured Output",
    "General",
]

# Anchor all output to the script's own folder,
# no matter where the terminal is running from.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Data lives next to the script by default. Docker (or anyone) can
# override this with the PROMPT_LOGGER_DATA environment variable,
# pointing it at a mounted volume.
DATA_DIR = os.environ.get("PROMPT_LOGGER_DATA", BASE_DIR)

CSV_FILE = os.path.join(DATA_DIR, "prompt_log.csv")
SAVE_FOLDER = os.path.join(DATA_DIR, "saved_responses")

# The contract that makes the save feature work.
# Shared by the CLI (this file) and the GUI (app.py).
SYSTEM_PROMPT = """You are a helpful AI assistant.

Most of the time, respond normally.

ONLY when the user explicitly asks you to create a PDF, TXT,
text file, report, notes, cheat sheet, study guide, or document,
respond with ONE JSON object and NOTHING else
(no explanation before or after, no markdown, no ``` fences):

{
    "save": true,
    "file_type": "pdf" or "txt" or "both",
    "title": "a short title",
    "content": "the full document text"
}

Otherwise respond normally."""

# First existing font on this list gets used for Arabic in PDFs.
# Tahoma/Arial ship with Windows and include Arabic glyphs.
ARABIC_FONT_CANDIDATES = [
    r"C:\Windows\Fonts\tahoma.ttf",
    r"C:\Windows\Fonts\arial.ttf",
    r"C:\Windows\Fonts\times.ttf",
    r"C:\Windows\Fonts\segoeui.ttf",
    "/usr/share/fonts/opentype/fonts-hosny-amiri/Amiri-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]


# ==========================================================
# Helper Functions
# ==========================================================

def sanitize_filename(text: str) -> str:
    """
    Convert a prompt into a safe filename.
    """

    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)

    words = text.split()[:5]
    filename = "_".join(words)

    if not filename:
        filename = "response"

    return filename


def ensure_directory(path: str):
    """
    Create directory (and parents) if it doesn't exist.
    """

    if not os.path.exists(path):
        os.makedirs(path)


def next_file_number(folder: str) -> str:
    """
    Returns:
        001
        002
        003
        ...
    """

    ensure_directory(folder)

    highest = 0

    for file in os.listdir(folder):
        match = re.match(r"(\d{3})_", file)
        if match:
            highest = max(highest, int(match.group(1)))

    return f"{highest + 1:03d}"


def ask_float(label: str, default: float) -> float:
    """
    Ask for a float. Enter keeps the default, garbage keeps the default.
    """

    raw = input(f"{label} [{default}]: ").strip()

    if raw == "":
        return default

    try:
        return float(raw)
    except ValueError:
        print(f"Invalid number, keeping {default}.")
        return default


def ask_int(label: str, default: int) -> int:
    """
    Ask for an int. Enter keeps the default, garbage keeps the default.
    """

    raw = input(f"{label} [{default}]: ").strip()

    if raw == "":
        return default

    try:
        return int(raw)
    except ValueError:
        print(f"Invalid number, keeping {default}.")
        return default


# ==========================================================
# Arabic Support
# ==========================================================

ARABIC_PATTERN = re.compile(r"[\u0600-\u06FF]")


def contains_arabic(text: str) -> bool:
    return bool(ARABIC_PATTERN.search(text))


def shape_arabic(text: str) -> str:
    """
    Join the letters into their connected forms and reorder
    them right-to-left. Needed because neither terminals nor
    reportlab do Arabic shaping themselves.
    """
    return get_display(arabic_reshaper.reshape(text))


def display_text(text: str) -> str:
    """
    Prepare text for terminal printing.
    Arabic lines get wrapped, shaped, and right-aligned.
    Everything else passes through untouched.
    """

    if not (ARABIC_SUPPORT and contains_arabic(text)):
        return text

    width = max(40, shutil.get_terminal_size((100, 20)).columns - 4)

    lines = []

    for line in text.split("\n"):
        if contains_arabic(line):
            for chunk in textwrap.wrap(line, width) or [""]:
                lines.append(shape_arabic(chunk).rjust(width))
        else:
            lines.append(line)

    return "\n".join(lines)


def register_arabic_font():
    """
    Register the first available Arabic-capable font for PDFs.
    Returns the font name, or None if nothing was found.
    """

    for path in ARABIC_FONT_CANDIDATES:
        if os.path.exists(path):
            try:
                pdfmetrics.registerFont(TTFont("ArabicFont", path))
                return "ArabicFont"
            except Exception:
                continue

    return None


PDF_ARABIC_FONT = register_arabic_font()


# ==========================================================
# Model Selection
# ==========================================================

def installed_models() -> list:
    """
    Ask the local Ollama server which models are installed.
    Returns a list of (name, size_in_gb) tuples,
    or an empty list if the server can't be reached.
    """

    try:
        response = ollama_list()
    except Exception:
        return []

    raw_models = (
        response.models
        if hasattr(response, "models")
        else response.get("models", [])
    )

    models = []

    for item in raw_models:

        if isinstance(item, dict):
            name = item.get("model") or item.get("name") or ""
            size = item.get("size") or 0
        else:
            name = getattr(item, "model", "") or getattr(item, "name", "") or ""
            size = getattr(item, "size", 0) or 0

        if name:
            models.append((name, size / 1_000_000_000))

    return models


def choose_model() -> str:
    """
    Show the models installed in Ollama and let the user pick one.
    Falls back to typing a name if the server can't be reached.
    """

    models = installed_models()

    if not models:
        print("\nCouldn't fetch the model list from Ollama.")
        name = input(f"Model name [{DEFAULT_MODEL}]: ").strip()
        return name or DEFAULT_MODEL

    default_index = 1

    for index, (name, _) in enumerate(models, start=1):
        if name == DEFAULT_MODEL or name.split(":")[0] == DEFAULT_MODEL:
            default_index = index
            break

    print("\nChoose a model:\n")

    for index, (name, size_gb) in enumerate(models, start=1):
        print(f"  {index}. {name}  ({size_gb:.1f} GB)")

    while True:
        raw = input(f"\nChoice 1-{len(models)} (Enter = {default_index}): ").strip()

        if raw == "":
            return models[default_index - 1][0]

        if raw.isdigit():
            number = int(raw)
            if 1 <= number <= len(models):
                return models[number - 1][0]

        print("Invalid choice, try again.")


# ==========================================================
# Experiment Selection
# ==========================================================

def existing_experiment_folders() -> list:
    """
    List the experiment folders that already exist.
    """

    ensure_directory(SAVE_FOLDER)

    return sorted(
        entry for entry in os.listdir(SAVE_FOLDER)
        if os.path.isdir(os.path.join(SAVE_FOLDER, entry))
    )


def ask_custom_experiment() -> str:
    """
    Ask for a custom experiment name.
    If it looks like a typo of an existing folder, offer to reuse it,
    so 'frw_shot' can never create a second folder next to 'few_shot'.
    """

    existing = existing_experiment_folders()

    while True:
        name = input("Custom experiment name: ").strip()

        if not name:
            print("Name can't be empty.")
            continue

        slug = sanitize_filename(name)

        match = difflib.get_close_matches(slug, existing, n=1, cutoff=0.75)

        if match and match[0] != slug:
            answer = input(
                f'Found a similar experiment "{match[0]}". Use it instead? (Y/N): '
            ).strip().lower()

            if answer == "y":
                return match[0]

        return slug


def choose_experiment() -> str:
    """
    Show a fixed menu of experiment types instead of free typing.
    """

    print("\nChoose experiment type:\n")

    for index, name in enumerate(EXPERIMENT_TYPES, start=1):
        print(f"  {index}. {name}")

    custom_option = len(EXPERIMENT_TYPES) + 1
    print(f"  {custom_option}. Custom name")

    while True:
        raw = input(f"\nChoice 1-{custom_option} (Enter = General): ").strip()

        if raw == "":
            return "General"

        if raw.isdigit():
            number = int(raw)

            if 1 <= number <= len(EXPERIMENT_TYPES):
                return EXPERIMENT_TYPES[number - 1]

            if number == custom_option:
                return ask_custom_experiment()

        print("Invalid choice, try again.")


# ==========================================================
# CSV Logging
# ==========================================================

def create_csv():
    """
    Create prompt_log.csv if it doesn't exist.
    """

    ensure_directory(DATA_DIR)

    if os.path.exists(CSV_FILE):
        return

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Experiment",
            "Timestamp",
            "Prompt",
            "Response",
            "Response Time (s)",
            "Model",
            "Temperature",
            "Top P",
            "Top K",
            "Repeat Penalty",
            "Max Tokens",
            "Context Size",
            "Seed"
        ])


def log_to_csv(experiment, prompt, response, response_time, options, model):
    """
    Save one interaction into the CSV.
    Self-healing: if the CSV was deleted for a reset, it is
    recreated with its header row before this row is written.
    """

    create_csv()

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            experiment,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            prompt,
            response,
            response_time,
            model,
            options["temperature"],
            options["top_p"],
            options["top_k"],
            options["repeat_penalty"],
            options["num_predict"],
            options["num_ctx"],
            options["seed"]
        ])


# ==========================================================
# Document Saving
# ==========================================================

def build_document(experiment, prompt, response, response_time, options, model):
    """
    Builds the document text used for both PDF and TXT.
    """

    return f"""
Prompt Logger

==================================================

Experiment:
{experiment}

Date:
{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Model:
{model}

Response Time:
{response_time:.2f} seconds

==================================================

Parameters

Temperature: {options["temperature"]}
Top P: {options["top_p"]}
Top K: {options["top_k"]}
Repeat Penalty: {options["repeat_penalty"]}
Max Tokens: {options["num_predict"]}
Context Size: {options["num_ctx"]}
Seed: {options["seed"]}

==================================================

Prompt

{prompt}

==================================================

Response

{response}
"""


def save_txt(filepath, content):
    """
    Save document as TXT.
    """

    with open(filepath, "w", encoding="utf-8") as file:
        file.write(content)


def save_pdf(filepath, content):
    """
    Save document as PDF.
    escape() is required: reportlab parses Paragraph text as mini-HTML,
    so a raw & or < in the model's answer would crash the save.
    Arabic lines get their own shaped, right-aligned style.
    """

    styles = getSampleStyleSheet()

    arabic_style = None

    if ARABIC_SUPPORT and PDF_ARABIC_FONT:
        arabic_style = ParagraphStyle(
            "Arabic",
            parent=styles["Normal"],
            fontName=PDF_ARABIC_FONT,
            fontSize=12,
            leading=18,
            alignment=TA_RIGHT,
            wordWrap="RTL",
        )

    document = SimpleDocTemplate(filepath)

    story = []

    for line in content.split("\n"):

        if line.strip() == "":
            continue

        if arabic_style and contains_arabic(line):
            story.append(Paragraph(escape(shape_arabic(line)), arabic_style))
        else:
            story.append(Paragraph(escape(line), styles["Normal"]))

    document.build(story)


# ==========================================================
# JSON Parser
# ==========================================================

def parse_json_response(text):
    """
    Try to pull a JSON object out of the model's reply.

    Handles the three ways small models mess this up:
    - wrapping the JSON in ```json fences
    - adding text before/after the JSON
    - putting real newlines inside "content"
      (json.loads rejects that unless strict=False)
    """

    cleaned = text.strip()

    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```[a-zA-Z]*\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)

    try:
        data = json.loads(cleaned, strict=False)
        if isinstance(data, dict):
            return data
    except Exception:
        pass

    match = re.search(r"\{.*\}", cleaned, re.DOTALL)

    if match:
        try:
            data = json.loads(match.group(0), strict=False)
            if isinstance(data, dict):
                return data
        except Exception:
            pass

    return None


# ==========================================================
# Main Program
# ==========================================================

def main():

    print("=" * 55)
    print("Prompt Logger")
    print("=" * 55)

    if not ARABIC_SUPPORT:
        print("\n(Arabic display off — run: pip install arabic-reshaper python-bidi)")

    # ------------------------------------------------------
    # Model selection
    # ------------------------------------------------------

    model_name = choose_model()
    print(f"\nModel: {model_name}")

    # ------------------------------------------------------
    # Experiment selection
    # ------------------------------------------------------

    experiment = choose_experiment()

    experiment_folder = os.path.join(
        SAVE_FOLDER,
        sanitize_filename(experiment)
    )

    ensure_directory(experiment_folder)
    create_csv()

    print(f"\nExperiment: {experiment}")
    print(f"Files will be saved in: {experiment_folder}")

    # ------------------------------------------------------
    # Model parameters
    # ------------------------------------------------------

    options = DEFAULT_OPTIONS.copy()

    choice = input("\nUse default parameters? (Y/N): ").strip().lower()

    if choice == "n":

        print("\nEnter custom parameters (press Enter to keep a default)\n")

        options["temperature"] = ask_float("Temperature", options["temperature"])
        options["top_p"] = ask_float("Top P", options["top_p"])
        options["top_k"] = ask_int("Top K", options["top_k"])
        options["repeat_penalty"] = ask_float("Repeat Penalty", options["repeat_penalty"])
        options["num_predict"] = ask_int("Max Tokens", options["num_predict"])
        options["num_ctx"] = ask_int("Context Size", options["num_ctx"])
        options["seed"] = ask_int("Seed", options["seed"])

    # ------------------------------------------------------
    # System prompt
    # ------------------------------------------------------

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # ------------------------------------------------------
    # Main chat loop
    # ------------------------------------------------------

    while True:

        user_input = input("\nYou: ").strip()

        if user_input.lower() in ["exit", "quit"]:
            print("\nGoodbye!")
            break

        if user_input == "":
            continue

        messages.append({
            "role": "user",
            "content": user_input
        })

        start = time.perf_counter()

        try:
            response = chat(
                model=model_name,
                messages=messages,
                options=options
            )
        except Exception as error:
            print(f"\n[!] Could not reach Ollama: {error}")
            messages.pop()  # remove the user message so history stays consistent
            continue

        end = time.perf_counter()
        response_time = end - start

        assistant_message = response.message.content.strip()

        messages.append({
            "role": "assistant",
            "content": assistant_message
        })

        log_to_csv(
            experiment,
            user_input,
            assistant_message,
            response_time,
            options,
            model_name
        )

        # --------------------------------------------------
        # Check if the model returned a save request
        # --------------------------------------------------

        data = parse_json_response(assistant_message)

        if data and data.get("save"):

            file_type = str(data.get("file_type", "")).lower()
            title = data.get("title") or sanitize_filename(user_input)
            content = data.get("content") or assistant_message

            # Store the clean document text in history instead of raw JSON,
            # otherwise the model starts answering EVERYTHING in JSON.
            messages[-1] = {"role": "assistant", "content": content}

            print("\nAI:\n")
            print(display_text(content))

            if file_type not in ("pdf", "txt", "both"):
                print("\n[!] Unknown file_type, nothing was saved.")
                continue

            number = next_file_number(experiment_folder)
            filename = f"{number}_{sanitize_filename(title)}"

            document = build_document(
                experiment=experiment,
                prompt=user_input,
                response=content,
                response_time=response_time,
                options=options,
                model=model_name
            )

            saved_paths = []

            try:
                if file_type in ("pdf", "both"):
                    pdf_path = os.path.join(experiment_folder, filename + ".pdf")
                    save_pdf(pdf_path, document)
                    saved_paths.append(pdf_path)

                if file_type in ("txt", "both"):
                    txt_path = os.path.join(experiment_folder, filename + ".txt")
                    save_txt(txt_path, document)
                    saved_paths.append(txt_path)

            except Exception as error:
                print(f"\n[!] Failed while saving: {error}")

            if saved_paths:
                print("\nSaved:")
                for path in saved_paths:
                    print(path)

        else:

            # Normal conversation
            print("\nAI:\n")
            print(display_text(assistant_message))


if __name__ == "__main__":
    main()