"""Reference solution for Exercise 02 — Conversation state."""

from __future__ import annotations

from agent_course import Message


class Conversation:
    def __init__(self, system: str | None = None) -> None:
        self._messages: list[Message] = []
        if system is not None:
            self._messages.append(Message(role="system", content=system))

    def user(self, text: str) -> None:
        self._messages.append(Message(role="user", content=text))

    def assistant(self, text: str) -> None:
        self._messages.append(Message(role="assistant", content=text))

    def tool(self, observation: str) -> None:
        self._messages.append(Message(role="tool", content=observation))

    @property
    def messages(self) -> list[Message]:
        return list(self._messages)

    def last(self) -> Message:
        return self._messages[-1]

    def history_text(self) -> str:
        return "\n".join(f"{m.role}: {m.content}" for m in self._messages)
