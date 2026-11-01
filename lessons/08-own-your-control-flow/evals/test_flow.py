"""Offline checks for control flow. Run: python evals/test_flow.py"""
import json
import os
import sys
from pathlib import Path

os.environ["PROVIDER"] = "mock"
sys.path.insert(0, str(Path(__file__).parent.parent / "starter"))

import flow  # noqa: E402
from context import Thread  # noqa: E402


def check(name: str, ok: bool) -> bool:
    print("PASS" if ok else "FAIL", "-", name)
    return ok


def start(request: str) -> Thread:
    thread = Thread()
    thread.add("user_request", request)
    return thread


def emails_sent(thread: Thread) -> int:
    return sum("[fake] Email sent" in e.data for e in thread.events)


# Read-only work runs straight through
trace: list[tuple[str, str]] = []
readonly = start("Which region sold the most units?")
readonly_out = flow.run_flow(readonly, on_event=lambda k, d: trace.append((k, d)))

# High stakes -> stop for approval. Missing info -> stop to ask.
risky = start("Email the total units by region to boss@example.com")
risky_out = flow.run_flow(risky)
missing = start("Email the total units by region to my boss")
missing_out = flow.run_flow(missing)

# A guard blocks external recipients. The model sees the reason and gives up on sending.
guarded = start("Email the total units by region to someone@gmail.com")
guarded_out = flow.run_flow(guarded, guards=[flow.internal_only_guard("example.com")])
guard_errors = [e.data for e in guarded.events if e.type == "error"]

# A limit guard stops a model that repeats itself forever
looping = start("total units by region")
stuck = lambda system, user: json.dumps(  # noqa: E731
    {"function": "group_sum", "filename": "sales.csv", "group_by": "region", "value_column": "units"}
)
loop_out = flow.run_flow(looping, ask=stuck, max_steps=14)
group_runs = sum(e.type == "tool_result" for e in looping.events)

# Changing the table changes behavior: make reading require approval too
strict = start("Which region sold the most units?")
strict_out = flow.run_flow(strict, routes={**flow.ROUTES, "group_sum": "approve"})

results = [
    check("read-only request finishes by itself", readonly_out == "done"),
    check("trace shows what happened", ("ran", "group_sum") in trace and trace[-1][0] == "done"),
    check("risky tool waits for approval", risky_out == "waiting_for_approval" and emails_sent(risky) == 0),
    check("missing info waits for a human", missing_out == "waiting_for_human"),
    check("guard blocks an external address", emails_sent(guarded) == 0 and any("only be sent" in e for e in guard_errors)),
    check("agent recovers after a guard says no", guarded_out == "done"),
    check("limit guard stops repeated calls", group_runs == 3 and loop_out == "stopped"),
    check("unknown tools need approval by default", flow.route("mystery_tool") == "approve"),
    check("editing the routing table changes behavior", strict_out == "waiting_for_approval"),
]
print(f"\n{sum(results)}/{len(results)} passed")
