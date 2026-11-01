"""Offline checks for asking humans. Run: python evals/test_human.py"""
import os
import sys
import tempfile
from pathlib import Path

os.environ["PROVIDER"] = "mock"
sys.path.insert(0, str(Path(__file__).parent.parent / "starter"))

import human  # noqa: E402
from agent import load_thread  # noqa: E402


def check(name: str, ok: bool) -> bool:
    print("PASS" if ok else "FAIL", "-", name)
    return ok


def sent(store: Path, thread_id: str) -> bool:
    return any("[fake] Email sent" in e.data for e in load_thread(store / f"{thread_id}.json").events)


store = Path(tempfile.mkdtemp())

# Missing info: the agent asks instead of guessing an address
first = human.launch("Email the total units by region to my boss", store)
question = first["waiting_for"]
sent_before_answer = sent(store, first["id"])

# A bad answer is rejected and the agent keeps waiting
try:
    human.reply(first["id"], "   ", store)
    empty_rejected = False
except ValueError:
    empty_rejected = True

# A good answer: the agent continues, then pauses for approval of the email itself
second = human.reply(first["id"], "boss@example.com", store)
third = human.reply(second["id"], "yes", store)

# Fully specified request skips the question
direct = human.launch("Email the total units by region to ceo@example.com", store)

# Questions with fixed formats are validated
fmt = human.RequestHumanInput(question="Proceed?", format="multiple_choice", choices=["A", "B"])
try:
    human._check_answer({"kind": "question", **fmt.model_dump()}, "C")
    choice_checked = False
except ValueError:
    choice_checked = True

events = [e.type for e in load_thread(store / f"{first['id']}.json").events]

results = [
    check("missing address -> asks a question", first["status"] == "waiting_for_human" and question["kind"] == "question"),
    check("question is structured (text, format, urgency)", question["format"] == "free_text" and "email" in question["question"].lower()),
    check("nothing is sent before the answer", not sent_before_answer),
    check("empty answers are rejected", empty_rejected),
    check("answer leads to an approval pause", second["status"] == "waiting_for_human" and second["waiting_for"]["kind"] == "approval"),
    check("approval sends and finishes", third["status"] == "done" and sent(store, first["id"])),
    check("human answer is recorded as an event", "human_response" in events),
    check("complete request needs no question", direct["waiting_for"]["kind"] == "approval"),
    check("multiple-choice answers are validated", choice_checked),
]
print(f"\n{sum(results)}/{len(results)} passed")
