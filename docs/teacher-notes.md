# Teacher Notes

This project is designed to teach the shape of agents before adding complexity.

Pay attention to three files:

- `messages.py`: how the agent stores context.
- `tools.py`: how external capabilities are wrapped.
- `agent.py`: how decisions become actions and observations.

The most important idea is separation:

- The brain decides.
- The tools do work.
- The loop coordinates.
- The trace explains.

Once that separation feels natural, add a real model provider as a new brain implementation.

