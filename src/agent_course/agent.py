from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal, Protocol

from agent_course.messages import Message
from agent_course.tools import CalculatorTool, NotesTool, Tool


DecisionKind = Literal["answer", "tool"]


@dataclass(frozen=True)
class Decision:
    kind: DecisionKind
    content: str
    tool_name: str | None = None


@dataclass(frozen=True)
class ToolCall:
    name: str
    input: str
    output: str


@dataclass(frozen=True)
class AgentResult:
    answer: str
    messages: list[Message]
    trace: list[str]
    tool_calls: list[ToolCall]


class Brain(Protocol):
    def decide(self, messages: list[Message], tools: dict[str, Tool]) -> Decision:
        """Choose whether to answer or call a tool."""


class TeachingBrain:
    """A deterministic stand-in for an LLM, useful while learning the agent loop."""

    def decide(self, messages: list[Message], tools: dict[str, Tool]) -> Decision:
        latest = messages[-1].content

        if messages[-1].role == "tool":
            return Decision(kind="answer", content=f"Here is what I found: {latest}")

        if "calculator" in tools and re.search(r"\d+\s*[-+*/^]\s*\d+", latest):
            return Decision(kind="tool", tool_name="calculator", content=latest)

        if "notes" in tools and any(word in latest.lower() for word in ["agent", "tool", "memory", "trace"]):
            return Decision(kind="tool", tool_name="notes", content=latest)

        return Decision(
            kind="answer",
            content="I can explain agent concepts or use simple tools. Try asking about memory or 8 * 7.",
        )


class Agent:
    def __init__(self, brain: Brain | None = None, tools: list[Tool] | None = None, max_steps: int = 4) -> None:
        self.brain = brain or TeachingBrain()
        self.tools = {tool.name: tool for tool in tools or [CalculatorTool(), NotesTool()]}
        self.max_steps = max_steps

    def run(self, user_input: str) -> AgentResult:
        messages = [
            Message(role="system", content="You are a teaching agent that explains its own steps."),
            Message(role="user", content=user_input),
        ]
        trace = [f"user goal: {user_input}"]
        tool_calls: list[ToolCall] = []

        for step in range(1, self.max_steps + 1):
            decision = self.brain.decide(messages, self.tools)
            trace.append(f"step {step}: decision={decision.kind}")

            if decision.kind == "answer":
                messages.append(Message(role="assistant", content=decision.content))
                trace.append(f"final answer: {decision.content}")
                return AgentResult(decision.content, messages, trace, tool_calls)

            if decision.tool_name not in self.tools:
                answer = f"I wanted to use an unknown tool: {decision.tool_name}"
                messages.append(Message(role="assistant", content=answer))
                trace.append(answer)
                return AgentResult(answer, messages, trace, tool_calls)

            tool = self.tools[decision.tool_name]
            trace.append(f"calling tool: {tool.name}")
            observation = tool.run(decision.content)
            tool_calls.append(ToolCall(name=tool.name, input=decision.content, output=observation))
            messages.append(Message(role="tool", content=observation))
            trace.append(f"observation: {observation}")

        answer = "I reached the step limit before finishing."
        messages.append(Message(role="assistant", content=answer))
        trace.append(answer)
        return AgentResult(answer, messages, trace, tool_calls)

