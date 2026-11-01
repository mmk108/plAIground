# Lesson 11: Trigger From Anywhere

> **Business track:** read this page and try the commands. **Builder track:** also do `exercises.md`. New to a word? See the [glossary](../../GLOSSARY.md).

## The idea

People don't want to open a special app to use an agent. They want to email it, message it in chat, or have it run by itself every Monday. So let **any channel** start the agent, and let the agent answer in the same place.

The agent doesn't change. Each channel only needs two small jobs:

1. **Adapter:** turn the incoming message into a request.
2. **Delivery:** send the agent's questions and answers back the same way.

**Everyday analogy:** a receptionist who handles phone, email and walk-ins, and always replies the way you contacted them.

## What you'll build

`starter/triggers.py`:

| Entry point | Who starts it | Where replies go |
|---|---|---|
| `from_email` | a person emailing | back to the sender |
| `from_chat` | a person in chat | the same user, short messages |
| `from_webhook` | another system | a callback URL |
| `from_schedule` | **a clock, no human** | a named owner, only when the agent needs one |

How can a reply hours later find its way home? The channel is saved as the first event in the thread (`trigger`). `handle_reply` reads it.

`starter/server.py` adds a small web API (stdlib only), so anything that can send an HTTP request can use the agent:

```
POST /agents            {"request": "..."}      launch
GET  /agents/<id>                                status
POST /agents/<id>/reply {"answer": "yes"}        answer
```

## Try it (no account needed)

```powershell
python lessons/11-trigger-from-anywhere/evals/test_triggers.py
python lessons/11-trigger-from-anywhere/starter/server.py   # then POST to http://127.0.0.1:8000/agents
```

Nothing is actually emailed. Messages are collected in an `outbox` list. A real app would call an email or chat API there.

> **Safety note:** the demo server has no login and listens on localhost only. Before exposing anything like it, add authentication and decide who may approve what. An approval channel anyone can write to isn't an approval.

## Business lens

- **The value:** adoption. Agents that live in email and chat get used. Scheduled agents ("every Monday, prepare the report and ask me to approve") do work while nobody's watching.
- **The risk:** more doors, more security questions. Who is allowed to trigger it? Who may approve a risky action?
- **Ask your engineers:** which channels, and how do we know the person replying is allowed to?

## Check yourself

- What two jobs does each channel have?
- How does a reply find the right channel later?
- What's different about a schedule trigger?

Answers: [answers.md](answers.md)

## Ask your assistant

- "Add a Slack-style `from_chat` that threads replies under the original message."
- "Add an `allowed_approvers` check to `handle_reply`."

## Further reading

[Factor 11: Trigger from anywhere, meet users where they are](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-11-trigger-from-anywhere.md)

Next: [Lesson 12: Stateless Reducer](../12-stateless-reducer/README.md)
