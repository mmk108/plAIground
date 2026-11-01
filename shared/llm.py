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

    if "done_for_now" in system:
        return _mock_data_agent(system, user)

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


def _mock_data_agent(system: str, user: str) -> str:
    """Mock for Lessons 4-12: decides the next step from the event history in the context."""
    import json
    import re

    first = re.search(r"<user_request>\n(.*?)\n</user_request>", user, re.S)
    request = first.group(1) if first else user
    low = request.lower()
    tags = re.findall(r"<(user_request|tool_call|tool_result|error|done_for_now|human_response)>", user)
    last_tag = tags[-1] if tags else None
    called = set(re.findall(r'"function":\s*"(\w+)"', user))
    results = re.findall(r"<tool_result>\n(.*?)\n</tool_result>", user, re.S)
    last_result = results[-1] if results else ""
    human_replies = re.findall(r"<human_response>\n(.*?)\n</human_response>", user, re.S)
    can_ask = "request_human_input" in system

    def call(**fields) -> str:
        return json.dumps(fields)

    def done(message: str) -> str:
        return call(function="done_for_now", message=message)

    if last_tag == "tool_result" and "rejected" in last_result:
        return done("Understood. I did not send it.")
    if last_tag == "tool_result" and "send_report" in called:
        return done("Done. The report was sent.")
    email = re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", " ".join([request, *human_replies]))
    can_send = "- send_report:" in system
    if low.startswith("send this report") and email and can_send and "send_report" not in called:
        body = request.split(":\n", 1)[-1]
        return call(function="send_report", to=email.group(), subject="Sales report", body=body)
    if "profit" in low and last_tag in ("user_request", "error"):
        # Practice for Lesson 9: first guess a column that doesn't exist, then fix it from the error
        column = "units" if last_tag == "error" else "profit"
        return call(function="group_sum", filename="sales.csv", group_by="region", value_column=column)
    if "files" in low and "list_files" not in called:
        return call(function="list_files")
    wants_data = any(w in low for w in ("sold", "sales", "units", "total", "most", "region", "product"))
    if wants_data and "group_sum" not in called:
        group_by = "product" if "product" in low else "region"
        return call(function="group_sum", filename="sales.csv", group_by=group_by, value_column="units")
    if "email" in low and not email and can_ask and "request_human_input" not in called:
        return call(
            function="request_human_input",
            question="What email address should I send it to?",
            format="free_text",
            urgency="low",
        )
    if email and can_send and "group_sum" in called and "send_report" not in called:
        return call(function="send_report", to=email.group(), subject="Sales report", body=last_result)
    if last_result:
        return done("Here's what I found:\n" + last_result)
    return done("I can't help with that using the tools I have.")


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
