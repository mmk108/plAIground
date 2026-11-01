# Field guide: the repos, checked against their own READMEs

Read on 2026-11-01 from each repo's README (and the LangChain docs). Layers follow [the map](README.md).
"Lessons" shows which of your lessons explains the core idea.

| Repo | What it is (from its README) | Layer | Lessons | Best for learning |
|---|---|---|---|---|
| [strands-agents/harness-sdk](https://github.com/strands-agents/harness-sdk) | Monorepo with the Strands **SDK** (agent loop, model providers, tools) and the **harness** (`create_harness()`: a fully assembled agent), Python and TypeScript. Apache-2.0. | SDK + harness | 4, 5, 8, 9 | Seeing "SDK vs harness" in one repo: same loop, one hand-assembled, one pre-assembled |
| LangChain docs: [products](https://docs.langchain.com/oss/python/concepts/products), [LangGraph](https://docs.langchain.com/oss/python/langgraph/overview) | LangChain separates **runtime** (LangGraph: durable execution, streaming, human-in-the-loop, persistence), **framework** (LangChain: abstractions) and **harness** (Deep Agents SDK: planning, sub-agents, file system, context management). | Vocabulary for all layers | 5, 6, 7, 12 | The clearest definitions of runtime / framework / harness. Read this first |
| [humanlayer/agentcontrolplane](https://github.com/humanlayer/agentcontrolplane) | "Agent Control Plane": a Kubernetes-based scheduler for long-running agents with async tool calls, human approval, humans as tools, and sub-agents. Says it embraces 12-factor-agents. **Alpha**, last pushed 2025-07. | Runtime / control plane | 6, 7, 10 | Factors 6, 7, 10 at infrastructure scale. Read for ideas, don't depend on it |
| [openclaw/openclaw](https://github.com/openclaw/openclaw) | Open-source personal assistant on your own devices that talks to you in Discord, Slack, WhatsApp, iMessage and 20+ channels through one Gateway. Models and harnesses are swappable plugins. MIT. | Harness + gateway | 11 | Factor 11 (trigger from anywhere) done at scale |
| [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) | A self-hosted agent with a "learning loop": creates and improves skills from experience, keeps memory, searches past conversations, reachable from Telegram, Discord, Slack, CLI. Any model. MIT. | Harness | 5, 11, 12 | How memory and skills grow over time on top of a thread |
| [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) | 11 plugins (sales, legal, finance, data, support, marketing...) for Claude Cowork / Claude Code. Each bundles skills, connectors, slash commands and sub-agents. Apache-2.0. | Plugins | 2, 4 | **Best match for business readers**: a plugin is a prompt + tools for one job |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | 25 engineering skills and 9 slash commands (`/spec`, `/plan`, `/build`, `/test`, `/review`, `/ship`) covering the dev lifecycle. Installable via the `skills` CLI. MIT. | Skills | 2, 8 | Skills as written-down workflows with quality gates |
| [mattpocock/skills](https://github.com/mattpocock/skills) | The author's daily agent skills, "small, easy to adapt, composable", works with any model. MIT. | Skills | 2 | Small skills you can read in a minute and copy |
| [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) | One `CLAUDE.md` with four principles (think before coding, simplicity first, surgical changes, goal-driven execution) derived from a public post by Andrej Karpathy. No license listed. | Prompt / skill | 2, 3 | The smallest possible example: a system prompt as a file. Lesson 2 in the wild |
| [microsoft/hve-core](https://github.com/microsoft/hve-core) | "Hypervelocity Engineering": agents, instructions, prompts and skills for GitHub Copilot. Principle: "AI carries the rules, humans keep the judgment." Its README says treat it as a **source of patterns, not a stable platform**. MIT. | Skills / governance | 2, 7, 8 | Governance and human judgment at team scale |
| [affaan-m/ECC](https://github.com/affaan-m/ECC) | A large harness add-on for Claude Code, Codex and others: 71 agents, 314 skills, hooks, rules, memory, a security scanner. Install via `npx`. MIT. | Skills + harness tuning | 8, 9, 10 | Showing how far a skill collection can grow. **Large; read before installing** |
| [ruvnet/ruflo](https://github.com/ruvnet/ruflo) | "Agent meta-harness" for Claude Code and Codex: swarms of agents, memory, routing, federation. Formerly Claude Flow. MIT. | Orchestration | 10, 11 | Many-agent coordination. Compare to Lesson 10's plain-code router |
| [beita6969/ScienceClaw](https://github.com/beita6969/ScienceClaw) | Research agent for science. Turns replay-verified runs into reusable **Skills** and typed **Operators**. Has a paper and benchmark. MIT. | Harness (research) | 12 | Factor 12's `replay` used to verify and keep improvements |
| [vercel-labs/json-render](https://github.com/vercel-labs/json-render) | "Generative UI": the model emits JSON constrained to a catalog of components you define; renderers for React, Vue, mobile, PDF, email and more. Apache-2.0. | Structured output for UI | 1, 4 | Lesson 4's idea for screens: the model fills the form, your code draws it |

## How to read these without getting lost

1. Start with the **LangChain products page** for vocabulary.
2. Read **multica Karpathy skills** (one file) and one **knowledge-work plugin** (for example `data`). These are Lessons 2 and 4 in plain text.
3. Skim **Strands** to see the same agent at SDK level and harness level.
4. Skim **OpenClaw** or **Hermes** for channels and memory.
5. Only then look at the big collections (ECC, Ruflo, hve-core).

## Which would you pick?

| Your situation | Try |
|---|---|
| "I want my team to use AI for a repeated job" | A plugin or skill (Knowledge Work Plugins, Matt Pocock skills) |
| "I want to write my own agent in Python" | An SDK (Strands SDK, LangChain). Keep your Lesson 5 thread idea |
| "I want a working agent today, then tune it" | A harness (Strands harness, Hermes, OpenClaw) |
| "My agent runs for hours and needs approvals" | A runtime (LangGraph, Temporal) |
| "I need many agents or many channels" | A control plane (OpenClaw gateway, ACP, Ruflo) |

## Verify before you trust

- Check the license, last commit date and open issues.
- Read every hook, script and plugin command before installing. They run as you.
- Ask: which of the 12 factors does this hide from me, and can I turn that off?
