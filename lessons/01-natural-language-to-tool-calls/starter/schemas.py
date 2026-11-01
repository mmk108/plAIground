"""Tool schemas: the 'menu' of things the model is allowed to ask for.

Validation rules live here, so a bad request is rejected before anything runs.
"""
from typing import Literal, Union

from pydantic import BaseModel, Field, field_validator


class ReadSpreadsheet(BaseModel):
    function: Literal["read_spreadsheet"]
    filename: str = Field(description="CSV file inside the data/ folder")

    @field_validator("filename")
    @classmethod
    def must_be_safe_csv(cls, v: str) -> str:
        # Safety rule: only .csv files, only inside data/, no path tricks
        if not v.endswith(".csv") or "/" in v or "\\" in v or ".." in v:
            raise ValueError("filename must be a plain .csv name inside data/")
        return v


class FetchWebpage(BaseModel):
    function: Literal["fetch_webpage"]
    url: str

    @field_validator("url")
    @classmethod
    def must_be_http(cls, v: str) -> str:
        if not v.startswith(("http://", "https://")):
            raise ValueError("url must start with http:// or https://")
        return v


class Unsupported(BaseModel):
    function: Literal["unsupported"]
    reason: str


# To add a tool: define it above, add it here, then update dispatcher.py and the prompt
ToolCall = Union[ReadSpreadsheet, FetchWebpage, Unsupported]
