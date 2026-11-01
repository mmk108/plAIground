"""Render scored tasks as a markdown assessment a client can read."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import rubric  # noqa: E402
from rubric import Task  # noqa: E402

LABEL = {1: "low", 2: "med", 3: "high"}


def render(tasks: list[Task], title: str = "AI opportunity assessment") -> str:
    ranked = sorted(tasks, key=rubric.priority, reverse=True)
    lines = [
        f"# {title}",
        "",
        f"{len(tasks)} tasks reviewed. Ratings marked `keywords` are first guesses: "
        "a person must confirm them before anything is built.",
        "",
        "| # | Task | AI fit | Risk | Human control | Build | Rated by |",
        "|---|---|---|---|---|---|---|",
    ]
    for i, t in enumerate(ranked, 1):
        lines.append(
            f"| {i} | {t.text} | {rubric.fit(t)}/9 | {rubric.risk(t)}/6 "
            f"| {rubric.control_level(t)} | {rubric.build_shape(t)} | {t.rated_by} |"
        )
    lines += ["", "## Control levels", ""]
    lines += [f"- **{k}**: {v}" for k, v in rubric.CONTROL_LEVELS.items()]
    starters = [t for t in ranked if rubric.control_level(t) != "keep_human"][:3]
    lines += ["", "## Suggested starting points", ""]
    if starters:
        for t in starters:
            tools = ", ".join(t.tools) or "no external tools"
            lines.append(
                f"- {t.text} ({tools}; repeatable {LABEL[t.repeatable]}, "
                f"error cost {LABEL[t.error_cost]})"
            )
    else:
        lines.append("- None yet. Gather more detail on the tasks above.")
    return "\n".join(lines) + "\n"
