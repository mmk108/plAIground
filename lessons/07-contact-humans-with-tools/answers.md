# Lesson 7 Answers

Try the questions first!

**Why is "ask a human" better as a structured tool than as free text?**
Free text can't be checked or routed. A structured request has a question, a format and an urgency, so your code can validate the answer (is it really yes/no?), choose a channel, and show it in a proper form.

**What are the two kinds of wait, and how do they differ?**
A *question* means the agent is missing information, so the human's answer is the result. An *approval* means the agent knows what to do but needs permission, so a "yes" runs the pending tool and a "no" cancels it. Both are saved as `human_response` events.

**What should happen if the human gives an invalid answer?**
The agent keeps waiting and the human is told what's wrong ("please answer yes or no"). The bad answer is never fed to the model as if it were valid.

**Why does the agent ask instead of guessing the address?**
A wrong guess on a risky action (sending a report to a stranger) is worse than a short delay.
