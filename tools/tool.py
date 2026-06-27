from abc import ABC, abstractmethod
from typing import Any

from models.tool_parameter import ToolParameter


class Tool(ABC):

    def __init__(
        self,
        name: str,
        description: str,
        input_schema: list[ToolParameter]
    ):
        self.name = name
        self.description = description
        self.input_schema = input_schema

    def run(self, arguments: dict[str, Any]) -> Any:

        self.validate_input(arguments)

        return self.execute(arguments)

    def validate_input(self, arguments: dict[str, Any]) -> None:

        for parameter in self.input_schema:

            if parameter.required and parameter.name not in arguments:
                raise ValueError(
                    f"Missing required parameter '{parameter.name}'."
                )

            if parameter.name not in arguments:
                continue

            value = arguments[parameter.name]

            if not isinstance(value, parameter.type):
                raise TypeError(
                    f"Parameter '{parameter.name}' must be of type "
                    f"{parameter.type.__name__}."
                )

    @abstractmethod
    def execute(self, arguments: dict[str, Any]) -> Any:
        """
        Execute the tool.
        """
        pass
