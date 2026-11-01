"""Offline checks for launch/pause/resume. Run: python evals/test_service.py"""
import os
import sys
import tempfile
from pathlib import Path

os.environ["PROVIDER"] = "mock"
sys.path.insert(0, str(Path(__file__).parent.parent / "starter"))

import service  # noqa: E402
from agent import load_thread  # noqa: E402


def check(name: str, ok: bool) -> bool:
    print("PASS" if ok else "FAIL", "-", name)
    return ok


def sent(store: Path, thread_id: str) -> bool:
    events = load_thread(store / f"{thread_id}.json").events
    return any("[fake] Email sent" in e.data for e in events)


store = Path(tempfile.mkdtemp())
email_request = "Email the total units by region to boss@example.com"

# Safe request: no pause
plain = service.launch("Which region sold the most units?", store)

# Risky request: pauses before sending
paused = service.launch(email_request, store)
not_sent_while_paused = not sent(store, paused["id"])
status_later = service.get_status(paused["id"], store)  # like a separate process checking in
approved = service.resume(paused["id"], approved=True, store=store)

# Rejection path
paused2 = service.launch(email_request, store)
rejected = service.resume(paused2["id"], approved=False, store=store)

try:
    service.resume(plain["id"], approved=True, store=store)
    resume_done_fails = False
except ValueError:
    resume_done_fails = True

results = [
    check("safe request finishes without pausing", plain["status"] == "done"),
    check("risky request pauses", paused["status"] == "paused" and "send_report" in paused["waiting_for"]),
    check("nothing is sent while paused", not_sent_while_paused),
    check("status survives (saved to disk)", status_later["status"] == "paused"),
    check("approval sends and finishes", approved["status"] == "done" and sent(store, paused["id"])),
    check("rejection finishes without sending", rejected["status"] == "done" and not sent(store, paused2["id"])),
    check("can't resume an agent that isn't paused", resume_done_fails),
    check("list shows all agents", len(service.list_agents(store)) == 3),
]
print(f"\n{sum(results)}/{len(results)} passed")
