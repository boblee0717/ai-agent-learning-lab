import pytest

from agent_course import Agent, CalculatorTool, NotesTool, ToolError


class _BoomTool:
    name = "boom"
    description = "Always raises, used to exercise error handling."

    def run(self, tool_input: str) -> str:
        raise RuntimeError("kaboom")


class TestAgent:
    def test_calculator_path(self) -> None:
        result = Agent().run("What is 8 * 7?")
        assert result.answer == "Here is what I found: 56"
        assert result.tool_calls[0].name == "calculator"

    def test_notes_path(self) -> None:
        result = Agent().run("Explain agent memory")
        assert "Memory is information" in result.answer
        assert result.tool_calls[0].name == "notes"

    def test_falls_back_when_no_tool_matches(self) -> None:
        result = Agent().run("Hello there")
        assert result.tool_calls == []
        assert "agent concepts" in result.answer

    def test_step_limit_returns_graceful_message(self) -> None:
        # max_steps=1 means: first iteration must answer; for a tool-shaped
        # prompt it will call the tool, but the loop exits before the second
        # decision can produce a final answer.
        result = Agent(max_steps=1).run("What is 8 * 7?")
        assert "step limit" in result.answer.lower()


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
        from agent_course.agent import Decision, TeachingBrain
        from agent_course.messages import Message
        from agent_course.tools import Tool

        class GhostBrain(TeachingBrain):
            def decide(self, messages: list[Message], tools: dict[str, Tool]) -> Decision:
                return Decision(kind="tool", tool_name="ghost", content="x")

        result = Agent(brain=GhostBrain()).run("anything")
        assert "unknown tool" in result.answer.lower()

    def test_tool_exception_is_surfaced(self) -> None:
        from agent_course.agent import Decision, TeachingBrain
        from agent_course.messages import Message
        from agent_course.tools import Tool

        class BoomBrain(TeachingBrain):
            def decide(self, messages: list[Message], tools: dict[str, Tool]) -> Decision:
                if messages[-1].role == "tool":
                    return Decision(kind="answer", content=messages[-1].content)
                return Decision(kind="tool", tool_name="boom", content="go")

        agent = Agent(brain=BoomBrain(), tools=[_BoomTool()])
        result = agent.run("trigger")
        # We expect the loop to capture the failure as an observation rather
        # than crashing the whole run. The exact message is asserted in PR2.
        assert result.tool_calls and result.tool_calls[0].name == "boom"
