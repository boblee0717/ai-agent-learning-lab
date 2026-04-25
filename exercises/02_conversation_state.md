# Exercise 02 — Conversation State

Lesson: `lessons/02_messages_and_state.md`

## Goal

Build a tiny `Conversation` helper that owns the message list and enforces basic invariants. Real agent libraries usually have something like this so the agent loop never has to remember "did I add the system prompt yet?".

## Steps

1. Open `exercises/starter/ex02_conversation.py`.
2. Implement `Conversation` so the tests pass.
3. Run:
   ```bash
   pytest exercises/tests/test_02_conversation.py -q
   ```

## Required interface

```python
class Conversation:
    def __init__(self, system: str | None = None) -> None: ...
    def user(self, text: str) -> None: ...
    def assistant(self, text: str) -> None: ...
    def tool(self, observation: str) -> None: ...

    @property
    def messages(self) -> list[Message]: ...
    def last(self) -> Message: ...
    def history_text(self) -> str: ...   # "system: ...\nuser: ...\n..."
```

## Hints

- Reuse `agent_course.Message`. Do not invent a new dataclass.
- The system message should appear first in `messages` if (and only if) one was provided.
- `history_text()` should be reusable as a debug print and as a poor-man's LLM prompt body.

## Acceptance

- A fresh `Conversation()` has zero messages.
- A fresh `Conversation("you are helpful")` has exactly one `system` message.
- After `c.user("hi"); c.assistant("hello")`, `c.last().role == "assistant"`.
- `c.history_text()` joins messages as `"<role>: <content>"` lines in insertion order.
