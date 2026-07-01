from tools.tool import Tool


class ToolRegistry:

    def __init__(self):

        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:

        if tool.name in self._tools:
            raise ValueError(
                f"Tool '{tool.name}' is already registered."
            )

        self._tools[tool.name] = tool

    def get(self, tool_name: str) -> Tool:

        if tool_name not in self._tools:
            raise ValueError(
                f"Unknown tool '{tool_name}'."
            )

        return self._tools[tool_name]

    def list_tools(self) -> list[Tool]:

        return list(self._tools.values())
