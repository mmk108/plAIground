# Lesson 12: Make Your Agent a Stateless Reducer

> **Business track:** read the idea and the "why it matters" list. **Builder track:** also run the tests and do `exercises.md`. New to a word? See the [glossary](../../GLOSSARY.md).

## The idea

Here is the whole agent in one sentence:

> **new history = step(old history)**

`step` looks at everything that happened so far, does **one** thing (ask the model, or run a tool), and returns the history with one more event. It keeps nothing in memory and never edits what you gave it.

Run it again and again until it says "done" or "paused". That's the entire agent, and it's what you've been building since Lesson 5.

**Everyday analogy:** a bank statement. The balance isn't stored anywhere secret. It's worked out from the list of transactions. Keep the list and you can rebuild everything.

## What you'll build

`starter/reducer.py`, about 40 lines:

| Function | Job |
|---|---|
| `step(events)` | One move. Returns `(new events, "continue" / "done" / "paused")` |
| `fold(events)` | Call `step` until done or paused |
| `replay(events)` | Re-run a past run using *recorded* model replies and tool results: no model, no tools |
| `rewind(events, n)` | Go back to event `n`, then try something different |

## Why it matters

- **Testing without AI.** Replay a real run in milliseconds, for free, and get the same result every time.
- **Debugging.** Rewind to just before something went wrong and try a different model reply.
- **Resilience.** Save the history anywhere, resume anywhere (Lessons 5 and 6).
- **Auditing.** The history is the full, trustworthy record of what happened.

## Try it (no account needed)

```powershell
python lessons/12-stateless-reducer/evals/test_reducer.py
```

One test deliberately breaks the AI provider and still replays a whole run perfectly. That's the point: replay never needs the model.

> **Honest caveat:** `step` is "pure" with respect to the history, but running a real tool (like sending an email) has real-world effects. In `replay`, tool results are *recorded*, so nothing is re-sent.

## Business lens

- **The value:** you can prove what the agent did and re-test changes against real past cases before shipping them.
- **Ask your engineers:** do we keep complete histories of runs, and can we replay them when we change a prompt?

## Check yourself

- What does `step` do, and what doesn't it do?
- Why can `replay` work without calling a model?
- What can you do with a history that you can't do with a variable inside a running program?

Answers: [answers.md](answers.md)

## Ask your assistant

- "Walk me through `fold` and `step`."
- "Write a `diff` function showing where two histories first differ."

## Further reading

[Factor 12: Make your agent a stateless reducer](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-12-stateless-reducer.md)

**You've finished the 12 factors.** Next: [what's next, and how SDKs, harnesses and skills fit in](../../README.md) (coming soon).
