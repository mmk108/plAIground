# Exercises

1. **Predict, then run.** Trace "Email the total units by region to boss@example.com" by hand: which agents run, and where does it stop?
2. **Add an agent.** Create a `SUMMARIZER` with only `done_for_now` and a 2-step budget. Put it between the analyst and the emailer.
3. **Tighten a budget.** Set `ANALYST.max_steps` to 2. What happens, and is "stopped" a good outcome for a user?
4. **Persist it.** Save each agent's thread with `save_thread` (Lesson 5) so the approval can happen tomorrow.
5. **Route by topic.** Add a second analyst for a different spreadsheet and let the router choose by keywords.
6. **Compare.** Count tools shown in the prompt for the monolithic agent (Lesson 6) vs each small agent.
