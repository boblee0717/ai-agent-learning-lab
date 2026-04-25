"""Showcase swapping the brain for an LLM-style brain.

By default this uses ``EchoLlmBrain``, which builds a real LLM-style prompt
but answers locally so it costs nothing and is fully deterministic.

Set ``USE_OPENAI=1`` (and ``OPENAI_API_KEY``) to route through the optional
``OpenAiBrain`` instead. Install the extra first:

    pip install -e .[llm]
"""

from __future__ import annotations

import os

from agent_course import Agent
from agent_course.brains import EchoLlmBrain


def build_brain():
    if os.environ.get("USE_OPENAI") == "1":
        from agent_course.brains import OpenAiBrain
        return OpenAiBrain()
    return EchoLlmBrain(print_prompt=True)


def main() -> None:
    agent = Agent(brain=build_brain())
    result = agent.run("What is 8 * 7?")
    print(f"\nAnswer: {result.answer}")


if __name__ == "__main__":
    main()
