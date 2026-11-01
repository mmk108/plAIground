"""Measure translation accuracy. Run: python evals/run_evals.py"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "starter"))

from translate import determine_next_step  # noqa: E402

cases = json.loads((Path(__file__).parent / "cases.json").read_text())
passed = 0
for case in cases:
    try:
        got = determine_next_step(case["input"]).model_dump()
    except ValueError:
        # Rejected by validation (e.g. unsafe path). Counts as 'unsupported'.
        got = {"function": "unsupported"}
    # A case passes if every expected field matches
    ok = all(got.get(k) == v for k, v in case["expected"].items())
    passed += ok
    print("PASS" if ok else "FAIL", "-", case["input"])
print(f"\n{passed}/{len(cases)} passed")
