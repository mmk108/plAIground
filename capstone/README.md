# Capstone: your first two agent tools

Built for an AI engineer and strategist who helps companies find where AI can work, then builds it with humans in control. Two small tools, each paired with a skill file.

| Tool | Question it answers | Who decides |
|---|---|---|
| [Workflow assessor](assessor/) | Which of this client's tasks suit AI, and how much human control does each need? | A person confirms every rating |
| [GitHub scout](scout/) | Does a skill, MCP server or plugin for this task already exist, and is it safe to look at? | A person reads the code before installing |

Both are read-only. Neither sends, installs or changes anything outside the report it writes.

## Try it

```bash
# 1. Score the sample workflow (fictional accounts-payable team)
python capstone/assessor/cli.py capstone/examples/client_notes.md

# 2. Find existing tools for a task (needs internet; optional GITHUB_TOKEN)
python capstone/scout/cli.py "invoice processing"

# 3. Offline tests
python capstone/evals/test_capstone.py
```

## How it applies the 12 factors

| Piece | Factor | Lesson |
|---|---|---|
| Ratings are structured values, validated (1-3) | 1, 4 | 4 |
| Scoring is plain code, not model opinion | 8 | 8 |
| Control levels decide who approves | 6, 7, 8 | 6-8 |
| Model reply must be valid JSON, otherwise fall back to keywords | 9 | 9 |
| Each tool does one job | 10 | 10 |
| Reports and evals are files you own | 2, 3 | 2, 3 |

## The control levels

| Level | Meaning |
|---|---|
| `keep_human` | A person does it. AI may research. |
| `ai_prepares_human_approves` | AI prepares. A person approves before anything leaves. |
| `ai_drafts_human_reviews` | AI drafts. A person reviews. |
| `automate_with_logs` | AI runs it. A person samples the logs. |

## Skills

- [`skills/workflow-assessment/SKILL.md`](skills/workflow-assessment/SKILL.md)
- [`skills/github-scout/SKILL.md`](skills/github-scout/SKILL.md)

A skill is instructions the agent loads when a task needs them. See [Build your own harness](../whats-next/build-your-own.md).

## Limits

- Offline ratings are keyword guesses. They are useful for a first pass, not a verdict. With `PROVIDER=anthropic` or `github` the model proposes ratings, which have **not** been tested here against a real model.
- The rubric weights are a starting opinion. Tune them against real client work.
- The scout ranks by stars, recency and license. That is a triage, not a security review.
- Use anonymized or fictional client notes in shared repos.

## Next steps

1. Run the assessor on a real (anonymized) workflow and fix the ratings it got wrong. Each fix becomes an eval.
2. Turn the top task into a skill, then wrap its tools as an MCP server.
3. Add the pause-and-approve loop from Lessons 6-7 so the human gate is built in, not promised.
