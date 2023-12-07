"""
Provides object definitions used in DLR calculations.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

import numpy as np
from numpy import float_, nan
from numpy.typing import NDArray

from lv_physics.core.dynamic_objects import DynamicConductor
from lv_physics.core.scene_objects import Air, Geography, Solar


@dataclass
class Heat:
    convective: float = nan
    radiative: float = nan
    resistive: float = nan
    solar: float = nan

    @property
    def net(self):
        return self.resistive + self.solar + self.convective + self.radiative


@dataclass
class DLR:
    heat: Heat = field(default_factory=Heat)
    loading: float = nan
    thermalization_time: float = nan


@dataclass
class DLRMCSigmas:
    air_speed: float = 0.0
    air_temperature: float = 0.0
    conductor_absorptivity: float = 0.0
    conductor_emissivity: float = 0.0
    conductor_loading: float = 0.0
    conductor_temperature: float = 0.0
    solar_intensity: float = 0.0


@dataclass
class DLRMCParams:
    n_flops: int
    sigmas: DLRMCSigmas
    method: str = "cigre"


@dataclass
class Distribution:
    values: NDArray[float_]

    def __getitem__(self, index: int) -> float:
        """Retrieve the value at the specified index from the distribution."""
        return self.values[index]

    @property
    def std(self) -> float:
        """Calculate and return the standard deviation of the distribution."""
        return np.nanstd(self.values)

    @property
    def mean(self) -> float:
        """Calculate and return the mean of the distribution."""
        return np.nanmean(self.values)

    @property
    def median(self) -> float:
        """Calculate and return the median of the distribution."""
        return np.nanmedian(self.values)

    def percentile(self, p: float) -> float:
        """Calculate and return the specified percentile of the distribution."""
        return np.nanpercentile(self.values, p)


@dataclass
class DLRMCDistributions:
    air_speed: Distribution
    air_temperature: Distribution
    conductor_temperature: Distribution
    conductor_temperature_ss: Distribution
    q_convective: Distribution
    q_radiative: Distribution
    q_resistive: Distribution
    q_solar: Distribution
    q_convective_rating: Distribution
    q_radiative_rating: Distribution
    q_resistive_rating: Distribution
    q_solar_rating: Distribution
    rating: Distribution


@dataclass
class DLRModelGroup:
    air: Air
    conductor: DynamicConductor
    geography: Geography
    solar: Solar
    dttm: Optional[datetime] = None
    dlr: Optional[DLR] = None
    heat: Optional[Heat] = None
