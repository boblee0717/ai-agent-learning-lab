"""Exercise 06 — Keyword-routed brain that still uses the LLM prompt format."""

from __future__ import annotations

from agent_course.agent import Decision
from agent_course.brains import EchoLlmBrain
from agent_course.messages import Message
from agent_course.tools import Tool


def keyword_responder(
    prompt: str,
    messages: list[Message],
    tools: dict[str, Tool],
) -> Decision:
    """Return a Decision based on simple keyword rules over the latest user
    message. The ``prompt`` string is the rendered LLM prompt; you can use
    it (or ignore it) — your call.
    """
    # TODO: implement the four rules described in the brief.
    raise NotImplementedError


def build_brain() -> EchoLlmBrain:
    return EchoLlmBrain(responder=keyword_responder)
