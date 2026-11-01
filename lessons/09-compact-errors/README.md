# Lesson 9: Compact Errors

> **Business track:** read this page and try the commands. **Builder track:** also do `exercises.md`. New to a word? See the [glossary](../../GLOSSARY.md).

## The idea

Tools fail: a file is missing, a column has a different name, a website is down. A good agent reads the error and **fixes its own mistake**, like you would.

Three habits make this work well:

1. **Short errors.** Put one clean line in the context window, not a 200-line stack trace.
2. **Forget what's fixed.** Once a later step works, hide the earlier errors from the model. They're noise now. (Lesson 3 already knows how to hide resolved errors.)
3. **Know when to stop.** After 3 failures in a row, don't try forever. Ask a human (Lesson 7).

**Everyday analogy:** a spreadsheet says `#REF!`. You glance at it, fix the formula, and move on. You don't re-read the error forever, and after the third failed attempt you ask a colleague.

## What you'll build

`starter/errors.py`:

| Function | Job |
|---|---|
| `format_error` | `"group_sum failed: ValueError: No column 'profit'. Columns are: ..."` (one line) |
| `consecutive_errors` | Counts errors in a row, from the thread (no separate counter, Lesson 5) |
| `mark_resolved` | After a success, flags earlier errors so they're hidden from the model |
| `run_resilient` | The loop: retry on error, escalate after 3 |

## Try it (no account needed)

```powershell
python lessons/09-compact-errors/evals/test_errors.py
```

The mock model asks about "profit". There is no such column, so it fails. It reads the error, picks `units`, and succeeds. Open the tests to see the saved thread keep the error (for your audit trail) while the next prompt doesn't show it.

## Business lens

- **The value:** self-healing means fewer "the AI broke" support tickets.
- **The risk:** an agent that retries the same bad step forever burns money and time. The streak limit is your safety net.
- **Ask your engineers:** how many retries do we allow, and what happens at the limit?

## Check yourself

- Why must the model see an error *while it is unresolved*?
- Why hide errors once they're fixed?
- What should happen when the same error repeats three times?

Answers: [answers.md](answers.md)

## Ask your assistant

- "Walk me through `mark_resolved`."
- "Make the retry limit different per tool."
- "Detect when the model repeats the *exact same* failing call and escalate sooner."

## Further reading

[Factor 9: Compact errors into context window](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-09-compact-errors.md)

Next: [Lesson 10: Small, Focused Agents](../10-small-focused-agents/README.md)
