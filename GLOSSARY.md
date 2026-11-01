# Glossary

**Agent**: AI plus code that can take actions (not just chat) in a loop until a task is done.

**LLM (large language model)**: the AI that reads text and writes text, like Claude or GPT.

**Prompt**: the written instructions you give the model.

**Context window**: everything the model sees in one call (instructions, history, data). It has a size limit.

**Token**: a small chunk of text (roughly 3/4 of a word). Models are limited and billed by tokens.

**Tool**: a normal function you wrote that the agent can ask to run, like `read_spreadsheet`.

**Tool call**: the model's request to run a tool, written as structured data.

**JSON**: a text format for structured data, like `{"name": "Terri", "amount": 750}`.

**Schema**: the rules for what a piece of data must look like (which fields, what types, what limits).

**Validation**: checking data against the schema before using it.

**Dispatcher**: plain code that looks at a tool call and runs the matching function.

**Eval**: a test. A list of inputs with expected outputs, used to measure how well the agent works.

**Redaction**: replacing sensitive data (card numbers, emails) with placeholders before the model sees it.

**Truncation**: cutting long text down to a size limit.

**API**: a way for programs to talk to a service (like a model provider or Stripe).

**API key**: a secret password that identifies your account to an API. Keep it private.

**MCP (Model Context Protocol)**: a standard way to package tools so different agents can discover and use them.

**Mock model**: a free stand-in that follows simple rules instead of using real AI. Used here so lessons run without an account.

**Virtual environment (`.venv`)**: an isolated folder of Python packages for one project.
