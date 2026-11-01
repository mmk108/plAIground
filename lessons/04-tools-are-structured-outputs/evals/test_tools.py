"""Offline checks for the tool registry. Run: python evals/test_tools.py"""
import os
import sys
from pathlib import Path

os.environ["PROVIDER"] = "mock"
sys.path.insert(0, str(Path(__file__).parents[3]))
sys.path.insert(0, str(Path(__file__).parent.parent / "starter"))

from tools import build_system_prompt, parse_tool_call, run_tool  # noqa: E402

from shared.llm import ask_llm  # noqa: E402


def check(name: str, ok: bool) -> bool:
    print("PASS" if ok else "FAIL", "-", name)
    return ok


def rejects(raw: str, expect: str) -> bool:
    try:
        parse_tool_call(raw)
    except ValueError as err:
        return expect in str(err)
    return False


good = '{"function": "group_sum", "filename": "sales.csv", "group_by": "region", "value_column": "units"}'
call = parse_tool_call(good)
mail = parse_tool_call('{"function": "send_report", "to": "a@b.com", "subject": "s", "body": "b"}')

results = [
    check("valid call is parsed", call.name == "group_sum"),
    check("fenced JSON is accepted", parse_tool_call(f"```json\n{good}\n```").name == "group_sum"),
    check("unknown tool names the valid ones", rejects('{"function": "hack"}', "list_files")),
    check("bad email is rejected", rejects('{"function": "send_report", "to": "nope", "subject": "s", "body": "b"}', "email")),
    check("path tricks are rejected", rejects('{"function": "group_sum", "filename": "../x.csv", "group_by": "a", "value_column": "b"}', "group_sum")),
    check("non-JSON is rejected", rejects("sure, here you go", "JSON")),
    check("group_sum adds correctly", "East=32" in run_tool(call)),
    check("dry run does not run", "[dry run]" in run_tool(mail, dry_run=True) and "[fake]" not in run_tool(mail, dry_run=True)),
    check("prompt lists every tool", all(t in build_system_prompt() for t in ("list_files", "group_sum", "send_report", "done_for_now"))),
    check("mock picks group_sum for a data question", parse_tool_call(ask_llm(build_system_prompt(), "which region sold the most units?")).name == "group_sum"),
    check("mock refuses an unrelated request", parse_tool_call(ask_llm(build_system_prompt(), "book me a flight")).name == "done_for_now"),
]
print(f"\n{sum(results)}/{len(results)} passed")
