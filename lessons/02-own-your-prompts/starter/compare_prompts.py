"""Compare prompt versions on the same test cases.

Run: python lessons/02-own-your-prompts/starter/compare_prompts.py
Reuses the tools from Lesson 1, so only the prompt changes between runs.
"""
import json
import sys
from pathlib import Path

LESSON_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(LESSON_DIR.parent / "01-natural-language-to-tool-calls" / "starter"))

from translate import determine_next_step  # noqa: E402


def score(prompt_path: Path, cases: list[dict]) -> tuple[int, list[str]]:
    passed, failures = 0, []
    for case in cases:
        try:
            got = determine_next_step(case["input"], prompt_path).model_dump()
        except ValueError:
            got = {"function": "unsupported"}
        if all(got.get(k) == v for k, v in case["expected"].items()):
            passed += 1
        else:
            failures.append(f'{case["input"]!r} -> {got}')
    return passed, failures


if __name__ == "__main__":
    cases = json.loads((LESSON_DIR / "evals" / "cases.json").read_text())
    for prompt_path in sorted((LESSON_DIR / "prompts").glob("*.md")):
        passed, failures = score(prompt_path, cases)
        print(f"{prompt_path.name}: {passed}/{len(cases)} passed")
        for f in failures:
            print("   FAIL:", f)
