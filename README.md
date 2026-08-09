# 🤖 AI Engineering Summer Training 2026

[![Progress](https://img.shields.io/badge/progress-6%2F7%20weeks-blue)]()
[![Status](https://img.shields.io/badge/status-in%20progress-yellow)]()
[![Made with](https://img.shields.io/badge/made%20with-Python%20%7C%20Claude%20%7C%20n8n-informational)]()

A running log of a **7-week AI Engineering Summer Training Program** — LLMs, prompt engineering, AI-assisted development, Claude Skills, agentic AI, and workflow automation, learned through daily hands-on exercises and shipped mini-projects (not just notes).

Alongside the program itself, I have also been juggling **4+ personal projects, a hackathon win, and a stack of parallel certifications** — see [Side Hustles](#-side-hustles--beyond-the-curriculum) below.

---

## Table of Contents

- [Roadmap](#-roadmap)
- [Side Hustles — Beyond the Curriculum](#-side-hustles--beyond-the-curriculum)
- [Technologies](#-technologies)
- [Repository Structure](#-repository-structure)
- [Goal](#-goal)

---

## 🗺 Roadmap

| Week | Topic | Status | Details |
|:----:|-------|:------:|---------|
| 1 | Foundations of AI Engineering | ✅ Done | [Week 1 README](Week-1%20Foundations/WEEK1_README.md) |
| 2 | AI-Assisted Development — *CoinQuest* | ✅ Done | [Week 2 README](Week-2-AI-Assisted-Development/WEEK2-README.md) |
| 3 | Markdown for AI — *Coddiction* | ✅ Done | [Week 3 README](Week-3-Writing-md-Files-to-AI/WEEK3-README.md) |
| 4 | Claude Skills — *cv-reviewer → cv-optimizer* | ✅ Done | [Week 4 README](Week-4-Using-and-Building-Claude-Skills/WEEK4-README.md) |
| 5 | Agentic AI | ✅ Done | [Week 5 README](/Week-5-Agentic-AI-Fundamentals/WEEK5-README.md) |
| 6 | n8n Automation | 🛠️ Working on it | *`Week 6 README`* |
| 7 | Capstone Project | ⏳ Upcoming | — |

<details>
<summary><strong>📅 Week 1 — Foundations of AI Engineering</strong></summary>

| Day | Topic | What happened | Status | Link |
|:---:|-------|----------------|:------:|------|
| 1 | LLM Setup | Set up Python/VS Code/Ollama, ran a local LLM, and made the first API call while learning basic model parameters. | ✅ Done | [FIRST_API_CALL.md](Week-1%20Foundations/Day-1%20LLM%20Setup/FIRST_API_CALL.md) |
| 2 | Prompting Fundamentals | Dockerized a Jupyter notebook (`prompts_level.ipynb`) and verified it actually executes prompt-engineering exercises inside the container, not just locally. | ✅ Done | [DOCKER_TESTING.md](Week-1%20Foundations/Day-2%20Prompt%20Fundamentals/DOCKER_TESTING.md) |
| 3 | The AI Development Toolchain | Instead of a static write-up, built a **live interactive site** that animates a prompt traveling through `User → Prompt → LLM → API → Application`, explaining APIs, CLIs, and IDEs along the way. | ✅ Done | [DIAGRAM.md](Week-1%20Foundations/Day-3%20The%20AI%20Development%20Toolchain/DIAGRAM.md) |
| 4 & 5 | Mini-ChatBot (mini-project) | Built a local Ollama chat app that logs every prompt/response/parameter to CSV, lets the model trigger PDF/TXT saving via a hand-built function-calling pattern, supports Arabic end-to-end (terminal, PDFs, filenames), and ships as CLI + Gradio GUI, fully Dockerized. | ✅ Done | [MINI_CHATBOT.md](Week-1%20Foundations/Day-4%20&%205%20Prompt%20Patterns/MINI_CHATBOT.md) |

</details>

<details>
<summary><strong>📅 Week 2 — AI-Assisted Development (project: CoinQuest)</strong></summary>

| Day | Topic | What happened | Status | Link |
|:---:|-------|----------------|:------:|------|
| 1 | Vibe-Coding-Start | Spent ~3 hours researching, longlisted 19 project ideas, and picked **CoinQuest** — a gamified finance tracker with enough real logic to support a full week of build → review → debug → ship. | ✅ Done | [SPECS.md](Week-2-AI-Assisted-Development/Day-1-Vibe-Coding-Start/SPECS.md) |
| 2 | Building with an AI Partner | Shipped CoinQuest v0.1: a FastAPI + SQLite thin vertical slice, using **two Claude instances in different roles** — one as architect, one as hands-on builder. | ✅ Done | [SKELETON-V01.md](Week-2-AI-Assisted-Development/Day-2-Building-with-an-AI-Partner/SKELETON-V01.md) |
| 3 | Reading AI-Written Code | Reviewed the AI-generated v0.1 line by line and found **10 improvements** (readability, efficiency, correctness, plus a security hole and a deprecated API), documented the plan, then had Claude Code apply it file-by-file. | ✅ Done | [COINQUEST-V02.md](Week-2-AI-Assisted-Development/Day-3-Reading-AI-Written-Code/COINQUEST-V02.md) |
| 4 | Debugging with AI | Planted **8 deliberate bugs** across 3 difficulty tiers (easy/medium/hard) and debugged them with Claude Code using **symptoms only** — never revealing bug locations. | ✅ Done | [REVIEW.md](Week-2-AI-Assisted-Development/Day-4-Debugging-with-AI/REVIEW.md) |
| 5 | Polishing and Shipping | Took CoinQuest from a plain, functional v0.5 to a fully gamified finance RPG (v1.0) with XP, a "Damage History" log, and a real UI — one focused Claude Code session per upgrade. | ✅ Done | [COINQUEST-V10.md](Week-2-AI-Assisted-Development/Day-5-Polishing-and-Shipping/COINQUEST-V10.md) |

</details>

<details>
<summary><strong>📅 Week 3 — Markdown for AI (project: Coddiction)</strong></summary>

| Day | Topic | What happened | Status | Link |
|:---:|-------|----------------|:------:|------|
| 1 | Why Structure Matters | Scoped a new project, **Coddiction** (a shrunk-down LeetCode-style site), and converted an unstructured description into clean, machine-readable Markdown. | ✅ Done | [DAY1-REPORT.md](Week-3-Writing-md-Files-to-AI/Day-1-Why-Structure-Matters/DAY1-REPORT.md) |
| 2 | Context Engineering | Wrote `CONTEXT.md` — everything an AI needs *around* the task (no build instructions) so it stops guessing at libraries, scope, and edge cases. | ✅ Done | [DAY2-REPORT.md](Week-3-Writing-md-Files-to-AI/Day-2-Context-Engineering/DAY2-REPORT.md) |
| 3 | Writing Clear Specs | Turned vague requirements ("there's a timer," "you get points") into an unambiguous `SPEC.md` with exact formulas, scoring, and verdict-priority rules. | ✅ Done | [DAY3-REPORT.md](Week-3-Writing-md-Files-to-AI/Day-3-Writing-Clear-Specs/DAY3-REPORT.md) |
| 4 | System Prompts & Documentation | Wrote two documents for the same project aimed at two different readers: a human-facing `README.md` and a rule-enforcing `system-prompt.txt` for an AI collaborator. | ✅ Done | [DAY4-REPORT.md](Week-3-Writing-md-Files-to-AI/Day-4-System-Prompts-&-Documentations/DAY4-REPORT.md) |
| 5 | Test & Iterate | Ran fresh AI sessions against the spec repeatedly, scored each rebuild against an acceptance checklist, and iterated the docs until output was consistent. | ✅ Done | [DAY5-REPORT.md](Week-3-Writing-md-Files-to-AI/Day-5-Test-&-Iterate/DAY5-REPORT.md) |

</details>

<details>
<summary><strong>📅 Week 4 — Claude Skills (built: cv-reviewer → cv-optimizer)</strong></summary>

| Day | Topic | What happened | Status | Link |
|:---:|-------|----------------|:------:|------|
| 1 | What is a Skill | Analyzed three existing Claude Skills and wrote up when each should trigger and what problem it solves. | ✅ Done | [DAY1-REPORT.md](Week-4-Using-and-Building-Claude-Skills/Day-1-What-is-a-skill/DAY1-REPORT.md) |
| 2 | Using Existing Skills | Ran those skills against real personal inputs (the actual CoinQuest backlog, real documents) and compared results to what each skill promises. | ✅ Done | [DAY2-REPORT.md](Week-4-Using-and-Building-Claude-Skills/Day-2-Using-Existing-Skills/DAY2-REPORT.md) |
| 3 | The SKILL.md File | Designed a first-draft, annotated `SKILL.md` template — folder layout, frontmatter, `references/`, `scripts/`, `assets/`. | ✅ Done | [DAY3-REPORT.md](Week-4-Using-and-Building-Claude-Skills/Day-3-The-SKILL-md-Structure/DAY3-REPORT.md) |
| 4 | Build Your Own Skill | Built a complete, production-quality skill from scratch: **cv-reviewer**, an AI CV/Resume reviewer with a scoring rubric, ATS rules, and a common-mistakes checklist. | ✅ Done | [DAY4-REPORT.md](Week-4-Using-and-Building-Claude-Skills/Day-4-Build-Your-Own-Skill/DAY4-REPORT.md) |
| 5 | Test and Chain Skills | Built a second skill, **cv-optimizer**, that consumes `cv-reviewer`'s output and rewrites the resume without fabricating anything, then proved the two-skill pipeline end-to-end. | ✅ Done | [DAY5-REPORT.md](Week-4-Using-and-Building-Claude-Skills/Day-5-Test-and-Chain-Skills/DAY5-REPORT.md) |

</details>

<details>
<summary><strong>📅 Week 5 — Agentic AI (project: Star Gazer)</strong></summary>

| Day | Topic | What happened | Status | Link |
|:---:|-------|----------------|:------:|------|
| 1 | Agents vs. chatbots / the ReAct loop | designed Star Gazer, wrote the agent design doc and Day 1 report, made both diagrams, and confirmed your Gemini vision API works with a real test photo — cleaned up next with structured JSON output and caching. You're set for Day 2. | ✅ Done | [DAY1-REPORT.md](/Week-5-Agentic-AI-Fundamentals/Day-1-Agents-vs-Chatbots/DAY1-REPORT.md) |
| 2 | Tool use / function calling | built basic_agent.py, a single-tool agent using Gemini vision with real function calling. Fixed the .env loading bug, ran it against 5 real photos, and confirmed the loop worked correctly — it called the tool the right number of times on its own and correctly said there was no shared theme across unrelated photos instead of making one up. | ✅ Done | [DAY2-REPORT.md](/Week-5-Agentic-AI-Fundamentals/Day-2-Tool-Use-and-Function-Calling/DAY2-REPORT.md) |
| 3 | Adding tools & memory | added the second tool (propose_constellation, validated by code before it's accepted) and persistent memory. Ran it against 10 real photos — it correctly caught a duplicate, correctly grouped the 6 people-photos, and correctly left 4 unrelated ones alone instead of forcing a theme. Then proved memory across two separate runs: told it the butterfly and strawberry were from your garden, re-ran organize, and it built "My Garden Wonders" using that reasoning without you repeating it. Also caught and reported honestly that "The Social Circle" is a shallow grouping — a real finding, not swept under the rug. | ✅ Done | [DAY3-REPORT.md](/Week-5-Agentic-AI-Fundamentals/Day-3-Adding-Tools-and-Memory/DAY3-REPORT.md) |
| 4 | Planning & task decomposition | expanded to 20 photos with real thematic variety, hit and fixed a rate-limit issue with prewarm_cache.py, then ran the full multi-step organize pass. It described all 20 photos, then proposed 4 constellations in one clean pass with zero rejections — two of them (Fruit Still Lifes, Friends of Furry Kind) genuinely well-reasoned, one (Friends and Gatherings) repeating the same shallow "category not memory" pattern flagged in Day 3. | ✅ Done | [DAY4-REPORT.md](/Week-5-Agentic-AI-Fundamentals/Day-4-Planning-and-Decomposition/DAY4-REPORT.md) |
| 5 | Failure modes & guardrails | Built and tested three guardrails against real failure modes from earlier days. Two passed clean: the agent correctly refused to re-propose constellations that already existed, and correctly declined to force a theme onto random unrelated photos. The third failed — after a simulated photo failure, the agent's summary claimed all 20 photos were processed, when one had actually errored out. Only an external check caught the false claim; the agent had no way to catch its own dishonesty. Chose to report that gap honestly instead of quietly patching it. | ✅ Done  | [DAY5-REPORT.md](/Week-5-Agentic-AI-Fundamentals/Day-5-Failure-Modes-and-Guardrails/DAY5-REPORT.md) |

</details>

<details open>
<summary><strong>📅 Week 6 — n8n Automation (project: jobber - personalized-automated freelance job looker)</strong></summary>

| Day | Topic | What happened | Status | Link |
|:---:|-------|----------------|:------:|------|
| 1 | Automation foundations & intro to n8n | Built the first n8n workflow and the data spine of FreelanceScout: a scheduled workflow that pulls 50 live freelance projects from the Freelancer.com API every morning, splits them into individual items, normalizes them into 8 clean columns, and appends them to Google Sheets. Verified it running unattended, then exported it and wrote it up. | ✅ Done | [DAY1-REPORT.md](/Week-6-Automation-and-Orchestration-with-n8n/Day-1-Automation-Foundations-and-Intro-to-n8n/DAY1-REPORT.md)|
| 2 | Connecting tools & APIs | Connected three external APIs and two tools into a single n8n workflow — Freelancer.com and Arbeitnow as job sources, a live exchange-rate API to make their budgets comparable, then Google Sheets to store and Gmail to notify. Also closed out the duplication bug Day 1 exposed, and tested four candidate APIs before picking the second source instead of guessing. | ✅ Done | [DAY2-REPORT.md](/Week-6-Automation-and-Orchestration-with-n8n/Day-2-Connecting-Tools-and-APIs-in-n8n/DAY2-REPORT.md) |
| 3 | AI workflows & the AI Agent node | Turned FreelanceScout from a job scraper into the actual product. Built a 15-node workflow that reads a CV from Google Drive, extracts a skill profile with Gemini, scores all 64 collected gigs against it with DeepSeek, and writes tailored pitches for the top 5 with Llama 3.3 on Groq — three chained LLM steps, three different models, each one feeding the next. Also built a fully synthetic CV as the test fixture so nothing personal goes to third-party APIs. | ✅ Done | [DAY3-REPORT.md](/Week-6-Automation-and-Orchestration-with-n8n/Day-3-AI-Workflows-and-Chaining-Agents/DAY3-REPORT.md) |
| 4 | Error handling & human-in-the-loop | Hardened Day 3's matching chain and put a human in front of the only step that changes anything. Added three layers of failure handling — retries, error branches, and a separate Error Trigger workflow — plus a Gmail approval gate, taking it from 15 nodes to 22. Then tested all four paths for real: approve, decline, a handled API failure, and an unhandled crash. | ✅ Done | [DAY4-REPORT.md](/Week-6-Automation-and-Orchestration-with-n8n/Day-4-Error-Handling-and-Human-in-The-Loop/DAY4-REPORT.md) |
| 5 | Build an automation | — | ⏳ | — |

</details>

<details>
<summary><strong>📅 Week 7 — Capstone: Agentic AI Application</strong> (upcoming)</summary>

| Milestone | What happened | Status | Link |
|-----------|----------------|:------:|------|
| Project Planning | — | ⏳ | — |
| Build & Integrate | — | ⏳ | — |
| Testing & Evaluation | — | ⏳ | — |
| Documentation | — | ⏳ | — |
| Demo Day | — | ⏳ | — |

</details>

---

## 🚀 Side Hustles — Beyond the Curriculum

This training hasn't happened in a vacuum — it's been running in parallel with several other things:

- 🏆 **Hackathon — KANZ-AI:** Won. *(Project details are gonna be in another repository)*
  - **AI tools used:** Replit, Claude, NotebookLM, Mini Studio, Magnific, ElevenLabs, HeyGen, Suno, n8n
- 🛠 **4+ personal projects** — in progress alongside the daily coursework. *(Projects details kept private for now.)*
- 🎓 **Many courses completed through:**
  - Udemy (online) — `[NLP / ML]`
  - Coursera (online) — `[LLM's / Chatbots]`
  - IBM SkillsBuild (online) — `[Agentic AI / Automation]`
- ☁️ **Cloud Computing Workshop** (in person) — `[Google Developer Group - GDG]`

---

## 🛠 Technologies

| Category | Tools |
|----------|-------|
| Language | Python, JavaScript |
| Web | HTML, CSS |
| LLM Runtime | Ollama, Llama 3.2 |
| Notebooks | Jupyter Notebook, Google Colab |
| AI Tooling | Claude, Claude Code, Claude Skills |
| Automation | n8n |
| Containers | Docker, Docker Compose |
| Version Control | Git, GitHub |
| Editor | VS Code |

---

## 📌 Repository Structure

```
AI-Engineering-Summer-Training-2026/
│
├── README.md
├── Week-1 Foundations/
├── Week-2-AI-Assisted-Development/
├── Week-3-Writing-md-Files-to-AI/
├── Week-4-Using-and-Building-Claude-Skills/
├── Week-5-Agentic-AI/            
├── Week-6-n8n-Automation/      
└── Week-7-Capstone-Project/      (coming soon)
```

---

## 🎯 Goal

By the end of this program, this repository will contain all notebooks, projects, and exercises completed throughout the training — a full record of hands-on progress in AI Engineering, from first API call to a shipped capstone project.

---

⭐ Follow along as this repository grows week by week.
