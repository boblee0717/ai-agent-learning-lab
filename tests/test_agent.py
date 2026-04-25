import pytest

from agent_course import Agent, CalculatorTool, NotesTool, ToolError, Trace
from agent_course.agent import Decision, TeachingBrain
from agent_course.messages import Message
from agent_course.tools import Tool


class _BoomTool:
    name = "boom"
    description = "Always raises, used to exercise error handling."

    def run(self, tool_input: str) -> str:
        raise RuntimeError("kaboom")


class _GhostBrain(TeachingBrain):
    def decide(self, messages: list[Message], tools: dict[str, Tool]) -> Decision:
        return Decision(kind="tool", tool_name="ghost", content="x")


class _BoomBrain(TeachingBrain):
    def decide(self, messages: list[Message], tools: dict[str, Tool]) -> Decision:
        if messages[-1].role == "tool":
            return Decision(kind="answer", content=messages[-1].content)
        return Decision(kind="tool", tool_name="boom", content="go")


class TestAgent:
    def test_calculator_path(self) -> None:
        result = Agent().run("What is 8 * 7?")
        assert result.answer == "Here is what I found: 56"
        assert result.tool_calls[0].name == "calculator"
        assert result.tool_calls[0].error is False

    def test_notes_path(self) -> None:
        result = Agent().run("Explain agent memory")
        assert "Memory is information" in result.answer
        assert result.tool_calls[0].name == "notes"

    def test_falls_back_when_no_tool_matches(self) -> None:
        result = Agent().run("Hello there")
        assert result.tool_calls == []
        assert "agent concepts" in result.answer

    def test_step_limit_returns_graceful_message(self) -> None:
        result = Agent(max_steps=1).run("What is 8 * 7?")
        assert "step limit" in result.answer.lower()


class TestTrace:
    def test_trace_is_structured(self) -> None:
        result = Agent().run("What is 2 + 2?")
        assert isinstance(result.trace, Trace)
        kinds = [ev.kind for ev in result.trace.events]
        assert kinds[0] == "goal"
        assert "tool_call" in kinds
        assert "observation" in kinds
        assert kinds[-1] == "answer"

    def test_trace_iterates_as_strings_for_back_compat(self) -> None:
        result = Agent().run("What is 2 + 2?")
        for line in result.trace:
            assert isinstance(line, str)

    def test_decision_reasoning_is_in_trace(self) -> None:
        result = Agent().run("What is 2 + 2?")
        thoughts = [ev for ev in result.trace.events if ev.kind == "thought"]
        assert thoughts, "Expected the brain's reasoning to appear as a thought event."


class TestCalculatorTool:
    def test_basic(self) -> None:
        assert CalculatorTool().run("12 * (3 + 4)") == "84"

    def test_int_result_is_not_float(self) -> None:
        assert CalculatorTool().run("10 / 2") == "5"

    def test_division_by_zero_raises_tool_error(self) -> None:
        with pytest.raises(ToolError):
            CalculatorTool().run("1 / 0")

    def test_huge_exponent_is_blocked(self) -> None:
        with pytest.raises(ToolError):
            CalculatorTool().run("2 ** 1000")

    def test_overlong_input_is_blocked(self) -> None:
        with pytest.raises(ToolError):
            CalculatorTool().run("1+" * 200)

    def test_no_expression_raises_tool_error(self) -> None:
        with pytest.raises(ToolError):
            CalculatorTool().run("hello world")


class TestNotesTool:
    def test_known_keyword(self) -> None:
        assert "agent" in NotesTool().run("what is an agent").lower()

    def test_unknown_keyword(self) -> None:
        assert "No note matched" in NotesTool().run("xyzzy")


class TestAgentErrorRecovery:
    def test_unknown_tool_returns_graceful_answer(self) -> None:
        result = Agent(brain=_GhostBrain()).run("anything")
        assert "unknown tool" in result.answer.lower()

    def test_tool_exception_is_surfaced_as_observation(self) -> None:
        agent = Agent(brain=_BoomBrain(), tools=[_BoomTool()])
        result = agent.run("trigger")
        assert result.tool_calls and result.tool_calls[0].error is True
        assert "tool error" in result.answer.lower() or "kaboom" in result.answer.lower()

    def test_calculator_error_is_observation_not_crash(self) -> None:
        # The brain wants the calculator, but the user gave it an impossible
        # expression. The agent should not crash; it should answer with the
        # tool error so a human (or future LLM brain) can decide what to do.
        agent = Agent()
        result = agent.run("What is 1 / 0?")
        assert result.tool_calls and result.tool_calls[0].error is True
        assert "fail" in result.answer.lower() or "error" in result.answer.lower()
