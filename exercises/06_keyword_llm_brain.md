# Exercise 06 — Keyword LLM Brain

Lesson: `lessons/06_replacing_the_brain_with_an_llm.md`

## Goal

Build `KeywordLlmBrain` — a brain that uses the **same prompt format an LLM would receive**, but resolves it locally with simple keyword routing. This is a stepping-stone exercise: it teaches you how the prompt and the decision relate without needing API access.

You will reuse `EchoLlmBrain`'s `responder` hook — that is exactly what it is for.

## Steps

1. Open `exercises/starter/ex06_keyword_brain.py`.
2. Implement `keyword_responder(prompt, messages, tools) -> Decision`.
3. Run:
   ```bash
   pytest exercises/tests/test_06_keyword_brain.py -q
   ```

## Hints

- The `prompt` string already contains `Tools:` lines and the conversation history. You can ignore most of it and just inspect the latest user message via `messages[-1].content`.
- Suggested rules (in order):
  1. If the last message is a tool observation, return an `answer` summarising it.
  2. If the user message contains digits and an operator, call `calculator`.
  3. If it starts with `remember ` or `recall `, call `memory`.
  4. Otherwise, answer with `"I do not know."`.
- Wrap your function in `EchoLlmBrain(responder=keyword_responder)` to plug into the agent.

## Acceptance

- `Agent(brain=build_brain()).run("What is 8 * 7?")` answers with `"56"` and uses the calculator.
- `Agent(brain=build_brain(), tools=[CalculatorTool(), NotesTool(), MemoryTool()]).run("remember name Bob")` uses the memory tool.
- `Agent(brain=build_brain()).run("hello")` answers with `"I do not know."`.
- The brain object is an `EchoLlmBrain` instance (so the LLM-style prompt actually flows through `_format_prompt`).
