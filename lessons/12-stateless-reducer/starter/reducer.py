"""The agent as a stateless reducer: new_state = step(old_state).

`step` takes the whole history, does ONE thing (ask the model, or run a tool), and returns a new history.
It keeps nothing in memory between calls and never edits what you gave it.
An agent run is then just "fold": call step again and again until it says done or paused.

Why bother? Because with no hidden state you can:
  * save and resume anywhere (Lessons 5-6)
  * replay a past run with NO model calls and NO tool calls (great for tests)
  * rewind to any point and try something different ("what if the model had said X?")
"""
import sys
from dataclasses import replace
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).parents[3]
for sub in ("", "lessons/03-own-your-context-window/starter", "lessons/04-tools-are-structured-outputs/starter",
            "lessons/05-unify-execution-state/starter"):
    sys.path.insert(0, str(ROOT / sub))

from agent import MAX_STEPS, decide, execute_pending, status  # noqa: E402
from context import Event, Thread  # noqa: E402
from tools import parse_tool_call  # noqa: E402

from shared.llm import ask_llm  # noqa: E402

History = tuple[Event, ...]


def _copy(events: History) -> Thread:
    return Thread([replace(e) for e in events])  # work on a copy so the input is never changed


def step(
    events: History,
    ask: Callable = ask_llm,
    execute: Callable = execute_pending,
    pause_before: Callable | None = None,
) -> tuple[History, str]:
    """One move. Returns (new history, "continue" | "done" | "paused")."""
    thread = _copy(events)
    current = status(thread)
    if current == "done":
        return events, "done"
    if current == "ready_to_execute":
        if pause_before and pause_before(parse_tool_call(thread.events[-1].data)):
            return events, "paused"
        execute(thread)
    else:
        decide(thread, ask)
    return tuple(thread.events), "continue"


def fold(events: History, max_steps: int = MAX_STEPS, **hooks) -> tuple[History, str]:
    """Keep stepping until done or paused. The whole agent loop in four lines."""
    for _ in range(max_steps):
        events, outcome = step(events, **hooks)
        if outcome != "continue":
            return events, outcome
    return events, "stopped"


# ---- Replay and what-if ----

def replay(events: History, pause_before: Callable | None = None) -> tuple[History, str]:
    """Re-run a finished history from its first request, using the RECORDED model replies and tool results."""
    start = next(i for i, e in enumerate(events) if e.type == "user_request")
    model_replies = iter(e.data for e in events if e.type in ("tool_call", "done_for_now"))
    tool_results = iter(e.data for e in events if e.type == "tool_result")
    return fold(
        events[: start + 1],
        ask=lambda system, user: next(model_replies),
        execute=lambda thread: thread.add("tool_result", next(tool_results)),
        pause_before=pause_before,
    )


def rewind(events: History, keep: int) -> History:
    """Go back in time: keep only the first `keep` events."""
    return tuple(events[:keep])
