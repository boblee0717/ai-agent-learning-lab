"""Reference solution for Exercise 04 — Retry brain."""

from __future__ import annotations

from agent_course.agent import Decision
from agent_course.messages import Message
from agent_course.tools import Tool


class RetryBrain:
    def __init__(self, inner, max_retries: int = 2) -> None:
        self.inner = inner
        self.max_retries = max_retries
        self._failures: dict[str, int] = {}
        self._last_tool_decision: Decision | None = None

    def reset(self) -> None:
        self._failures.clear()
        self._last_tool_decision = None

    def decide(self, messages: list[Message], tools: dict[str, Tool]) -> Decision:
        latest = messages[-1]
        if (
            latest.role == "tool"
            and latest.content.startswith("tool error:")
            and self._last_tool_decision is not None
        ):
            tool_name = self._last_tool_decision.tool_name or "?"
            self._failures[tool_name] = self._failures.get(tool_name, 0) + 1
            if self._failures[tool_name] <= self.max_retries:
                return Decision(
                    kind="tool",
                    tool_name=tool_name,
                    content=self._last_tool_decision.content,
                    reasoning=f"Retrying {tool_name} (attempt {self._failures[tool_name]}).",
                )
            return Decision(
                kind="answer",
                content=(
                    f"Giving up on {tool_name} after {self.max_retries} retries. "
                    f"Failing input was: {self._last_tool_decision.content!r}."
                ),
                reasoning="Retry budget exhausted.",
            )

        decision = self.inner.decide(messages, tools)
        if decision.kind == "tool":
            self._last_tool_decision = decision
        return decision
