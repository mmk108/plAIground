# Lesson 6 Answers

Try the questions first!

**Why does the agent pause before sending, not after?**
After is too late: the email is already out. The pause has to sit between the model *choosing* an action and your code *doing* it, so a human can still say no.

**What makes it possible to resume in a completely different process?**
The thread is saved to disk after every step, and the thread is the agent's only state (Lesson 5). Any process that loads the file can continue.

**What happens if the human rejects the action?**
A `human_response` of "rejected" is recorded, and a tool result tells the model not to retry. The model sees this and replies instead, e.g. "Understood. I did not send it."

**Why is the approval stored in the thread?**
It becomes part of the audit trail: what was proposed, who answered, and when.
