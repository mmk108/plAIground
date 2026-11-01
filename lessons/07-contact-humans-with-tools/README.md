# Lesson 7: Contact Humans With Tools

> **Business track:** read this page and try the commands. **Builder track:** also do `exercises.md`. New to a word? See the [glossary](../../GLOSSARY.md).

## The idea

So far the agent either answers or uses a tool. But real work has a third move: **"I'm missing something. I need to ask a person."**

The trick is to make asking a human *just another tool*. Instead of the model rambling in free text, it fills in a form:

```json
{"function": "request_human_input",
 "question": "What email address should I send it to?",
 "format": "free_text",
 "urgency": "low"}
```

Your code sees that, saves the thread, and stops. Hours later the answer arrives and becomes an event. The agent carries on.

**Everyday analogy:** a new assistant who, instead of guessing your boss's email address, sends you a sticky note: "What's the address?" and waits.

## Why a tool and not plain chat?

- **Structured:** `format` can be `yes_no` or `multiple_choice`, and you can *validate* the answer.
- **Routable:** `urgency` decides if it's a text message or a daily digest.
- **Works without a chat window:** a scheduled agent can ask a human too (Lesson 11).
- **Durable:** it's the same pause/resume as Lesson 6, so the wait can be a week.

## What you'll build

`starter/human.py`, one new tool plus three calls:

| Call | What it does |
|------|--------------|
| `launch(request)` | Run until done, or until the agent needs a human |
| `get_status(id)` | Says *what kind* of wait: a `question` or an `approval` |
| `reply(id, answer)` | Validates the answer, records it, and continues |

Notice that approvals (Lesson 6) and questions are two kinds of the same thing: **the agent is waiting for a human.**

## Try it (no account needed)

```powershell
python lessons/07-contact-humans-with-tools/starter/cli.py launch "Email the total units by region to my boss"
python lessons/07-contact-humans-with-tools/starter/cli.py reply <id> "boss@example.com"
python lessons/07-contact-humans-with-tools/starter/cli.py reply <id> "yes"
python lessons/07-contact-humans-with-tools/evals/test_human.py
```

First the agent asks for the address (it never guesses). After you answer, it pauses again to ask permission to send. Then it sends.

## Business lens

- **The value:** agents that ask good questions make fewer expensive mistakes than agents that guess.
- **The risk:** if every step asks, nobody will use it. Decide what is worth a question.
- **Ask your engineers:** who gets asked, through which channel, and what happens if nobody answers?

## Check yourself

- Why is "ask a human" better as a structured tool than as free text?
- What are the two kinds of wait, and how do they differ?
- What should happen if the human gives an invalid answer?

Answers: [answers.md](answers.md)

## Ask your assistant

- "Walk me through `reply()` in `human.py`."
- "Add a `timeout` so an unanswered question escalates after 24 hours."

## Further reading

[Factor 7: Contact humans with tool calls](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-07-contact-humans-with-tools.md)

Next: [Lesson 8: Own Your Control Flow](../08-own-your-control-flow/README.md)
