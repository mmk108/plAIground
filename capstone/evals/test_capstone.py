"""Offline checks for the assessor and scout. Run: python capstone/evals/test_capstone.py"""
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

os.environ["PROVIDER"] = "mock"
root = Path(__file__).parent.parent
sys.path.insert(0, str(root / "assessor"))
sys.path.insert(0, str(root / "scout"))

import assess  # noqa: E402
import report  # noqa: E402
import rubric  # noqa: E402
import scout  # noqa: E402

results = []


def check(name: str, ok: bool) -> None:
    print("PASS" if ok else "FAIL", "-", name)
    results.append(ok)


# --- rubric
easy = rubric.Task("x", repeatable=3, rules=3, data=3, error_cost=1, sensitivity=1)
risky = rubric.Task("x", repeatable=3, rules=3, data=3, error_cost=3, sensitivity=3)
vague = rubric.Task("x", repeatable=1, rules=1, data=1)
check("low risk and high fit can automate", rubric.control_level(easy) == "automate_with_logs")
check("high risk needs approval", rubric.control_level(risky) == "ai_prepares_human_approves")
check("low fit stays with a person", rubric.control_level(vague) == "keep_human")
try:
    rubric.Task("x", repeatable=5)
    check("bad rating rejected", False)
except ValueError:
    check("bad rating rejected", True)
check("tool plus many steps suggests a harness",
      rubric.build_shape(rubric.Task("x", repeatable=3, rules=3, data=3, tools=["email"], steps=3))
      == "harness + MCP server")

# --- extraction
notes = (root / "examples" / "client_notes.md").read_text(encoding="utf-8")
tasks = assess.extract_tasks(notes)
check("one task per bullet, heading skipped", len(tasks) == 7)
payment = next(t for t in tasks if t.text.startswith("Send a payment"))
check("sending payments is never automated", rubric.control_level(payment) == "keep_human")
negotiate = next(t for t in tasks if "Negotiate" in t.text)
check("judgment work is marked low-rules", negotiate.rules == 1)
check("offline ratings are labelled as guesses", all(t.rated_by == "keywords" for t in tasks))

# --- report
text = report.render(tasks)
check("report has every task", all(t.text in text for t in tasks))
check("report warns that keyword ratings are guesses", "first guesses" in text)

# --- scout (no network: fake fetch)
NOW = datetime(2026, 11, 1, tzinfo=timezone.utc)


def item(name, stars, pushed, lic="MIT", archived=False):
    return {"full_name": name, "description": "d | x", "stargazers_count": stars,
            "pushed_at": pushed, "license": {"spdx_id": lic} if lic else None,
            "archived": archived, "html_url": f"https://github.com/{name}"}


def fake_fetch(url):
    if "mcp" in url:
        return {"items": [item("a/good", 5000, "2026-10-20T00:00:00Z"),
                          item("a/old", 4000, "2024-01-01T00:00:00Z", lic=None),
                          item("a/dead", 9000, "2026-10-01T00:00:00Z", archived=True)]}
    if "skills" in url:
        return {"items": [item("a/good", 5000, "2026-10-20T00:00:00Z"),
                          item("b/new", 10, "2026-10-30T00:00:00Z")]}
    return {"items": []}


short = scout.shortlist("invoices", fake_fetch, NOW)
mcp = short["mcp server"]
check("archived repos are dropped", all(c.full_name != "a/dead" for c in mcp))
check("duplicates across kinds are removed", [c.full_name for c in short["skill"]] == ["b/new"])
check("healthy repo outranks stale repo", mcp[0].full_name == "a/good")
old = next(c for c in mcp if c.full_name == "a/old")
check("stale and unlicensed repo is flagged", "stale" in old.flags and "no clear license" in old.flags)
check("young repo is flagged", "few stars" in short["skill"][0].flags)
out = scout.render("invoices", short)
check("scout report includes install checklist", "Before you install" in out)
check("pipes in descriptions do not break the table", "d / x" in out)
try:
    scout.build_queries("  ")
    check("blank query raises", False)
except ValueError:
    check("blank query raises", True)

print(f"\n{sum(results)}/{len(results)} passed")
sys.exit(0 if all(results) else 1)
