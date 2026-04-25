# 02: Messages And State

Agents need state because each step depends on what happened before.

This project uses four message roles:

- `system`: background instruction.
- `user`: the user's request.
- `tool`: an observation returned by a tool.
- `assistant`: the final answer.

Open `src/agent_course/messages.py`. The `Message` class is small on purpose. Many real systems use the same idea with more metadata.

## Exercise

In `src/agent_course/agent.py`, change the system message text. Run `examples\02_run_agent.py` again and inspect `result.messages` in a debugger or temporary print.

