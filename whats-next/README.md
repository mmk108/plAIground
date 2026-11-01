# What's next: SDKs, harnesses, skills and plugins

You just built an agent by hand: a loop, a tool list, a thread of events, a pause for humans.
That was on purpose. Now every popular agent project is made of pieces **you already know**.

> Python taught you more once you stopped copy-pasting and wrote a loop yourself.
> Agents work the same way. After 12 lessons, you can read other people's agents.

## The map: five layers

Names are used loosely in the industry. This is one useful way to sort them, not a standard.

| Layer | Plain meaning | Your lessons | Examples (see [the field guide](repos.md)) |
|---|---|---|---|
| **SDK / framework** | A library that gives you the loop, tools and model plumbing so you don't hand-write them | 4, 5, 8 | Strands SDK, LangChain, Vercel AI SDK |
| **Runtime** | Makes the loop durable: saves state, resumes, streams, waits for humans | 5, 6, 7, 12 | LangGraph, Temporal, Agent Control Plane |
| **Harness** | An agent already assembled: tools, prompts, memory, context handling, sub-agents | 3, 9, 10 | Strands harness, Deep Agents, Hermes, OpenClaw |
| **Skills / plugins** | Reusable instructions and tool bundles you add to a harness | 2, 4 | Agent Skills, Matt Pocock skills, Knowledge Work Plugins |
| **Orchestration / control plane** | Runs many agents, triggers, approvals and channels | 6, 10, 11 | Agent Control Plane, Ruflo, OpenClaw gateway |

A seventh idea sits beside these: **UI the agent can safely generate** (json-render). It is Lesson 4 applied to screens: the model fills a structured object and your code renders it.

## One sentence each

- **SDK**: "I will write the product, give me the building blocks."
- **Runtime**: "My agent runs for hours and must not lose its place." (Lessons 5, 6, 12)
- **Harness**: "Give me a working agent now, I'll tune it." (You built a tiny one.)
- **Skill**: "A folder of instructions the agent loads when a task needs it." Lesson 2's prompts, packaged.
- **Plugin**: skills + connectors + commands, bundled for one job (sales, legal, data).

## Why the 12 factors still matter

A harness hides decisions. If you can't see them, you can't fix them. Use the factors as a checklist when you evaluate any tool:

| Ask | Factor | Lesson |
|---|---|---|
| Can I see and edit the exact prompt the model gets? | 2, 3 | 2, 3 |
| Are tools plain structured calls I can validate? | 1, 4 | 1, 4 |
| Is state one thread I can save and replay? | 5, 12 | 5, 12 |
| Can it pause for a human and resume later? | 6, 7 | 6, 7 |
| Can I control the flow, not just hope? | 8 | 8 |
| What happens when a tool fails? | 9 | 9 |
| Is it small and focused, or one giant agent? | 10 | 10 |
| Can it be triggered from where people already work? | 11 | 11 |

## Reading order

1. [The field guide](repos.md): what each repo you picked actually is, checked against its own README.
2. [Build your own harness](build-your-own.md): how your lesson code grows into a harness, and where a library helps.
3. [Roadmap for Lessons 13-18](roadmap-13-18.md): telemetry, evals, SDKs, MCP, security and enterprise cloud, with the evidence behind each pick.
3. [Capstone](../capstone/README.md): a workflow assessor and a GitHub scout, with skill files.

## Honest caveats

- These projects change weekly. Star counts and features here were read on 2026-11-01. Re-check before you depend on one.
- Popular is not the same as safe. Plugins, hooks and skills run with your permissions. Read them before installing.
- Several repos are one author's personal setup. Treat them as ideas to borrow, not standards.
