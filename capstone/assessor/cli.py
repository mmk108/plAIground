"""Run: python capstone/assessor/cli.py notes.txt [-o assessment.md]

Reads workflow notes, writes a markdown assessment. Never sends or changes anything else.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import assess  # noqa: E402
import report  # noqa: E402


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Score workflow notes for AI fit and control.")
    parser.add_argument("notes", help="text or markdown file with one task per line")
    parser.add_argument("-o", "--output", help="write the report here instead of printing it")
    args = parser.parse_args()

    notes = Path(args.notes).read_text(encoding="utf-8")
    tasks = assess.extract_tasks(notes)
    if not tasks:
        print("No tasks found. Put one task per line.", file=sys.stderr)
        return 1
    text = report.render(tasks)
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
        print(f"Wrote {args.output}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
