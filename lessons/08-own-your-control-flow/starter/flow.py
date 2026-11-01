"""Own your control flow: YOU decide what happens after each tool call.

The model only proposes the next step. A routing table plus a few guards decide whether your code
runs it, asks a human, or says no. Change the table and you change the agent's behavior.

Routes:
  run      do it now, show the result to the model, and keep going
  approve  stop and wait for a human to approve (high stakes)
  ask      stop and wait for a human's answer
(When the model says done_for_now, the loop simply ends.)
"""
import json
import sys
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).parents[3]
for sub in ("lessons/07-contact-humans-with-tools/starter",):
    sys.path.insert(0, str(ROOT / sub))

import human  # noqa: E402,F401  (registers the request_human_input tool)
from agent import MAX_STEPS, decide, execute_pending, status  # noqa: E402
from context import Thread  # noqa: E402
from tools import parse_tool_call  # noqa: E402

from shared.llm import ask_llm  # noqa: E402

# ---- 1. The routing table: one line per tool ----

ROUTES = {
    "list_files": "run",
    "group_sum": "run",
    "send_report": "approve",
    "request_human_input": "ask",
}


def route(name: str, routes: dict = ROUTES) -> str:
    """Anything not in the table needs approval. Unknown means unsafe until a human says otherwise."""
    return routes.get(name, "approve")


# ---- 2. Guards: small rules that can say "no" before a tool runs ----
# A guard gets (call, thread) and returns None if fine, or a reason string if not.
# The reason goes back to the model as an error, so it can pick another step.

def limit_guard(limits: dict[str, int]) -> Callable:
    def guard(call, thread: Thread) -> str | None:
        used = sum(
            json.loads(e.data)["function"] == call.name for e in thread.events if e.type == "tool_call"
        ) - 1  # the current call is already in the thread
        if call.name in limits and used >= limits[call.name]:
            return f"{call.name} is limited to {limits[call.name]} calls per run"
        return None

    return guard


def internal_only_guard(domain: str) -> Callable:
    def guard(call, thread: Thread) -> str | None:
        to = getattr(call.args, "to", "")
        if call.name == "send_report" and not to.endswith("@" + domain):
            return f"Reports may only be sent to @{domain} addresses"
        return None

    return guard


DEFAULT_GUARDS = [limit_guard({"group_sum": 3, "send_report": 1})]


# ---- 3. The loop ----

def run_flow(
    thread: Thread,
    ask: Callable = ask_llm,
    routes: dict = ROUTES,
    guards: list[Callable] | None = None,
    on_event: Callable[[str, str], None] | None = None,
    max_steps: int = MAX_STEPS,
) -> str:
    """Advance the thread. Returns: done, waiting_for_approval, waiting_for_human, or stopped."""
    guards = DEFAULT_GUARDS if guards is None else guards
    log = on_event or (lambda kind, detail: None)  # tracing, metrics, rate limits can all hook in here

    for _ in range(max_steps):
        current = status(thread)
        if current == "done":
            log("done", "")
            return "done"
        if current != "ready_to_execute":
            decide(thread, ask)
            log("decided", thread.events[-1].type)
            continue

        call = parse_tool_call(thread.events[-1].data)
        objection = next((r for g in guards if (r := g(call, thread))), None)
        if objection:
            thread.add("error", objection)
            log("blocked", f"{call.name}: {objection}")
            continue

        action = route(call.name, routes)
        if action == "approve":
            log("waiting_for_approval", call.name)
            return "waiting_for_approval"
        if action == "ask":
            log("waiting_for_human", call.name)
            return "waiting_for_human"
        execute_pending(thread)
        log("ran", call.name)

    if status(thread) == "done":
        return "done"
    thread.add("error", f"Stopped after {max_steps} steps without finishing")
    return "stopped"
