# Glossary

- **Agent**: a system that can decide actions while pursuing a goal.
- **Brain**: the decision maker. In real systems this is usually an LLM. In this repo it is any object satisfying the `Brain` protocol.
- **Tool**: a callable capability outside the brain. Has `name`, `description`, and `run(input) -> str`.
- **Decision**: the brain's next move. Either `answer` or call a `tool`. Can carry `reasoning` for the trace.
- **Observation**: the output returned by a tool. Errors are observations too — that is what makes self-correction possible.
- **Trace**: the structured record of `goal`, `thought`, `tool_call`, `observation`, `answer`, `error`, and `limit` events.
- **Memory**: information carried across steps (short-term, via `messages`) or runs (long-term, via the `Memory` protocol).
- **Guardrail**: a rule or check that keeps the agent inside intended behavior. Examples in this repo: calculator input length cap, exponent cap, step limit, unknown-tool handling.
- **Step limit**: hard cap on loop iterations. Prevents infinite tool/observation cycles.
