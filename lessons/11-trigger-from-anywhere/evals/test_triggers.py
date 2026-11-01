"""Offline checks for triggers. Run: python evals/test_triggers.py"""
import json
import os
import sys
import tempfile
import threading
import urllib.request
from pathlib import Path

os.environ["PROVIDER"] = "mock"
sys.path.insert(0, str(Path(__file__).parent.parent / "starter"))

import server  # noqa: E402
import triggers  # noqa: E402
from agent import load_thread  # noqa: E402


def check(name: str, ok: bool) -> bool:
    print("PASS" if ok else "FAIL", "-", name)
    return ok


store = Path(tempfile.mkdtemp())
outbox: list[dict] = []

# Same agent, four doors
email = triggers.from_email("alice@example.com", "Sales", "Which region sold the most units?", outbox, store)
chat = triggers.from_chat("@bob", "Email the total units by region to boss@example.com", outbox, store)
hook = triggers.from_webhook({"request": "what files do I have?", "callback": "https://example.com/hook"}, outbox, store)
cron = triggers.from_schedule("monday-report", "Email the total units by region to team@example.com", "ops@example.com", outbox, store)

# Replies go back out the SAME channel they came in on
by_channel = lambda ch: [m for m in outbox if m["channel"] == ch]  # noqa: E731
chat_reply = triggers.handle_reply(chat["id"], "yes", outbox, store)

# Bad answers are explained, not crashed on
bad = triggers.handle_reply(cron["id"], "maybe", outbox, store)

# The agent is saved with where it came from
source = triggers.source_of(email["id"], store)
first_event = load_thread(store / f"{email['id']}.json").events[0].type

# HTTP: start, check, answer
http_outbox: list[dict] = []
srv = server.make_server(http_outbox, store, port=0)
threading.Thread(target=srv.serve_forever, daemon=True).start()
base = f"http://127.0.0.1:{srv.server_address[1]}"


def call(method: str, path: str, body: dict | None = None) -> dict:
    req = urllib.request.Request(
        base + path, method=method, data=json.dumps(body).encode() if body is not None else None,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


launched = call("POST", "/agents", {"request": "Email the total units by region to boss@example.com", "callback": "x"})
polled = call("GET", f"/agents/{launched['id']}")
answered = call("POST", f"/agents/{launched['id']}/reply", {"answer": "yes"})
srv.shutdown()

results = [
    check("email trigger answers by email", email["status"] == "done" and by_channel("email")[0]["to"] == "alice@example.com"),
    check("email reply has a subject", by_channel("email")[0]["subject"].startswith("Re:")),
    check("chat trigger asks for approval in chat", chat["status"] == "waiting_for_human" and "Approval needed" in by_channel("chat")[0]["text"]),
    check("chat approval completes the job", chat_reply["status"] == "done" and by_channel("chat")[-1]["text"].startswith("Done")),
    check("webhook trigger works", hook["status"] == "done"),
    check("schedule trigger needs no human to start", cron["status"] == "waiting_for_human" and by_channel("schedule")[0]["to"] == "ops@example.com"),
    check("a bad answer is explained on the same channel", bad["status"] == "waiting_for_human" and "yes or no" in by_channel("schedule")[-1]["text"]),
    check("channel is saved in the thread", source["channel"] == "email" and first_event == "trigger"),
    check("HTTP launch and status agree", polled["id"] == launched["id"] and polled["status"] == "waiting_for_human"),
    check("HTTP reply finishes the agent", answered["status"] == "done"),
]
print(f"\n{sum(results)}/{len(results)} passed")
