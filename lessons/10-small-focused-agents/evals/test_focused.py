"""Offline checks for small focused agents. Run: python evals/test_focused.py"""
import json
import os
import sys
from pathlib import Path

os.environ["PROVIDER"] = "mock"
sys.path.insert(0, str(Path(__file__).parent.parent / "starter"))

import focused  # noqa: E402
from tools import build_system_prompt  # noqa: E402


def check(name: str, ok: bool) -> bool:
    print("PASS" if ok else "FAIL", "-", name)
    return ok


def sent(result: dict) -> bool:
    return any("[fake] Email sent" in e.data for e in result["emailer_thread"].events)


# Read-only question: only the analyst runs
read = focused.pipeline("Which region sold the most units?")

# Email request: analyst -> router -> emailer -> approval pause
mail = focused.pipeline("Email the total units by region to boss@example.com")
sent_while_waiting = sent(mail)
mail = focused.approve(mail, approved=True)

# Rejection
no = focused.pipeline("Email the total units by region to boss@example.com")
no = focused.approve(no, approved=False)

# Router spots a missing address without calling a model
missing = focused.pipeline("Email the total units by region to my boss")

# Each agent only gets its own tools, in the prompt AND in validation
analyst_prompt = build_system_prompt(focused.ANALYST.tools)
emailer_prompt = build_system_prompt(focused.EMAILER.tools)
wrong_tool = lambda system, user: json.dumps(  # noqa: E731
    {"function": "send_report", "to": "a@b.com", "subject": "x", "body": "y"}
)
_, wrong_outcome = focused.run_agent(focused.ANALYST, "total units by region", ask=wrong_tool)
wrong_thread, _ = focused.run_agent(focused.ANALYST, "total units by region", ask=wrong_tool)

# Step budget: an agent that never finishes is stopped
spin = lambda system, user: json.dumps({"function": "list_files"})  # noqa: E731
_, spin_outcome = focused.run_agent(focused.EMAILER.__class__("tiny", ["list_files", "done_for_now"], 3), "x", ask=spin)

results = [
    check("simple question needs only the analyst", read["status"] == "done" and "emailer" not in read["threads"]),
    check("email request pauses before sending", mail is not None and not sent_while_waiting),
    check("approval sends the email", mail["status"] == "done" and sent(mail)),
    check("rejection does not send", no["status"] == "done" and not sent(no)),
    check("router asks for a missing address", missing["status"] == "needs_input" and "Who should I email" in missing["answer"]),
    check("analyst prompt hides send_report", "send_report" in emailer_prompt and "- send_report" not in analyst_prompt),
    check("emailer prompt hides data tools", "- group_sum" not in emailer_prompt and "- group_sum" in analyst_prompt),
    check("agent can't call a tool outside its list", wrong_outcome != "done" and any("Unknown tool" in e.data for e in wrong_thread.events)),
    check("step budget stops a runaway agent", spin_outcome == "stopped"),
    check("each agent's thread stays short", all(len(t.events) <= 6 for t in mail["threads"].values())),
]
print(f"\n{sum(results)}/{len(results)} passed")
