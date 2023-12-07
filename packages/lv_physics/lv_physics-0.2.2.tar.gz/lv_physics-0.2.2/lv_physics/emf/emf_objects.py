"""
This module provides the mostly-static data objects as dataclasses which the EMF model depends on.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, OrderedDict, Union

import numpy as np
import numpy.typing as npt
from dataclasses_json import dataclass_json

from lv_physics.core.ohl_objects import Conductor, Sensor
from lv_physics.core.rotations import apply_rotation, extrinsic_rotation_matrix
from lv_physics.utils.dataclass_helpers import datetime_field, datetime_zero_factory


# ----------------------------------------------------------------------------------------------------------------------


@dataclass_json
@dataclass(kw_only=True)
class EMFSensor(Sensor):
    """
    Represents an EMF sensor object and its mostly-static masterdata information required for an EMF model
    calculation.

    :param model_group_id: a unique integer identifier for the EMFModelGroup to which the sensor belongs
    :param phase_adjustment: a float representing the adjustment to make to all phase angle measurements made by the
                             actual sensor; can correct for skews in E-field-referenced magnetic phase angles
    """

    model_group_id: int
    phase_adjustment: float = 0.0

    def rotate_phasor_vector(self, phasor_vector: npt.NDArray[np.complex_]):
        """
        Takes an EMFMeasurement.phasor_vector, as measured in the sensor frame, and returns a rotated phasor vector as
        would be measured in the span frame.  This should always be called on EMFMeasurement.phasor_vectors before they
        are used in any EMF model calculations.

        :param measurement: the EMFMeasurement object for which to form rotated phasor vectors
        :returns: a rotated phasor Vector representing the EMFMeasurement in the overall model group coordinate frame
        """
        ext_rot_matrix = extrinsic_rotation_matrix(
            angles=self.ext_angles,
            axes=np.array([0, 1, 2], dtype=np.int_),  # always X, Y, & Z axes
            order=self.rotation_order,
        )

        return apply_rotation(ext_rot_matrix, phasor_vector)


@dataclass_json
@dataclass
class EMFMeasurement:
    """
    Represents a single measurement from an EMFSensor.

    :param id: a unique integer identifier for the measurement
    :param sensor_id: a unique integer identifier for the sensor the measurement came from
    :param e: the electric field magnitude of the measurement
    :param bx: the magnetic field magnitude of the measurement from the sensor's X coil
    :param by: the magnetic field magnitude of the measurement from the sensor's Y coil
    :param bz: the magnetic field magnitude of the measurement from the sensor's Z coil
    :param phasex: the phase angle between the bx and e waveforms in radians
    :param phasey: the phase angle between the by and e waveforms in radians
    :param phasez: the phase angle between the bz and e waveforms in radians
    :param dttm: datetime of the measurement
    :param create_dttm: datetime the measurement was ingested by data pipeline
    """

    id: str
    sensor_id: int
    e: float
    bx: float
    by: float
    bz: float
    phasex: float
    phasey: float
    phasez: float
    dttm: datetime = datetime_field(default_factory=datetime_zero_factory)
    create_dttm: datetime = datetime_field(default_factory=datetime_zero_factory)

    @property
    def phasor_vector(self):
        return np.array(
            [
                self.bx * np.exp(1.0j * self.phasex),
                self.by * np.exp(1.0j * self.phasey),
                self.bz * np.exp(1.0j * self.phasez),
            ],
            dtype=np.complex_,
        )


@dataclass_json
@dataclass(kw_only=True)
class EMFConductor(Conductor):
    """
    Represents a conductor in an EMFModelGroup context, with all masterdata information required for an EMF model
    calculation.
    NOTE: a conductor is never considered to be present in multiple spans in EMFModelGroup calculations, so this object
          is most similar to a record in conductor_span table in masterdata DB at time of writing 2022-04-24

    :param id: a unique integer identifier for the conductor
    :param span_id: a unique integer identifier for the span this conductor is in
    :param phase: the phase of this conductor in its circuit: A, B, or C
    """

    id: int
    span_id: int
    phase: str


@dataclass_json
@dataclass
class EMFCircuitSpan:
    """
    Represents a circuit's presence in a span for an EMFModelGroup context; basically just the sub-grouping of the 3
    conductors for the circuit in this single span.

    :param id: a unique integer identifier for the span the circuit is present in
    :param circuit_id: a unique integer identifier for the circuit
    :param conductors: a len-3 Dict of EMFConductor's, keyed by their ids
    """

    id: int
    circuit_id: int
    conductors: Dict[int, EMFConductor]


@dataclass_json
@dataclass
class EMFCircuit:
    """
    Represents a circuit in an EMFModelGroup context; contains all the masterdata required to simulate a circuit's
    conductor locations, phases, and E-field profiles.

    :param id: a unique integer identifier for the circuit
    :param model_group_id: a unique integer identifier for the EMFModelGroup to which the circuit belongs
    :param spans: a len-N Dict of CircuitSpan's, keyed by their ids
    :param voltage: a float representing the line-to-line voltage of the circuit in volts (V)
    """

    id: int
    model_group_id: int
    spans: Dict[int, EMFCircuitSpan]
    voltage: float = 100000.0


@dataclass_json
@dataclass
class EMFModelGroup:
    """
    Represents a collection of all EMFSensors and Circuits (and their related objects) required to simulate the
    coefficient matrix, or "h-matrix", that is used in a single EMF -> loading model calculation.

    :param id: a unique integer identifier for the EMFModelGroup
    :param sensors: a len-N Dict of EMFSensor's, keyed by their ids
    :param circuits: a len-N Dict of Circuit's, keyed by their ids
    """

    id: int
    sensors: OrderedDict[int, EMFSensor]
    circuits: OrderedDict[int, EMFCircuit]


@dataclass_json
@dataclass
class EMFModelGroupMeasurement:
    """
    Represents a collection of one EMFMeasurement from each EMFSensor in an EMFModelGroup, ~synchronized in time. One
    of these objects together w/ the corresponding EMFModelGroup's "h-matrix" comprise the inputs to a single EMF ->
    loading model calculation.

    :param model_group_id: a unique integer identifier for the corresponding EMFModelGroup
    :param measurements: a Dict of EMFMeasurement's keyed by the corresponding EMFSensor ids
    """

    model_group_id: int
    measurements: OrderedDict[int, EMFMeasurement]
    dttm: datetime = datetime_field(default_factory=datetime_zero_factory)


@dataclass_json
@dataclass
class EMFModelResult:
    """
    Represents the results of a single calculation of the EMF model.

    :param model_group_id: a unique integer identifier for the corresponding EMFModelGroup
    :param loading_by_circ_id: a Dict of loading values in amps keyed by the corresponding Circuit's id
    """

    model_group_id: int
    dttm: datetime
    loading_by_circ_id: Dict[int, Union[float, complex]]
