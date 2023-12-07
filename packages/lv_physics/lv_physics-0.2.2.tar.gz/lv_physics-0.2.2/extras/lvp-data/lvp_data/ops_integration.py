import os
from dataclasses import dataclass
from datetime import datetime

import numpy as np
from dataclasses_json import dataclass_json
from numpy import array
from numpy.typing import NDArray

from lv_physics.utils.dataclass_helpers import datetime_field


@dataclass_json
@dataclass
class Weather:
    dttm: datetime = datetime_field()
    humidity: float
    precipitation_mm: float
    solar_intensity: float
    sky: float
    temperature: float
    wind_dir: float
    wind_speed: float


def interp_weather_series(dttms: NDArray[datetime], weather_series: NDArray[Weather]) -> NDArray[Weather]:

    timestamp = array([dttm.timestamp() for dttm in dttms])

    # get weather series values
    ws_timestamp = array([row.dttm.timestamp() for row in weather_series])
    ws_humidity = array([row.humidity for row in weather_series])
    ws_precipitation_mm = array([row.precipitation_mm for row in weather_series])
    ws_solar_intensity = array([row.solar_intensity for row in weather_series])
    ws_sky = array([row.sky for row in weather_series])
    ws_temperature = array([row.temperature for row in weather_series])
    ws_wind_dir = array([row.wind_dir for row in weather_series])
    ws_wind_speed = array([row.wind_speed for row in weather_series])

    # interpolate each value
    new_precipitation_mm = np.interp(timestamp, ws_timestamp, ws_precipitation_mm)
    new_humidity = np.interp(timestamp, ws_timestamp, ws_humidity)
    new_temperature = np.interp(timestamp, ws_timestamp, ws_temperature)
    new_solar_intensity = np.interp(timestamp, ws_timestamp, ws_solar_intensity)
    new_sky = np.interp(timestamp, ws_timestamp, ws_sky)
    new_wind_dir = np.interp(timestamp, ws_timestamp, ws_wind_dir)
    new_wind_speed = np.interp(timestamp, ws_timestamp, ws_wind_speed)

    return array([
        Weather(
            dttm=dttms[m],
            humidity=new_humidity[m],
            precipitation_mm=new_precipitation_mm[m],
            solar_intensity=new_solar_intensity[m],
            sky=new_sky[m],
            temperature=new_temperature[m],
            wind_dir=np.degrees(np.radians(new_wind_dir[m])),
            wind_speed=new_wind_speed[m],
        )
        for m in range(len(timestamp))
    ])


def pull_weather_series(
    site_group_id: int, start: datetime, end: datetime, interp_on: NDArray[datetime] = None
) -> NDArray[Weather]:

    os.environ["ENV"] = "dev"
    from ops.weather.singletons import weather_service

    ops_weather_series = weather_service.pull_site_group_weather(
        site_group_id, start, end, legacy_format=False
    )

    weather_series = array([
        Weather(
            dttm=row.datetime_iso,
            humidity=row.humidity,
            precipitation_mm=row.precip_mm,
            temperature=row.temp_c,
            solar_intensity=row.solrad_wm2,
            sky=row.sky,
            wind_dir=row.wind_dir_deg,
            wind_speed=row.wind_speed_kph * 1000 / 3600,  # [k/h] -> [m/s]
        )
        for row in ops_weather_series
    ])

    if interp_on is not None:
        return interp_weather_series(interp_on, weather_series)

    else:
        return weather_series
