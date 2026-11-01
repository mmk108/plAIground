"""Run: python main.py "create a payment link for $750 to Terri" """
import sys

from dispatcher import dispatch
from translate import determine_next_step

if __name__ == "__main__":
    text = " ".join(sys.argv[1:]) or "create a payment link for $750 to Terri for the AI meetup"
    try:
        call = determine_next_step(text)
    except ValueError as err:
        print(f"Rejected: {err}")
        sys.exit(1)
    print("Model chose:", call.model_dump_json(indent=2))
    print(dispatch(call))
