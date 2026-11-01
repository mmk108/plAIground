# plAIground

Learn to build AI agents, one lesson at a time. Think *Automate the Boring Stuff with Python*, but for agents: everyday tasks like reading a spreadsheet or pulling text from a web page, explained in plain language, with starter Python code you can run and make your own.

Based on the [12-factor agents](https://github.com/humanlayer/12-factor-agents) principles.

## How it works

Each folder in `lessons/` is one principle:

| File | Purpose |
|------|---------|
| `README.md` | The idea in simple language, with an example |
| `starter/` | Minimal runnable code |
| `prompts/` | The prompt, kept as its own file |
| `evals/` | Test cases to measure how well it works |
| `exercises.md` | Ways to customize it |

## Lessons

| # | Lesson | Status |
|---|--------|--------|
| 1 | [Natural language to tool calls](lessons/01-natural-language-to-tool-calls/README.md) | Ready |
| 2 | [Own your prompts](lessons/02-own-your-prompts/README.md) | Ready |
| 3 | [Own your context window](lessons/03-own-your-context-window/README.md) | Ready |
| 4-12 | Coming soon | |

## Setup

You can read every lesson without an account. To **run** the code you need an API key from one provider:

- **Anthropic** (Claude Sonnet): paid, cheap for these lessons.
- **GitHub Models**: free tier, uses a GitHub token.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .
copy .env.example .env   # then fill in your key
python lessons/01-natural-language-to-tool-calls/starter/main.py "what's in sales.csv?"
```

## Use an AI assistant to learn

Open this folder in VS Code with Claude Code or GitHub Copilot. Each lesson has starter prompts to ask your assistant.
