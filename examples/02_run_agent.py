from agent_course import Agent


def main() -> None:
    agent = Agent()

    for prompt in [
        "What is an agent?",
        "What is 8 * 7?",
        "What is trace used for?",
        "What is 1 / 0?",
    ]:
        result = agent.run(prompt)
        print(f"Prompt: {prompt}")
        print(f"Answer: {result.answer}")
        print("Trace:")
        for ev in result.trace.events:
            step = f"step {ev.step} " if ev.step else ""
            print(f"  - {step}{ev.kind}: {ev.message}")
        print()


if __name__ == "__main__":
    main()
