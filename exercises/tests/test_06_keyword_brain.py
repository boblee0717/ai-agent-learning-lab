from starter.ex06_keyword_brain import build_brain

from agent_course import Agent, CalculatorTool, MemoryTool, NotesTool
from agent_course.brains import EchoLlmBrain


class TestKeywordLlmBrain:
    def test_brain_is_echo_llm_brain(self) -> None:
        assert isinstance(build_brain(), EchoLlmBrain)

    def test_calculator_routing(self) -> None:
        agent = Agent(brain=build_brain())
        result = agent.run("What is 8 * 7?")
        assert "56" in result.answer
        assert result.tool_calls and result.tool_calls[0].name == "calculator"

    def test_memory_routing(self) -> None:
        memory = MemoryTool()
        agent = Agent(brain=build_brain(), tools=[CalculatorTool(), NotesTool(), memory])
        agent.run("remember name Bob")
        assert memory.store.all() == {"name": "Bob"}

    def test_unknown_prompt_answers_with_default(self) -> None:
        agent = Agent(brain=build_brain())
        result = agent.run("hello")
        assert result.answer.lower() == "i do not know."
        assert result.tool_calls == []
