"""Turn messy workflow notes into scored tasks.

Offline: keyword guesses (rated_by="keywords"). With a real PROVIDER the model
proposes ratings as JSON, and the result is validated like any tool call (Lesson 4).
Either way a person reviews the ratings: the report says who rated each task.
"""
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "shared"))

from rubric import Task  # noqa: E402

TOOL_WORDS = {
    "spreadsheet": ["excel", "spreadsheet", "csv", "sheet"],
    "email": ["email", "e-mail", "inbox"],
    "crm": ["crm", "salesforce", "hubspot"],
    "web": ["website", "web page", "portal", "online"],
    "database": ["sql", "database", "warehouse"],
    "chat": ["slack", "teams"],
    "documents": ["pdf", "contract", "document", "report", "deck"],
}
REPEAT = ["weekly", "daily", "monthly", "every", "each", "recurring", "routine", "quarterly"]
RULEY = ["format", "copy", "compile", "reconcile", "summar", "look up", "lookup", "extract",
         "compare", "check", "calculate", "list", "update", "pull", "collect", "log", "track"]
JUDGMENT = ["negotiat", "decide", "judge", "strategy", "relationship", "approve", "creative",
            "persuade", "coach", "interview"]
HIGH_COST = ["payment", "invoice", "legal", "contract", "compliance", "regulat", "hire",
             "terminate", "refund", "wire", "audit", "customer-facing", "to the client"]
SENSITIVE = ["salary", "medical", "patient", "personal", "confidential", "pii", "ssn", "bank",
             "passport"]
CUSTOMER = ["client", "customer", "vendor", "supplier"]

SYSTEM_PROMPT = """You rate workplace tasks for AI suitability.
Return ONLY JSON: {"tasks": [{"text": str, "repeatable": 1-3, "rules": 1-3, "data": 1-3,
"error_cost": 1-3, "sensitivity": 1-3, "tools": [str], "steps": int}]}
repeatable: 3 = happens often. rules: 3 = clear rules, 1 = needs judgment.
data: 3 = inputs are already digital. error_cost: 3 = a mistake is costly.
sensitivity: 3 = confidential or regulated data. One entry per task. Do not invent tasks."""


def split_tasks(notes: str) -> list[str]:
    """One task per bullet, numbered item or non-empty line. Headings are skipped."""
    tasks = []
    for line in notes.splitlines():
        line = re.sub(r"^\s*(?:[-*•]|\d+[.)])\s*", "", line).strip()
        if line and not line.startswith("#") and len(line.split()) >= 3:
            tasks.append(line)
    return tasks


def rate_offline(text: str) -> Task:
    low = text.lower()
    has = lambda words: any(w in low for w in words)  # noqa: E731
    tools = [name for name, words in TOOL_WORDS.items() if has(words)]
    rules = 1 if has(JUDGMENT) else 3 if has(RULEY) else 2
    sensitivity = 3 if has(SENSITIVE) else 2 if has(CUSTOMER) else 1
    steps = 1 + len(re.findall(r"\b(?:then|and then|after that|before)\b|,\s*then", low))
    return Task(
        text=text,
        repeatable=3 if has(REPEAT) else 2,
        rules=rules,
        data=3 if tools else 1,
        error_cost=3 if has(HIGH_COST) else 2,
        sensitivity=sensitivity,
        tools=tools,
        steps=steps,
    )


def _task_from_json(item: dict) -> Task:
    return Task(
        text=str(item["text"]),
        repeatable=int(item["repeatable"]),
        rules=int(item["rules"]),
        data=int(item["data"]),
        error_cost=int(item["error_cost"]),
        sensitivity=int(item["sensitivity"]),
        tools=[str(t) for t in item.get("tools", [])],
        steps=max(1, int(item.get("steps", 1))),
        rated_by="model",
    )


def rate_with_model(notes: str) -> list[Task]:
    from llm import ask_llm

    raw = ask_llm(SYSTEM_PROMPT, notes)
    match = re.search(r"\{.*\}", raw, re.S)
    if not match:
        raise ValueError("model reply had no JSON")
    data = json.loads(match.group())
    return [_task_from_json(item) for item in data["tasks"]]


def extract_tasks(notes: str) -> list[Task]:
    """Model ratings if a real provider is set and its reply is valid. Otherwise keywords."""
    if os.getenv("PROVIDER", "mock").lower() != "mock":
        try:
            tasks = rate_with_model(notes)
            if tasks:
                return tasks
        except (ValueError, KeyError, TypeError, json.JSONDecodeError):
            pass
    return [rate_offline(t) for t in split_tasks(notes)]
