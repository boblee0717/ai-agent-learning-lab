from agent_course.tools import CalculatorTool, NotesTool


def main() -> None:
    calculator = CalculatorTool()
    notes = NotesTool()

    print("Tool call: calculator")
    print(calculator.run("12 * (3 + 4)"))
    print()

    print("Tool call: notes")
    print(notes.run("What is an agent?"))


if __name__ == "__main__":
    main()

