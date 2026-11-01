"""Asking a human is just another tool call: request_human_input.

The model doesn't "chat" with the user. It emits a structured request, the agent saves its
thread and stops, and a human answer later arrives as an event. Same pause/resume as Lesson 6.

launch(request)        -> start; may end up waiting for a question or an approval
get_status(id)         -> what is it waiting for, exactly?
reply(id, answer)      -> the human's answer (text for a question, yes/no for an approval)
"""
import sys
import uuid
from pathlib import Path
from typing import Callable, Literal

ROOT = Path(__file__).parents[3]
for sub in ("", "lessons/03-own-your-context-window/starter", "lessons/04-tools-are-structured-outputs/starter",
            "lessons/05-unify-execution-state/starter"):
    sys.path.insert(0, str(ROOT / sub))

from pydantic import BaseModel, Field  # noqa: E402

from agent import execute_pending, load_thread, run, save_thread, status, summary  # noqa: E402
from context import Thread  # noqa: E402
from tools import TOOLS, Tool, parse_tool_call  # noqa: E402

from shared.llm import ask_llm  # noqa: E402

DEFAULT_STORE = ROOT / "threads"
ASK = "request_human_input"
YES = {"yes", "y", "approve", "approved", "ok"}
NO = {"no", "n", "reject", "rejected"}


# ---- 1. Asking a human is a tool, so it's described like any other ----

class RequestHumanInput(BaseModel):
    question: str = Field(description="what you need to know")
    format: Literal["free_text", "yes_no", "multiple_choice"] = "free_text"
    choices: list[str] = Field(default_factory=list, description="options, if multiple_choice")
    urgency: Literal["low", "medium", "high"] = "low"


def register() -> None:
    """Add the tool to the Lesson 4 registry. Adding a tool is one entry."""
    TOOLS[ASK] = Tool(ASK, "Ask the human a question when you are missing information.", RequestHumanInput)


register()


# ---- 2. What makes the agent stop? ----

def waits_for_human(call) -> bool:
    return call.name == ASK or TOOLS[call.name].risky


def _path(store: Path, thread_id: str) -> Path:
    return store / f"{thread_id}.json"


def _advance(thread_id: str, thread: Thread, store: Path, ask: Callable) -> dict:
    run(thread, ask=ask, pause_before=waits_for_human)
    save_thread(thread, _path(store, thread_id))
    return get_status(thread_id, store)


# ---- 3. The API ----

def launch(request: str, store: Path = DEFAULT_STORE, ask: Callable = ask_llm, source: str | None = None) -> dict:
    thread = Thread()
    if source:
        thread.add("trigger", source)  # Lesson 11 uses this to remember where a request came from
    thread.add("user_request", request)
    return _advance(uuid.uuid4().hex[:8], thread, store, ask)


def get_status(thread_id: str, store: Path = DEFAULT_STORE) -> dict:
    thread = load_thread(_path(store, thread_id))
    info = {"id": thread_id, **summary(thread), "waiting_for": None, "answer": None}
    if status(thread) == "ready_to_execute":
        pending = parse_tool_call(thread.events[-1].data)
        if pending.name == ASK:
            info["status"] = "waiting_for_human"
            info["waiting_for"] = {"kind": "question", **pending.args.model_dump()}
        elif TOOLS[pending.name].risky:
            info["status"] = "waiting_for_human"
            info["waiting_for"] = {"kind": "approval", "action": pending.raw}
    elif status(thread) == "done":
        info["answer"] = parse_tool_call(thread.events[-1].data).args.message
    return info


def _check_answer(waiting: dict, answer: str) -> str:
    """Validate the human's answer against what was asked. Returns the cleaned answer."""
    answer = answer.strip()
    if not answer:
        raise ValueError("Answer is empty")
    if waiting["kind"] == "approval" or waiting["format"] == "yes_no":
        if answer.lower() not in YES | NO:
            raise ValueError("Please answer yes or no")
    elif waiting["format"] == "multiple_choice" and answer not in waiting["choices"]:
        raise ValueError(f"Please pick one of: {', '.join(waiting['choices'])}")
    return answer


def reply(thread_id: str, answer: str, store: Path = DEFAULT_STORE, ask: Callable = ask_llm) -> dict:
    waiting = get_status(thread_id, store)["waiting_for"]
    if waiting is None:
        raise ValueError(f"Agent {thread_id} is not waiting for a human")
    answer = _check_answer(waiting, answer)
    thread = load_thread(_path(store, thread_id))

    if waiting["kind"] == "question":
        thread.add("human_response", answer)  # the answer is the result; nothing to execute
    elif answer.lower() in YES:
        thread.add("human_response", "approved")
        execute_pending(thread)
    else:
        thread.add("human_response", "rejected")
        thread.add("tool_result", "The human rejected this action. Do not retry it.")
    return _advance(thread_id, thread, store, ask)
