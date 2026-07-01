from typing import Any

from models.tool_parameter import ToolParameter
from tools.tool import Tool


class CalculatorTool(Tool):

    def __init__(self):

        super().__init__(
            name="calculator",
            description="Evaluates mathematical expressions.",
            input_schema=[
                ToolParameter(
                    name="expression",
                    type=str,
                    description="Mathematical expression to evaluate."
                )
            ]
        )

    def execute(self, arguments: dict[str, Any]) -> Any:

        expression = arguments["expression"]

        # NOTE:
        # eval() is intentionally used here to keep this example tool simple.
        # Production systems should never evaluate untrusted user input directly.
        # A safer implementation would use Python's ast module or a dedicated
        # expression parser.
        return eval(expression)
