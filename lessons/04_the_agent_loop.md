# 04: The Agent Loop

The core loop is:

```text
Receive goal
Decide what to do (with reasoning)
If tool is needed, call tool
Record observation (errors included)
Decide again
Return final answer
```

Open `src/agent_course/agent.py` and find `Agent.run`. That is the heart of the project.

## What Each Iteration Looks Like

Every `Decision` carries three things:

- `kind`: `"answer"` or `"tool"`.
- `content`: the answer text or the tool input.
- `reasoning`: a short note explaining *why* this decision was made. Rule-based brains write this by hand; LLM brains usually generate it.

The loop also captures every step in a structured `Trace`:

- `goal`, `thought`, `tool_call`, `observation`, `answer`, `error`, `limit`.

That structure is what real agent UIs and observability tools render.

## Errors Are Just Observations

When a tool raises, the loop captures the failure as an observation and feeds it back to the brain. This is the same pattern real frameworks use to enable self-correction: the model sees the error, then decides what to do next.

Try:

```bash
python -m agent_course "What is 1 / 0?"
```

Notice how the trace contains both the failed `tool_call` and an `observation` describing the error before the agent answers.

## Why The Loop Matters

Once you understand the loop, real agent frameworks become easier to reason about. They mostly give you stronger versions of the same pieces: model calls, tools, memory, tracing, retries, and guardrails.

## Exercise

1. Change `max_steps` to `1` when creating the agent. What answer do you get for a question that needs a tool?
2. Inspect `result.trace.events` instead of printing strings. Notice how each event has `kind`, `step`, and `message` fields you can group, filter, or render however you want.
