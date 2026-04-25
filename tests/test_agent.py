import unittest

from agent_course import Agent


class AgentTests(unittest.TestCase):
    def test_agent_can_use_calculator(self) -> None:
        result = Agent().run("What is 8 * 7?")

        self.assertEqual(result.answer, "Here is what I found: 56")
        self.assertEqual(result.tool_calls[0].name, "calculator")

    def test_agent_can_use_notes(self) -> None:
        result = Agent().run("Explain agent memory")

        self.assertIn("Memory is information", result.answer)
        self.assertEqual(result.tool_calls[0].name, "notes")


if __name__ == "__main__":
    unittest.main()

