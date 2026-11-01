# Exercises

1. **Add your own file.** Drop a CSV of your own (expenses, grades, anything) into `data/` and ask: "what's in my_file.csv?"
2. **Add a tool.** Create `ListFiles` that lists what's in `data/`. Update `schemas.py`, `dispatcher.py`, and the prompt, then add an eval case.
3. **Break a safety rule.** Remove the `..` check in `schemas.py` and ask for `../../secrets.csv`. Put the check back and see the rejection.
4. **Improve accuracy.** Add 5 tricky requests to `evals/cases.json` (typos, vague wording). Edit the prompt until they pass.
5. **Go further.** Add `read_excel` using the `openpyxl` library, or a `search_web` tool.
