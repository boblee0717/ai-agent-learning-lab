from __future__ import annotations

import ast
import operator
import re
from dataclasses import dataclass
from typing import Protocol


class Tool(Protocol):
    name: str
    description: str

    def run(self, tool_input: str) -> str:
        """Run the tool and return a text observation."""


@dataclass(frozen=True)
class ToolSpec:
    name: str
    description: str


class CalculatorTool:
    name = "calculator"
    description = "Use for simple arithmetic, such as 2 + 2 or 12 * (3 + 4)."

    _operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
    }

    def run(self, tool_input: str) -> str:
        expression = _extract_expression(tool_input)
        value = self._eval(ast.parse(expression, mode="eval").body)
        if isinstance(value, float) and value.is_integer():
            value = int(value)
        return str(value)

    def _eval(self, node: ast.AST) -> int | float:
        if isinstance(node, ast.Constant) and isinstance(node.value, int | float):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in self._operators:
            left = self._eval(node.left)
            right = self._eval(node.right)
            return self._operators[type(node.op)](left, right)
        if isinstance(node, ast.UnaryOp) and type(node.op) in self._operators:
            return self._operators[type(node.op)](self._eval(node.operand))
        raise ValueError("Only simple arithmetic is supported.")


class NotesTool:
    name = "notes"
    description = "Use for short notes about agents, tools, memory, and traces."

    def __init__(self, notes: dict[str, str] | None = None) -> None:
        self.notes = notes or {
            "agent": "An agent uses a brain plus tools and state to pursue a goal.",
            "tool": "A tool is a callable capability the agent can use outside its own brain.",
            "memory": "Memory is information carried across steps or conversations.",
            "trace": "A trace is the record of decisions, tool calls, observations, and answers.",
        }

    def run(self, tool_input: str) -> str:
        lowered = tool_input.lower()
        matches = [note for keyword, note in self.notes.items() if keyword in lowered]
        if matches:
            return " ".join(matches)
        return "No note matched. Try asking about agent, tool, memory, or trace."


def _extract_expression(text: str) -> str:
    matches = re.findall(r"[\d\s+\-*/().^]+", text)
    if not matches:
        raise ValueError("No arithmetic expression found.")
    expression = max((match.strip() for match in matches), key=len)
    expression = expression.strip(" .,!?;:").replace("^", "**")
    if not expression:
        raise ValueError("No arithmetic expression found.")
    return expression
