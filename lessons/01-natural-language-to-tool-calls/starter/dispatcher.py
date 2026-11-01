"""Plain code that runs a validated tool call. No LLM in here."""
from schemas import CreatePaymentLink, SendEmail, ToolCall


def dispatch(call: ToolCall) -> str:
    if isinstance(call, CreatePaymentLink):
        # Replace with a real Stripe call when you're ready
        return f"[fake] Payment link for ${call.amount:.2f} to {call.customer}: https://pay.example.com/abc123"
    if isinstance(call, SendEmail):
        return f"[fake] Email sent to {call.to}: {call.subject}"
    return f"Unknown tool: {call}"
