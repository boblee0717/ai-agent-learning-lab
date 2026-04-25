# Exercise 01 — Chatbot vs Agent

Lesson: `lessons/01_what_is_an_agent.md`

## Goal

Show in code, not in prose, how a chatbot differs from an agent. You will write two functions:

- `answer_as_chatbot(prompt) -> str`: answers from a hard-coded dictionary, never calls a tool.
- `answer_as_agent(prompt) -> str`: builds a real `Agent` (with the calculator + notes tools) and returns its final answer.

Both must accept the **same prompt set** and produce reasonable answers, but only the agent version should perform a tool call.

## Steps

1. Open `exercises/starter/ex01_chatbot_vs_agent.py`.
2. Fill in the two TODO blocks.
3. Run:
   ```powershell
   pytest exercises/tests/test_01_chatbot_vs_agent.py -q
   ```

## Hints

- The chatbot can be a single dict lookup with a default fallback string.
- The agent should reuse `agent_course.Agent` with no custom configuration.
- Your tests will inspect the agent's `tool_calls`, so make sure the agent path actually invokes a tool for `"What is 8 * 7?"`.

## Acceptance

- `answer_as_chatbot("What is 8 * 7?")` returns a string that contains `"56"` (because the dict gave it a hard-coded answer).
- `answer_as_agent("What is 8 * 7?")` returns a string that contains `"56"` **and** records exactly one calculator tool call.
- The chatbot version never imports `Agent`.
