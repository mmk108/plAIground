# Lesson 2 Answers

Try the questions first!

**Why does a hidden framework prompt make debugging harder?**
You can't see what the model was told, so you can't tell whether a mistake came from wording, a missing rule, or a conflict. You'd be guessing.

**How do you know a prompt edit made things better?**
Run the same eval cases before and after and compare pass counts. Opinions and one-off tries aren't reliable, because models vary.

**Why change only one thing at a time?**
So you know which change caused the improvement or the regression. It's the same as a science experiment: one variable at a time.

**Why did `v1_vague.md` fail some cases?**
It had no "unsupported" option, so the model had to pick a tool even when nothing fit, and it guessed a file name.
