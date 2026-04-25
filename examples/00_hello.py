"""Smallest possible smoke test: import the package and run one prompt.

Useful when you cloned the repo on a new machine and just want to see
whether everything is wired up.
"""

from agent_course import Agent


def main() -> None:
    result = Agent().run("What is 2 + 2?")
    print(result.answer)


if __name__ == "__main__":
    main()
