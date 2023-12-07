"""
Defines EMF const. objects used for testing and scripts.
"""
from collections import OrderedDict
from dataclasses import replace
from datetime import datetime, timezone

import numpy as np
from numpy import array, float_

from lv_physics.core.ohl_objects import ConductorShape, Insulator
from lv_physics.emf.emf_objects import (
    EMFCircuit,
    EMFCircuitSpan,
    EMFConductor,
    EMFMeasurement,
    EMFModelGroup,
    EMFModelGroupMeasurement,
    EMFSensor,
)


# ---- TYPICAL HORIZONTAL EXAMPLE ---- #


EMF_SENSOR_1 = EMFSensor(
    id=1,
    model_group_id=1,
    position=array([0.0, 0.0, 0.0], dtype=float_),
    ext_angles=array([0.0, 0.0, 0.0], float_),
)

EMF_MEASUREMENT_1 = EMFMeasurement(
    id="123abc",
    sensor_id=1,
    e=10.0,
    bx=10.0,
    by=0.0,
    bz=10.0,
    phasex=np.pi / 4,
    phasey=0.0,
    phasez=np.pi / 4,
    dttm=datetime(1970, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
    create_dttm=datetime(1970, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
)

EMF_CONDUCTOR_1 = EMFConductor(
    id=1,
    span_id=1,
    phase="B",
    shape=ConductorShape(curvature=500.0),
    insulators=[
        Insulator(connect=array([-3.0, 0.0, 15.0])),
        Insulator(connect=array([-3.0, 100.0, 15.0])),
    ],
)

EMF_CONDUCTOR_2 = EMFConductor(
    id=2,
    span_id=1,
    phase="A",
    shape=ConductorShape(curvature=500.0),
    insulators=[
        Insulator(connect=array([0.0, 0.0, 15.0])),
        Insulator(connect=array([0.0, 100.0, 15.0])),
    ],
)

EMF_CONDUCTOR_3 = EMFConductor(
    id=3,
    span_id=1,
    phase="C",
    shape=ConductorShape(curvature=500.0),
    insulators=[
        Insulator(connect=array([3.0, 0.0, 15.0])),
        Insulator(connect=array([3.0, 100.0, 15.0])),
    ],
)

EMF_CONDUCTOR_4 = replace(
    EMF_CONDUCTOR_1,
    id=4,
    insulators=[
        Insulator(connect=array([-3.0, -100.0, 15.0])),
        Insulator(connect=EMF_CONDUCTOR_1.connects[0]),
    ],
)

EMF_CONDUCTOR_5 = replace(
    EMF_CONDUCTOR_2,
    id=5,
    insulators=[
        Insulator(connect=array([0.0, -100.0, 15.0])),
        Insulator(connect=EMF_CONDUCTOR_2.connects[0]),
    ],
)

EMF_CONDUCTOR_6 = replace(
    EMF_CONDUCTOR_3,
    id=6,
    insulators=[
        Insulator(connect=array([3.0, -100.0, 15.0])),
        Insulator(connect=EMF_CONDUCTOR_3.connects[0]),
    ],
)

EMF_CIRCUIT_SPAN_1 = EMFCircuitSpan(
    id=1,
    circuit_id=1,
    conductors={1: EMF_CONDUCTOR_1, 2: EMF_CONDUCTOR_2, 3: EMF_CONDUCTOR_3},
)

EMF_CIRCUIT_SPAN_2 = EMFCircuitSpan(
    id=2,
    circuit_id=1,
    conductors={4: EMF_CONDUCTOR_4, 5: EMF_CONDUCTOR_5, 6: EMF_CONDUCTOR_6},
)

EMF_CIRCUIT_1 = EMFCircuit(
    id=1,
    model_group_id=1,
    spans={1: EMF_CIRCUIT_SPAN_1, 2: EMF_CIRCUIT_SPAN_2},
    voltage=100000.0,
)

EMF_MODEL_GROUP_1 = EMFModelGroup(
    id=1,
    sensors=OrderedDict({1: EMF_SENSOR_1}),
    circuits=OrderedDict({1: EMF_CIRCUIT_1}),
)

EMF_MODEL_GROUP_MEASUREMENT_1 = EMFModelGroupMeasurement(
    model_group_id=1,
    dttm=datetime(1970, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
    measurements=OrderedDict({1: EMF_MEASUREMENT_1}),
)


if __name__ == "__main__":
    import json
    import os

    data_path = "data/emf_test_objects/"

    with open(os.path.join(data_path, "emf_conductor_1.json"), "w") as fp:
        json.dump(EMF_CONDUCTOR_1.to_dict(), fp, indent=2)

    with open(os.path.join(data_path, "emf_circuit_1.json"), "w") as fp:
        json.dump(EMF_CIRCUIT_1.to_dict(), fp, indent=2)

    with open(os.path.join(data_path, "emf_circuit_span_1.json"), "w") as fp:
        json.dump(EMF_CIRCUIT_SPAN_1.to_dict(), fp, indent=2)

    with open(os.path.join(data_path, "emf_sensor_1.json"), "w") as fp:
        json.dump(EMF_SENSOR_1.to_dict(), fp, indent=2)

    with open(os.path.join(data_path, "emf_measurement_1.json"), "w") as fp:
        json.dump(EMF_MEASUREMENT_1.to_dict(), fp, indent=2)

    with open(os.path.join(data_path, "emf_model_group_1.json"), "w") as fp:
        json.dump(EMF_MODEL_GROUP_1.to_dict(), fp, indent=2)

    with open(os.path.join(data_path, "emf_model_group_measurement_1.json"), "w") as fp:
        json.dump(EMF_MODEL_GROUP_MEASUREMENT_1.to_dict(), fp, indent=2)
