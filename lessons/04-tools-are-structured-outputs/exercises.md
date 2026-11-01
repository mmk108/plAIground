# Exercises

1. **Predict, then run.** Before running, guess what the demo will output for "what files do I have?" Then run it.
2. **Add a tool.** Create `top_n(filename, column, n)` in `tools.py`: inputs model, function, registry entry. Check that it appears in the generated menu.
3. **Break validation.** Remove the `..` check in `_safe_csv_name`, then ask for `../../secrets.csv`. Put it back.
4. **Dry run for everything.** Make `run_tool` dry-run any `risky` tool by default. Where would a real company want this?
5. **Better errors.** Make "unknown tool" errors suggest the closest valid name.
6. **Your data.** Drop your own CSV in `data/` and ask a question about it.
