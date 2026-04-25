"""Exercise 03 — Add a UnitConverterTool."""

from __future__ import annotations

from agent_course import ToolError  # noqa: F401  (use it in your raise)
from agent_course.agent import Agent, Decision, TeachingBrain
from agent_course.messages import Message
from agent_course.tools import Tool


class UnitConverterTool:
    name = "unit_converter"
    description = (
        "Convert between common units. "
        "Input examples: '5 km to miles', '100 f to c', '2 hours to minutes'."
    )

    _KM_TO_MILES = 0.621371

    def run(self, tool_input: str) -> str:
        # TODO:
        # 1) parse a (value, from_unit, to_unit) triple out of tool_input.
        # 2) compute the converted value (km<->miles, f<->c, hours<->minutes).
        # 3) return the result as a string with 2 decimal places.
        # 4) raise ToolError for unsupported unit pairs or unparseable input.
        raise NotImplementedError


class UnitAwareBrain(TeachingBrain):
    """TeachingBrain + routing for unit-conversion prompts."""

    def decide(self, messages: list[Message], tools: dict[str, Tool]) -> Decision:
        # TODO: when the latest user message looks like a unit conversion
        # ("X unit to unit" / "X unit in unit"), return a Decision that calls
        # the unit_converter tool. Otherwise delegate to ``super().decide``.
        raise NotImplementedError


def build_agent() -> Agent:
    """Helper used by the autograder."""
    return Agent(brain=UnitAwareBrain(), tools=[UnitConverterTool()])
