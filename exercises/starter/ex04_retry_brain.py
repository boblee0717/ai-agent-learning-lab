"""Exercise 04 — A brain that retries failed tool calls.

Wraps any inner brain. The agent loop stays untouched.
"""

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
        """Clear retry bookkeeping. Call between agent runs to start fresh."""
        # TODO: clear ``_failures`` and ``_last_tool_decision``.
        raise NotImplementedError

    def decide(self, messages: list[Message], tools: dict[str, Tool]) -> Decision:
        # TODO:
        # 1) If the most recent message is a tool error AND we still have
        #    retries left for that tool, return a Decision that re-runs the
        #    same tool with the same input (use ``self._last_tool_decision``).
        #    Increment the per-tool failure counter.
        # 2) If the most recent message is a tool error AND retries are
        #    exhausted, return an ``answer`` Decision that mentions
        #    "giving up" and the failing tool input.
        # 3) Otherwise delegate to ``self.inner.decide``. If that decision is
        #    a tool call, remember it on ``self._last_tool_decision`` so step 1
        #    can replay it on the next turn.
        raise NotImplementedError
