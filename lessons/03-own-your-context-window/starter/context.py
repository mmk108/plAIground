"""Build the model's context window from events: redact, truncate, format."""
import re
from dataclasses import dataclass, field

CARD = re.compile(r"\b(?:\d[ -]?){13,19}\b")
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")


@dataclass
class Event:
    type: str  # e.g. "user_request", "read_spreadsheet", "read_spreadsheet_result", "error"
    data: str
    resolved: bool = False  # set True on errors that were later fixed


@dataclass
class Thread:
    events: list[Event] = field(default_factory=list)

    def add(self, type: str, data: str) -> Event:
        event = Event(type, data)
        self.events.append(event)
        return event


def redact(text: str) -> str:
    """Mask sensitive values so the model never sees them."""
    emails: dict[str, str] = {}

    def mask_email(match: re.Match) -> str:
        return emails.setdefault(match.group(), f"[EMAIL_{len(emails) + 1}]")

    text = CARD.sub("[CARD_REDACTED]", text)
    return EMAIL.sub(mask_email, text)


def truncate(text: str, max_chars: int = 1500) -> str:
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + f"\n... [truncated {len(text) - max_chars} more characters]"


def event_to_prompt(event: Event) -> str:
    data = truncate(redact(event.data))
    return f"<{event.type}>\n{data}\n</{event.type}>"


def thread_to_prompt(thread: Thread, question: str = "What's the next step?") -> str:
    # Resolved errors are noise once the problem is fixed, so leave them out
    visible = [e for e in thread.events if not (e.type == "error" and e.resolved)]
    body = "\n\n".join(event_to_prompt(e) for e in visible)
    return f"Here's everything that happened so far:\n\n{body}\n\n{question}"
