"""Search GitHub for skills, MCP servers and plugins, then flag what to check before trusting them.

Read-only: it searches and reports. It never installs or runs anything it finds.
`fetch` is injectable so tests run offline.
"""
import json
import math
import os
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timezone

API = "https://api.github.com/search/repositories"
STALE_DAYS = 180
YOUNG_STARS = 50


@dataclass
class Candidate:
    full_name: str
    description: str
    stars: int
    pushed_at: str
    license: str | None
    archived: bool
    url: str
    kind: str = ""
    flags: list[str] = field(default_factory=list)
    score: float = 0.0


def http_get(url: str) -> dict:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "plaiground-scout"}
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))


def build_queries(task: str) -> dict[str, str]:
    task = task.strip()
    if not task:
        raise ValueError("Describe the task to search for")
    return {
        "mcp server": f"{task} mcp server",
        "skill": f"{task} agent skills",
        "plugin": f"{task} agent plugin",
    }


def search(query: str, fetch=http_get, per_page: int = 8) -> list[Candidate]:
    params = urllib.parse.urlencode({"q": query, "sort": "stars", "order": "desc",
                                     "per_page": per_page})
    data = fetch(f"{API}?{params}")
    return [
        Candidate(
            full_name=item["full_name"],
            description=item.get("description") or "",
            stars=int(item.get("stargazers_count", 0)),
            pushed_at=item.get("pushed_at") or "",
            license=(item.get("license") or {}).get("spdx_id"),
            archived=bool(item.get("archived")),
            url=item.get("html_url", ""),
        )
        for item in data.get("items", [])
    ]


def days_since(iso: str, now: datetime) -> int | None:
    if not iso:
        return None
    pushed = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    return (now - pushed).days


def assess(c: Candidate, now: datetime | None = None) -> Candidate:
    now = now or datetime.now(timezone.utc)
    age = days_since(c.pushed_at, now)
    c.flags = []
    if c.archived:
        c.flags.append("archived")
    if age is None or age > STALE_DAYS:
        c.flags.append("stale")
    if c.license in (None, "NOASSERTION"):
        c.flags.append("no clear license")
    if c.stars < YOUNG_STARS:
        c.flags.append("few stars")
    recency = 0.0 if age is None else max(0.0, 1 - age / 365)
    c.score = round(math.log10(c.stars + 1) + 2 * recency - 2 * len(c.flags), 2)
    return c


def shortlist(task: str, fetch=http_get, now: datetime | None = None, top: int = 5) -> dict:
    """Best candidates per kind, de-duplicated across kinds. Archived repos are dropped."""
    seen: set[str] = set()
    result: dict[str, list[Candidate]] = {}
    for kind, query in build_queries(task).items():
        found = []
        for c in search(query, fetch):
            if c.full_name in seen or c.archived:
                continue
            seen.add(c.full_name)
            c.kind = kind
            found.append(assess(c, now))
        result[kind] = sorted(found, key=lambda c: c.score, reverse=True)[:top]
    return result


def render(task: str, results: dict) -> str:
    lines = [f"# GitHub scout: {task}", "",
             "Search results, not endorsements. Read the code before installing: skills, "
             "hooks and MCP servers run with your permissions.", ""]
    for kind, items in results.items():
        lines += [f"## {kind}", ""]
        if not items:
            lines += ["No candidates found.", ""]
            continue
        lines += ["| Repo | Stars | Last push | License | Flags | What it says |",
                  "|---|---|---|---|---|---|"]
        for c in items:
            desc = c.description.replace("|", "/")[:90]
            lines.append(
                f"| [{c.full_name}]({c.url}) | {c.stars} | {c.pushed_at[:10]} "
                f"| {c.license or 'none'} | {', '.join(c.flags) or '-'} | {desc} |"
            )
        lines.append("")
    lines += ["## Before you install", "",
              "- [ ] Read the README and the files that run (scripts, hooks, commands)",
              "- [ ] Check the license fits your client work",
              "- [ ] Check the last commit date and open issues",
              "- [ ] Try it in a throwaway folder first",
              "- [ ] Decide which actions need human approval (Lesson 8)"]
    return "\n".join(lines) + "\n"
