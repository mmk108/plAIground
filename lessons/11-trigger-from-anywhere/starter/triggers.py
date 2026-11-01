"""Trigger from anywhere: email, chat, a webhook, or a schedule can all start (and answer) the same agent.

Every channel does only two jobs:
  1. turn an incoming message into a request   (an "adapter")
  2. deliver the agent's replies back to the same place

The agent itself (Lesson 7's launch / reply) never knows which channel it is talking through.
We save the channel in the thread as a `trigger` event, so a reply hours later goes to the right place.
"""
import json
import sys
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).parents[3]
sys.path.insert(0, str(ROOT / "lessons" / "07-contact-humans-with-tools" / "starter"))

import human  # noqa: E402
from agent import load_thread  # noqa: E402

from shared.llm import ask_llm  # noqa: E402

DEFAULT_STORE = human.DEFAULT_STORE


# ---- 1. Delivery: one function per channel format. Here they only record messages. ----
# A real app would call an email API or the Slack API here.

def deliver(outbox: list[dict], source: dict, text: str, thread_id: str) -> None:
    channel = source["channel"]
    message = {"channel": channel, "to": source["reply_to"], "thread": thread_id, "text": text}
    if channel == "email":
        message["subject"] = f"Re: your request [{thread_id}]"
    elif channel == "chat":
        message["text"] = text[:300]  # chat messages should be short
    outbox.append(message)


def announce(status: dict, source: dict, outbox: list[dict]) -> None:
    """Tell the human on this channel what the agent needs or found."""
    waiting = status["waiting_for"]
    if waiting and waiting["kind"] == "question":
        text = waiting["question"]
    elif waiting:
        text = f"Approval needed: {waiting['action']}. Reply yes or no."
    elif status["answer"]:
        text = status["answer"]
    else:
        text = f"Agent finished with status {status['status']}."
    deliver(outbox, source, text, status["id"])


# ---- 2. Starting an agent from a channel ----

def _start(request: str, source: dict, outbox: list[dict], store: Path, ask: Callable) -> dict:
    status = human.launch(request, store, ask, source=json.dumps(source))
    announce(status, source, outbox)
    return status


def from_email(sender: str, subject: str, body: str, outbox, store=DEFAULT_STORE, ask=ask_llm) -> dict:
    return _start(f"{subject}. {body}".strip(". "), {"channel": "email", "reply_to": sender}, outbox, store, ask)


def from_chat(user: str, text: str, outbox, store=DEFAULT_STORE, ask=ask_llm) -> dict:
    return _start(text, {"channel": "chat", "reply_to": user}, outbox, store, ask)


def from_webhook(payload: dict, outbox, store=DEFAULT_STORE, ask=ask_llm) -> dict:
    source = {"channel": "webhook", "reply_to": payload.get("callback", "unknown")}
    return _start(payload["request"], source, outbox, store, ask)


def from_schedule(job: str, request: str, notify: str, outbox, store=DEFAULT_STORE, ask=ask_llm) -> dict:
    """No human started this. A clock did. The agent only contacts a human when it needs one."""
    return _start(request, {"channel": "schedule", "job": job, "reply_to": notify}, outbox, store, ask)


# ---- 3. Answering: the reply goes back out the same way it came in ----

def source_of(thread_id: str, store: Path = DEFAULT_STORE) -> dict:
    first = load_thread(store / f"{thread_id}.json").events[0]
    if first.type != "trigger":
        raise ValueError("This thread was not started from a channel")
    return json.loads(first.data)


def handle_reply(thread_id: str, text: str, outbox, store=DEFAULT_STORE, ask=ask_llm) -> dict:
    source = source_of(thread_id, store)
    try:
        status = human.reply(thread_id, text, store, ask)
    except ValueError as err:
        deliver(outbox, source, f"Sorry: {err}", thread_id)  # bad answers are explained on the same channel
        return human.get_status(thread_id, store)
    announce(status, source, outbox)
    return status
