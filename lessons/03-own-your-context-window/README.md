# Lesson 3: Own Your Context Window

> **Business track:** read this page and run the demo. **Builder track:** also do `exercises.md`. New to a word? See the [glossary](../../GLOSSARY.md).

## The idea

The model remembers nothing between calls. Every time, it gets one block of text: "here's everything that happened so far, what's next?" That block is the **context window**, and you build it.

> Better input, better output. You decide what goes in, what stays out, and how it's formatted.

**Everyday analogy:** you're briefing a colleague who just walked in. You wouldn't hand over a 100,000-row spreadsheet, a customer's card number, and last week's resolved mistakes. You'd give a clean summary.

## What you'll build

`starter/context.py` turns a list of events into the text the model sees, with three habits:

1. **Redact** sensitive data (card numbers, emails) before the model sees it.
2. **Truncate** huge results so they don't flood the window.
3. **Hide resolved errors** so old mistakes don't clutter or mislead.

## Run it (no API key needed)

```powershell
python lessons/03-own-your-context-window/starter/demo.py
python lessons/03-own-your-context-window/evals/test_context.py
```

The demo prints the raw customer file, then the context the model would receive. Compare them. Add `--ask` to send it to a real model.

## Important limits

Regex redaction is a starting point, not a guarantee. It can miss names, addresses, or odd formats. For real sensitive data, drop the columns you don't need entirely and test your redaction.

## Business lens

- **The value:** you control exactly what data leaves your systems. That is the foundation of privacy and compliance.
- **The risk:** anything in the context is sent to the model provider. Redaction must happen *before* the call, and regex alone isn't enough for regulated data.
- **Ask your engineers:** what data reaches the model, and how is it tested?

## Check yourself

Answers: [answers.md](answers.md)

- What would you do before putting a 100,000-row file in the context?
- Why hide an error once it's fixed? When should you keep it?
- Why redact before the model sees data instead of asking the model to ignore it?

## Ask your assistant

- "Walk me through `thread_to_prompt` step by step."
- "Add redaction for phone numbers and add tests."

Next: Lesson 4, Tools Are Structured Outputs (coming soon).
