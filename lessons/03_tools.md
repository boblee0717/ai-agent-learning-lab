# 03: Tools

A tool is a callable capability. It can be a calculator, search engine, database query, browser action, file editor, API call, or code runner.

In this repo, every tool has:

- `name`
- `description`
- `run(tool_input)`

The agent does not need to know how the tool works internally. It only needs to know when to call it and how to use the observation.

## Exercise

Run:

```powershell
python examples\01_run_tool.py
```

Then open `examples\03_add_a_tool.py` and look at `WeatherTool`. It adds a new capability without changing the agent loop.

