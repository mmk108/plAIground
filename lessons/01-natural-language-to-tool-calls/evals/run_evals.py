"""Measure translation accuracy. Run from this folder: python run_evals.py"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "starter"))

from translate import determine_next_step  # noqa: E402

cases = json.loads((Path(__file__).parent / "cases.json").read_text())
passed = 0
for case in cases:
    try:
        call = determine_next_step(case["input"])
        got_function = call.function
        got = call.model_dump()
    except ValueError:
        # 'unsupported' isn't in our schemas, so it is correctly rejected
        got_function = "unsupported"
        got = {}
    ok = got_function == case["expected_function"] and all(
        got.get(k) == v for k, v in case["expected"].items()
    )
    passed += ok
    print(("PASS" if ok else "FAIL"), "-", case["input"])
print(f"\n{passed}/{len(cases)} passed")
