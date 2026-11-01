"""Compact errors: let the agent see its mistakes, short and clean, and fix them itself.

Three small ideas:
  1. Make errors short (one line, no stack trace) before they go in the context window.
  2. When a later step works, mark the earlier errors as resolved. Lesson 3's prompt builder hides them.
  3. Count consecutive errors. After too many, stop retrying and ask a human.
"""
import json
import sys
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).parents[3]
sys.path.insert(0, str(ROOT / "lessons" / "07-contact-humans-with-tools" / "starter"))

import human  # noqa: E402,F401  (registers request_human_input)
from agent import MAX_STEPS, decide, status  # noqa: E402
from context import Thread  # noqa: E402
from tools import parse_tool_call, run_tool  # noqa: E402

from shared.llm import ask_llm  # noqa: E402

MAX_CONSECUTIVE_ERRORS = 3
RESETS = {"tool_result", "human_response", "user_request"}  # a good outcome ends a streak of errors


def format_error(err: Exception, tool: str, limit: int = 300) -> str:
    """One line: which tool, what kind of error, and the message. No stack trace."""
    first_line = (str(err).strip().splitlines() or [""])[0]
    text = f"{tool} failed: {type(err).__name__}: {first_line}"
    return text if len(text) <= limit else text[: limit - 3] + "..."


def consecutive_errors(thread: Thread) -> int:
    """How many errors in a row, with no success in between? Worked out from the thread (Lesson 5)."""
    count = 0
    for event in reversed(thread.events):
        if event.type == "error":
            count += 1
        elif event.type in RESETS or event.type == "done_for_now":
            break
    return count


def mark_resolved(thread: Thread) -> None:
    """After a success, the errors before it were fixed. Keep them in the log, hide them from the model."""
    for event in reversed(thread.events[:-1]):
        if event.type in RESETS:
            break
        if event.type == "error":
            event.resolved = True


def execute(thread: Thread) -> None:
    last_call = next(e for e in reversed(thread.events) if e.type == "tool_call")
    call = parse_tool_call(last_call.data)
    try:
        thread.add("tool_result", run_tool(call))
        mark_resolved(thread)
    except Exception as err:
        thread.add("error", format_error(err, call.name))


def escalate(thread: Thread, attempts: int) -> None:
    """Hand the problem to a human (Lesson 7) instead of retrying forever."""
    last_error = next(e.data for e in reversed(thread.events) if e.type == "error")
    question = f"I'm stuck after {attempts} failed attempts. Last error: {last_error} What should I do?"
    thread.add("tool_call", json.dumps({"function": "request_human_input", "question": question}))


def run_resilient(
    thread: Thread,
    ask: Callable = ask_llm,
    max_consecutive: int = MAX_CONSECUTIVE_ERRORS,
    max_steps: int = MAX_STEPS,
) -> str:
    """Returns done, escalated (a question for a human is pending), or stopped."""
    for _ in range(max_steps):
        if status(thread) == "done":
            return "done"
        streak = consecutive_errors(thread)
        if streak >= max_consecutive:
            escalate(thread, streak)
            return "escalated"
        if status(thread) == "ready_to_execute":
            execute(thread)
        else:
            decide(thread, ask)
    if status(thread) == "done":
        return "done"
    thread.add("error", f"Stopped after {max_steps} steps without finishing")
    return "stopped"
