# Lesson 5: Unify Execution State

> **Business track:** read this page and run the demo. **Builder track:** also do `exercises.md`. New to a word? See the [glossary](../../GLOSSARY.md).

## The idea

Most software tracks two kinds of state:

- **Execution state**: where is the process? Which step? Waiting? How many retries?
- **Business state**: what has happened so far? What did we ask, what came back?

Agents can keep these in two places, which creates bugs when they disagree. A simpler way: **keep one list of events, and work out everything else by reading it.**

> One source of truth: the thread.

**Everyday analogy:** a case file. You don't need a separate sticky note saying "step 3 of 5." Read the file and you can tell: the form was filed, the reply came back, nothing's pending, so you're done.

## What you'll build

An agent loop in `starter/agent.py`:

```
read the thread -> ask the model what's next -> record it -> run the tool -> record the result -> repeat
```

There is no `current_step` variable. `status(thread)` just looks at the **last event**:

| Last event | Status |
|------------|--------|
| `done_for_now` | done |
| `tool_call` | ready to execute |
| anything else | the model needs to decide |

Errors are just events too. If the model replies with garbage, an `error` event is added, the model sees it next round, and can fix itself. A step limit stops runaway agents.

## Run it (no account needed)

```powershell
python lessons/05-unify-execution-state/starter/demo.py "Which region sold the most units?"
python lessons/05-unify-execution-state/evals/test_agent.py
```

The demo prints the whole thread, saves it to a file, reloads it, and shows the state is identical. Because the thread is the only state, saving and loading is trivial.

## What this unlocks

- **Debugging:** read the thread top to bottom.
- **Saving and resuming:** load the thread and continue (Lesson 6).
- **Auditing:** a complete record of what the agent did and why.

## Business lens

- **The value:** every agent run leaves a complete, readable record. That's what auditors, support teams, and debuggers need.
- **The risk:** the thread may contain sensitive data. It's saved to disk, so treat it like any other record (access, retention). Cards are masked before the model sees them, but the saved thread keeps what tools returned.
- **Ask your engineers:** can we replay a run from its record?

## Check yourself

- How does the agent know it's finished, without a "done" flag?
- What happens when the model returns invalid JSON?
- Why does one list of events make saving and resuming easier?

Answers: [answers.md](answers.md)

## Ask your assistant

- "Walk me through `run()` in `agent.py` step by step."
- "Add a `status` of `stuck` when the last 3 events are all errors, with a test."

Next: [Lesson 6: Launch, Pause, Resume](../06-launch-pause-resume/README.md)
