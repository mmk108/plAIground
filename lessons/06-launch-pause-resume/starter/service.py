"""A simple API to launch, check, and resume an agent. Pausing is safe because the thread is saved.

launch(request)        -> start a new agent run
get_status(id)         -> what is it doing? is it waiting for me?
resume(id, approved)   -> answer a paused agent and continue
"""
import sys
import uuid
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).parents[3]
sys.path.insert(0, str(ROOT / "lessons" / "05-unify-execution-state" / "starter"))

from agent import execute_pending, load_thread, run, save_thread, status, summary  # noqa: E402
from context import Thread  # noqa: E402
from tools import TOOLS, parse_tool_call  # noqa: E402

from shared.llm import ask_llm  # noqa: E402

DEFAULT_STORE = ROOT / "threads"


def needs_approval(call) -> bool:
    """Risky tools (real-world effects) must wait for a human."""
    return TOOLS[call.name].risky


def _path(store: Path, thread_id: str) -> Path:
    return store / f"{thread_id}.json"


def _advance(thread_id: str, thread: Thread, store: Path, ask: Callable) -> dict:
    run(thread, ask=ask, pause_before=needs_approval)
    save_thread(thread, _path(store, thread_id))  # saved every time, so we can stop at any point
    return get_status(thread_id, store)


def launch(request: str, store: Path = DEFAULT_STORE, ask: Callable = ask_llm) -> dict:
    thread = Thread()
    thread.add("user_request", request)
    return _advance(uuid.uuid4().hex[:8], thread, store, ask)


def get_status(thread_id: str, store: Path = DEFAULT_STORE) -> dict:
    thread = load_thread(_path(store, thread_id))
    info = {"id": thread_id, **summary(thread), "waiting_for": None, "answer": None}
    if status(thread) == "ready_to_execute":
        pending = parse_tool_call(thread.events[-1].data)
        if needs_approval(pending):
            info["status"] = "paused"
            info["waiting_for"] = pending.raw
    elif status(thread) == "done":
        info["answer"] = parse_tool_call(thread.events[-1].data).args.message
    return info


def resume(thread_id: str, approved: bool, store: Path = DEFAULT_STORE, ask: Callable = ask_llm) -> dict:
    if get_status(thread_id, store)["status"] != "paused":
        raise ValueError(f"Agent {thread_id} is not waiting for approval")
    thread = load_thread(_path(store, thread_id))
    thread.add("human_response", "approved" if approved else "rejected")
    if approved:
        execute_pending(thread)
    else:
        thread.add("tool_result", "The human rejected this action. Do not retry it.")
    return _advance(thread_id, thread, store, ask)


def list_agents(store: Path = DEFAULT_STORE) -> list[dict]:
    return [get_status(p.stem, store) for p in sorted(store.glob("*.json"))] if store.exists() else []
