# Exercises

1. **Predict, then run.** Start the agent via `from_chat` with "Email the total units by region to boss@example.com". What lands in the outbox, and when?
2. **New channel.** Add `from_sms(phone, text, outbox)`. What does delivery need to do differently for 160 characters?
3. **Approver list.** In `handle_reply`, only accept an approval from the original requester or a list of approvers. Write a test where a stranger tries.
4. **Digest.** Make `low` urgency questions wait for a daily digest instead of being sent right away. Where does urgency live? (Lesson 7.)
5. **Call the API.** Start `server.py` and drive an agent with `curl` or PowerShell `Invoke-RestMethod`.
6. **Schedule it.** Use Windows Task Scheduler or cron to call `from_schedule` every Monday.
