# Roadmap draft: Lessons 13-18 (for review)

Status: **draft, nothing built yet.** Data read on 2026-11-01 from GitHub's API, PyPI download stats and each vendor's own docs.

## How to read the evidence

- **Stars / forks / last push** come from the GitHub API.
- **PyPI downloads (last month)** come from pypistats.org. They include CI runs and mirrors, so compare orders of magnitude only.
- **"Clones" are not available.** GitHub only shows clone counts to repo admins, so downloads and forks stand in for adoption.
- Popularity is not quality. Where something looks risky, it's flagged.

## What the research changed

| Finding | Effect on the plan |
|---|---|
| OpenTelemetry's GenAI conventions **moved** to a new repo, `open-telemetry/semantic-conventions-genai` (504 stars). Its README still says the schema URL is "TODO". | Teach OTel as the transport. Treat attribute names as moving and pin a version. |
| Azure's agent service is now **Microsoft Foundry Agent Service** (the old `ai-foundry` URL redirects). | Use the new name. Re-check names before publishing. |
| Google's `agent-builder/agent-engine` page now redirects to **Gemini Enterprise Agent Platform** (Agent Runtime, Sessions, Memory Bank). | Same. Don't teach "Vertex Agent Engine" as the current name. |
| `GoogleCloudPlatform/agent-starter-pack` is **archived** (maintenance mode). It points to `google/agents-cli`. | Don't build on the starter pack. |
| `langchain-ai/langsmith-sdk` is **archived**. The SDK moved to `langsmith-python` and `langsmith-javascript`. The PyPI package name `langsmith` is unchanged. | Link to the new repos. |
| `microsoft/autogen`'s README is badged "archived" and points to `microsoft/agent-framework`. GitHub's archived flag is still off. | Teach Microsoft Agent Framework, not AutoGen. |
| MCP's latest spec is dated **2026-07-28**. It lists a **Tasks** extension for long-running work, plus elicitation (a server asking the user for input). | Lesson 16 maps directly to your Lessons 6-7. |
| AWS **AgentCore** is a modular platform: Harness, Runtime, Memory, Gateway, Identity, Code Interpreter, Browser. It works with LangGraph, Strands, ADK, CrewAI and others. | Use as the third cloud example. |
| Could not load a current **OWASP LLM Top 10** page (the 2025 URL returned 404; the index page names only the 2023-24 list). | Lesson 17 must be checked against OWASP directly before writing. |

## Evidence table

| Area | Project | Stars | Forks | Last push | PyPI / month | Note |
|---|---|---|---|---|---|---|
| Telemetry | opentelemetry-python | 2.7k | 1.1k | 11-01 | 444M (`opentelemetry-api`) | Apache-2.0. The standard |
| Telemetry | open-telemetry/semantic-conventions-genai | 504 | 136 | 11-01 | n/a | New home of GenAI conventions. Early |
| Telemetry | langfuse/langfuse | 36.8k | 4.1k | 11-01 | 23.6M | Accepts OTLP over HTTP (not gRPC). License shows NOASSERTION: read it |
| Telemetry | LangSmith (`langsmith`) | 1.1k (archived repo) | n/a | n/a | 77M | Packages unchanged. New repos are small (21 stars) |
| Telemetry | Arize-ai/phoenix | 12.1k | 1.3k | 11-01 | 626k | License NOASSERTION: read it |
| Evals | promptfoo/promptfoo | 26.7k | 2.6k | 11-01 | npm | MIT |
| Evals | confident-ai/deepeval | 19.2k | 2.2k | 11-01 | 2.6M | Apache-2.0 |
| Evals | ragas (now `vibrantlabsai/ragas`) | 16.2k | 1.8k | **02-24** | 1.1M | Moved org. Slower activity: check |
| SDK / framework | langchain-ai/langchain | 148.8k | 25.0k | 11-01 | 170M | MIT |
| SDK / runtime | langchain-ai/langgraph | 44.3k | 7.6k | 11-01 | 44.8M | MIT. Durable execution, HITL, persistence |
| SDK / harness | langchain-ai/deepagents | 30.9k | 4.3k | 11-01 | n/a | MIT |
| SDK | openai/openai-agents-python | 30.4k | 5.0k | 11-01 | 12.4M | MIT |
| SDK | google/adk-python | 22.1k | 4.3k | 11-01 | 10.1M | Apache-2.0 |
| SDK | pydantic/pydantic-ai | 21.0k | 3.1k | 11-01 | 5.4M | MIT |
| SDK + harness | strands-agents/harness-sdk | 9.0k | 1.5k | 11-01 | 37.1M (`strands-agents`) | Apache-2.0 |
| SDK (Microsoft) | microsoft/agent-framework | 14.5k | 2.6k | 11-01 | 190k | MIT. Python, .NET. Young, so low downloads |
| SDK (Microsoft) | microsoft/semantic-kernel | 28.7k | 4.9k | 10-31 | 301k | MIT |
| Runtime | temporalio/temporal | 24.1k | 2.1k | 11-01 | 38.1M (`temporalio`) | MIT. General durable execution |
| Protocol | modelcontextprotocol/python-sdk | 24.7k | 4.1k | 11-01 | 235M (`mcp`) | MIT |
| Protocol | modelcontextprotocol/modelcontextprotocol | 9.6k | 1.9k | 10-31 | n/a | License NOASSERTION: read it |
| Protocol | awslabs/mcp | 9.9k | 1.8k | 11-01 | n/a | Apache-2.0. AWS MCP servers |
| Cloud | aws/bedrock-agentcore-sdk-python | 782 | 161 | 10-30 | 5.3M | Apache-2.0 |
| Cloud | Azure (`azure-ai-projects`) | n/a | n/a | n/a | 7.3M | Foundry client SDK |
| Cloud | google/agents-cli | 6.3k | n/a | 10-27 | n/a | Successor to the archived starter pack |
| Security | microsoft/presidio (now `data-privacy-stack/presidio`) | 11.6k | 1.4k | 11-01 | 5.2M | MIT. PII detection |
| Security | NVIDIA NeMo Guardrails | 7.4k | 890 | 11-01 | 526k | License NOASSERTION: read it |
| Security | guardrails-ai/guardrails | 7.6k | 731 | 10-31 | 101k | Apache-2.0 |
| Memory (optional) | chroma-core/chroma | 29.6k | 2.6k | 10-30 | 6.5M | Apache-2.0 |
| Memory (optional) | mem0ai/mem0 | 68.2k | 8.1k | 10-30 | 2.0M | Apache-2.0 |
| Memory (optional) | getzep/graphiti | 32.4k | 3.3k | 11-01 | n/a | Apache-2.0 |
| Memory (optional) | letta-ai/letta | 25.3k | 2.7k | 10-18 | **15k** | Stars far outrun downloads. Treat cautiously |
| Retrieval (optional) | pgvector/pgvector | 23.6k | 1.4k | 10-31 | n/a | A Postgres extension |

## The six lessons

Every lesson keeps the pattern: plain analogy, tiny offline-testable code, a Business lens, exercises and answers. Each ends with a "what the real tool does" table.

### 13. See what your agent did (telemetry)
- **Idea:** A trace is a recording of every model call and tool call, with timing and cost. Your `Thread` is almost one already.
- **Build:** `trace.py` turns thread events into OpenTelemetry spans. It prints to the console, so no account is needed. It has an optional OTLP export to Langfuse.
- **Show real tools:** Langfuse, LangSmith, Phoenix, Foundry tracing, Cloud Trace (names from vendor docs).
- **Caveat to teach:** GenAI attribute names are still moving. Pin a version.
- **Factors:** 5, 9, 12.

### 14. Prove it keeps working (evals)
- **Idea:** Tests for a model that can be wrong in new ways. You need a dataset, a grader and a regression gate.
- **Build:** Turn the existing `evals/` into a dataset file, add a pass-rate gate, add a model-graded check (mock offline).
- **Show real tools:** promptfoo, DeepEval, Ragas, cloud eval services.
- **Factors:** 2, 8, 9.

### 15. SDKs and runtimes, side by side
- **Idea:** The same Lesson 5 agent in two ways: an SDK (pick one: OpenAI Agents SDK, Strands, Microsoft Agent Framework or ADK) and LangGraph (runtime). Your thread maps to the framework's state.
- **Build:** A mapping doc plus one small runnable port. Requires a real API key, so tests stay on the mock where possible.
- **Deliverable:** A "which would you choose" decision table for consulting clients.
- **Factors:** 5, 8, 10, 12.
- **Risk:** Framework APIs change quickly. Pin versions and keep the port tiny.

### 16. MCP: tools that other agents can use
- **Idea:** MCP is a standard plug for tools, resources and prompts. The 2026-07-28 spec adds a Tasks extension for long jobs and elicitation for asking a human.
- **Build:** Wrap a Lesson 4 tool as a minimal MCP server using the official Python SDK, then call it from your agent.
- **Link to your work:** `request_human_input` (Lesson 7) is the same idea as MCP elicitation. The spec's Tasks is the same idea as Lesson 6.
- **Factors:** 1, 4, 6, 7.

### 17. Keep it safe (security and guardrails)
- **Idea:** Treat model output and tool results as untrusted. Cover prompt injection, over-powered tools, data leakage and approvals.
- **Build:** An injection test set for the Lesson 8 guards, PII redaction using Presidio patterns, and a permission table for tools.
- **Needs checking first:** the current OWASP LLM Top 10 edition. Do not cite a list until verified.
- **Factors:** 7, 8, 9.

### 18. Run it for a company (enterprise cloud)
- **Idea:** What changes at scale: identity per agent, secrets, sandboxed code, durable queues, cost limits, audit logs, approvals, regions and compliance.
- **Build:** A design document and a checklist, plus a "deploy shape" diagram for each cloud. No real deployment inside the repo.
- **Three cloud examples:**
  - Microsoft Foundry Agent Service: Agent Runtime, Toolboxes (managed MCP endpoint), Entra identity, tracing with Application Insights, publishing to Teams.
  - Gemini Enterprise Agent Platform: Agent Runtime, Sessions, Memory Bank, Code Execution, IAM agent identity, Cloud Trace and Logging.
  - AWS Bedrock AgentCore: Runtime, Memory, Gateway, Identity, Code Interpreter, Browser, Observability.
- **Neutral options:** LangGraph or Temporal on your own infrastructure.
- **Factors:** 6, 8, 11, 12.

### Optional appendix A: memory and retrieval
- Covers Factor 13 (pre-fetch), simple retrieval, and memory stores. The tools are the most hyped and least settled, so teach concepts first and treat names as examples.

## What I'd rather not do

- Don't push a single "best" framework. Teach the decision criteria, with your Lesson 5 thread as the stable idea underneath.
- Don't paste vendor marketing. Each claim in a lesson should link to the vendor's own docs.
- Don't write lessons 15 and 18 from memory. Re-read the docs the day of writing.

## Open questions for you

1. Which cloud do your clients use most, so Lesson 18 goes deepest there?
2. For Lesson 15, which SDK first: OpenAI Agents SDK, Strands, Microsoft Agent Framework or Google ADK?
3. Should the lessons need a real API key for some steps, or must everything run on the mock?
4. Is memory/RAG a lesson of its own or just an appendix?
