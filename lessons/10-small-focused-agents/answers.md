# Lesson 10 Answers

Try the questions first!

**Why does a long context window hurt the model?**
More text means more to track. Models lose focus, mix up facts and repeat earlier mistakes as the context grows. Keeping each agent to a few steps keeps the context short.

**Why is the router plain code instead of another AI?**
Deciding "is there an email address in this request?" is something a simple rule does perfectly, instantly and for free. Use AI only where judgment is needed. Agents are one building block in a mostly deterministic system.

**What does giving each agent its own tool list protect against?**
Mistakes and misuse. The analyst can't send email even if the model tries, because the prompt doesn't offer it and validation rejects it. It's least privilege for agents.

**Why pass only the report to the emailer?**
The emailer doesn't need the analyst's tool calls or errors. A fresh short thread keeps it focused and cheap.

**What if LLMs get smarter?**
Then agents can handle bigger scopes. But small, tested pieces still let you grow scope gradually and know where problems come from.
