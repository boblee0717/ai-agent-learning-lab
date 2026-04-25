"""Exercise 01 — Chatbot vs Agent.

Implement two functions that answer the same prompts in two very different
ways. See exercises/01_chatbot_vs_agent.md for the brief.
"""

from __future__ import annotations

_CANNED: dict[str, str] = {
    "What is 8 * 7?": "I think 56.",
    "What is an agent?": "Something like a chatbot but smarter, I guess.",
}


def answer_as_chatbot(prompt: str) -> str:
    """Return a canned answer. Must NOT call any tool or import Agent."""
    # TODO: look ``prompt`` up in ``_CANNED``. If it is missing, return a
    # sensible default string explaining the chatbot does not know.
    raise NotImplementedError


def answer_as_agent(prompt: str) -> str:
    """Build a default ``Agent`` and return its final answer for ``prompt``."""
    # TODO:
    # 1) import Agent from agent_course (do this inside the function so the
    #    chatbot side of the file is import-safe even if Agent is broken).
    # 2) build a default agent and call ``.run(prompt)``.
    # 3) return ``result.answer``.
    raise NotImplementedError


def agent_tool_calls(prompt: str) -> list[str]:
    """Return the list of tool names the agent called for ``prompt``.

    Used by the autograder to confirm the agent path actually used a tool.
    """
    # TODO: same as ``answer_as_agent`` but return ``[tc.name for tc in result.tool_calls]``.
    raise NotImplementedError
