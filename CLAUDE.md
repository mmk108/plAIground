# plAIground assistant instructions

This is a teaching repo for aspiring AI engineers. When helping:

- Explain in plain language first, then show code. Assume the user is a beginner.
- Follow the lesson structure: `README.md`, `starter/`, `prompts/`, `evals/`, `exercises.md`.
- Keep code small and readable. Prefer clarity over cleverness.
- All model calls go through `shared/llm.py` (`ask_llm`). Never hard-code a provider in a lesson.
- Never commit or print API keys. Keys live in `.env`.
- When the user changes a prompt or schema, suggest adding or updating an eval case.
- Don't skip ahead to later lessons unless asked.
