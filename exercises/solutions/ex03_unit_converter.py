"""Reference solution for Exercise 03 — Unit converter tool."""

from __future__ import annotations

import re

from agent_course import ToolError
from agent_course.agent import Agent, Decision, TeachingBrain
from agent_course.messages import Message
from agent_course.tools import Tool


_PATTERN = re.compile(r"(\d+(?:\.\d+)?)\s*(\w+)\s*(?:to|in)\s*(\w+)", re.IGNORECASE)

_LENGTH = {"km": 1.0, "miles": 1 / 0.621371, "mile": 1 / 0.621371, "mi": 1 / 0.621371}
_TIME = {"hours": 1.0, "hour": 1.0, "minutes": 1 / 60, "minute": 1 / 60, "min": 1 / 60}


def _convert(value: float, src: str, dst: str) -> float:
    src, dst = src.lower(), dst.lower()
    if src in _LENGTH and dst in _LENGTH:
        return value * _LENGTH[src] / _LENGTH[dst]
    if src in _TIME and dst in _TIME:
        return value * _TIME[src] / _TIME[dst]
    if src == "f" and dst == "c":
        return (value - 32) * 5 / 9
    if src == "c" and dst == "f":
        return value * 9 / 5 + 32
    raise ToolError(f"Unsupported unit pair: {src} -> {dst}")


class UnitConverterTool:
    name = "unit_converter"
    description = "Convert between common units."

    def run(self, tool_input: str) -> str:
        m = _PATTERN.search(tool_input)
        if not m:
            raise ToolError(f"Could not parse conversion: {tool_input!r}")
        value = float(m.group(1))
        return f"{_convert(value, m.group(2), m.group(3)):.2f}"


class UnitAwareBrain(TeachingBrain):
    def decide(self, messages: list[Message], tools: dict[str, Tool]) -> Decision:
        latest = messages[-1]
        if (
            latest.role != "tool"
            and "unit_converter" in tools
            and any(kw in latest.content.lower() for kw in (" to ", " in "))
            and any(ch.isdigit() for ch in latest.content)
        ):
            return Decision(
                kind="tool",
                tool_name="unit_converter",
                content=latest.content,
                reasoning="Looks like a unit conversion request.",
            )
        return super().decide(messages, tools)


def build_agent() -> Agent:
    return Agent(brain=UnitAwareBrain(), tools=[UnitConverterTool()])
