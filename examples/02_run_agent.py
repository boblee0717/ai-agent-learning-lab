from agent_course import Agent


def main() -> None:
    agent = Agent()

    for prompt in [
        "What is an agent?",
        "What is 8 * 7?",
        "What is trace used for?",
    ]:
        result = agent.run(prompt)
        print(f"Prompt: {prompt}")
        print(f"Answer: {result.answer}")
        print("Trace:")
        for item in result.trace:
            print(f"  - {item}")
        print()


if __name__ == "__main__":
    main()

