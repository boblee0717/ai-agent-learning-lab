# 06: Replacing The Brain With An LLM

The current `TeachingBrain` uses rules. A real agent usually uses an LLM as the brain.

To replace it, keep the same shape:

```python
class LlmBrain:
    def decide(self, messages, tools):
        ...
        return Decision(...)
```

The LLM brain should receive:

- The user's goal.
- Recent messages.
- Tool names and descriptions.
- Instructions for when to answer vs call a tool.

It should return either:

- An `answer` decision.
- A `tool` decision with `tool_name` and tool input.

Keeping this interface stable lets you swap the teaching brain for a real model without rewriting the agent loop.

