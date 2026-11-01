# Lesson 1 Answers

Try the questions first!

**Why is validation between the model and the real action important?**
The model can be wrong or be tricked. Validation is your safety net: it rejects bad requests (like `../../secrets.csv`) before anything runs. Like a bank checking a form before moving money.

**Is a tool a function or logic?**
Both. The *tool* is a regular function you wrote (`read_spreadsheet`). The *dispatcher* is plain `if` logic that picks which function to run. The model only chooses and fills in the details.

**What happens if you ask for something with no matching tool?**
The prompt gives the model an "unsupported" option, so it says so instead of guessing. If it returns something invalid anyway, validation rejects it. Never crash and never guess.

**Why JSON instead of the model calling the API directly?**
Control (you validate first), safety (you can require approval), and testability (you can check the JSON without touching real systems).
