from __future__ import annotations

import ast
import operator
import re
from dataclasses import dataclass
from typing import ClassVar, Protocol


class ToolError(Exception):
    """Raised when a tool fails in an expected way (bad input, unsupported op, etc.)."""


class Tool(Protocol):
    name: str
    description: str

    def run(self, tool_input: str) -> str:
        """Run the tool and return a text observation."""


@dataclass(frozen=True)
class ToolSpec:
    name: str
    description: str


# Safety limits for the teaching calculator. Prevents pathological inputs like
# 2 ** 10_000_000 from hanging the interpreter or eating all the memory.
_MAX_EXPRESSION_LENGTH = 200
_MAX_POW_EXPONENT = 64


class CalculatorTool:
    name = "calculator"
    description = "Use for simple arithmetic, such as 2 + 2 or 12 * (3 + 4)."

    _operators: ClassVar[dict[type[ast.AST], object]] = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
    }

    def run(self, tool_input: str) -> str:
        expression = _extract_expression(tool_input)
        try:
            tree = ast.parse(expression, mode="eval")
        except SyntaxError as exc:
            raise ToolError(f"Could not parse expression: {expression!r}") from exc

        try:
            value = self._eval(tree.body)
        except ZeroDivisionError as exc:
            raise ToolError("Division by zero.") from exc

        if isinstance(value, float) and value.is_integer():
            value = int(value)
        return str(value)

    def _eval(self, node: ast.AST) -> int | float:
        if isinstance(node, ast.Constant) and isinstance(node.value, int | float):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in self._operators:
            left = self._eval(node.left)
            right = self._eval(node.right)
            if isinstance(node.op, ast.Pow) and isinstance(right, int | float) and right > _MAX_POW_EXPONENT:
                raise ToolError(f"Exponent too large (>{_MAX_POW_EXPONENT}).")
            return self._operators[type(node.op)](left, right)
        if isinstance(node, ast.UnaryOp) and type(node.op) in self._operators:
            return self._operators[type(node.op)](self._eval(node.operand))
        raise ToolError("Only simple arithmetic is supported.")


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
    if len(text) > _MAX_EXPRESSION_LENGTH:
        raise ToolError(f"Input too long (>{_MAX_EXPRESSION_LENGTH} chars).")
    matches = re.findall(r"[\d\s+\-*/().^]+", text)
    if not matches:
        raise ToolError("No arithmetic expression found.")
    expression = max((match.strip() for match in matches), key=len)
    expression = expression.strip(" .,!?;:").replace("^", "**")
    if not expression:
        raise ToolError("No arithmetic expression found.")
    return expression
