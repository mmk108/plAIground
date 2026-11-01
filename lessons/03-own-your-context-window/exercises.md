# Exercises

1. **Run the demo** and find every value that was masked. Did anything sensitive slip through?
2. **Add a rule.** Redact phone numbers, then add a test to `evals/test_context.py`.
3. **Drop columns.** Make the context builder remove the `card_number` column entirely rather than masking it.
4. **Shrink it.** Change `truncate` to keep the first and last 500 characters. Which is more useful to the model?
5. **Change the format.** Switch the XML-style tags to YAML or plain text. Use `--ask` and see if answers change.
6. **Your data.** Put a CSV of your own in `data/` and check what the model would see.
