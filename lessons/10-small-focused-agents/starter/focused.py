"""Small, focused agents: each does ONE job with its own tools and a step budget.

A plain-Python router connects them. The agents are the smart parts; the system around them is
ordinary, predictable code.

   request --> [router] --> analyst agent --> (report) --> emailer agent --> (needs approval) --> sent
"""
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).parents[3]
for sub in ("", "lessons/03-own-your-context-window/starter", "lessons/04-tools-are-structured-outputs/starter",
            "lessons/05-unify-execution-state/starter"):
    sys.path.insert(0, str(ROOT / sub))

from agent import execute_pending, run  # noqa: E402
from context import Thread  # noqa: E402
from tools import TOOLS, parse_tool_call  # noqa: E402

from shared.llm import ask_llm  # noqa: E402

EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")


# ---- 1. A small agent is a name, a short tool list, and a step budget ----

@dataclass
class SmallAgent:
    name: str
    tools: list[str]  # the ONLY tools it can see or call
    max_steps: int  # keeps its context window short


ANALYST = SmallAgent("analyst", ["list_files", "group_sum", "done_for_now"], max_steps=6)
EMAILER = SmallAgent("emailer", ["send_report", "done_for_now"], max_steps=4)


def needs_approval(call) -> bool:
    return TOOLS[call.name].risky


def run_agent(agent: SmallAgent, request: str, ask: Callable = ask_llm) -> tuple[Thread, str]:
    thread = Thread()
    thread.add("user_request", request)
    outcome = run(thread, ask=ask, pause_before=needs_approval, max_steps=agent.max_steps, tools=agent.tools)
    return thread, outcome


def final_message(thread: Thread) -> str:
    return parse_tool_call(thread.events[-1].data).args.message


# ---- 2. The router: plain code, no model needed ----

def pipeline(request: str, ask: Callable = ask_llm) -> dict:
    """Analyst first. If the user also wants an email, hand its report to the emailer."""
    analyst_thread, outcome = run_agent(ANALYST, request, ask)
    result = {"status": "failed", "answer": None, "threads": {"analyst": analyst_thread}, "emailer_thread": None}
    if outcome != "done":
        return result
    report = final_message(analyst_thread)
    result["answer"] = report

    wants_email = "email" in request.lower()
    address = EMAIL.search(request)
    if not wants_email:
        result["status"] = "done"
    elif not address:
        result["status"] = "needs_input"  # the router knows what's missing without asking a model
        result["answer"] = report + "\n\nWho should I email this to?"
    else:
        emailer_thread, outcome = run_agent(EMAILER, f"Send this report to {address.group()}:\n{report}", ask)
        result["threads"]["emailer"] = emailer_thread
        result["emailer_thread"] = emailer_thread
        result["status"] = "waiting_for_approval" if outcome == "paused" else "failed"
    return result


def approve(result: dict, approved: bool, ask: Callable = ask_llm) -> dict:
    """A human answers the emailer's pending action."""
    thread = result["emailer_thread"]
    if result["status"] != "waiting_for_approval":
        raise ValueError("Nothing is waiting for approval")
    thread.add("human_response", "approved" if approved else "rejected")
    if approved:
        execute_pending(thread)
    else:
        thread.add("tool_result", "The human rejected this action. Do not retry it.")
    outcome = run(thread, ask=ask, pause_before=needs_approval, max_steps=EMAILER.max_steps, tools=EMAILER.tools)
    result["status"] = "done" if outcome == "done" else "failed"
    result["answer"] = final_message(thread) if outcome == "done" else None
    return result
