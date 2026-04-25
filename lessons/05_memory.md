# 05: Memory

Memory lets an agent carry information across steps or conversations.

There are two common kinds:

- **Short-term memory**: messages and observations in the current run. The `messages` list inside `Agent.run` already does this.
- **Long-term memory**: facts saved across runs.

This repo gives you a `Memory` protocol and an `InMemoryStore` implementation in `src/agent_course/memory.py`. The `MemoryTool` (in `src/agent_course/tools.py`) exposes that store to the agent as a regular tool. Anything that satisfies the `Memory` protocol can replace `InMemoryStore` later — SQLite, Redis, a vector database — without touching the agent loop.

## Try It

```powershell
python examples\04_memory.py
```

Notice that the same `MemoryTool` instance is reused across every `agent.run` call, so facts persist between conversations.

## Exercise

1. Add a `--persist` flag to `examples\04_memory.py` that pickles `memory_tool.store.all()` to disk before exit and reloads on startup. The agent should remember things between processes.
2. Replace `InMemoryStore` with a SQLite-backed implementation. The agent loop should not change a single line.
