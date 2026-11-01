"""Offline checks for the reducer. Run: python evals/test_reducer.py"""
import json
import os
import sys
from pathlib import Path

os.environ["PROVIDER"] = "mock"
sys.path.insert(0, str(Path(__file__).parent.parent / "starter"))

import reducer  # noqa: E402
from agent import run  # noqa: E402
from context import Event, Thread  # noqa: E402


def check(name: str, ok: bool) -> bool:
    print("PASS" if ok else "FAIL", "-", name)
    return ok


def plain(events) -> list[tuple]:
    return [(e.type, e.data) for e in events]


start = (Event("user_request", "Which region sold the most units?"),)

# One step does one thing and doesn't touch its input
before = plain(start)
after_one, outcome_one = reducer.step(start)
input_unchanged = plain(start) == before

# The fold finishes the job
final, outcome = reducer.fold(start)

# Same result as the Lesson 5 loop
thread = Thread([Event("user_request", "Which region sold the most units?")])
run(thread)
same_as_loop = [e.type for e in final] == [e.type for e in thread.events]

# Replay: no model, no tools. Break the provider to prove it isn't used.
os.environ["PROVIDER"] = "does-not-exist"
replayed, replay_outcome = reducer.replay(final)
os.environ["PROVIDER"] = "mock"

# Rewind and try a different model reply ("what if it had just answered?")
midpoint = reducer.rewind(final, 2)  # request + first tool call
what_if, what_if_outcome = reducer.fold(
    midpoint, ask=lambda s, u: json.dumps({"function": "done_for_now", "message": "Skipping the lookup."})
)

# Pausing is just "stop folding"
mail = (Event("user_request", "Email the total units by region to boss@example.com"),)
risky = lambda call: call.name == "send_report"  # noqa: E731
held, held_outcome = reducer.fold(mail, pause_before=risky)

results = [
    check("step adds exactly one event", len(after_one) == len(start) + 1 and outcome_one == "continue"),
    check("step never changes its input", input_unchanged),
    check("fold runs to done", outcome == "done" and final[-1].type == "done_for_now"),
    check("fold matches the Lesson 5 loop", same_as_loop),
    check("replay reproduces the run exactly", plain(replayed) == plain(final) and replay_outcome == "done"),
    check("replay needs no model (provider was broken)", replay_outcome == "done"),
    check("rewind + a different reply gives a different ending", what_if_outcome == "done" and plain(what_if) != plain(final)),
    check("rewind leaves the original untouched", len(final) > len(midpoint)),
    check("fold can pause before a risky tool", held_outcome == "paused" and held[-1].type == "tool_call"),
]
print(f"\n{sum(results)}/{len(results)} passed")
