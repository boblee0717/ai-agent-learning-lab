# Teacher Notes

This project is designed to teach the *shape* of agents before adding complexity.

## The Five Files That Matter Most

- `messages.py` — how the agent stores context.
- `tools.py` — how external capabilities are wrapped (note `ToolError`).
- `agent.py` — how decisions become actions and observations (note the try/except feedback loop).
- `trace.py` — what real observability surfaces look like.
- `memory.py` — the seam between an in-process dict and a real vector store.

## The Big Idea: Separation Of Concerns

- The **brain** decides.
- The **tools** do work.
- The **loop** coordinates.
- The **trace** explains.
- **Memory** outlives a single run.

Once that separation feels natural, swap pieces independently:

- Replace `TeachingBrain` with `EchoLlmBrain` to see what the LLM would receive.
- Replace `EchoLlmBrain` with `OpenAiBrain` to make it real.
- Replace `InMemoryStore` with SQLite or a vector DB.
- Render `Trace` to a UI instead of stdout.

None of those changes should require touching `Agent.run`.

## Common Beginner Confusions

- *"Why doesn't the brain call the tool itself?"* Because then a different brain (LLM, tests, simulation) would have to re-implement tool dispatch and error handling. Keep the loop in charge.
- *"Why is `Decision.content` overloaded for both answer text and tool input?"* It is the simplest contract that still maps cleanly onto OpenAI/Anthropic tool-use payloads. When you outgrow it, split it into `answer_text` and `tool_input`.
- *"Why do tool errors come back as observations?"* So the brain can see them and decide what to do, the same way an LLM sees `function_call_error` and can retry or give up.
