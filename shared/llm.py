"""One place for all model calls. Lessons only use ask_llm().

Switch providers by changing PROVIDER in your .env file.
"""
import os

from dotenv import load_dotenv

load_dotenv()


def ask_llm(system: str, user: str) -> str:
    """Send a system prompt and a user message, return the model's text reply."""
    provider = os.getenv("PROVIDER", "anthropic").lower()
    if provider == "anthropic":
        return _ask_anthropic(system, user)
    if provider == "github":
        return _ask_github(system, user)
    raise ValueError(f"Unknown PROVIDER '{provider}'. Use 'anthropic' or 'github'.")


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
