"""Long-term memory abstractions.

The agent loop deliberately knows nothing about *how* memory is stored. It only
knows the ``Memory`` protocol: remember a fact, recall facts that look related
to a query. That keeps the door open for replacing the in-memory dict below
with a real vector database, SQLite, Redis, or a hosted service.

This file is the seam that lessons/05 talks about.
"""

from __future__ import annotations

from typing import Protocol


class Memory(Protocol):
    def remember(self, key: str, value: str) -> None:
        """Store a fact under ``key``."""

    def recall(self, query: str) -> list[str]:
        """Return facts that look related to ``query``."""

    def all(self) -> dict[str, str]:
        """Return all stored facts (handy for debugging and tests)."""


class InMemoryStore:
    """Smallest useful Memory implementation. Naive substring match on recall."""

    def __init__(self, initial: dict[str, str] | None = None) -> None:
        self._store: dict[str, str] = dict(initial or {})

    def remember(self, key: str, value: str) -> None:
        self._store[key.strip().lower()] = value.strip()

    def recall(self, query: str) -> list[str]:
        q = query.lower()
        return [
            f"{key}: {value}"
            for key, value in self._store.items()
            if key in q or any(token and token in q for token in value.lower().split())
        ]

    def all(self) -> dict[str, str]:
        return dict(self._store)
