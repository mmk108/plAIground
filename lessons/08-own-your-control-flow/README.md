# Lesson 8: Own Your Control Flow

> **Business track:** read this page and try the commands. **Builder track:** also do `exercises.md`. New to a word? See the [glossary](../../GLOSSARY.md).

## The idea

The model suggests the next step. **Your code decides what happens with it.**

Different steps deserve different treatment:

| The model asks for... | Your code should... |
|---|---|
| Look up the file list | just do it and show the result |
| Send an email | **stop** and wait for approval |
| Missing info | **stop** and ask a human |
| Something it's already done 3 times | **refuse** and say why |

Owning your control flow means writing that table yourself, in plain code, instead of letting a framework decide.

**Everyday analogy:** a manager's rules for a new hire. "Look things up freely. Ask me before spending money. Never email outside the company."

## What you'll build

`starter/flow.py` has three small pieces:

1. **A routing table** (`ROUTES`): one line per tool, `run`, `approve` or `ask`. Anything not listed needs approval. Unknown means unsafe.
2. **Guards**: tiny functions that can say "no" before a tool runs. The reason goes back to the model as an error, so it can pick something else.
   - `limit_guard`: max calls per tool per run
   - `internal_only_guard`: reports only go to `@yourcompany.com`
3. **A trace hook** (`on_event`): called at every step, so you can log, time, or count.

You can see each piece by changing one line and re-running the tests.

## Try it (no account needed)

```powershell
python lessons/08-own-your-control-flow/evals/test_flow.py
```

Then open `flow.py`, change `"group_sum": "run"` to `"approve"`, and run the tests again. One test breaks on purpose: the agent now stops before reading data.

## Business lens

- **The value:** this is where *policy* lives. Compliance, spending limits and "who can see what" are code you can read, not model behavior you hope for.
- **The risk:** guards only protect what you thought of. Start strict and loosen with evidence.
- **Ask your engineers:** show me the routing table. Which tools run without a human, and why?

## Check yourself

- Why do unknown tools default to "approve" instead of "run"?
- What does the model see when a guard blocks it, and why does that matter?
- Which part is model judgment and which part is your policy?

Answers: [answers.md](answers.md)

## Ask your assistant

- "Walk me through the loop in `run_flow`."
- "Add a guard that blocks `group_sum` on files with more than 10,000 rows."
- "Add an LLM-as-judge guard that checks the email body for sensitive info."

## Further reading

[Factor 8: Own your control flow](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-08-own-your-control-flow.md)

Next: [Lesson 9: Compact Errors](../09-compact-errors/README.md)
