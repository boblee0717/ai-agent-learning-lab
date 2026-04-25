"""Showcase the long-term Memory abstraction.

The agent gets a single shared MemoryTool. Conversations across multiple
``agent.run`` calls now share state, because the tool instance (and the
underlying store) survive between runs.
"""

from agent_course import Agent, CalculatorTool, MemoryTool, NotesTool


def main() -> None:
    memory_tool = MemoryTool()
    agent = Agent(tools=[CalculatorTool(), NotesTool(), memory_tool])

    for prompt in [
        "remember name Bob",
        "remember language Chinese",
        "what is my name",
        "recall language",
    ]:
        result = agent.run(prompt)
        print(f"> {prompt}")
        print(f"  {result.answer}")

    print("\nFinal store:", memory_tool.store.all())


if __name__ == "__main__":
    main()
