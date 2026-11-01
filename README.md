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
| `answers.md` | Answers to the "Check yourself" questions |

## Lessons

| # | Lesson | Status |
|---|--------|--------|
| 0 | [Start here](lessons/00-start-here/README.md): what is an agent, setup, tracks | Ready |
| 1 | [Natural language to tool calls](lessons/01-natural-language-to-tool-calls/README.md) | Ready |
| 2 | [Own your prompts](lessons/02-own-your-prompts/README.md) | Ready |
| 3 | [Own your context window](lessons/03-own-your-context-window/README.md) | Ready |
| 4 | [Tools are structured outputs](lessons/04-tools-are-structured-outputs/README.md) | Ready |
| 5 | [Unify execution state](lessons/05-unify-execution-state/README.md) | Ready |
| 6 | [Launch, pause, resume](lessons/06-launch-pause-resume/README.md) | Ready |
| 7-12 | Coming soon | |

New here? Start with [Lesson 0](lessons/00-start-here/README.md). Not sure what a word means? See the [glossary](GLOSSARY.md).

## Setup

**No account needed.** By default every lesson runs on a free, offline **mock model** (a simple rule-based stand-in, not a real AI). To use a real model, set `PROVIDER=github` (free tier) or `PROVIDER=anthropic` (paid) in `.env`.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .
copy .env.example .env   # defaults to the free mock model
python lessons/01-natural-language-to-tool-calls/starter/main.py "what's in sales.csv?"
```

## Use an AI assistant to learn

Open this folder in VS Code with Claude Code or GitHub Copilot. Each lesson has starter prompts to ask your assistant.
