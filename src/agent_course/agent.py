from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal, Protocol

from agent_course.messages import Message
from agent_course.tools import CalculatorTool, NotesTool, Tool, ToolError
from agent_course.trace import Trace

DecisionKind = Literal["answer", "tool"]


@dataclass(frozen=True)
class Decision:
    kind: DecisionKind
    content: str
    tool_name: str | None = None
    # Free-form reasoning the brain wants to expose in the trace. Real LLM
    # brains often produce something like "I should call the calculator
    # because the user asked for arithmetic." Keeping this in the contract
    # means swapping the brain later does not change any consumers.
    reasoning: str = ""


@dataclass(frozen=True)
class ToolCall:
    name: str
    input: str
    output: str
    error: bool = False


@dataclass(frozen=True)
class AgentResult:
    answer: str
    messages: list[Message]
    trace: Trace
    tool_calls: list[ToolCall]


class Brain(Protocol):
    def decide(self, messages: list[Message], tools: dict[str, Tool]) -> Decision:
        """Choose whether to answer or call a tool."""


class TeachingBrain:
    """A deterministic stand-in for an LLM, useful while learning the agent loop."""

    def decide(self, messages: list[Message], tools: dict[str, Tool]) -> Decision:
        latest = messages[-1].content

        if messages[-1].role == "tool":
            # If the previous tool failed, admit it instead of pretending.
            if latest.startswith("tool error:"):
                return Decision(
                    kind="answer",
                    content=f"The tool failed: {latest.removeprefix('tool error:').strip()}",
                    reasoning="Last observation was an error, so stop and report it.",
                )
            return Decision(
                kind="answer",
                content=f"Here is what I found: {latest}",
                reasoning="The previous step produced an observation, so I can answer now.",
            )

        if "calculator" in tools and re.search(r"\d+\s*[-+*/^]\s*\d+", latest):
            return Decision(
                kind="tool",
                tool_name="calculator",
                content=latest,
                reasoning="Input contains an arithmetic pattern, calculator is the right tool.",
            )

        lowered = latest.lower()
        if "memory" in tools and (
            lowered.startswith(("remember ", "recall "))
            or "what is my " in lowered
            or "what are my " in lowered
        ):
            return Decision(
                kind="tool",
                tool_name="memory",
                content=latest,
                reasoning="Input asks to remember or recall a fact, route to memory tool.",
            )

        if "notes" in tools and any(
            word in lowered for word in ["agent", "tool", "memory", "trace"]
        ):
            return Decision(
                kind="tool",
                tool_name="notes",
                content=latest,
                reasoning="Input mentions an agent concept, the notes tool can explain it.",
            )

        return Decision(
            kind="answer",
            content="I can explain agent concepts or use simple tools. Try asking about memory or 8 * 7.",
            reasoning="No matching tool pattern, fall back to a generic explanation.",
        )


class Agent:
    def __init__(
        self,
        brain: Brain | None = None,
        tools: list[Tool] | None = None,
        max_steps: int = 4,
    ) -> None:
        self.brain = brain or TeachingBrain()
        self.tools = {tool.name: tool for tool in tools or [CalculatorTool(), NotesTool()]}
        self.max_steps = max_steps

    def run(self, user_input: str) -> AgentResult:
        messages: list[Message] = [
            Message(role="system", content="You are a teaching agent that explains its own steps."),
            Message(role="user", content=user_input),
        ]
        trace = Trace()
        trace.add("goal", user_input)
        tool_calls: list[ToolCall] = []

        for step in range(1, self.max_steps + 1):
            decision = self.brain.decide(messages, self.tools)
            if decision.reasoning:
                trace.add("thought", decision.reasoning, step=step)

            if decision.kind == "answer":
                messages.append(Message(role="assistant", content=decision.content))
                trace.add("answer", decision.content, step=step)
                return AgentResult(decision.content, messages, trace, tool_calls)

            if decision.tool_name is None or decision.tool_name not in self.tools:
                answer = f"I wanted to use an unknown tool: {decision.tool_name}"
                messages.append(Message(role="assistant", content=answer))
                trace.add("error", answer, step=step)
                return AgentResult(answer, messages, trace, tool_calls)

            tool = self.tools[decision.tool_name]
            trace.add("tool_call", f"{tool.name}({decision.content!r})", step=step)

            error = False
            try:
                observation = tool.run(decision.content)
            except ToolError as exc:
                # Expected failure: feed it back to the brain as an observation
                # so the brain (or a future LLM brain) gets a chance to recover.
                observation = f"tool error: {exc}"
                error = True
            except Exception as exc:
                # Unexpected failure: still feed back, but tag visibly. This is
                # the same pattern real frameworks use to enable self-correction.
                observation = f"tool error: {type(exc).__name__}: {exc}"
                error = True

            tool_calls.append(
                ToolCall(name=tool.name, input=decision.content, output=observation, error=error)
            )
            messages.append(Message(role="tool", content=observation))
            trace.add("observation", observation, step=step)

        answer = "I reached the step limit before finishing."
        messages.append(Message(role="assistant", content=answer))
        trace.add("limit", answer)
        return AgentResult(answer, messages, trace, tool_calls)
