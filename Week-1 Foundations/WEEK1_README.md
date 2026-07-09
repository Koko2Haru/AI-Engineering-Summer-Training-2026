# 📘 Week 1 — Foundations of AI Engineering

**AI Engineering Summer Training 2026**
Instructor: **Eng. Abdullah Barghash**
Student: **Alwi** ([koko2haru](https://github.com/koko2haru))

The first week of the program: from *what a token is* to a **Dockerized, Arabic-capable LLM application** by the end. Five days, each building on the last — LLM literacy, prompting, the developer toolchain, prompt patterns, and a full end-to-end mini-project.

---

## 🗺️ The week at a glance

| Day | Focus | Outcome | Deliverable |
|:---:|-------|---------|-------------|
| **1** | Course intro & how LLMs work | Working dev environment + first API call | [`FIRST_API_CALL.md`](Day-1%20LLM%20Setup/FIRST_API_CALL.md) |
| **2** | Prompting fundamentals | A logged 5-prompt comparison | [`DOCKER_TESTING.md`](Day-2%20Prompt%20Fundamentals/DOCKER_TESTING.md) |
| **3** | The AI dev toolchain | A map of the AI dev workflow | [`DIAGRAM.md`](Day-3%20The%20AI%20Development%20Toolchain/DIAGRAM.md) · [🌐 live site](https://koko2haru.github.io/AI-Engineering-Summer-Training-2026/Week-1%20Foundations/Day-3%20The%20AI%20Development%20Toolchain/) |
| **4 & 5** | Prompt patterns + mini-project | A reusable prompt-pattern log → a complete app | [`MINI_CHATBOT.md`](Day-4%20&%205%20Prompt%20Patterns/MINI_CHATBOT.md) · [📦 Prompt Logger](Day-4%20&%205%20Prompt%20Patterns/Prompt_Logger/Helpful_Notes) |

---

## 📅 Day 1 — Course Intro & How LLMs Work

**Focus:** tokens, context windows, temperature; setting up Git, Python, and an LLM API/CLI.
**Skills:** LLM literacy · environment setup.
**Tools:** Git · Python · LLM API/CLI.

**Task:** install the full toolchain (Python, Git, VS Code, an LLM client/API), make the first successful API call, and explain every API parameter — temperature, max tokens, model, and the rest.

This day laid the foundation everything else stands on. Getting Ollama running and making that first call is what made all four later days possible — and understanding the parameters here is exactly what became the tunable settings (`temperature`, `top_p`, `top_k`, `num_predict`, `num_ctx`, `seed`) logged in the Day 4–5 project.

📄 **[FIRST_API_CALL.md](Day-1%20LLM%20Setup/FIRST_API_CALL.md)** — the first API call and parameter breakdown.
Also in the folder: `day1-first_API_call.py` (the code), `outputs.txt`, and `Screenshots/`.

---

## 📅 Day 2 — Prompting Fundamentals

**Focus:** the anatomy of a good prompt; writing five prompts on one task and comparing outputs.
**Skills:** prompt writing · output comparison.
**Tools:** LLM chat / API.

**Task:** write five different prompts that solve the *same* problem, compare the outputs, and explain which prompt performed best and why.

The core deliverable was the notebook `prompts_level.ipynb`. Alongside the main task, the instructor introduced **Docker** as a parallel learning goal — first hands-on exposure to containers, captured in `DOCKER_TESTING.md` and an early `Dockerfile`. That early start paid off directly in Day 4–5, where the mini-project was containerized for real.

📄 **[DOCKER_TESTING.md](Day-2%20Prompt%20Fundamentals/DOCKER_TESTING.md)** — early Docker notes.
Also in the folder: `prompts_level.ipynb` (the five-prompt comparison) and `requirements.txt`.

---

## 📅 Day 3 — The AI Development Toolchain

**Focus:** APIs, CLIs, IDEs, and where the model fits in a real workflow.
**Skills:** toolchain fluency.
**Tools:** API · CLI · IDE.

**Task:** draw the complete AI development workflow — `User → Prompt → LLM → API → Application` — and identify where each tool fits in the pipeline.

Instead of a static diagram, this became an **interactive website**: type a prompt, hit Run, and watch the request travel through all five stages with a terminal-style trace log narrating each hop. Clickable stage panels, plain-language cards for API/CLI/IDE, and tabbed real-world examples (ChatGPT, an AI-powered website, a Python script) — built in pure HTML/CSS/JS with an IBM Plex blueprint aesthetic, then deployed to GitHub Pages.

The deployment itself was a lesson: setting up Pages, finding the right URL, un-freezing a build after the source was pointed at a nonexistent `/docs` folder, and learning why binary files (a PDF) must be *uploaded* rather than pasted as text.

📄 **[DIAGRAM.md](Day-3%20The%20AI%20Development%20Toolchain/DIAGRAM.md)** — project write-up.
📊 **[demo-slides.pdf](Day-3%20The%20AI%20Development%20Toolchain/demo-slides.pdf)** — presentation slides.
🌐 **[Live site](https://koko2haru.github.io/AI-Engineering-Summer-Training-2026/Week-1%20Foundations/Day-3%20The%20AI%20Development%20Toolchain/)** — the interactive pipeline, running on GitHub Pages.
Also in the folder: `index.html`, `css/`, `js/`.

---

## 📅 Day 4 & 5 — Prompt Patterns + Mini-Project

These two days are combined, because the mini-project grew directly out of the Day-4 work into one continuous build.

### Day 4 — Prompt Patterns
**Focus:** few-shot, role prompting, step-by-step reasoning; building a prompt log.
**Skills:** prompt patterns.
**Tools:** LLM API · prompt log.
**Task:** create four prompt templates using **Role Prompting, Few-Shot, Chain-of-Thought, and Structured Output**, and test each on one problem.

### Day 5 — Mini-Project & Review
**Focus:** solve a small task end-to-end using prompting; group review.
**Skills:** applied prompting.
**Tools:** LLM API.
**Task:** solve a real-world problem end-to-end and document the iterations and final solution.

### What was built: the Prompt Logger 🧪

The two tasks merged into one project — a local LLM chat application that treats every conversation as a logged experiment, and lets the model save its answers as PDF/TXT documents on request (a hand-built version of function calling). It started as a single terminal script (`MINI_CHATBOT.md` captures that origin) and grew, over the two days, into:

- a **hardened, tested engine** (16 real bugs found and fixed, 40+ test cases),
- **four prompt-pattern templates** — the Day-4 deliverable — as reusable, documented references,
- full **Arabic support** — terminal display, right-to-left PDF rendering, Arabic filenames,
- **live model selection** that turns the CSV log into a model-comparison tool,
- a **Gradio web GUI** built on the same engine,
- and a **Docker deployment** — putting Day 2's Docker groundwork to real use.

📄 **[MINI_CHATBOT.md](Day-4%20&%205%20Prompt%20Patterns/MINI_CHATBOT.md)** — the mini-project origin notes.
📦 **[Prompt Logger — notes and templates](Day-4%20&%205%20Prompt%20Patterns/Prompt_Logger/Helpful_Notes)** — the complete README: features, architecture, the full problem log, run guides (CLI / GUI / Docker), Arabic support, and the four prompt templates.

---

## 🧵 The through-line

Each day fed the next, which is the point:

- **Day 1's** API parameters → the tunable, logged settings in the Prompt Logger.
- **Day 2's** prompt-comparison mindset → the experiment-tracking core of the logger, *and* its Docker groundwork → the logger's containerization.
- **Day 3's** toolchain understanding → knowing exactly where the LLM, the API, and the app sit in the pipeline being built.
- **Day 4's** prompt patterns → the templates, and the categories the logger organizes experiments by.
- **Day 5** → tying it all into one shipped, documented, running application.

A week that started with "what is a token" and ended with a Dockerized app. 🚀

---

*Part of [AI-Engineering-Summer-Training-2026](https://github.com/koko2haru/AI-Engineering-Summer-Training-2026).*