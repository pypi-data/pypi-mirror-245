from dataclasses import dataclass

from dataclasses_json import dataclass_json
from numpy import nan


@dataclass_json
@dataclass
class ConductorFit:
    alpha: float = nan
    beta: float = nan
    gamma: float = nan
    curvature: float = nan
    error: float = nan
