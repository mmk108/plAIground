# Lesson 0: Start Here

## Pick your track

| | Business track | Builder track |
|---|---|---|
| For | Managers, analysts, anyone deciding what to build | Students and anyone who wants to code |
| Do | Read each lesson's README, run the demos, read the "Business lens" | Everything, including `exercises.md` |
| Skip | Writing code | Nothing |

You can switch tracks any time.

## What is an AI agent?

A normal chatbot answers a question. An **agent** can also *do things*: read a file, look something up, send a message. It works in a loop:

```
You ask  ->  AI decides the next step  ->  Your code does it  ->  AI sees the result  ->  repeat until done
```

The AI is the decision-maker. **Your code is the hands**, and it also holds the rules about what's allowed.

Everyday example: "Which region sold the most last quarter?" The agent reads your spreadsheet, adds things up, and tells you.

## Why these lessons?

They're based on [12-factor agents](https://github.com/humanlayer/12-factor-agents), a set of habits for building agents that are reliable instead of flaky. One habit per lesson.

## Setup (about 10 minutes)

1. Install [Python 3.10+](https://www.python.org/downloads/) and [VS Code](https://code.visualstudio.com/).
2. Download this repo and open the folder in VS Code.
3. Open the terminal (Terminal menu, New Terminal) and run:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .
copy .env.example .env
```

(On Mac/Linux: `source .venv/bin/activate` and `cp .env.example .env`.)

4. Try it:

```powershell
python lessons/01-natural-language-to-tool-calls/starter/main.py "what's in sales.csv?"
```

**No account needed.** By default the repo uses a free **mock model**, a simple stand-in that follows rules so you can run every lesson. It is *not* a real AI, so it only handles what the lessons teach.

## Using a real model (optional)

Edit `.env`:

- **GitHub Models** (free tier): `PROVIDER=github` and add a `GITHUB_TOKEN`.
- **Anthropic** (paid): `PROVIDER=anthropic` and add `ANTHROPIC_API_KEY`.

Never share your keys or commit your `.env` file. Students under 18: ask a parent or teacher before creating accounts or adding payment details.

## Using an AI assistant

Open the repo in VS Code with GitHub Copilot or Claude Code and ask things like "Explain `context.py` to me like I'm new to Python." Stuck words? See the [glossary](../../GLOSSARY.md).

Next: [Lesson 1](../01-natural-language-to-tool-calls/README.md)
