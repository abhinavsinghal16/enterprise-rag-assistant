from typing import Any

from models.tool_parameter import ToolParameter
from tools.tool import Tool
from tools.weather.weather_client import WeatherClient


class CurrentWeatherTool(Tool):

    def __init__(
        self,
        weather_client: WeatherClient
    ):
        super().__init__(
            name="current_weather",
            description="Gets the current weather for a location.",
            input_schema=[
                ToolParameter(
                    name="location",
                    description="The city or location name.",
                    type=str,
                    required=True
                )
            ]
        )

        self.weather_client = weather_client

    def execute(
        self,
        arguments: dict[str, Any]
    ):

        location = arguments["location"]

        return self.weather_client.get_current_weather(
            location
        )
