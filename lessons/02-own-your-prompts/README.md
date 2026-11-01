# Lesson 2: Own Your Prompts

## The idea

The prompt is the instruction sheet you hand the model. Many frameworks write it for you behind the scenes (`Agent(role="...", goal="...")`). That's convenient, but when the agent misbehaves you can't see what it was told, so you can't fix it.

> Treat your prompt like code: write it yourself, keep it in a file, test it, and track changes in git.

**Everyday analogy:** it's like giving a new coworker written instructions. If someone else wrote them and you can't read them, you can't figure out why the coworker keeps making the same mistake.

## What you'll do

Compare two prompts for the Lesson 1 assistant on the same test cases:

- `prompts/v1_vague.md`: a short, generic prompt.
- `prompts/v2_clear.md`: lists tools, rules, and examples, with an "unsupported" escape hatch.

```powershell
python lessons/02-own-your-prompts/starter/compare_prompts.py
```

You'll see a pass count per prompt and which cases failed. That's how you know whether an edit helped, instead of guessing.

## The workflow

1. Write the prompt as a file in `prompts/`.
2. Add test cases to `evals/cases.json` (input plus expected output).
3. Run `compare_prompts.py`.
4. Change **one thing**, re-run, compare.
5. Commit what works.

## Tips for good prompts

- Say exactly what format to reply in.
- List every tool and its fields.
- Give 2-3 examples, including one "I can't do that" example.
- State rules for edge cases (missing info, unsafe input).
- Add a failing case to your evals *before* fixing it, so it stays fixed.

## Check yourself

- Why does a hidden framework prompt make debugging harder?
- How do you know a prompt edit made things better?
- Why change only one thing at a time?

## Ask your assistant

- "Look at which cases `v1_vague.md` fails and explain why."
- "Make a `v3` prompt that handles typos in file names, and add eval cases for it."

Next: [Lesson 3: Own Your Context Window](../03-own-your-context-window/README.md)
