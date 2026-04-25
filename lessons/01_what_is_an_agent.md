# 01: What Is An Agent?

A chatbot usually answers directly. An agent can decide to do work before answering.

## Chatbot vs Agent

```text
Chatbot
  user -> model -> answer

Agent
  user -> brain -> decide
                      |--> answer  (done)
                      \--> tool -> observation -> brain -> ...
```

The smallest useful agent has:

- A goal from the user.
- A brain that decides what to do (and *why*, via `reasoning`).
- Tools it can call.
- State that records what happened (`messages` + structured `Trace`).
- A final answer.

In this repo, `TeachingBrain` is not an LLM. It is a clear, deterministic substitute so you can learn the structure first. Later lessons swap it for `EchoLlmBrain` (a real prompt with no network) and `OpenAiBrain` (the real thing).

## Exercise

Run (works on macOS, Linux, and Windows):

```bash
python -m agent_course "What is 8 * 7?"
python -m agent_course "What is 1 / 0?"
```

Read the trace. Notice that the agent does not just answer; it decides, calls a tool, observes (errors included), then answers.
