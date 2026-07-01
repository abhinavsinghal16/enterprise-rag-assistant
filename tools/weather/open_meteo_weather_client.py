import requests

from models.coordinates import Coordinates
from models.current_weather import CurrentWeather
from tools.weather.weather_client import WeatherClient


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"

WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


class OpenMeteoWeatherClient(WeatherClient):

    def get_current_weather(
        self,
        location: str
    ) -> CurrentWeather:

        coordinates = self._geocode(location)

        return self._fetch_weather(
            location,
            coordinates
        )

    def _geocode(
        self,
        location: str
    ) -> Coordinates:

        response = requests.get(
            GEOCODING_URL,
            params={
                "name": location,
                "count": 1
            }
        )

        response.raise_for_status()

        data = response.json()

        results = data.get("results")

        if not results:
            raise ValueError(
                f"Unknown location '{location}'."
            )

        result = results[0]

        return Coordinates(
            latitude=result["latitude"],
            longitude=result["longitude"]
        )

    def _fetch_weather(
        self,
        location: str,
        coordinates: Coordinates
    ) -> CurrentWeather:

        response = requests.get(
            WEATHER_URL,
            params={
                "latitude": coordinates.latitude,
                "longitude": coordinates.longitude,
                "current": "temperature_2m,weather_code"
            }
        )

        response.raise_for_status()

        data = response.json()

        current = data["current"]

        return CurrentWeather(
            location=location,
            temperature=current["temperature_2m"],
            condition=self._weather_code_to_condition(
                current["weather_code"]
            )
        )

    def _weather_code_to_condition(
        self,
        weather_code: int
    ) -> str:

        weather_codes = {
            0: "Clear Sky",
            1: "Mainly Clear",
            2: "Partly Cloudy",
            3: "Overcast",
            45: "Fog",
            48: "Depositing Rime Fog",
            51: "Light Drizzle",
            53: "Moderate Drizzle",
            55: "Dense Drizzle",
            61: "Slight Rain",
            63: "Moderate Rain",
            65: "Heavy Rain",
            71: "Slight Snow",
            73: "Moderate Snow",
            75: "Heavy Snow",
            80: "Rain Showers",
            95: "Thunderstorm"
        }

        return weather_codes.get(
            weather_code,
            "Unknown"
        )
