"""Reference solution for Exercise 01 — Chatbot vs Agent."""

from __future__ import annotations

_CANNED: dict[str, str] = {
    "What is 8 * 7?": "I think 56.",
    "What is an agent?": "Something like a chatbot but smarter, I guess.",
}


def answer_as_chatbot(prompt: str) -> str:
    return _CANNED.get(prompt, "Sorry, I am just a chatbot — I do not know that one.")


def answer_as_agent(prompt: str) -> str:
    from agent_course import Agent

    return Agent().run(prompt).answer


def agent_tool_calls(prompt: str) -> list[str]:
    from agent_course import Agent

    return [tc.name for tc in Agent().run(prompt).tool_calls]
