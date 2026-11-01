---
name: workflow-assessment
description: Break a client's workflow notes into tasks and score each for AI fit, risk and the amount of human control needed. Use at the start of an AI opportunity assessment.
---

# Workflow assessment

## When to use
The user gives workflow notes, an interview transcript or a process list and wants to know where AI can help.

## Steps
1. Split the notes into one task per line. Do not invent tasks.
2. Rate each task 1-3 on: repeatable, rules (3 = clear rules), data (3 = already digital), error_cost, sensitivity.
3. List the external tools each task touches and how many steps it has.
4. Run `python capstone/assessor/cli.py <notes>` to score and rank. The scoring is code, not model opinion.
5. Show the table. Ask the human to confirm or change every rating marked `keywords`.
6. Only after confirmation, recommend what to build: a skill, an MCP server, or a harness.

## Rules
- Never recommend automating a task rated `keep_human`.
- Money movement, bank detail changes and anything customer-facing need a person to approve.
- If the notes are vague, ask a question instead of guessing (Lesson 7).
- Do not store client names or confidential data in the report. Anonymize first.
