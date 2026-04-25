# AI Agent Learning Lab

A teaching-first project for learning how to build an AI agent from the inside out.

The repo starts with a tiny deterministic agent instead of a real LLM. That is deliberate: you can see the moving parts clearly before adding model calls, APIs, vector databases, or frameworks.

## What You Will Learn

- What makes an agent different from a plain chatbot.
- How messages, tools, decisions, observations, and traces fit together.
- How an agent loop works: decide, act, observe, repeat.
- How to add a new tool.
- Where memory and real LLM calls belong later.

## Quick Start

```powershell
cd E:\coding\ai-agent-learning-lab
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"

# Smoke test
python examples\00_hello.py

# Walk-through examples
python examples\01_run_tool.py
python examples\02_run_agent.py
python examples\03_add_a_tool.py
python examples\04_memory.py
python examples\05_llm_brain.py

# Talk to the agent from the command line
python -m agent_course "What is 8 * 7?"
python -m agent_course "What is 1 / 0?"

# Tests + lint
pytest
ruff check .
```

To use a real LLM brain, install the optional extra and provide a key:

```powershell
pip install -e ".[llm]"
$env:OPENAI_API_KEY = "sk-..."
$env:USE_OPENAI = "1"
python examples\05_llm_brain.py
```

If you do not want to create a virtual environment yet, run examples with:

```powershell
$env:PYTHONPATH="E:\coding\ai-agent-learning-lab\src"
python examples\02_run_agent.py
```

## How To Study This Repo

Read one lesson, run the matching example, then make a small edit.

1. `lessons/01_what_is_an_agent.md`
2. `lessons/02_messages_and_state.md`
3. `lessons/03_tools.md`
4. `lessons/04_the_agent_loop.md`
5. `lessons/05_memory.md`
6. `lessons/06_replacing_the_brain_with_an_llm.md`

## Repo Map

- `src/agent_course/messages.py`: message objects used by the agent.
- `src/agent_course/tools.py`: tool protocol, `ToolError`, calculator, notes, memory.
- `src/agent_course/memory.py`: `Memory` protocol + `InMemoryStore`.
- `src/agent_course/trace.py`: structured `Trace` and `TraceEvent`.
- `src/agent_course/agent.py`: the agent loop and the teaching brain.
- `src/agent_course/brains.py`: `EchoLlmBrain` (offline) and `OpenAiBrain` (optional).
- `src/agent_course/cli.py`: `python -m agent_course "..."` entry point.
- `examples/00_hello.py`: 3-line smoke test.
- `examples/01_run_tool.py`: call a tool directly.
- `examples/02_run_agent.py`: run the full agent loop.
- `examples/03_add_a_tool.py`: add a custom tool without changing the agent loop.
- `examples/04_memory.py`: long-term memory across runs.
- `examples/05_llm_brain.py`: swap the brain for an LLM-style brain.
- `docs/glossary.md`: short definitions for agent terms.
- `docs/teacher-notes.md`: what to pay attention to while learning.

## Learning Rule

Do not rush to frameworks. First understand the loop. Once the loop makes sense, frameworks feel much less magical.
