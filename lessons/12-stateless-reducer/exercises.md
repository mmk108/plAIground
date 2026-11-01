# Exercises

1. **Predict, then run.** How many events will "Which region sold the most units?" produce? Count by hand, then check `len(final)`.
2. **Step by step.** In a Python shell, call `step` one at a time and print the last event after each.
3. **Diff.** Write `first_difference(a, b)` that returns the index where two histories first differ. Use it in the rewind test.
4. **Regression test.** Save a real run's history as JSON. Write a test that replays it and asserts the final answer. Why is this a great test?
5. **Why copy events?** `_copy` copies each event, not just the list. Find a case where sharing events would leak changes between histories. (Hint: Lesson 9's `mark_resolved` flips `event.resolved`.)
6. **What if.** Rewind a risky run to just before `send_report` and give it a model reply that sends to a different address.
