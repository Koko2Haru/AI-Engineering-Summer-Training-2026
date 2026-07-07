/* ============================================================
   Day 3 · The AI Development Toolchain — interactions
   1) Pipeline simulation with a live trace log
   2) Clickable stage details
   3) "Pipeline in the wild" example tabs
   ============================================================ */

// ---------- data ----------

const STAGE_ORDER = ["user", "prompt", "llm", "api", "app"];

const STAGES = {
  user: {
    title: "01 · User",
    what: "Everything starts with a human and a goal — a question, a task, a problem. The user never sees models or servers; they see an input box and expect an answer.",
    ex: "Me, opening a chat app and typing: \u201cfix this Python error.\u201d",
    tools: "None — this step is human. But it defines what every other step has to deliver."
  },
  prompt: {
    title: "02 · Prompt",
    what: "The goal becomes text the model can work with: the user's words, plus (often) hidden instructions the app adds behind the scenes — tone, format, extra context.",
    ex: "In ChatGPT, your message travels together with a system prompt you never see.",
    tools: "When the prompt is part of a program, it's written in the IDE — a prompt is just a string until the pipeline moves it."
  },
  llm: {
    title: "03 · LLM",
    what: "The Large Language Model reads the prompt as tokens and generates a response one token at a time, using patterns it learned in training. GPT, Claude and Gemini all live at this stage.",
    ex: "The model turns \u201cexplain APIs simply\u201d into an actual explanation, word by word.",
    tools: "Hosted by the provider — I don't run the model myself, I reach it through the API."
  },
  api: {
    title: "04 · API",
    what: "The bridge, in both directions. My application sends the prompt to the provider as an HTTP request (with an API key), and the model's answer travels back as JSON.",
    ex: "A POST request to the provider's endpoint \u2192 a 200 OK with the answer inside.",
    tools: "This stage IS the API — and the CLI is where I test it while building, e.g. with curl."
  },
  app: {
    title: "05 · Application",
    what: "The finished product takes the raw JSON answer and turns it into something a person actually uses: a chat bubble, a summary on a webpage, a printed result in the terminal.",
    ex: "ChatGPT's interface, a store's support widget, or the output of my own Python script.",
    tools: "Built in the IDE, run and deployed from the CLI — this is where all the tools meet."
  }
};

const EXAMPLES = {
  chatgpt: {
    rows: [
      ["User", "You, in the browser"],
      ["Prompt", "Your message (+ hidden system instructions)"],
      ["LLM", "A GPT model in OpenAI's data center"],
      ["API", "OpenAI's own API connects the web app to the model"],
      ["Application", "The chat interface at chatgpt.com"]
    ],
    note: "It feels like one magic box, but it's the same five hops — OpenAI just built every one of them for you. You only ever touch step 01."
  },
  website: {
    rows: [
      ["User", "A customer on an online store"],
      ["Prompt", "Their question + product info the site adds automatically"],
      ["LLM", "Claude / GPT, hosted by the model provider"],
      ["API", "The site's backend calls the provider's API over HTTPS"],
      ["Application", "The support chat widget on the page"]
    ],
    note: "Same five hops, different owner: the site builds steps 02, 04 and 05 itself, and rents step 03 through the API."
  },
  python: {
    rows: [
      ["User", "Me, running  python summarize.py"],
      ["Prompt", "A string variable inside my code"],
      ["LLM", "The provider's model, reached over the internet"],
      ["API", "requests.post(...) with my API key"],
      ["Application", "The script itself — it prints the answer"]
    ],
    note: "The pipeline at its most visible — every hop is a line of code I wrote.",
    code: [
      { t: "import requests", c: false },
      { t: "", c: false },
      { t: "prompt = \"Summarize this article in 3 lines\"   ", c: false, tail: "# 02 Prompt" },
      { t: "", c: false },
      { t: "r = requests.post(                             ", c: false, tail: "# 04 API" },
      { t: "    \"https://api.model.com/v1/messages\",", c: false },
      { t: "    headers={\"x-api-key\": KEY},", c: false },
      { t: "    json={\"prompt\": prompt},                   ", c: false, tail: "# 03 \u2192 LLM" },
      { t: ")", c: false },
      { t: "", c: false },
      { t: "print(r.json()[\"answer\"])                      ", c: false, tail: "# 05 Application" }
    ]
  }
};

// ---------- helpers ----------

const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => Array.from(document.querySelectorAll(sel));
const wait = (ms) => new Promise((r) => setTimeout(r, ms));
const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

// ---------- stage detail panel ----------

const stageButtons = $$(".stage");

function selectStage(id) {
  stageButtons.forEach((b) => b.classList.toggle("is-active", b.dataset.stage === id));
  const s = STAGES[id];
  $("#detailTitle").textContent = s.title;
  $("#detailWhat").textContent = s.what;
  $("#detailEx").textContent = s.ex;
  $("#detailTools").textContent = s.tools;
}

stageButtons.forEach((btn) => {
  btn.addEventListener("click", () => selectStage(btn.dataset.stage));
});

selectStage("user"); // default

// ---------- simulation ----------

const traceBody = $("#traceBody");
const runBtn = $("#runBtn");
const arrows = $$(".arrow");
let running = false;

function logLine(tag, text, ok = false) {
  const p = document.createElement("p");
  if (tag) {
    const span = document.createElement("span");
    span.className = "t-tag";
    span.textContent = tag;
    p.appendChild(span);
  }
  const rest = document.createElement("span");
  if (ok) rest.className = "t-ok";
  rest.textContent = text;
  p.appendChild(rest);
  traceBody.appendChild(p);
}

async function runSimulation(promptText) {
  if (running) return;
  running = true;
  runBtn.disabled = true;

  // reset
  traceBody.innerHTML = "";
  stageButtons.forEach((b) => b.classList.remove("is-lit"));
  arrows.forEach((a) => a.classList.remove("is-lit"));

  const shown = promptText.length > 46 ? promptText.slice(0, 46) + "\u2026" : promptText;
  const delay = reducedMotion.matches ? 0 : 620;

  const steps = [
    { stage: "user",   tag: "[01 user]",   text: "intent captured \u2014 someone wants an answer" },
    { stage: "prompt", tag: "[02 prompt]", text: "\"" + shown + "\" packed into a request" },
    { stage: "llm",    tag: "[03 llm]",    text: "tokens in \u2192 tokens out \u00b7 model is thinking\u2026" },
    { stage: "api",    tag: "[04 api]",    text: "answer returned as JSON \u00b7 200 OK" },
    { stage: "app",    tag: "[05 app]",    text: "rendered on screen for the user" }
  ];

  logLine("", "> run", true);

  for (let i = 0; i < steps.length; i++) {
    await wait(delay);
    if (i > 0) arrows[i - 1].classList.add("is-lit");
    const btn = stageButtons.find((b) => b.dataset.stage === steps[i].stage);
    if (btn) btn.classList.add("is-lit");
    logLine(steps[i].tag, steps[i].text);
  }

  await wait(delay);
  const secs = (1 + Math.random() * 0.9).toFixed(2);
  logLine("", "\u2713 pipeline complete in " + secs + "s", true);

  running = false;
  runBtn.disabled = false;
}

$("#simForm").addEventListener("submit", (e) => {
  e.preventDefault();
  const input = $("#promptInput");
  const text = input.value.trim() || input.placeholder;
  runSimulation(text);
});

// ---------- example tabs ----------

const tabPanel = $("#tabPanel");
const tabButtons = $$(".tab");

function renderExample(key) {
  const ex = EXAMPLES[key];
  tabPanel.innerHTML = "";

  ex.rows.forEach(([k, v]) => {
    const row = document.createElement("div");
    row.className = "map-row";
    const kEl = document.createElement("span");
    kEl.className = "k";
    kEl.textContent = k;
    const vEl = document.createElement("span");
    vEl.textContent = v;
    row.append(kEl, vEl);
    tabPanel.appendChild(row);
  });

  if (ex.code) {
    const pre = document.createElement("pre");
    ex.code.forEach((line) => {
      pre.appendChild(document.createTextNode(line.t));
      if (line.tail) {
        const c = document.createElement("span");
        c.className = "c";
        c.textContent = line.tail;
        pre.appendChild(c);
      }
      pre.appendChild(document.createTextNode("\n"));
    });
    tabPanel.appendChild(pre);
  }

  const note = document.createElement("p");
  note.className = "map-note";
  note.textContent = ex.note;
  tabPanel.appendChild(note);
}

tabButtons.forEach((btn) => {
  btn.addEventListener("click", () => {
    tabButtons.forEach((b) => {
      b.classList.toggle("is-on", b === btn);
      b.setAttribute("aria-selected", b === btn ? "true" : "false");
    });
    renderExample(btn.dataset.ex);
  });
});

renderExample("chatgpt"); // default