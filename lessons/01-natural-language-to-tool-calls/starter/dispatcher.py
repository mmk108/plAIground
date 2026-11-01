"""Plain code that runs a validated tool call. No LLM in here."""
import csv
import re
import urllib.request
from pathlib import Path

from schemas import FetchWebpage, ReadSpreadsheet, ToolCall, Unsupported

DATA_DIR = Path(__file__).parent.parent / "data"


def read_spreadsheet(filename: str) -> str:
    path = DATA_DIR / filename
    if not path.exists():
        return f"File not found: {filename}. Files available: {[p.name for p in DATA_DIR.glob('*.csv')]}"
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    lines = [f"{filename}: {len(rows)} rows, columns: {', '.join(rows[0].keys())}"]
    for col in rows[0]:
        if col.endswith("_id"):
            continue  # IDs are labels, not quantities
        try:
            values = [float(r[col]) for r in rows]
            lines.append(f"  {col}: sum={sum(values):g}, avg={sum(values) / len(values):.2f}")
        except ValueError:
            pass  # not a number column
    lines.append("First 3 rows: " + "; ".join(str(r) for r in rows[:3]))
    return "\n".join(lines)


def fetch_webpage(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "plAIground-lesson"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
    except OSError as err:
        return f"Could not fetch {url}: {err}"
    html = re.sub(r"(?is)<(script|style).*?</\1>", " ", html)
    text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html)).strip()
    return f"Text from {url} (first 1500 chars):\n{text[:1500]}"


def dispatch(call: ToolCall) -> str:
    if isinstance(call, ReadSpreadsheet):
        return read_spreadsheet(call.filename)
    if isinstance(call, FetchWebpage):
        return fetch_webpage(call.url)
    if isinstance(call, Unsupported):
        return f"I can't do that yet: {call.reason}"
    return f"Unknown tool: {call}"
