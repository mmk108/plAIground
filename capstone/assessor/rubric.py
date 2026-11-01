"""Score a task for AI fit, risk and how much human control it needs.

Pure code, no model. Ratings are 1 (low) to 3 (high). A human can override any of them.
"""
from dataclasses import dataclass, field

CONTROL_LEVELS = {
    "keep_human": "Keep with a person. AI may help with research only.",
    "ai_prepares_human_approves": "AI prepares the work, a person approves before anything leaves.",
    "ai_drafts_human_reviews": "AI drafts, a person reviews the result.",
    "automate_with_logs": "AI runs it. A person samples the logs.",
}


@dataclass
class Task:
    text: str
    repeatable: int = 2
    rules: int = 2
    data: int = 2
    error_cost: int = 2
    sensitivity: int = 1
    tools: list[str] = field(default_factory=list)
    steps: int = 1
    rated_by: str = "keywords"

    def __post_init__(self):
        for name in ("repeatable", "rules", "data", "error_cost", "sensitivity"):
            value = getattr(self, name)
            if value not in (1, 2, 3):
                raise ValueError(f"{name} must be 1, 2 or 3, got {value!r}")


def fit(task: Task) -> int:
    """3-9. Higher means easier for AI: repeated, rule-based, digital inputs."""
    return task.repeatable + task.rules + task.data


def risk(task: Task) -> int:
    """2-6. Higher means a mistake matters more."""
    return task.error_cost + task.sensitivity


def control_level(task: Task) -> str:
    f, r = fit(task), risk(task)
    if f < 5:
        return "keep_human"
    if r >= 5:
        return "ai_prepares_human_approves"
    if f >= 7 and r <= 3:
        return "automate_with_logs"
    return "ai_drafts_human_reviews"


def build_shape(task: Task) -> str:
    """What to build: a skill, an MCP server, or a harness."""
    if control_level(task) == "keep_human":
        return "none"
    if task.tools and task.steps > 1:
        return "harness + MCP server"
    if task.tools:
        return "MCP server + skill"
    return "skill"


def priority(task: Task) -> float:
    """Where to start. High fit, low risk first."""
    return fit(task) * 2 - risk(task)
