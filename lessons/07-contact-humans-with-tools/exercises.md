# Exercises

1. **Predict, then run.** Run the CLI with "Email the total units by region to my boss". Guess how many times it will stop before the email is sent. (Answer: twice.)
2. **Yes/no question.** Change the mock or your prompt so the agent asks a `yes_no` question like "Include the Gadget product?". Try answering "maybe". What happens?
3. **Multiple choice.** Make the agent ask "Which region?" with `choices` of East, West, North. Where is the answer validated?
4. **Urgency.** Add logic so `urgency="high"` questions print in capital letters, and `low` ones are batched. Which file changes?
5. **Escalate.** Add a rule: if a question is unanswered, record an `escalation` event after a deadline. (Hint: a timestamp on the event.)
6. **Your data.** Ask something with no obvious answer, like "send the numbers to finance". What does the agent ask?
