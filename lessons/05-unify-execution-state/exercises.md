# Exercises

1. **Read a thread.** Run the demo and write, in your own words, what happened at each numbered event.
2. **Trigger an error.** In `evals/test_agent.py`, copy the "invalid reply" test and change the bad reply. What does the error event say?
3. **Add a status.** Make `status()` return `"stuck"` when the last 3 events are all errors. Add a test.
4. **Count retries.** Add `retries` to `summary()`, calculated only from the thread.
5. **Fork it.** Copy the first 2 events of a thread into a new thread and run it. What changed? (Forking is easy when state is just a list.)
6. **Change the limit.** Set `MAX_STEPS` to 2 and ask a question that needs 3 steps. Read the thread to see what happened.
