import pytest

from agent_course import Agent, InMemoryStore, MemoryTool, ToolError
from agent_course.agent import Decision
from agent_course.brains import EchoLlmBrain, _decision_from_json, _format_prompt
from agent_course.messages import Message
from agent_course.tools import CalculatorTool, NotesTool


class TestInMemoryStore:
    def test_remember_and_recall(self) -> None:
        store = InMemoryStore()
        store.remember("Name", "  Bob  ")
        assert store.all() == {"name": "Bob"}
        assert store.recall("what is my name") == ["name: Bob"]

    def test_recall_misses(self) -> None:
        assert InMemoryStore().recall("anything") == []


class TestMemoryTool:
    def test_remember_then_recall(self) -> None:
        tool = MemoryTool()
        assert "Remembered" in tool.run("remember name Bob")
        assert "Bob" in tool.run("recall name")
        assert "Bob" in tool.run("what is my name")

    def test_recall_unknown(self) -> None:
        tool = MemoryTool()
        assert "do not remember" in tool.run("recall language")

    def test_invalid_input_raises_tool_error(self) -> None:
        with pytest.raises(ToolError):
            MemoryTool().run("totally random sentence")


class TestAgentWithMemory:
    def test_memory_persists_across_runs(self) -> None:
        memory_tool = MemoryTool()
        agent = Agent(tools=[CalculatorTool(), NotesTool(), memory_tool])

        agent.run("remember name Alice")
        result = agent.run("what is my name")

        assert "Alice" in result.answer
        assert memory_tool.store.all() == {"name": "Alice"}


class TestEchoLlmBrain:
    def test_default_responder_matches_teaching_brain(self) -> None:
        agent = Agent(brain=EchoLlmBrain())
        result = agent.run("What is 8 * 7?")
        assert result.answer == "Here is what I found: 56"

    def test_custom_responder_is_called(self) -> None:
        captured: dict[str, str] = {}

        def responder(prompt: str, messages, tools) -> Decision:
            captured["prompt"] = prompt
            return Decision(kind="answer", content="forced", reasoning="test")

        agent = Agent(brain=EchoLlmBrain(responder=responder))
        result = agent.run("anything")
        assert result.answer == "forced"
        assert "Tools:" in captured["prompt"]
        assert "user: anything" in captured["prompt"]

    def test_format_prompt_lists_tools(self) -> None:
        prompt = _format_prompt(
            [Message(role="user", content="hi")],
            {"calculator": CalculatorTool(), "notes": NotesTool()},
        )
        assert "- calculator:" in prompt
        assert "- notes:" in prompt


class TestDecisionFromJson:
    def test_clean_json(self) -> None:
        d = _decision_from_json('{"kind": "answer", "content": "hi", "reasoning": "r"}')
        assert d.kind == "answer"
        assert d.content == "hi"
        assert d.reasoning == "r"

    def test_messy_json_with_text_around(self) -> None:
        d = _decision_from_json('Sure! {"kind": "tool", "tool_name": "x", "content": "y"} done')
        assert d.kind == "tool"
        assert d.tool_name == "x"

    def test_unknown_kind_falls_back_to_answer(self) -> None:
        d = _decision_from_json('{"kind": "garbage"}')
        assert d.kind == "answer"
