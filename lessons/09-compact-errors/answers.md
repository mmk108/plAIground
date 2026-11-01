# Lesson 9 Answers

Try the questions first!

**Why must the model see an error while it is unresolved?**
The error is the model's only clue about what went wrong. Without it, it would repeat the same mistake. ("No column 'profit'. Columns are: ..." tells it exactly what to change.)

**Why hide errors once they're fixed?**
They no longer help, and they cost space in the context window and can distract the model into repeating old mistakes. They stay in the saved thread for debugging; only the prompt leaves them out.

**What should happen when the same error repeats three times?**
Stop retrying. A model stuck in a loop won't fix itself. Escalate: ask a human (Lesson 7), or restart with a cleaner context. The agent here adds a `request_human_input` question that includes the last error.

**Exercise 1:** one error in the thread, zero in the next prompt (it was marked resolved).

**Why count errors from the thread instead of a variable?**
Because the thread is the only state (Lesson 5). If the program restarts, the count is still right.
