# 04: The Agent Loop

The core loop is:

```text
Receive goal
Decide what to do
If tool is needed, call tool
Record observation
Decide again
Return final answer
```

Open `src/agent_course/agent.py` and find `Agent.run`. That is the heart of the project.

## Why The Loop Matters

Once you understand the loop, real agent frameworks become easier to reason about. They mostly give you stronger versions of the same pieces: model calls, tools, memory, tracing, retries, and guardrails.

## Exercise

Change `max_steps` to `1` when creating the agent. What answer do you get for a question that needs a tool?

