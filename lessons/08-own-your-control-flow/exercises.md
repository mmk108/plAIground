# Exercises

1. **Predict, then run.** Before running the tests, guess which tools stop for a human. Then read `ROUTES` to check.
2. **Make it strict.** Change `group_sum` to `"approve"`. Which test fails, and why is that the *right* failure?
3. **Add a guard.** Write `weekday_guard` that blocks `send_report` on weekends. Use `datetime`. Add a test using a fake date.
4. **Better trace.** Make `on_event` print one line per step with a timestamp. Which events happen in a normal run?
5. **Budget guard.** Stop the agent after 5 tool calls total, whatever the tool. Where does the count come from? (Hint: the thread.)
6. **Judge.** Write a guard that calls `ask_llm` to review an email body and returns a reason if it looks sensitive. What should the guard do if the model call itself fails?
