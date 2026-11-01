# Lesson 4 Answers

Try the questions first!

**What does the model actually produce when it "uses a tool"?**
Just text: a JSON object like `{"function": "group_sum", ...}`. Your code parses and validates it, then decides what to run.

**Why is it useful that your code can handle a tool call differently?**
The model's request isn't a command. You can dry-run it, ask a human first, log it, rate-limit it, or reject it. That keeps you in control of anything with real-world effects.

**What should happen when the model asks for a tool that doesn't exist?**
Don't crash and don't guess. Return a clear error naming the valid tools. In Lesson 5 that error goes back to the model so it can correct itself.

**Why generate the tool list in the prompt from the registry?**
So the prompt and code can't disagree. Add a tool once and the model hears about it automatically.
