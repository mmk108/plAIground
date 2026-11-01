# Exercises

1. **Add a tool.** Create `CreateRefund` in `starter/schemas.py`, add it to `ToolCall`, handle it in `dispatcher.py`, and describe it in `prompts/system.md`.
2. **Break it.** Remove the "unsupported" rule from the prompt. Run the evals. What fails?
3. **Add a safety rule.** Change the `le=10000` limit on `amount`. What happens when you ask for a $50,000 link?
4. **Improve accuracy.** Add 5 tricky sentences to `evals/cases.json` (typos, slang, missing info). Edit the prompt until they pass.
5. **Go real.** Replace the fake Stripe response in `dispatcher.py` with a real Stripe test-mode call.
