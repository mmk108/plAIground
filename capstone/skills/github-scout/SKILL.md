---
name: github-scout
description: Search GitHub for existing skills, MCP servers and plugins that fit a task, and flag which ones need caution. Use before building something new.
---

# GitHub scout

## When to use
You have a task (for example "invoice matching") and want to know if a skill, MCP server or plugin already exists.

## Steps
1. State the task in plain words.
2. Run `python capstone/scout/cli.py "<task>"`. It searches three ways: MCP server, skill, plugin.
3. Read the flags: `archived`, `stale` (no push in 180 days), `no clear license`, `few stars`.
4. For each repo you might use, read its README and every file that runs (scripts, hooks, commands).
5. Try it in a throwaway folder. Never install straight into a client environment.
6. Record the decision: adopt, borrow ideas, or build your own.

## Rules
- Read-only. The scout never installs or runs what it finds.
- Stars show popularity, not safety. A flagged repo can still be fine; an unflagged one can still be unsafe.
- Check the license before using anything in client work.
