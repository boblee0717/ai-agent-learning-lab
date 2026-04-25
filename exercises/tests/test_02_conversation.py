import pytest
from starter.ex02_conversation import Conversation

from agent_course import Message


class TestConversationBasics:
    def test_empty_conversation(self) -> None:
        c = Conversation()
        assert c.messages == []

    def test_system_seed(self) -> None:
        c = Conversation("you are helpful")
        assert len(c.messages) == 1
        assert c.messages[0].role == "system"
        assert c.messages[0].content == "you are helpful"

    def test_appends_in_order(self) -> None:
        c = Conversation()
        c.user("hi")
        c.assistant("hello")
        c.tool("obs")
        roles = [m.role for m in c.messages]
        assert roles == ["user", "assistant", "tool"]

    def test_last_returns_most_recent(self) -> None:
        c = Conversation()
        c.user("hi")
        c.assistant("hello")
        assert c.last() == Message(role="assistant", content="hello")

    def test_last_on_empty_raises(self) -> None:
        with pytest.raises(IndexError):
            Conversation().last()


class TestEncapsulation:
    def test_messages_property_returns_copy(self) -> None:
        c = Conversation("sys")
        snapshot = c.messages
        snapshot.append(Message(role="user", content="injected"))
        assert len(c.messages) == 1, (
            "Conversation.messages should return a copy, otherwise outside "
            "callers can corrupt the conversation."
        )


class TestHistoryText:
    def test_history_text_format(self) -> None:
        c = Conversation("sys")
        c.user("hi")
        c.assistant("hello")
        assert c.history_text() == "system: sys\nuser: hi\nassistant: hello"
