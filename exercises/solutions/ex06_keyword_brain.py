"""Reference solution for Exercise 06 — Keyword LLM brain."""

from __future__ import annotations

import re

from agent_course.agent import Decision
from agent_course.brains import EchoLlmBrain
from agent_course.messages import Message
from agent_course.tools import Tool


def keyword_responder(
    prompt: str,
    messages: list[Message],
    tools: dict[str, Tool],
) -> Decision:
    latest = messages[-1]
    if latest.role == "tool":
        if latest.content.startswith("tool error:"):
            return Decision(kind="answer", content=f"Tool failed: {latest.content}")
        return Decision(kind="answer", content=latest.content)

    text = latest.content.lower()
    if "calculator" in tools and re.search(r"\d+\s*[-+*/^]\s*\d+", text):
        return Decision(kind="tool", tool_name="calculator", content=latest.content)
    if "memory" in tools and (text.startswith("remember ") or text.startswith("recall ")):
        return Decision(kind="tool", tool_name="memory", content=latest.content)
    return Decision(kind="answer", content="I do not know.")


def build_brain() -> EchoLlmBrain:
    return EchoLlmBrain(responder=keyword_responder)
