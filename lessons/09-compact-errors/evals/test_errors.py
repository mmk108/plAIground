"""Offline checks for compact errors. Run: python evals/test_errors.py"""
import json
import os
import sys
from pathlib import Path

os.environ["PROVIDER"] = "mock"
sys.path.insert(0, str(Path(__file__).parent.parent / "starter"))

import errors  # noqa: E402
from context import Thread, thread_to_prompt  # noqa: E402
from tools import parse_tool_call  # noqa: E402


def check(name: str, ok: bool) -> bool:
    print("PASS" if ok else "FAIL", "-", name)
    return ok


def start(request: str) -> Thread:
    thread = Thread()
    thread.add("user_request", request)
    return thread


def bad_column(system: str, user: str) -> str:
    return json.dumps({"function": "group_sum", "filename": "sales.csv", "group_by": "region", "value_column": "profit"})


# 1. Self-healing: the model guesses a column that doesn't exist, reads the error, and fixes it
healing = start("total profit by region")
heal_out = errors.run_resilient(healing)
error_events = [e for e in healing.events if e.type == "error"]
prompt = thread_to_prompt(healing)

# 2. While an error is unresolved, the model MUST see it (that's how it fixes things)
mid = start("total profit by region")
errors.decide(mid)
errors.execute(mid)
mid_prompt = thread_to_prompt(mid)

# 3. A model that never learns: stop after 3 errors in a row and ask a human
stuck = start("total profit by region")
stuck_out = errors.run_resilient(stuck, ask=bad_column, max_steps=12)
stuck_errors = sum(e.type == "error" for e in stuck.events)
escalation = parse_tool_call(stuck.events[-1].data)

# 4. Errors are short
long_error = errors.format_error(ValueError("line one\n" + "Traceback (most recent call last)\n" * 50), "group_sum")
very_long = errors.format_error(ValueError("x" * 1000), "group_sum")

# 5. A success resets the streak
reset = start("anything")
reset.add("error", "a")
reset.add("error", "b")
streak_before = errors.consecutive_errors(reset)
reset.add("tool_result", "ok")

results = [
    check("agent fixes its own mistake and finishes", heal_out == "done"),
    check("exactly one error happened, and it was marked resolved", len(error_events) == 1 and error_events[0].resolved),
    check("resolved errors are hidden from the next prompt", "No column 'profit'" not in prompt),
    check("unresolved errors ARE shown to the model", "No column 'profit'" in mid_prompt),
    check("error is one clean line with the column list", "Columns are:" in error_events[0].data and "\n" not in error_events[0].data),
    check("stuck agent escalates after 3 errors", stuck_out == "escalated" and stuck_errors == 3),
    check("escalation is a question for a human", escalation.name == "request_human_input"),
    check("long errors are trimmed to one line", "\n" not in long_error and "Traceback" not in long_error and len(very_long) <= 300),
    check("success resets the error streak", streak_before == 2 and errors.consecutive_errors(reset) == 0),
]
print(f"\n{sum(results)}/{len(results)} passed")
