# Lesson 8 Answers

Try the questions first!

**Why do unknown tools default to "approve" instead of "run"?**
A tool you forgot to classify is exactly the one you haven't thought about. Defaulting to "wait for a human" fails safe; defaulting to "run" fails dangerous.

**What does the model see when a guard blocks it, and why does that matter?**
An `error` event with the reason (e.g. "Reports may only be sent to @example.com addresses"). Because it sees *why*, it can choose another step or stop gracefully, instead of retrying blindly.

**Which part is model judgment and which part is your policy?**
The model judges *what to try next*. Your routing table and guards decide *what is allowed to happen*. Policy never depends on the model behaving.

**Exercise 6 hint:** if the judge call fails, block the action ("fail closed") and tell the human. Never let a broken checker silently wave things through.
