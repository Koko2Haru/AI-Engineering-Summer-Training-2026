# 🧰 Day 3 — The AI Development Toolchain

**AI Engineering Summer Training 2026 · Week 1 · Day 3**

An interactive website built as the Day 3 deliverable — instead of a static
markdown file, the tasks are presented as a live, clickable page.

🔗 **Live demo:** [Open the interactive site](https://koko2haru.github.io/AI-Engineering-Summer-Training-2026/Week-1%20Foundations/Day-3%20The%20AI%20Development%20Toolchain/)

---

## 📋 The Task

Day 3 covered APIs, CLIs, IDEs, and where the model fits in a real workflow:

1. **Explore the tools** — explain API, CLI, and IDE in my own words
2. **Draw the workflow** — diagram `User → Prompt → LLM → API → Application`,
   explain what happens at each step, and map it to practical examples
   (ChatGPT, a website using AI, a Python script calling an API)

## 💡 The Approach

Rather than just describing the pipeline, the site **demonstrates** it:
you type a prompt, press **Run**, and watch the request travel through all
five stages while a terminal-style trace log narrates every hop.

## ✨ What the Site Includes

| Section | What it does |
|---------|--------------|
| **Live pipeline simulator** | Animates a request through `User → Prompt → LLM → API → Application` with a trace log |
| **Stage details** | Click any stage to see what happens there, a real-world example, and which tools touch it |
| **Task 1 — The tools** | Plain-language cards for API, CLI, and IDE, each with a "where it fits" note |
| **Task 2 — Examples** | Tabs mapping the same five stages onto ChatGPT, an AI-powered website, and a Python script (with labeled code) |

## 🗂️ Project Structure

```
Day-3 AI dev toolchain\
├── index.html        → page structure & content
├── css\
│   └── styles.css    → design system (IBM Plex, blueprint-on-paper look)
├── js\
│   └── script.js     → simulation, stage details, example tabs
└── DIAGRAM.md         → this file
```

## ▶️ How to Run

No installs, no build step — it's a static site:

1. Double-click `index.html` (opens in any modern browser), **or**
2. Drag the whole folder onto [Netlify Drop](https://app.netlify.com/drop)
   to get a live, shareable link

## 🛠️ Built With

- **HTML / CSS / JavaScript** — no frameworks, no dependencies
- **IBM Plex Sans & Mono** via Google Fonts (falls back to system fonts offline)
- Responsive layout, keyboard-accessible, respects reduced-motion settings

## 🧠 The Concepts in One Breath

- **API** — the messenger between my code and someone else's service:
  requests go in, JSON answers come back
- **CLI** — talking to the computer in text: install, run, and test from one line
- **IDE** — the workshop where the application (and its prompts and API calls)
  gets written
- **The pipeline** — a user's goal becomes a prompt, the LLM generates an answer,
  the API carries it both ways, and the application delivers it to a human

---

*Built by Ali — Week 1, Day 3.*