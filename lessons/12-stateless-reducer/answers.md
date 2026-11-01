# Lesson 12 Answers

Try the questions first!

**What does `step` do, and what doesn't it do?**
It reads the history, does one action (ask the model or run a tool), and returns a *new* history with that result added. It doesn't remember anything between calls and doesn't modify the history it was given.

**Why can `replay` work without calling a model?**
A finished history already contains every model reply and tool result. Replay feeds those recorded values back in place of the real model and tools, so the same steps happen with no outside calls.

**What can you do with a history that you can't do with a variable inside a running program?**
Save it, move it to another machine, resume it later, inspect it, replay it, and rewind it. A variable in memory disappears when the program stops.

**Exercise 1:** 4 events: the request, the `group_sum` call, its result, and `done_for_now`.

**Exercise 5:** events are mutable objects. If two histories shared the same event objects, changing one (like marking an error resolved) would silently change the other, including your "before" snapshot. Copying keeps each history independent. Hidden edits like this are what make agents hard to debug.
