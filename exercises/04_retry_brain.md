# Exercise 04 — Retry Brain

Lesson: `lessons/04_the_agent_loop.md`

## Goal

Build a `RetryBrain` that wraps any other brain and re-issues the same tool call up to N times when the previous observation looks like a `tool error: ...`. After N failures it should give up and return an `answer` decision explaining what happened.

This exercise teaches you that **the loop is fixed; new behavior comes from new brains**.

## Steps

1. Open `exercises/starter/ex04_retry_brain.py`.
2. Implement `RetryBrain.decide`.
3. Run:
   ```bash
   pytest exercises/tests/test_04_retry_brain.py -q
   ```

## Hints

- A brain only sees `messages` and `tools`. Inspect `messages[-1]` to detect a tool error (it will be a `tool` role message starting with `"tool error:"`).
- Track per-tool retry counts on `self`. The same brain instance is reused across the loop, so it is safe to keep state.
- When you decide to retry, you must remember the *original* tool name and tool input. The simplest way is to look at the most recent assistant/tool pair in `messages` — but our trace stores tool calls in the conversation as a `tool` observation only, so you should also keep the last `Decision` on `self`.

## Acceptance

- Wrapping `TeachingBrain` with `RetryBrain(max_retries=2)` and pointing the agent at a flaky tool that fails twice then succeeds should return the success on the third try.
- After exhausting retries, the final answer should mention `"giving up"` (case-insensitive) and the tool input that failed.
- `RetryBrain` must not cache decisions across different `Agent.run` calls — see `reset()` and the matching test.
