# Exercises

Hands-on practice for each lesson. Every exercise has three pieces:

| Piece | Path | Purpose |
|---|---|---|
| Brief | `exercises/NN_*.md` | What to build, hints, acceptance criteria |
| Starter | `exercises/starter/exNN_*.py` | Skeleton with `# TODO` markers — edit in place |
| Tests | `exercises/tests/test_NN_*.py` | Auto-grader. Pass = you got it |
| Solution | `exercises/solutions/exNN_*.py` | Reference implementation. Peek **after** you tried |

## Workflow

```powershell
# Run only the exercise tests
pytest exercises/tests -q

# Run a single exercise
pytest exercises/tests/test_03_unit_converter.py -q

# Run everything (course code + exercises)
pytest -q
```

When you start, the exercise tests should fail with messages that tell you what to implement next. As you fill in the `# TODO` blocks in `exercises/starter/`, more tests turn green.

> The starter files import the same `agent_course` package the lessons use. Make sure you ran `pip install -e ".[dev]"` once.

## Index

1. `01_chatbot_vs_agent.md` — Spot the difference and write the smallest agent that uses one tool.
2. `02_conversation_state.md` — Build a `Conversation` helper that owns the message list.
3. `03_unit_converter_tool.md` — Add a new `UnitConverterTool` that respects the `Tool` protocol.
4. `04_retry_brain.md` — Wrap an existing brain with retry-on-tool-error behavior.
5. `05_file_memory_store.md` — Implement a JSON-file backed `Memory` and prove it persists across processes.
6. `06_keyword_llm_brain.md` — Replace the brain using the `EchoLlmBrain` prompt-construction hook.

## Self-check

Each brief has an **Acceptance** section. If `pytest exercises/tests/test_NN_*.py` is green and the acceptance bullets feel true to you, you are done.

## If you really want to peek at a solution

```powershell
# Run the autograder against the reference solution for one exercise:
Copy-Item exercises\solutions\ex03_unit_converter.py exercises\starter\ex03_unit_converter.py -Force
pytest exercises/tests/test_03_unit_converter.py -q
```

But first, give yourself at least 20 minutes of struggle — that struggle is where the learning lives.
