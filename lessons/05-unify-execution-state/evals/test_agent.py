"""Offline checks for the agent loop. Run: python evals/test_agent.py"""
import json
import os
import sys
import tempfile
from pathlib import Path

os.environ["PROVIDER"] = "mock"
sys.path.insert(0, str(Path(__file__).parent.parent / "starter"))

from agent import load_thread, run, save_thread, status, summary  # noqa: E402
from context import Thread  # noqa: E402


def check(name: str, ok: bool) -> bool:
    print("PASS" if ok else "FAIL", "-", name)
    return ok


def new_thread(text: str) -> Thread:
    t = Thread()
    t.add("user_request", text)
    return t


def done(message: str) -> str:
    return json.dumps({"function": "done_for_now", "message": message})


# 1. Full run with the mock model
t = new_thread("Which region sold the most units?")
final = run(t)
types = [e.type for e in t.events]

# 2. A model that makes a mistake, then recovers after seeing the error
replies = iter(["not json at all", done("recovered")])
t2 = new_thread("hi")
run(t2, ask=lambda system, user: next(replies))

# 3. A model that never finishes
t3 = new_thread("loop forever")
final3 = run(t3, ask=lambda system, user: json.dumps({"function": "list_files"}), max_steps=3)

# 4. Save and reload
path = Path(tempfile.mkdtemp()) / "t.json"
save_thread(t, path)
reloaded = load_thread(path)

# 5. Card numbers never reach the model
seen = []
t5 = new_thread("my card is 4111 1111 1111 1111, email me at a@b.com")
run(t5, ask=lambda system, user: (seen.append(user), done("ok"))[1])

results = [
    check("run finishes", final == "done"),
    check("flow is request -> call -> result -> done", types == ["user_request", "tool_call", "tool_result", "done_for_now"]),
    check("answer mentions East=32", "East=32" in t.events[-1].data),
    check("invalid reply becomes an error event, then recovers", [e.type for e in t2.events] == ["user_request", "error", "done_for_now"]),
    check("step limit stops a runaway agent", final3 == "stopped" and summary(t3)["errors"] == 1),
    check("reloaded thread has identical state", summary(reloaded) == summary(t) and status(reloaded) == "done"),
    check("cards masked, emails kept", "4111" not in seen[0] and "a@b.com" in seen[0]),
]
print(f"\n{sum(results)}/{len(results)} passed")
