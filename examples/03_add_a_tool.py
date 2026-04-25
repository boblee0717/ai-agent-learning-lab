from agent_course.agent import Agent, Decision, TeachingBrain
from agent_course.messages import Message
from agent_course.tools import CalculatorTool, NotesTool, Tool


class WeatherTool:
    name = "weather"
    description = "Use for simple weather questions in the teaching demo."

    def run(self, tool_input: str) -> str:
        return "Sunny in the demo world. Real agents would call a weather API here."


class WeatherAwareBrain(TeachingBrain):
    def decide(self, messages: list[Message], tools: dict[str, Tool]) -> Decision:
        latest = messages[-1].content.lower()
        if messages[-1].role != "tool" and "weather" in latest and "weather" in tools:
            return Decision(kind="tool", tool_name="weather", content=messages[-1].content)
        return super().decide(messages, tools)


def main() -> None:
    agent = Agent(
        brain=WeatherAwareBrain(),
        tools=[CalculatorTool(), NotesTool(), WeatherTool()],
    )
    result = agent.run("What is the weather?")

    print(result.answer)
    print()
    print("Trace:")
    for item in result.trace:
        print(f"  - {item}")


if __name__ == "__main__":
    main()

