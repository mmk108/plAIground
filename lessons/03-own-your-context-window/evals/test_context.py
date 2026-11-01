"""Offline checks for the context builder. Run: python evals/test_context.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "starter"))

from context import Thread, redact, thread_to_prompt, truncate  # noqa: E402


def check(name: str, ok: bool) -> bool:
    print("PASS" if ok else "FAIL", "-", name)
    return ok


results = [
    check("card numbers are masked", "4111" not in redact("card 4111 1111 1111 1111")),
    check("dashed cards are masked", "5500" not in redact("5500-0000-0000-0004")),
    check("emails are masked", "ana@example.com" not in redact("mail ana@example.com")),
    check("same email gets same placeholder", redact("a@x.com a@x.com").count("[EMAIL_1]") == 2),
    check("short numbers are kept", "120.50" in redact("spend 120.50")),
    check("long text is truncated", "truncated" in truncate("x" * 5000)),
]

t = Thread()
err = t.add("error", "boom")
err.resolved = True
t.add("user_request", "hi")
results.append(check("resolved errors are hidden", "boom" not in thread_to_prompt(t)))

print(f"\n{sum(results)}/{len(results)} passed")
