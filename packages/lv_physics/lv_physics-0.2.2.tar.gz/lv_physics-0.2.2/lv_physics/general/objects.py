from dataclasses import dataclass, field
from typing import Dict, Optional

from dataclasses_json import dataclass_json
from numpy import float_
from numpy.typing import NDArray

from lv_physics.core.dynamic_objects import DynamicConductor
from lv_physics.core.ohl_objects import Sensor
from lv_physics.core.scene_objects import Geography
from lv_physics.lidar.objects import ConductorFit


@dataclass_json
@dataclass
class CircuitSpan:
    id: int
    name: str
    conductors: Dict[int, DynamicConductor]
    geography: Geography

    sensors: Dict[int, Sensor] = field(default_factory=dict)
    scans: Optional[Dict[int, NDArray[float_]]] = None
    fits: Optional[Dict[int, ConductorFit]] = None

    @property
    def conductor_ids(self):
        return [cond_id for cond_id in self.conductors.keys()]

    @property
    def sensor_ids(self):
        return [sensor_id for sensor_id in self.sensors.keys()]


@dataclass_json
@dataclass
class Span:
    id: int
    name: str
    circuits: Dict[int, CircuitSpan]

    @property
    def circuit_ids(self):
        return [circ_id for circ_id in self.circuits.keys()]
