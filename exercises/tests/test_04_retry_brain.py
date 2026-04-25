from starter.ex04_retry_brain import RetryBrain

from agent_course import Agent
from agent_course.agent import Decision, TeachingBrain
from agent_course.messages import Message
from agent_course.tools import Tool, ToolError


class _FlakyTool:
    """Fails the first ``failures`` times, then returns ``ok``."""

    name = "flaky"
    description = "Fails a few times before succeeding."

    def __init__(self, failures: int) -> None:
        self.calls = 0
        self.failures = failures

    def run(self, tool_input: str) -> str:
        self.calls += 1
        if self.calls <= self.failures:
            raise ToolError(f"transient #{self.calls}")
        return "ok"


class _AlwaysFlakyBrain(TeachingBrain):
    """Always wants to call the flaky tool until it gets a non-error obs."""

    def decide(self, messages: list[Message], tools: dict[str, Tool]) -> Decision:
        latest = messages[-1]
        if latest.role == "tool" and not latest.content.startswith("tool error:"):
            return Decision(kind="answer", content=f"Final: {latest.content}")
        return Decision(kind="tool", tool_name="flaky", content="please")


class TestRetryBrain:
    def test_recovers_after_a_few_failures(self) -> None:
        inner = _AlwaysFlakyBrain()
        brain = RetryBrain(inner, max_retries=3)
        flaky = _FlakyTool(failures=2)
        agent = Agent(brain=brain, tools=[flaky], max_steps=10)

        result = agent.run("trigger")

        assert "Final: ok" in result.answer
        assert flaky.calls == 3, "Should have called the tool 1 + 2 retries times."

    def test_gives_up_after_exhausting_retries(self) -> None:
        inner = _AlwaysFlakyBrain()
        brain = RetryBrain(inner, max_retries=1)
        flaky = _FlakyTool(failures=99)
        agent = Agent(brain=brain, tools=[flaky], max_steps=10)

        result = agent.run("trigger")

        assert "giving up" in result.answer.lower()
        assert "please" in result.answer, "Give-up answer should echo the failing tool input."

    def test_reset_clears_state_between_runs(self) -> None:
        inner = _AlwaysFlakyBrain()
        brain = RetryBrain(inner, max_retries=1)
        flaky = _FlakyTool(failures=99)
        agent = Agent(brain=brain, tools=[flaky], max_steps=10)

        agent.run("first")
        brain.reset()
        flaky2 = _FlakyTool(failures=0)
        agent2 = Agent(brain=brain, tools=[flaky2], max_steps=10)
        result = agent2.run("second")

        assert "Final: ok" in result.answer
