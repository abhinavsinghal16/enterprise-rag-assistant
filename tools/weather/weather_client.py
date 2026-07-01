from abc import ABC, abstractmethod

from models.current_weather import CurrentWeather


class WeatherClient(ABC):

    @abstractmethod
    def get_current_weather(
        self,
        location: str
    ) -> CurrentWeather:
        """
        Retrieve the current weather for a location.
        """
        pass
