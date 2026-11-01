# Lesson 3 Answers

Try the questions first!

**What would you do before putting a 100,000-row file in the context?**
Shrink it with plain code first: summarize (totals per group), sample a few rows plus column names, or truncate. The model only needs what answers the question.

**Why hide an error once it's fixed? When should you keep it?**
A fixed error is noise and can mislead the model into repeating or dwelling on it. Keep errors that are *unresolved*, so the model can learn from them and try something different.

**Why redact before the model sees data instead of asking the model to ignore it?**
Once data is in the context, you've already sent it to the provider. Asking the model to "ignore" it doesn't un-send it. Control happens in your code, before the call.

**Does regex redaction catch everything?**
No. It misses names, addresses, and unusual formats. Drop columns you don't need, and test your redaction.
