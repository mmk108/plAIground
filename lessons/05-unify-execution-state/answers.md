# Lesson 5 Answers

Try the questions first!

**How does the agent know it's finished, without a "done" flag?**
It reads the thread. If the last event is `done_for_now`, it's done. The state is derived from the history, so it can't get out of sync with it.

**What happens when the model returns invalid JSON?**
Validation fails and an `error` event is added to the thread. On the next round the model sees the error and can correct itself. The step limit prevents infinite retries.

**Why does one list of events make saving and resuming easier?**
There's only one thing to save. Save the list, load the list, and you're exactly where you left off. With separate state you'd have to save and re-sync several things.

**What's the downside?**
Threads can grow long (see Lesson 3 on trimming) and may contain sensitive data that you now store. Plan for retention and access.
