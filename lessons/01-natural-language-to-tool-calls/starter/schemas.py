"""Tool schemas: the 'menu' of things the model is allowed to ask for."""
from typing import Literal, Union

from pydantic import BaseModel, Field


class CreatePaymentLink(BaseModel):
    function: Literal["create_payment_link"]
    amount: float = Field(gt=0, le=10000, description="Amount in USD")
    customer: str = Field(min_length=1)
    memo: str = ""


class SendEmail(BaseModel):
    function: Literal["send_email"]
    to: str
    subject: str
    body: str


# Add new tools here, then add them to this Union and to dispatcher.py
ToolCall = Union[CreatePaymentLink, SendEmail]
