"""
Prompt Logger — Web GUI
-----------------------
A Gradio front-end for prompt_logger.py.

- prompt_logger.py is imported as a library: same CSV, same experiment
  folders, same save mechanism. The CLI still works in parallel —
  this is a second interface to the same engine.
- Arabic renders natively in the browser (bidi + shaping), including
  your own typing. That's why replies are returned RAW here:
  display_text() is for dumb terminals only — never use it in a GUI.

Run:
    pip install gradio
    python app.py
Then open http://127.0.0.1:7860
"""

import os
import time

import gradio as gr
from ollama import chat

import prompt_logger as pl


# ==========================================================
# Choices for the dropdowns
# ==========================================================

def model_choices() -> list:
    """
    Installed models from Ollama, or the default as a fallback
    if the server can't be reached at launch.
    """

    models = [name for name, _ in pl.installed_models()]

    if not models:
        models = [pl.DEFAULT_MODEL]

    return models


def default_model(models: list) -> str:
    """
    Prefer DEFAULT_MODEL if it's installed, else the first entry.
    """

    for name in models:
        if name == pl.DEFAULT_MODEL or name.split(":")[0] == pl.DEFAULT_MODEL:
            return name

    return models[0]


MODELS = model_choices()


# ==========================================================
# Chat handler
# ==========================================================

def respond(message, history, model, experiment, temperature, top_p, max_tokens):
    """
    Called by Gradio on every message.

    history arrives as [{"role": ..., "content": ...}] — exactly the
    format Ollama's chat() expects, so it plugs straight in after one
    cleaning pass: file-download bubbles from earlier saves have
    non-string content, and Ollama only eats strings.
    """

    message = (message or "").strip()

    if not message:
        return ""

    options = pl.DEFAULT_OPTIONS.copy()
    options["temperature"] = temperature
    options["top_p"] = top_p
    options["num_predict"] = int(max_tokens)

    clean_history = [
        {"role": entry.get("role", "assistant"), "content": entry["content"]}
        for entry in history
        if isinstance(entry.get("content"), str)
    ]

    messages = (
        [{"role": "system", "content": pl.SYSTEM_PROMPT}]
        + clean_history
        + [{"role": "user", "content": message}]
    )

    start = time.perf_counter()

    try:
        response = chat(model=model, messages=messages, options=options)
    except Exception as error:
        return f"[!] Could not reach Ollama: {error}"

    response_time = time.perf_counter() - start

    reply = response.message.content.strip()

    pl.log_to_csv(experiment, message, reply, response_time, options, model)

    # ------------------------------------------------------
    # Same save mechanism as the CLI
    # ------------------------------------------------------

    data = pl.parse_json_response(reply)

    if not (data and data.get("save")):
        return reply  # normal conversation

    file_type = str(data.get("file_type", "")).lower()
    title = data.get("title") or pl.sanitize_filename(message)
    content = data.get("content") or reply

    if file_type not in ("pdf", "txt", "both"):
        return content + "\n\n[!] Unknown file_type — nothing was saved."

    folder = os.path.join(pl.SAVE_FOLDER, pl.sanitize_filename(experiment))
    pl.ensure_directory(folder)

    number = pl.next_file_number(folder)
    filename = f"{number}_{pl.sanitize_filename(title)}"

    document = pl.build_document(
        experiment=experiment,
        prompt=message,
        response=content,
        response_time=response_time,
        options=options,
        model=model,
    )

    saved_paths = []

    try:
        if file_type in ("pdf", "both"):
            pdf_path = os.path.join(folder, filename + ".pdf")
            pl.save_pdf(pdf_path, document)
            saved_paths.append(pdf_path)

        if file_type in ("txt", "both"):
            txt_path = os.path.join(folder, filename + ".txt")
            pl.save_txt(txt_path, document)
            saved_paths.append(txt_path)

    except Exception as error:
        return content + f"\n\n[!] Failed while saving: {error}"

    listing = "\n".join(os.path.basename(path) for path in saved_paths)
    folder_rel = os.path.join("saved_responses", pl.sanitize_filename(experiment))

    # Visible in `docker compose logs` / the attached terminal
    print(f"[prompt-logger] saved: {', '.join(saved_paths)}", flush=True)

    return content + f"\n\n---\nSaved to {folder_rel}/\n{listing}"


# ==========================================================
# Interface
# ==========================================================

demo = gr.ChatInterface(
    fn=respond,
    title="Prompt Logger",
    description=(
        "Ollama chat with experiment tracking. Every message is logged to "
        "prompt_log.csv — ask for a PDF or TXT and it lands in the experiment folder."
    ),
    additional_inputs=[
        gr.Dropdown(
            choices=MODELS,
            value=default_model(MODELS),
            label="Model",
        ),
        gr.Dropdown(
            choices=pl.EXPERIMENT_TYPES,
            value="General",
            label="Experiment",
            allow_custom_value=True,  # typing a new name creates a new folder
        ),
        gr.Slider(0.0, 2.0, value=pl.DEFAULT_OPTIONS["temperature"], step=0.1, label="Temperature"),
        gr.Slider(0.0, 1.0, value=pl.DEFAULT_OPTIONS["top_p"], step=0.05, label="Top P"),
        gr.Slider(100, 2000, value=pl.DEFAULT_OPTIONS["num_predict"], step=50, label="Max Tokens"),
    ],
    additional_inputs_accordion="Settings",
)


if __name__ == "__main__":
    # For access from other devices on your home network, use:
    # demo.launch(server_name="0.0.0.0")
    demo.launch()