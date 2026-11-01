# Lesson 11 Answers

Try the questions first!

**What two jobs does each channel have?**
(1) An adapter that turns an incoming message into a request. (2) A delivery step that sends the agent's questions and answers back through the same channel. The agent core is shared.

**How does a reply find the right channel later?**
The channel and reply address are saved as a `trigger` event at the start of the thread. When a reply arrives with the thread ID, the code reads that event and responds there. Nothing is held in memory, so it works days later.

**What's different about a schedule trigger?**
No human starts it. The agent works alone and contacts a person only when it needs a question answered or an approval. This is the "outer loop": agents that begin with an event, not a chat.

**Why does the safety note matter?**
Anyone who can send a reply can approve a risky action. Channels need authentication, and approvals should be checked against who is allowed to give them.

**Exercise 1:** the outbox gets one chat message, "Approval needed ... Reply yes or no," right after launch. After `yes`, a second message says the report was sent.
