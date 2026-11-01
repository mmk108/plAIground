"""Run: python main.py "summarize sales.csv for me" """
import sys

from dispatcher import dispatch
from translate import determine_next_step

if __name__ == "__main__":
    text = " ".join(sys.argv[1:]) or "what's in sales.csv?"
    try:
        call = determine_next_step(text)
    except ValueError as err:
        print(f"Rejected: {err}")
        sys.exit(1)
    print("Model chose:", call.model_dump_json(indent=2))
    print("\nResult:\n" + dispatch(call))
