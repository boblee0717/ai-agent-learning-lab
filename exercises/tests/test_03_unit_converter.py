import pytest
from starter.ex03_unit_converter import UnitConverterTool, build_agent

from agent_course import ToolError


class TestUnitConverterTool:
    def test_km_to_miles(self) -> None:
        out = UnitConverterTool().run("5 km to miles")
        assert "3.11" in out

    def test_fahrenheit_to_celsius(self) -> None:
        out = UnitConverterTool().run("100 f to c")
        assert "37.78" in out

    def test_hours_to_minutes(self) -> None:
        out = UnitConverterTool().run("2 hours to minutes")
        assert "120" in out

    def test_unsupported_units_raise_tool_error(self) -> None:
        with pytest.raises(ToolError):
            UnitConverterTool().run("5 km to seconds")

    def test_unparseable_input_raises_tool_error(self) -> None:
        with pytest.raises(ToolError):
            UnitConverterTool().run("convert please")


class TestAgentIntegration:
    def test_agent_routes_to_unit_converter(self) -> None:
        agent = build_agent()
        result = agent.run("5 km to miles")
        assert result.tool_calls and result.tool_calls[0].name == "unit_converter"
        assert "3.11" in result.answer

    def test_agent_handles_failed_conversion_gracefully(self) -> None:
        agent = build_agent()
        result = agent.run("5 km to seconds")
        # Tool error should be captured as observation; agent should not crash.
        assert result.tool_calls and result.tool_calls[0].error is True
