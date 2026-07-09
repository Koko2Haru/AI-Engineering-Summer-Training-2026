# Prompt Logger — GUI container
# Architecture: Ollama stays on the host (keeps GPU + already-pulled models);
# this container runs only the Python app and reaches out via OLLAMA_HOST.

FROM python:3.12-slim

WORKDIR /app

# Arabic font for PDF generation, shipped with the project (SIL OFL license).
# COPY creates the target directories automatically — this exact path is
# what ARABIC_FONT_CANDIDATES in prompt_logger.py expects. No apt needed.
COPY Amiri-Regular.ttf /usr/share/fonts/opentype/fonts-hosny-amiri/Amiri-Regular.ttf

# Dependencies first: this layer only rebuilds when requirements.txt changes,
# so code edits rebuild in seconds instead of re-downloading everything.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# The code: the engine + the GUI
COPY prompt_logger.py app.py ./

# host.docker.internal = the machine running Docker (your PC)
ENV OLLAMA_HOST=http://host.docker.internal:11434
# Bind on all interfaces so the mapped port is reachable from outside the container
ENV GRADIO_SERVER_NAME=0.0.0.0
# All CSV + saved files go to the mounted volume
ENV PROMPT_LOGGER_DATA=/data

EXPOSE 7860

CMD ["python", "app.py"]