# 01: What Is An Agent?

A chatbot usually answers directly. An agent can decide to do work before answering.

The smallest useful agent has:

- A goal from the user.
- A brain that decides what to do.
- Tools it can call.
- State that records what happened.
- A final answer.

In this repo, `TeachingBrain` is not an LLM. It is a clear, deterministic substitute so you can learn the structure first.

## Exercise

Run:

```powershell
python examples\02_run_agent.py
```

Read the trace. Notice that the agent does not just answer; it decides, calls a tool, observes, then answers.

