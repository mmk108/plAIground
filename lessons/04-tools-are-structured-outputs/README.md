# Lesson 4: Tools Are Structured Outputs

> **Business track:** read this page and run the demo. **Builder track:** also do `exercises.md`. New to a word? See the [glossary](../../GLOSSARY.md).

## The idea

A "tool" sounds fancy, but it's two simple things:

1. The model writes a small piece of structured text (JSON) saying what it wants.
2. **Your code** reads it and decides what to do.

> The model never *runs* anything. It only *asks*. Your code decides whether, when, and how.

**Everyday analogy:** a restaurant order slip. The customer writes "1 burger, no onions." The kitchen decides what actually happens. If the slip is smudged, or asks for something not on the menu, the kitchen sends it back.

## What you'll build

A **tool registry**: one list where each tool has a name, a description, validated inputs, and a plain Python function.

| Tool | What it does | Risky? |
|------|--------------|--------|
| `list_files` | Lists the CSV files available | No |
| `group_sum` | Adds up a column, grouped by another ("units by region") | No |
| `send_report` | Emails a report (fake in this lesson) | **Yes** |
| `done_for_now` | Replies to the user | No |

Adding a tool means adding one entry in `starter/tools.py`. The tool list in the prompt is generated from the registry, so the prompt and the code can't drift apart.

## Run it (no account needed)

```powershell
python lessons/04-tools-are-structured-outputs/starter/demo.py "which product sold the most units?"
python lessons/04-tools-are-structured-outputs/starter/demo.py "email the units by region to boss@example.com" --dry-run
python lessons/04-tools-are-structured-outputs/evals/test_tools.py
```

Notice `--dry-run`: the *same* tool call is handled differently. The model asked to send an email, and your code chose to only describe it. That's the point of the lesson: a tool call is a request, not a command.

## Where the pieces live

| File | Role |
|------|------|
| `starter/tools.py` | The registry, validation, parsing, and the plain functions |
| `prompts/system.md` | The prompt, with `{{TOOLS}}` filled in from the registry |
| `starter/demo.py` | One step: sentence in, tool call out, run or dry-run |
| `evals/test_tools.py` | Offline checks |

## Business lens

- **The value:** you can add capabilities one small, testable tool at a time.
- **The risk:** a tool with real-world effects (email, payments, deletes) needs extra control. This is why `risky` exists.
- **Ask your engineers:** which tools can change things, and what stops a wrong call?

## Check yourself

- What does the model actually produce when it "uses a tool"?
- Why is it useful that your code can handle a tool call differently (like a dry run)?
- What should happen when the model asks for a tool that doesn't exist?

Answers: [answers.md](answers.md)

## Ask your assistant

- "Walk me through `parse_tool_call` line by line."
- "Add a `top_n` tool that returns the top N rows of a column, and add tests."

Next: [Lesson 5: Unify Execution State](../05-unify-execution-state/README.md)
