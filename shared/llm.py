"""One place for all model calls. Lessons only use ask_llm().

Switch providers by changing PROVIDER in your .env file.
"""
import os

from dotenv import load_dotenv

load_dotenv()


def ask_llm(system: str, user: str) -> str:
    """Send a system prompt and a user message, return the model's text reply."""
    provider = os.getenv("PROVIDER", "mock").lower()
    if provider == "mock":
        return _ask_mock(system, user)
    if provider == "anthropic":
        return _ask_anthropic(system, user)
    if provider == "github":
        return _ask_github(system, user)
    raise ValueError(f"Unknown PROVIDER '{provider}'. Use 'mock', 'anthropic' or 'github'.")


def _ask_mock(system: str, user: str) -> str:
    """A free, offline stand-in for a model. NOT a real LLM: it follows simple rules.

    It only imitates the Lesson 1-2 tool-picking task. If the prompt has no
    'unsupported' option, it behaves naively, so weak prompts visibly fail.
    """
    import json
    import re

    if "tool" not in system.lower():
        return "[mock model] Set PROVIDER=anthropic or github in .env to get a real answer."

    careful = "unsupported" in system.lower()

    def unsupported(reason: str) -> str:
        return json.dumps({"function": "unsupported", "reason": reason})

    url = re.search(r"https?://\S+", user)
    if url:
        return json.dumps({"function": "fetch_webpage", "url": url.group()})
    csv_name = re.search(r"[\w./\\:-]*\.csv", user)
    if csv_name:
        name = csv_name.group()
        if careful and (".." in name or "/" in name or "\\" in name):
            return unsupported("Only plain file names are allowed")
        return json.dumps({"function": "read_spreadsheet", "filename": name})
    if not careful:
        return json.dumps({"function": "read_spreadsheet", "filename": "data.csv"})  # a bad guess
    return unsupported("No matching tool, or no file name or URL given")


def _ask_anthropic(system: str, user: str) -> str:
    import anthropic

    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY
    response = client.messages.create(
        model=os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5"),
        max_tokens=1024,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return response.content[0].text


def _ask_github(system: str, user: str) -> str:
    from openai import OpenAI

    client = OpenAI(
        base_url="https://models.github.ai/inference",
        api_key=os.environ["GITHUB_TOKEN"],
    )
    response = client.chat.completions.create(
        model=os.getenv("GITHUB_MODEL", "openai/gpt-4o-mini"),
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    return response.choices[0].message.content
