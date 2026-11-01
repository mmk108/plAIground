"""Run the agent, save its thread, reload it, and see that nothing was lost.

Run: python lessons/05-unify-execution-state/starter/demo.py "Which region sold the most units?"
"""
import sys
from pathlib import Path

from agent import load_thread, run, save_thread, status, summary, to_markdown
from context import Thread

SAVE_PATH = Path(__file__).parents[3] / "threads" / "lesson5-demo.json"

if __name__ == "__main__":
    request = " ".join(sys.argv[1:]) or "Which region sold the most units?"
    thread = Thread()
    thread.add("user_request", request)

    final = run(thread)
    print("=== EVERYTHING THE AGENT KNOWS (the thread) ===")
    print(to_markdown(thread))
    print("\nState worked out from the thread:", summary(thread))

    save_thread(thread, SAVE_PATH)
    reloaded = load_thread(SAVE_PATH)
    print(f"\nSaved to {SAVE_PATH}")
    print("Reloaded from file, state:", summary(reloaded))
    assert status(reloaded) == status(thread) == final
