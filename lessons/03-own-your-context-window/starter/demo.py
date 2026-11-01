"""See exactly what the model would receive. No API key needed.

Run: python lessons/03-own-your-context-window/starter/demo.py
Add --ask to send the context to the model (needs an API key).
"""
import sys
from pathlib import Path

from context import Thread, thread_to_prompt

DATA = Path(__file__).parent.parent / "data" / "customers.csv"

if __name__ == "__main__":
    thread = Thread()
    thread.add("user_request", "Which plan has the highest average monthly spend?")

    bad = thread.add("error", "read_spreadsheet: file not found: customer.csv")
    thread.add("read_spreadsheet", "filename: customers.csv")
    bad.resolved = True  # the retry worked, so hide the old error

    thread.add("read_spreadsheet_result", DATA.read_text(encoding="utf-8"))

    prompt = thread_to_prompt(thread)
    print("=== RAW FILE (never sent) ===")
    print(DATA.read_text(encoding="utf-8"))
    print("=== CONTEXT THE MODEL SEES ===")
    print(prompt)

    if "--ask" in sys.argv:
        sys.path.insert(0, str(Path(__file__).parents[3]))
        from shared.llm import ask_llm

        print("\n=== MODEL ANSWER ===")
        print(ask_llm("You analyze data. Answer briefly.", prompt))
