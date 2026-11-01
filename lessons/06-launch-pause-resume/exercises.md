# Exercises

1. **Walk through it.** Run launch, status, and resume with the CLI. Then open `threads/<id>.json` and find the approval event.
2. **Reject it.** Launch again and use `--reject`. Read the thread. What did the model do after the rejection?
3. **Add `cancel`.** Add a command that stops a paused agent and records a `cancelled` event. Add a test.
4. **Approve by rule.** Auto-approve `send_report` when the recipient ends with `@yourcompany.com`, and pause otherwise.
5. **Who approved?** Record the approver's name in the `human_response` event.
6. **Make it a web API.** Wrap `launch`, `get_status`, and `resume` in a small web server (try FastAPI) so a button or webhook could call them.
