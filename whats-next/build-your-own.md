# Build your own harness

A harness is the workbench around the model. You already built most of one.

## What you have

| Harness part | Where in this repo |
|---|---|
| Model access (swappable) | `shared/llm.py` (Lesson 1) |
| Prompt files you own | `prompts/` (Lesson 2) |
| Context builder | Lesson 3 `context.py` |
| Tool registry and validation | Lesson 4 `tools.py` |
| Loop and one state object | Lesson 5 `agent.py` |
| Pause, resume, approvals | Lessons 6-7 |
| Routing and guards | Lesson 8 `flow.py` |
| Error handling | Lesson 9 `errors.py` |
| Small agents | Lesson 10 `focused.py` |
| Entry points | Lesson 11 `triggers.py`, `server.py` |
| Replay and rewind | Lesson 12 `reducer.py` |

## What real harnesses add

- **Many model providers and streaming** (SDKs do this well).
- **Durable storage and scheduling** (runtimes).
- **Memory** across sessions, and context summarising.
- **Sandboxes and permissions**: your Lesson 8 guards are the seed of this.
- **Tracing and evals**: your `evals/` folders are the seed.
- **Skills loading**: the agent reads a skill's instructions only when a task needs it.

## A skill, in this repo's terms

A skill is a folder with a short description and instructions, plus optional tools.
The harness shows the agent only the description. When a task matches, it loads the full text into the prompt.
That is Lesson 3 (context building) with a lookup in front.

```
skills/
  weekly-report/
    SKILL.md      # name, one-line description, step-by-step instructions
    tools.py      # optional tools (registered like Lesson 4)
    evals/        # tests that prove it works
```

## Steps to your own agent

1. **Pick one real job** you repeat (a report, a triage, a lookup).
2. **Write 3-5 example requests** and the result you want. These become evals.
3. **List tools** (each one safe, structured, validated). Mark which need approval.
4. **Write the prompt** as a file. Run the evals on the mock model, then a real one.
5. **Add the loop, thread and pause** by reusing Lessons 5-7.
6. **Add guards and error rules** (Lessons 8-9).
7. **Pick an entry point** (Lesson 11): email, chat, schedule.
8. **Only then** decide: stay on your code, or move to an SDK or harness.

## Rule of thumb

Build the first version by hand. Switch to an SDK when you are maintaining plumbing instead of solving your problem. Keep your evals either way: they work with any library.
