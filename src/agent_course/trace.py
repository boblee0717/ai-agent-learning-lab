"""Structured trace events.

A real agent framework records far more than a list of strings: each step has
a kind, a timestamp, an actor, and structured payload. We keep that shape
small and obvious here so a learner can grow it later without rewriting.

The list of events is still string-renderable via ``str(trace)`` so existing
lessons that print the trace keep working.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

EventKind = Literal["goal", "thought", "tool_call", "observation", "answer", "error", "limit"]


@dataclass(frozen=True)
class TraceEvent:
    kind: EventKind
    message: str
    step: int = 0


@dataclass
class Trace:
    events: list[TraceEvent] = field(default_factory=list)

    def add(self, kind: EventKind, message: str, step: int = 0) -> None:
        self.events.append(TraceEvent(kind=kind, message=message, step=step))

    def as_lines(self) -> list[str]:
        """Render events as the same one-line-per-event format used in lessons 1-4."""
        lines: list[str] = []
        for ev in self.events:
            prefix = f"step {ev.step}: " if ev.step else ""
            lines.append(f"{prefix}{ev.kind}: {ev.message}")
        return lines

    def __iter__(self):
        # Lets old code do ``for item in result.trace: print(item)`` and still
        # get a readable string, while new code can read ``result.trace.events``.
        return iter(self.as_lines())

    def __len__(self) -> int:
        return len(self.events)

    def __str__(self) -> str:
        return "\n".join(self.as_lines())
