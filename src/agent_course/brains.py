"""Drop-in alternative brains for the teaching agent.

The agent loop only depends on the ``Brain`` protocol (``decide(messages, tools)
-> Decision``). Anything that satisfies that contract is a valid brain. This
file ships two examples that bracket the spectrum:

- ``EchoLlmBrain`` builds a real LLM-style prompt (system + tool catalogue +
  history) but never calls the network. Instead, a deterministic
  ``responder`` decides what to do. This is the cheapest way to *practise*
  prompt construction without paying for tokens.
- ``OpenAiBrain`` is a thin wrapper around the official ``openai`` SDK. It is
  intentionally tiny (single chat completion + JSON parsing). Only imported
  when ``pip install -e .[llm]`` and an API key are present.
"""

from __future__ import annotations

import json
import os
import re
from collections.abc import Callable
from dataclasses import dataclass

from agent_course.agent import Decision
from agent_course.messages import Message
from agent_course.tools import Tool


def _format_prompt(messages: list[Message], tools: dict[str, Tool]) -> str:
    """Render the brain's input the way a real LLM brain would.

    Splitting this out makes both LLM-style brains share the same prompt shape
    so a learner can compare apples to apples.
    """
    tool_lines = [f"- {t.name}: {t.description}" for t in tools.values()] or ["(no tools)"]
    history = "\n".join(f"{m.role}: {m.content}" for m in messages)
    return (
        "You are an agent. On each turn, return JSON of the form:\n"
        '  {"kind": "answer", "content": "..."}                    # final answer\n'
        '  {"kind": "tool", "tool_name": "...", "content": "..."}  # call a tool\n'
        "Optionally include a short \"reasoning\" field.\n\n"
        "Tools:\n" + "\n".join(tool_lines) + "\n\n"
        "Conversation:\n" + history
    )


@dataclass
class EchoLlmBrain:
    """A 'pretend LLM' brain. Builds a real prompt, then answers locally.

    Pass ``responder`` to test the agent loop with a custom strategy; default
    falls back to ``TeachingBrain`` semantics so existing tests keep passing.
    """

    responder: Callable[[str, list[Message], dict[str, Tool]], Decision] | None = None
    print_prompt: bool = False

    def decide(self, messages: list[Message], tools: dict[str, Tool]) -> Decision:
        prompt = _format_prompt(messages, tools)
        if self.print_prompt:
            print("\n--- prompt sent to LLM ---\n" + prompt + "\n--- end prompt ---\n")

        if self.responder is not None:
            return self.responder(prompt, messages, tools)

        from agent_course.agent import TeachingBrain
        return TeachingBrain().decide(messages, tools)


class OpenAiBrain:
    """Minimal OpenAI-backed brain. Optional dependency.

    Install with ``pip install -e .[llm]`` and set ``OPENAI_API_KEY``.
    """

    def __init__(self, model: str = "gpt-4o-mini", api_key: str | None = None) -> None:
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError(
                "OpenAiBrain requires the 'openai' package. Install with: pip install -e .[llm]"
            ) from exc

        self._client = OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"))
        self.model = model

    def decide(self, messages: list[Message], tools: dict[str, Tool]) -> Decision:
        prompt = _format_prompt(messages, tools)
        completion = self._client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
        )
        content = completion.choices[0].message.content or "{}"
        return _decision_from_json(content)


def _decision_from_json(payload: str) -> Decision:
    """Turn a model response into a Decision, tolerating sloppy JSON."""
    try:
        data = json.loads(payload)
    except json.JSONDecodeError:
        # Fallback: pull out the first JSON object the model emitted.
        match = re.search(r"\{.*\}", payload, re.DOTALL)
        data = json.loads(match.group(0)) if match else {}

    kind = data.get("kind", "answer")
    if kind not in ("answer", "tool"):
        kind = "answer"
    return Decision(
        kind=kind,
        content=str(data.get("content", "")),
        tool_name=data.get("tool_name"),
        reasoning=str(data.get("reasoning", "")),
    )
