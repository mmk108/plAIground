"""One step: sentence in, validated tool call out, then run it (or just describe it).

Run: python lessons/04-tools-are-structured-outputs/starter/demo.py "which region sold the most units?"
Add --dry-run to see what WOULD happen without running anything.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[3]))

from tools import build_system_prompt, parse_tool_call, run_tool, tool_prompt  # noqa: E402

from shared.llm import ask_llm  # noqa: E402

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    text = " ".join(args) or "which region sold the most units?"
    dry_run = "--dry-run" in sys.argv

    print("=== TOOL MENU (generated from the registry) ===")
    print(tool_prompt())

    raw = ask_llm(build_system_prompt(), text)
    print("\n=== MODEL REPLY ===")
    print(raw)

    try:
        call = parse_tool_call(raw)
    except ValueError as err:
        print("\nRejected:", err)
        sys.exit(1)

    print(f"\n=== RESULT ({'dry run' if dry_run else 'real'}) ===")
    try:
        print(run_tool(call, dry_run=dry_run))
    except Exception as err:
        print("Tool failed:", err)
