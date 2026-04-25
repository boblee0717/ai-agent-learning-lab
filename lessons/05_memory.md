# 05: Memory

Memory lets an agent carry information across steps or conversations.

There are two common kinds:

- Short-term memory: messages and observations in the current run.
- Long-term memory: facts saved for later runs.

This repo currently has short-term memory through the `messages` list. Long-term memory is a good next exercise.

## Exercise

Create a `MemoryTool` with a small dictionary:

- `remember name Bob`
- `what is my name`

Then add it to the agent's tool list.

