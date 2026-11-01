# Lesson 10: Small, Focused Agents

> **Business track:** read this page and try the commands. **Builder track:** also do `exercises.md`. New to a word? See the [glossary](../../GLOSSARY.md).

## The idea

Don't build one giant agent that does everything. Build **small agents that each do one job**, and connect them with ordinary code.

Why? Every step adds to the context window, and models get worse as it grows: they lose focus, mix things up, and repeat themselves. A focused agent with 3 to 10 steps stays sharp. It's also easier to test and to fix.

**Everyday analogy:** a small team. An analyst pulls the numbers. An assistant sends the email. A coordinator (plain code) hands the work from one to the other. Nobody is expected to do everything.

## What you'll build

`starter/focused.py`:

| Piece | What it is |
|---|---|
| `ANALYST` | Tools: `list_files`, `group_sum`. Budget: 6 steps. |
| `EMAILER` | Tools: `send_report`. Budget: 4 steps. |
| `pipeline()` | **Plain Python**, no model. Runs the analyst, and if the user wants an email, hands the report to the emailer. |

Each agent:

- sees **only its own tools**, in its prompt and in validation. The analyst can't send mail even if it tries.
- has a **step budget**, so a runaway agent is stopped.
- starts with a **fresh, short thread**, with only what the previous agent handed over.

The router also catches "email my boss" with no address *without asking a model*. Not everything needs AI.

## Try it (no account needed)

```powershell
python lessons/10-small-focused-agents/evals/test_focused.py
```

## Business lens

- **The value:** small agents are easier to review ("what can the emailer do? One thing."), and cheaper (shorter prompts).
- **The risk:** more agents means more handoffs to design. Start with one and split when it gets confused.
- **Ask your engineers:** what is each agent's job, tool list and step limit?

## Check yourself

- Why does a long context window hurt the model?
- Why is the router plain code instead of another AI?
- What does giving each agent its own tool list protect against?

Answers: [answers.md](answers.md)

## Ask your assistant

- "Add a `summarizer` agent between the analyst and the emailer."
- "Why did we pass only the report, not the whole analyst thread, to the emailer?"

## Further reading

[Factor 10: Small, focused agents](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-10-small-focused-agents.md)

Next: [Lesson 11: Trigger From Anywhere](../11-trigger-from-anywhere/README.md)
