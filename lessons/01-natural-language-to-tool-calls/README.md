# Lesson 1: Natural Language to Tool Calls

> **Business track:** read this page and run the two commands below. **Builder track:** also do `exercises.md`. New to a word? See the [glossary](../../GLOSSARY.md).

## What you'll build

A tiny assistant that handles everyday tasks you'd normally do by hand:

- "What's in my sales spreadsheet?"
- "Grab the text from this web page."

You type a plain sentence. The AI figures out *which task* you mean and *what details* it needs. Your code does the actual work.

## The idea

An LLM is good at understanding messy language. It is not a good place to put real actions. So the pattern is:

> The model decides **what** to do. Your code decides **whether** and **how**.

```
"summarize sales.csv"
        |
        v
   LLM translates  -->  {"function": "read_spreadsheet", "filename": "sales.csv"}
        |
        v
   Validation rules  (is it a .csv? inside data/? no sneaky paths?)
        |
        v
   Your function runs the real work and returns the result
```

That JSON is a **tool call**. A *tool* is just a normal Python function you wrote, like `read_spreadsheet()`. The model only picks one and fills in the blanks.

## Why not let the model run things directly?

- **Control:** you check the request first. Try asking for `../../secrets.csv`; validation rejects it.
- **Safety:** you decide what's allowed. The model can only choose from your menu.
- **Testing:** you can check the JSON without touching real files or websites.

## Where the pieces live

| File | Role |
|------|------|
| `starter/schemas.py` | The menu of allowed tools plus safety rules |
| `prompts/system.md` | Tells the model about the menu, with examples |
| `starter/translate.py` | Calls the LLM, then validates what comes back |
| `starter/dispatcher.py` | Plain `if` logic that runs the tool |
| `data/sales.csv` | Sample spreadsheet to play with |
| `evals/` | Sentences paired with expected answers, to measure accuracy |

## Run it

```powershell
python lessons/01-natural-language-to-tool-calls/starter/main.py "what's in sales.csv?"
python lessons/01-natural-language-to-tool-calls/starter/main.py "pull the text from https://example.com"
python lessons/01-natural-language-to-tool-calls/evals/run_evals.py
```

## Where this goes next

Right now the assistant does one step and shows you raw results. In later lessons it will look at the results and write you an analysis, then decide on a next step by itself. That loop is what makes it an *agent*.

## Business lens

- **The value:** staff ask in plain language; the agent does the routine lookup.
- **The risk:** a model can misread a request. Your rules (validation, allowed-tool list) are what make it safe to use.
- **A good first use case:** read-only tasks with a clear "unsupported" answer, like reading reports.
- **Ask your engineers:** what can this agent touch, and what happens when it's wrong?

## Check yourself

Answers: [answers.md](answers.md)

- Why is validation between the model and the real action important?
- Is a tool a function or logic? (Hint: both. Which part is which?)
- What happens if you ask for something with no matching tool?

## Ask your assistant

- "Walk me through `translate.py` line by line."
- "Add a `list_files` tool and update the prompt and evals."
- "Why did my eval case fail? Suggest a prompt change."

Next: [Lesson 2: Own Your Prompts](../02-own-your-prompts/README.md)
