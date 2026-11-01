# Lesson 1: Natural Language to Tool Calls

## The idea

An LLM's core job in an agent is to turn a messy human sentence into a **structured request** (JSON) that names a tool and its inputs. Your normal code then checks it and runs it.

> The model decides **what**. Your code decides **whether** and **how**.

```
"bill Terri $750"  ->  LLM  ->  {"function": "create_payment_link", "amount": 750, "customer": "Terri"}
                                        |
                              validate (schema rules)
                                        |
                              dispatcher runs the real function
```

## Why not let the model call the API directly?

- **Control:** you validate the request first (amount must be a positive number under a limit).
- **Safety:** you can require approval, log it, or reject it.
- **Testability:** you can check the JSON without touching real systems.

## Where the pieces live

| File | Role |
|------|------|
| `starter/schemas.py` | The menu of allowed tools and their validation rules |
| `prompts/system.md` | Tells the model about the tools, with examples |
| `starter/translate.py` | Calls the LLM and validates what comes back |
| `starter/dispatcher.py` | Plain `if` logic that runs the tool |
| `evals/` | Sentences paired with expected output, to measure accuracy |

## Run it

```powershell
python starter/main.py "create a payment link for $750 to Terri"
python evals/run_evals.py
```

## What if the model asks for something unknown?

Don't crash and don't guess. `translate.py` rejects invalid output with a clear error. Later lessons feed that error back to the model so it can retry.

## How to improve the translation

1. Write clear tool descriptions and field types.
2. Add a few examples to the prompt.
3. Add an "unsupported" escape hatch.
4. Measure with evals, change one thing, measure again.

## Check yourself

- Why is validation between the LLM and the real action important?
- Is a tool a function, or logic? (Hint: both. Which part is which?)
- What does MCP add on top of this pattern?

## Ask your assistant

- "Walk me through `translate.py` line by line."
- "Add a `create_refund` tool and update the prompt and evals."
- "Why did my eval case fail? Suggest a prompt change."

Next: Lesson 2, Own Your Prompts (coming soon).
