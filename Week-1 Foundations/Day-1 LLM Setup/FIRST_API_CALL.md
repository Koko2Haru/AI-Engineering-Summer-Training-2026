# 🚀 Day 1 - LLM Setup

This document summarizes the concepts and tasks completed during **Day 1** of the AI Engineering Summer Training.

---

# 🎯 Objectives

The goal of Day 1 was to:

- Set up the development environment.
- Install the required tools.
- Run a local Large Language Model (LLM).
- Make the first API call using Python.
- Understand the basic model parameters.

---

# 🛠️ Environment Setup

The following tools were installed and configured:

- Python
- VS Code
- Ollama
- Virtual Environment (`.venv`)
- Jupyter Notebook

---

# 🤖 Running a Local LLM

Downloaded and tested local models using Ollama.

Models used:

- `llama3.2`
- `gemma3:4b`

Verified the installation by listing the available models and successfully running the model locally.

---

# 💻 First API Call

Created the first Python program using the Ollama Python library.

The application:

- Sends a prompt to the model.
- Receives the generated response.
- Prints the response to the terminal.

Example workflow:

```text
User Prompt
      │
      ▼
Ollama API
      │
      ▼
LLM (llama3.2)
      │
      ▼
Generated Response
```

---

# ⚙️ Model Parameters

Learned the purpose of the following generation parameters:

| Parameter | Purpose |
|-----------|---------|
| `temperature` | Controls randomness and creativity. |
| `top_p` | Limits token selection based on probability. |
| `top_k` | Restricts the number of candidate tokens. |
| `repeat_penalty` | Reduces repetitive responses. |
| `num_predict` | Maximum number of generated tokens. |
| `num_ctx` | Context window size remembered by the model. |
| `seed` | Produces reproducible outputs. |

---

# 💬 Building a Chat Loop

Extended the basic example into a simple conversational chatbot by:

- Accepting user input.
- Sending multiple prompts.
- Preserving conversation history.
- Exiting gracefully using commands such as `exit` or `quit`.

---

# 📚 Key Takeaways

By the end of Day 1, I was able to:

- ✅ Configure a local AI development environment.
- ✅ Run local LLMs using Ollama.
- ✅ Connect Python to an LLM.
- ✅ Generate responses programmatically.
- ✅ Understand the most important generation parameters.
- ✅ Build a simple interactive chatbot.

---

# 📁 Files Created

Examples completed during Day 1 include:

- `day1_firstAPIcall.py`
- Chatbot example
- Jupyter Notebook exercises

---

# 📝 Summary

Day 1 focused on building the foundation required for the rest of the training.

With the environment fully configured and the first local LLM successfully running, the project is now ready for more advanced topics such as prompt engineering, retrieval, model deployment, and AI application development.