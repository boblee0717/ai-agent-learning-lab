"""Exercise 02 — Conversation state."""

from __future__ import annotations

from agent_course import Message


class Conversation:
    """Owns an ordered list of ``Message`` objects.

    See exercises/02_conversation_state.md for required behaviour.
    """

    def __init__(self, system: str | None = None) -> None:
        # TODO: store an empty ``self._messages: list[Message]`` and, if
        # ``system`` is provided, append a single ``Message(role="system", ...)``.
        raise NotImplementedError

    def user(self, text: str) -> None:
        # TODO: append a user message.
        raise NotImplementedError

    def assistant(self, text: str) -> None:
        # TODO: append an assistant message.
        raise NotImplementedError

    def tool(self, observation: str) -> None:
        # TODO: append a tool observation message.
        raise NotImplementedError

    @property
    def messages(self) -> list[Message]:
        # TODO: return a *copy* of the internal list so callers cannot
        # mutate the conversation by reference.
        raise NotImplementedError

    def last(self) -> Message:
        # TODO: return the most recent message; raise IndexError if empty.
        raise NotImplementedError

    def history_text(self) -> str:
        # TODO: join messages as "<role>: <content>" lines, in order.
        raise NotImplementedError
