"""Translate natural language into a validated ToolCall (the LLM part)."""
import json
import re
from pathlib import Path

from pydantic import TypeAdapter, ValidationError

from schemas import ToolCall
from shared.llm import ask_llm

PROMPT_FILE = Path(__file__).parent.parent / "prompts" / "system.md"


def determine_next_step(user_text: str) -> ToolCall:
    """Ask the model for a tool call and validate it. Raises ValueError if invalid."""
    raw = ask_llm(PROMPT_FILE.read_text(encoding="utf-8"), user_text)
    # Models sometimes wrap JSON in ```json fences
    cleaned = re.sub(r"^```(?:json)?|```$", "", raw.strip(), flags=re.MULTILINE).strip()
    try:
        return TypeAdapter(ToolCall).validate_python(json.loads(cleaned))
    except (json.JSONDecodeError, ValidationError) as err:
        raise ValueError(f"Model output was not a valid tool call: {err}\nRaw: {raw}")
