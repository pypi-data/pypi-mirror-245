from dataclasses import dataclass

from dataclasses_json import dataclass_json
from numpy import nan


@dataclass_json
@dataclass
class Air:
    """
    Describes the properties of air, including conductivity, density, wind direction, speed, temperature, and viscosity.

    Attributes:
        conductivity: Thermal conductivity of the air.
        density: Density of the air.
        heading: Wind direction in degrees.
        speed: Wind speed.
        temperature: Temperature of the air.
        viscosity: Viscosity of the air.
    """

    conductivity: float = nan
    density: float = nan
    heading: float = nan
    speed: float = nan
    temperature: float = nan
    viscosity: float = nan


@dataclass_json
@dataclass
class Geography:
    """
    Specifies geographic information including elevation, heading, latitude, and longitude.

    Attributes:
        elevation: Elevation above sea level.
        heading: Geographic heading in degrees.
        latitude: Latitude coordinate.
        longitude: Longitude coordinate.
    """

    elevation: float = 9.0
    heading: float = 90.0
    latitude: float = 38.757540
    longitude: float = 30.538700


@dataclass_json
@dataclass
class Solar:
    """
    Represents solar parameters including altitude, azimuth, solar hour, and intensity.

    Attributes:
        altitude: Solar altitude angle.
        azimuth: Solar azimuth angle.
        hour: Solar hour of the day.
        intensity: Solar radiation intensity.
    """

    altitude: float = 0.0
    azimuth: float = 0.0
    hour: float = 0.0
    intensity: float = 0.0
