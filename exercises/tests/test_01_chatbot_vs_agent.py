import inspect

import pytest
from starter import ex01_chatbot_vs_agent as ex


class TestChatbot:
    def test_returns_known_answer(self) -> None:
        assert "56" in ex.answer_as_chatbot("What is 8 * 7?")

    def test_unknown_prompt_returns_default_string(self) -> None:
        out = ex.answer_as_chatbot("totally unknown prompt")
        assert isinstance(out, str) and out

    def test_chatbot_does_not_import_agent(self) -> None:
        source = inspect.getsource(ex.answer_as_chatbot)
        assert "Agent(" not in source, (
            "answer_as_chatbot should not instantiate Agent — "
            "it represents the dumb chatbot baseline."
        )


class TestAgent:
    def test_calculator_path(self) -> None:
        assert "56" in ex.answer_as_agent("What is 8 * 7?")

    def test_uses_calculator_tool(self) -> None:
        assert ex.agent_tool_calls("What is 8 * 7?") == ["calculator"]

    def test_falls_back_for_chitchat(self) -> None:
        # The default TeachingBrain should give the generic explanation when
        # nothing matches; what matters here is that it does not crash.
        out = ex.answer_as_agent("hello there")
        assert isinstance(out, str) and out


@pytest.mark.parametrize("fn", [ex.answer_as_chatbot, ex.answer_as_agent, ex.agent_tool_calls])
def test_implemented(fn) -> None:
    try:
        fn("What is 8 * 7?")
    except NotImplementedError:
        pytest.fail(f"{fn.__name__} is still a TODO — fill it in.")
