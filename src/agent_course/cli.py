"""Tiny command-line entry point: ``python -m agent_course "what is 8 * 7?"``.

Kept intentionally small so a learner can read the whole file in 30 seconds and
see how a goal flows into ``Agent.run`` and back out as a trace.
"""

from __future__ import annotations

import argparse
import sys

from agent_course.agent import Agent


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="agent-course",
        description="Run the teaching agent on a single prompt and print its trace.",
    )
    parser.add_argument("prompt", nargs="*", help="Goal to give the agent (quote it on the shell).")
    parser.add_argument("--no-trace", action="store_true", help="Only print the final answer.")
    parser.add_argument("--max-steps", type=int, default=4, help="Max loop iterations (default: 4).")
    args = parser.parse_args(argv)

    prompt = " ".join(args.prompt).strip()
    if not prompt:
        parser.print_help()
        return 1

    result = Agent(max_steps=args.max_steps).run(prompt)

    print(f"Answer: {result.answer}")
    if not args.no_trace:
        print("Trace:")
        for item in result.trace:
            print(f"  - {item}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
