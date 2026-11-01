# Exercises

1. **Predict, then run.** Ask for "total profit by region". How many errors will the thread contain? How many does the *next prompt* show?
2. **Different retry limit.** Change `MAX_CONSECUTIVE_ERRORS` to 1 and then 5. What changes for the stuck-model test?
3. **Per-tool limits.** Allow `group_sum` 3 failures but `send_report` only 1. Where does the tool name live? (Hint: the last `tool_call` event.)
4. **Same call twice.** Detect two identical failing calls in a row and escalate immediately.
5. **Better messages.** Make "No column" errors suggest the closest valid column name (use `difflib.get_close_matches`).
6. **Tidy up.** What if 50 *unresolved* errors pile up? Write a function that keeps only the last 3 in the prompt.
