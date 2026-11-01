"""A tool registry. Each tool = a name, a description, validated inputs, and a function.

Adding a tool means adding one entry to TOOLS. The prompt's tool list is generated from it.
"""
import csv
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from pydantic import BaseModel, Field, ValidationError, field_validator

LESSON = Path(__file__).parent.parent
DATA_DIR = LESSON / "data"
PROMPT_FILE = LESSON / "prompts" / "system.md"


def _safe_csv_name(name: str) -> str:
    if not name.endswith(".csv") or "/" in name or "\\" in name or ".." in name:
        raise ValueError("filename must be a plain .csv name inside data/")
    return name


# ---- 1. Inputs: what the model must provide for each tool ----

class ListFiles(BaseModel):
    pass


class GroupSum(BaseModel):
    filename: str = Field(description="CSV file in data/")
    group_by: str = Field(description="column to group by, e.g. region")
    value_column: str = Field(description="numeric column to add up, e.g. units")

    @field_validator("filename")
    @classmethod
    def check_filename(cls, v: str) -> str:
        return _safe_csv_name(v)


class SendReport(BaseModel):
    to: str = Field(description="recipient email address")
    subject: str
    body: str

    @field_validator("to")
    @classmethod
    def check_email(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("to must be an email address")
        return v


class DoneForNow(BaseModel):
    message: str = Field(description="what to tell the user")


# ---- 2. Actions: plain Python functions. No AI in here. ----

def list_files(_: ListFiles) -> str:
    return "Files: " + ", ".join(sorted(p.name for p in DATA_DIR.glob("*.csv")))


def group_sum(args: GroupSum) -> str:
    path = DATA_DIR / args.filename
    if not path.exists():
        raise FileNotFoundError(f"{args.filename} not found. Use list_files to see what exists.")
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise ValueError(f"{args.filename} has no rows")
    for col in (args.group_by, args.value_column):
        if col not in rows[0]:
            raise ValueError(f"No column '{col}'. Columns are: {', '.join(rows[0])}")
    totals: dict[str, float] = {}
    for row in rows:
        totals[row[args.group_by]] = totals.get(row[args.group_by], 0) + float(row[args.value_column])
    ranked = sorted(totals.items(), key=lambda kv: kv[1], reverse=True)
    return f"{args.value_column} by {args.group_by}: " + ", ".join(f"{k}={v:g}" for k, v in ranked)


def send_report(args: SendReport) -> str:
    return f"[fake] Email sent to {args.to} with subject '{args.subject}'"


# ---- 3. The registry: the single menu of tools ----

@dataclass
class Tool:
    name: str
    description: str
    params: type[BaseModel]
    run: Callable | None = None
    risky: bool = False  # real-world side effects; Lesson 6 pauses for approval
    terminal: bool = False  # ends the agent's turn instead of running code


TOOLS: dict[str, Tool] = {
    t.name: t
    for t in [
        Tool("list_files", "List the CSV files available.", ListFiles, list_files),
        Tool("group_sum", "Add up a numeric column, grouped by another column.", GroupSum, group_sum),
        Tool("send_report", "Email a report to someone.", SendReport, send_report, risky=True),
        Tool("done_for_now", "Reply to the user and stop.", DoneForNow, terminal=True),
    ]
}


# ---- 4. Parsing and running ----

@dataclass
class ToolCall:
    name: str
    args: BaseModel
    raw: str  # normalized JSON, stored in the thread


def parse_tool_call(raw: str, allowed: list[str] | None = None) -> ToolCall:
    """Turn the model's text into a validated ToolCall. Raises ValueError with a helpful message.

    allowed limits the menu (Lesson 10 uses this to give each small agent its own tools).
    """
    cleaned = re.sub(r"^```(?:json)?|```$", "", raw.strip(), flags=re.MULTILINE).strip()
    try:
        obj = json.loads(cleaned)
    except json.JSONDecodeError as err:
        raise ValueError(f"Reply was not valid JSON: {err}")
    if not isinstance(obj, dict) or "function" not in obj:
        raise ValueError('Reply must be a JSON object with a "function" field')
    name = obj["function"]
    menu = allowed if allowed is not None else list(TOOLS)
    if name not in TOOLS or name not in menu:
        raise ValueError(f"Unknown tool '{name}'. Choose from: {', '.join(menu)}")
    fields = {k: v for k, v in obj.items() if k != "function"}
    try:
        args = TOOLS[name].params.model_validate(fields)
    except ValidationError as err:
        problems = "; ".join(f"{'.'.join(map(str, e['loc']))}: {e['msg']}" for e in err.errors())
        raise ValueError(f"Bad arguments for {name}: {problems}")
    return ToolCall(name, args, json.dumps(obj))


def run_tool(call: ToolCall, dry_run: bool = False) -> str:
    """The same tool call can be handled differently. A dry run only describes it."""
    if dry_run:
        return f"[dry run] would run {call.name} with {call.args.model_dump()}"
    return TOOLS[call.name].run(call.args)


# ---- 5. Prompt text generated from the registry ----

def tool_prompt(names: list[str] | None = None) -> str:
    lines = []
    for tool in TOOLS.values():
        if names is not None and tool.name not in names:
            continue
        fields = ", ".join(
            f"{name} ({getattr(f.annotation, '__name__', f.annotation)})"
            + (f": {f.description}" if f.description else "")
            for name, f in tool.params.model_fields.items()
        )
        lines.append(f"- {tool.name}: {tool.description}\n  fields: {fields or '(none)'}")
    return "\n".join(lines)


def build_system_prompt(names: list[str] | None = None) -> str:
    return PROMPT_FILE.read_text(encoding="utf-8").replace("{{TOOLS}}", tool_prompt(names))
