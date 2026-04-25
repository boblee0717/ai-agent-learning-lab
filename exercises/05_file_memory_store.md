# Exercise 05 — File-backed Memory

Lesson: `lessons/05_memory.md`

## Goal

Implement `FileStore`, a `Memory` implementation that persists facts to a JSON file on disk. The agent loop should not change at all — that is the whole point of having `Memory` as a protocol.

## Steps

1. Open `exercises/starter/ex05_file_memory.py`.
2. Implement `FileStore` so it satisfies the `Memory` protocol from `agent_course.memory`.
3. Run:
   ```bash
   pytest exercises/tests/test_05_file_memory.py -q
   ```

## Hints

- Read on every `recall` is fine for this exercise (correctness over speed).
- Write atomically: dump to a temp file in the same directory, then `os.replace`. Otherwise a crash mid-write corrupts the JSON. Real systems care a lot about this.
- Recall logic can match the same way `InMemoryStore` does (substring on key or value).
- Wire the store through `MemoryTool(store=FileStore(path))` to verify it works inside the agent.

## Acceptance

- `FileStore` exposes `remember`, `recall`, and `all` with the same signatures as `InMemoryStore`.
- Two `FileStore(path)` instances pointing at the same path see each other's writes.
- Concurrent-ish use (write, then create a fresh instance, then `recall`) returns the persisted fact.
- An `Agent` configured with `MemoryTool(store=FileStore(tmp))` can `remember name Bob` in one `agent.run` and `recall name` in a second `agent.run` *after the agent and tool are recreated*.
