from dataclasses import dataclass


@dataclass(frozen=True)
class CurrentWeather:
    location: str
    temperature: float
    condition: str
