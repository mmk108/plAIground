"""Run: python capstone/scout/cli.py "invoice processing" [-o shortlist.md]

Searches GitHub (read-only) and prints a shortlist. Set GITHUB_TOKEN for a higher rate limit.
"""
import argparse
import sys
import urllib.error
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import scout  # noqa: E402


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Find skills, MCP servers and plugins on GitHub.")
    parser.add_argument("task", help="what you want the agent to do, in plain words")
    parser.add_argument("-o", "--output", help="write the shortlist to this file")
    args = parser.parse_args()
    try:
        text = scout.render(args.task, scout.shortlist(args.task))
    except urllib.error.HTTPError as e:
        print(f"GitHub returned {e.code}. If it is 403, wait a minute or set GITHUB_TOKEN.",
              file=sys.stderr)
        return 1
    except (urllib.error.URLError, ValueError) as e:
        print(f"Could not search: {e}", file=sys.stderr)
        return 1
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
        print(f"Wrote {args.output}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
