"""A tiny agent loop where the thread (list of events) is the ONLY state.

There is no separate 'current step' or 'retry count' variable. Everything,
including whether the agent is done, is worked out by reading the thread.
"""
import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).parents[3]
for sub in ("", "lessons/03-own-your-context-window/starter", "lessons/04-tools-are-structured-outputs/starter"):
    sys.path.insert(0, str(ROOT / sub))

from context import CARD, Event, Thread, thread_to_prompt  # noqa: E402
from tools import build_system_prompt, parse_tool_call, run_tool  # noqa: E402

from shared.llm import ask_llm  # noqa: E402

MAX_STEPS = 8


def mask_cards(text: str) -> str:
    # Emails stay visible: the agent may need an address to send a report. Card numbers never do.
    return CARD.sub("[CARD_REDACTED]", text)


# ---- Execution state, derived from the thread ----

def status(thread: Thread) -> str:
    """Where are we? Just look at the last event."""
    if not thread.events:
        return "empty"
    last = thread.events[-1].type
    if last == "done_for_now":
        return "done"
    if last == "tool_call":
        return "ready_to_execute"
    return "needs_decision"


def summary(thread: Thread) -> dict:
    count = lambda t: sum(e.type == t for e in thread.events)  # noqa: E731
    return {"status": status(thread), "tool_calls": count("tool_call"), "errors": count("error")}


# ---- The loop ----

def decide(thread: Thread, ask: Callable = ask_llm, tools: list[str] | None = None) -> None:
    """Show the model the thread and record its next step (or an error if the reply is invalid).

    tools optionally limits which tools this agent may use (Lesson 10).
    """
    prompt = thread_to_prompt(thread, redact_fn=mask_cards)
    try:
        call = parse_tool_call(ask(build_system_prompt(tools), prompt), allowed=tools)
    except ValueError as err:
        thread.add("error", str(err))  # the model sees this next time and can fix its mistake
        return
    thread.add("done_for_now" if call.name == "done_for_now" else "tool_call", call.raw)


def execute_pending(thread: Thread) -> None:
    """Run the most recent tool call and record the outcome."""
    last_call = next(e for e in reversed(thread.events) if e.type == "tool_call")
    call = parse_tool_call(last_call.data)
    try:
        thread.add("tool_result", run_tool(call))
    except Exception as err:
        thread.add("error", f"{call.name} failed: {err}")


def run(
    thread: Thread,
    ask: Callable = ask_llm,
    pause_before: Callable | None = None,
    max_steps: int = MAX_STEPS,
    tools: list[str] | None = None,
) -> str:
    """Advance the thread until it's done, paused, or out of steps. Returns the final status.

    pause_before(call) can return True to stop before a tool runs (used in Lesson 6).
    """
    if not thread.events:
        raise ValueError("Thread is empty. Add a user_request first.")
    for _ in range(max_steps):
        current = status(thread)
        if current == "done":
            return "done"
        if current == "ready_to_execute":
            pending = parse_tool_call(thread.events[-1].data)
            if pause_before and pause_before(pending):
                return "paused"
            execute_pending(thread)
        else:
            decide(thread, ask, tools)
    if status(thread) == "done":
        return "done"
    thread.add("error", f"Stopped after {max_steps} steps without finishing")
    return "stopped"


# ---- Because the thread is the state, saving and loading is trivial ----

def save_thread(thread: Thread, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps([asdict(e) for e in thread.events], indent=2), encoding="utf-8")


def load_thread(path: Path) -> Thread:
    return Thread([Event(**e) for e in json.loads(path.read_text(encoding="utf-8"))])


def to_markdown(thread: Thread) -> str:
    """A human-readable log of everything that happened."""
    return "\n".join(f"{i}. **{e.type}**: {e.data}" for i, e in enumerate(thread.events, 1))
