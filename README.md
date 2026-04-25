# AI Agent Learning Lab

A teaching-first project for learning how to build an AI agent from the inside out.

The repo starts with a tiny deterministic agent instead of a real LLM. That is deliberate: you can see the moving parts clearly before adding model calls, APIs, vector databases, or frameworks.

Runs on **macOS, Linux, and Windows** with the same code and the same commands.

## What You Will Learn

- What makes an agent different from a plain chatbot.
- How messages, tools, decisions, observations, and traces fit together.
- How an agent loop works: decide, act, observe, repeat.
- How to add a new tool.
- Where memory and real LLM calls belong later.

## Quick Start

> Detailed per-OS instructions live in [`docs/setup.md`](docs/setup.md). The TL;DR is below.

```bash
git clone https://github.com/boblee0717/ai-agent-learning-lab.git
cd ai-agent-learning-lab
```

Create and activate a virtualenv:

| OS / shell | Create | Activate |
|---|---|---|
| macOS / Linux | `python3 -m venv .venv` | `source .venv/bin/activate` |
| Windows PowerShell | `py -3 -m venv .venv` | `.\.venv\Scripts\Activate.ps1` |
| Windows cmd.exe | `py -3 -m venv .venv` | `.venv\Scripts\activate.bat` |

Then install and run:

```bash
pip install --upgrade pip
pip install -e ".[dev]"

# Smoke test
python examples/00_hello.py

# Walk-through examples
python examples/01_run_tool.py
python examples/02_run_agent.py
python examples/03_add_a_tool.py
python examples/04_memory.py
python examples/05_llm_brain.py

# Talk to the agent from the command line
python -m agent_course "What is 8 * 7?"
python -m agent_course "What is 1 / 0?"

# Tests + lint
pytest
ruff check .
```

To use a real LLM brain, install the optional extra and provide a key:

```bash
pip install -e ".[llm]"
# macOS / Linux
export OPENAI_API_KEY="sk-..."
export USE_OPENAI=1
# Windows PowerShell
#   $env:OPENAI_API_KEY = "sk-..."
#   $env:USE_OPENAI = "1"
python examples/05_llm_brain.py
```

> Forward slashes (`examples/00_hello.py`) work on every OS — Python normalizes them. No need to flip slashes when copy-pasting from these docs into PowerShell.

## How To Study This Repo

For each lesson: read the lesson, run the matching example, then do the matching exercise.

| # | Lesson | Example | Exercise |
|---|---|---|---|
| 1 | `lessons/01_what_is_an_agent.md` | `examples/01_run_tool.py` | `exercises/01_chatbot_vs_agent.md` |
| 2 | `lessons/02_messages_and_state.md` | `examples/02_run_agent.py` | `exercises/02_conversation_state.md` |
| 3 | `lessons/03_tools.md` | `examples/03_add_a_tool.py` | `exercises/03_unit_converter_tool.md` |
| 4 | `lessons/04_the_agent_loop.md` | `python -m agent_course "..."` | `exercises/04_retry_brain.md` |
| 5 | `lessons/05_memory.md` | `examples/04_memory.py` | `exercises/05_file_memory_store.md` |
| 6 | `lessons/06_replacing_the_brain_with_an_llm.md` | `examples/05_llm_brain.py` | `exercises/06_keyword_llm_brain.md` |

Run all auto-graders together:

```bash
pytest exercises/tests -q
```

## Repo Map

- `src/agent_course/messages.py` — message objects used by the agent.
- `src/agent_course/tools.py` — tool protocol, `ToolError`, calculator, notes, memory.
- `src/agent_course/memory.py` — `Memory` protocol + `InMemoryStore`.
- `src/agent_course/trace.py` — structured `Trace` and `TraceEvent`.
- `src/agent_course/agent.py` — the agent loop and the teaching brain.
- `src/agent_course/brains.py` — `EchoLlmBrain` (offline) and `OpenAiBrain` (optional).
- `src/agent_course/cli.py` — `python -m agent_course "..."` entry point.
- `examples/` — runnable demos for each lesson.
- `exercises/` — practice problems with auto-graders and reference solutions.
- `docs/setup.md` — per-OS install instructions and troubleshooting.
- `docs/glossary.md` — short definitions for agent terms.
- `docs/teacher-notes.md` — what to pay attention to while learning.

## Learning Rule

Do not rush to frameworks. First understand the loop. Once the loop makes sense, frameworks feel much less magical.
