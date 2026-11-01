# Lesson 6: Launch, Pause, Resume

> **Business track:** read this page and try the commands. **Builder track:** also do `exercises.md`. New to a word? See the [glossary](../../GLOSSARY.md).

## The idea

An agent is just a program, so it should behave like one: easy to **start**, easy to **check on**, able to **stop and wait**, and able to **continue later**.

Real work isn't instant. An agent may need a human's approval, or wait for a slow job. If the agent can only run start-to-finish in one go, it can't wait. If it can *pause* and *resume*, it can.

> The key: pause **between the model choosing an action and your code doing it.**

**Everyday analogy:** an expense report. You fill it in (the agent decides), it waits in your manager's inbox (paused), and when approved it gets paid (resumed). Nobody sits and holds the form open in the meantime.

## What you'll build

A tiny service in `starter/service.py` with three calls:

| Call | What it does |
|------|--------------|
| `launch(request)` | Start an agent, run until done or paused, return an ID |
| `get_status(id)` | Is it running, paused, or done? What is it waiting for? |
| `resume(id, approved)` | Approve or reject, then continue |

It works because of Lesson 5: the thread is saved to `threads/<id>.json` after every step. Pausing is just "stop and save." Resuming is "load and continue."

Any tool marked `risky` (like `send_report`) pauses **before** it runs. Nothing is sent until a human says yes.

## Try it (no account needed)

Each command is a separate run. The agent waits on disk in between.

```powershell
python lessons/06-launch-pause-resume/starter/cli.py launch "Email the total units by region to boss@example.com"
python lessons/06-launch-pause-resume/starter/cli.py status <id>
python lessons/06-launch-pause-resume/starter/cli.py resume <id> --approve
python lessons/06-launch-pause-resume/evals/test_service.py
```

Run it again and use `--reject` instead. The agent never sends the email and tells you so.

## Business lens

- **The value:** you can safely let an agent *prepare* actions and require approval to *execute* them. This is how most companies will adopt agents.
- **The risk:** a pause that can't be resumed, or an approval that isn't recorded, is a bug. Here the approval is an event in the saved thread.
- **Ask your engineers:** which actions need approval, who can approve, and where is the decision logged?

## Check yourself

- Why does the agent pause *before* sending, not after?
- What makes it possible to resume in a completely different process?
- What happens if the human rejects the action?

Answers: [answers.md](answers.md)

## Ask your assistant

- "Walk me through `resume()` in `service.py`."
- "Add a `cancel` command that stops a paused agent and records why."

Next: [Lesson 7: Contact Humans With Tools](../07-contact-humans-with-tools/README.md)
