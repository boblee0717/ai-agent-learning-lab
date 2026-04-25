# Exercise 03 — Unit Converter Tool

Lesson: `lessons/03_tools.md`

## Goal

Build a new `UnitConverterTool` that satisfies the `Tool` protocol and plug it into a `WeatherAwareBrain`-style brain so the agent uses it without changing the loop.

The tool must support these conversions:

- `5 km to miles`
- `100 f to c` (Fahrenheit → Celsius)
- `2 hours to minutes`

## Steps

1. Open `exercises/starter/ex03_unit_converter.py`.
2. Implement `UnitConverterTool.run` and `UnitAwareBrain.decide`.
3. Run:
   ```powershell
   pytest exercises/tests/test_03_unit_converter.py -q
   ```

## Hints

- Parse with a single regex like `r"(\d+(?:\.\d+)?)\s*(\w+)\s*(?:to|in)\s*(\w+)"`.
- Round results to two decimals so equality checks are deterministic.
- Raise `ToolError` on unsupported unit pairs — that puts the failure into the trace, which is the whole point of `ToolError`.
- For the brain, route to the converter only when the input contains the substring `" to "` or `" in "` and a digit.

## Acceptance

- `UnitConverterTool().run("5 km to miles")` returns `"3.11"` (or `"3.11 miles"`, your call — assert your own choice in tests).
- `UnitConverterTool().run("100 f to c")` returns `"37.78"`.
- An agent built with `UnitAwareBrain` and `[UnitConverterTool()]` answers `"5 km to miles"` and records exactly one `unit_converter` tool call.
- Unsupported units raise `ToolError`.
