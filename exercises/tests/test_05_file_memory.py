import json
from pathlib import Path

from starter.ex05_file_memory import FileStore

from agent_course import Agent, MemoryTool
from agent_course.tools import CalculatorTool, NotesTool


class TestFileStoreBasics:
    def test_creates_file_with_empty_dict(self, tmp_path: Path) -> None:
        path = tmp_path / "store.json"
        FileStore(path)
        assert path.exists()
        assert json.loads(path.read_text()) == {}

    def test_remember_and_all(self, tmp_path: Path) -> None:
        store = FileStore(tmp_path / "s.json")
        store.remember("Name", "  Bob  ")
        assert store.all() == {"name": "Bob"}

    def test_recall_matches_key_or_value(self, tmp_path: Path) -> None:
        store = FileStore(tmp_path / "s.json")
        store.remember("name", "Bob")
        store.remember("language", "Chinese")
        assert "name: Bob" in store.recall("what is my name")
        assert "language: Chinese" in store.recall("speaks Chinese")


class TestPersistenceAcrossInstances:
    def test_second_instance_sees_first_writes(self, tmp_path: Path) -> None:
        path = tmp_path / "s.json"
        FileStore(path).remember("city", "Hangzhou")
        assert FileStore(path).all() == {"city": "Hangzhou"}


class TestAgentIntegration:
    def test_memory_persists_across_processes_simulated(self, tmp_path: Path) -> None:
        path = tmp_path / "store.json"

        agent_a = Agent(tools=[CalculatorTool(), NotesTool(), MemoryTool(store=FileStore(path))])
        agent_a.run("remember name Alice")

        # Brand new agent + tool instance, same on-disk store.
        agent_b = Agent(tools=[CalculatorTool(), NotesTool(), MemoryTool(store=FileStore(path))])
        result = agent_b.run("what is my name")

        assert "Alice" in result.answer
