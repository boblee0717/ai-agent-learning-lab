# 06: Replacing The Brain With An LLM

The current `TeachingBrain` uses rules. A real agent usually uses an LLM as the brain.

To replace it, keep the same shape:

```python
class LlmBrain:
    def decide(self, messages, tools):
        ...
        return Decision(kind="answer" | "tool", content="...", tool_name=..., reasoning="...")
```

The LLM brain receives:

- The user's goal.
- Recent messages.
- Tool names and descriptions.
- Instructions for when to answer vs call a tool.

It returns either:

- An `answer` decision.
- A `tool` decision with `tool_name` and tool input.

Keeping this interface stable lets you swap the brain without rewriting the agent loop.

## Two Reference Implementations

`src/agent_course/brains.py` ships two examples to compare against:

- `EchoLlmBrain` builds the **real LLM-style prompt** (system instructions + tool catalogue + history) but answers locally. Use it to practise prompt construction without paying for tokens.
- `OpenAiBrain` is a thin wrapper around the official `openai` SDK. It is intentionally tiny: a single chat completion that returns JSON, which we parse into a `Decision`.

## Try It

```powershell
# Echo brain: prints the prompt that would be sent to a real LLM, then
# answers locally so the agent loop is fully deterministic.
python examples\05_llm_brain.py

# Real OpenAI call (optional). Install the extra and provide a key first.
pip install -e ".[llm]"
$env:OPENAI_API_KEY = "sk-..."
$env:USE_OPENAI = "1"
python examples\05_llm_brain.py
```

## Exercise

1. Read the prompt printed by `EchoLlmBrain`. Could you predict what an LLM would do given that prompt?
2. In `OpenAiBrain.decide`, switch to the `tools` parameter of the OpenAI API (function calling) instead of the JSON-in-content trick. Notice how the agent loop does not change.
