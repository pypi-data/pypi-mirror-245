import json
import os
from dataclasses import replace
from datetime import datetime

import numpy as np
from numpy import ndarray

from lv_physics import LVP_DATA_PATH
from lv_physics.emf.emf_const_objects import EMF_MEASUREMENT_1, EMF_SENSOR_1
from lv_physics.emf.emf_objects import (
    EMFCircuit,
    EMFCircuitSpan,
    EMFConductor,
    EMFMeasurement,
    EMFModelGroup,
    EMFModelGroupMeasurement,
    EMFSensor,
)


EMF_TEST_OBJECTS_PATH = os.path.join(LVP_DATA_PATH, "emf_test_objects")


# ----------------------------------------------------------------------------------------------------------------------


def test_phasor_vector_property():
    """
    Tests the phasor vector from an emf measurement object.
    """
    phasor_vector_should_be = np.array(
        [
            10.0 * np.exp(1.0j * np.pi / 4),
            0.0 * np.exp(1.0j * 0.0),
            10.0 * np.exp(1.0j * np.pi / 4),
        ],
        dtype=np.complex_,
    )

    assert np.allclose(EMF_MEASUREMENT_1.phasor_vector, phasor_vector_should_be)


def test_rotate_phasor_vector_method():
    """
    Tests the rotate phasor vector method of an EMFSensor.
    """
    # create an emf measurement that will have unique values after rotations
    test_emf_measurement = replace(EMF_MEASUREMENT_1, bx=1.0, by=2.0, bz=3.0)

    rotated_sensor_1 = replace(EMF_SENSOR_1, ext_angles=np.array([0.0, 0.0, np.pi]))
    rotated_phasor_vector_1 = np.array(
        [
            -test_emf_measurement.phasor_vector[0],  # a bx in the sensor frame is the same as a -bx in the span frame
            -test_emf_measurement.phasor_vector[1],
            +test_emf_measurement.phasor_vector[2],
        ],
        dtype=np.complex_,
    )
    assert np.allclose(
        rotated_phasor_vector_1,
        rotated_sensor_1.rotate_phasor_vector(test_emf_measurement.phasor_vector),
    )

    rotated_sensor_2 = replace(EMF_SENSOR_1, ext_angles=np.array([0.0, 0.0, np.pi / 2]))
    rotated_phasor_vector_2 = np.array(
        [
            -test_emf_measurement.phasor_vector[1],  # a by as in the sensor is the same as a -bx in the span frame
            +test_emf_measurement.phasor_vector[0],
            +test_emf_measurement.phasor_vector[2],
        ],
        dtype=np.complex_,
    )
    assert np.allclose(
        rotated_phasor_vector_2,
        rotated_sensor_2.rotate_phasor_vector(test_emf_measurement.phasor_vector),
    )

    rotated_sensor_3 = replace(EMF_SENSOR_1, ext_angles=np.array([0.0, np.pi / 2, np.pi / 2]))
    rotated_phasor_vector_3 = np.array(
        [
            +test_emf_measurement.phasor_vector[2],  # a bz in the sensor frame is unchanged after the first rotation
            +test_emf_measurement.phasor_vector[0],  # around the z-axis, and becomes bx after the second rotation
            +test_emf_measurement.phasor_vector[1],  # around the y-axis.
        ],
        dtype=np.complex_,
    )
    assert np.allclose(
        rotated_phasor_vector_3,
        rotated_sensor_3.rotate_phasor_vector(test_emf_measurement.phasor_vector),
    )


# ----------------------------------------------------------------------------------------------------------------------


def test_emf_sensor():
    """
    Tests the emf sensor dataclass-json object.
    """
    filename = os.path.join(EMF_TEST_OBJECTS_PATH, "emf_sensor_1.json")
    with open(filename, "r") as fp:
        emf_sensor_1 = EMFSensor.from_dict(json.load(fp))

    assert isinstance(emf_sensor_1.position, ndarray)
    assert isinstance(emf_sensor_1.ext_angles, ndarray)
    assert isinstance(emf_sensor_1.rotation_order, ndarray)


def test_emf_conductor():
    """
    Tests the emf conductor dataclass-json object.
    """
    filename = os.path.join(EMF_TEST_OBJECTS_PATH, "emf_conductor_1.json")
    with open(filename, "r") as fp:
        emf_conductor_1 = EMFConductor.from_dict(json.load(fp))

    assert isinstance(emf_conductor_1.connects[0], ndarray)
    assert isinstance(emf_conductor_1.connects[1], ndarray)


def test_circuit_span():
    """
    Tests the emf circuit span dataclass-json object.
    """
    filename = os.path.join(EMF_TEST_OBJECTS_PATH, "emf_circuit_span_1.json")
    with open(filename, "r") as fp:
        EMFCircuitSpan.from_dict(json.load(fp))


def test_circuit():
    """
    Tests the emf circuit dataclass-json object.
    """
    filename = os.path.join(EMF_TEST_OBJECTS_PATH, "emf_circuit_1.json")
    with open(filename, "r") as fp:
        EMFCircuit.from_dict(json.load(fp))


def test_emf_model_group():
    """
    Tests the emf model group dataclass-json object.
    """
    filename = os.path.join(EMF_TEST_OBJECTS_PATH, "emf_model_group_1.json")
    with open(filename, "r") as fp:
        EMFModelGroup.from_dict(json.load(fp))


def test_emf_measurement():
    """
    Tests the emf sensor dataclass-json object.
    """
    filename = os.path.join(EMF_TEST_OBJECTS_PATH, "emf_measurement_1.json")
    with open(filename, "r") as fp:
        emf_measurement_1 = EMFMeasurement.from_dict(json.load(fp))

    assert isinstance(emf_measurement_1.dttm, datetime)
    assert isinstance(emf_measurement_1.create_dttm, datetime)


def test_emf_model_group_measurement():
    """
    Tests the emf sensor dataclass-json object.
    """
    filename = os.path.join(EMF_TEST_OBJECTS_PATH, "emf_model_group_measurement_1.json")
    with open(filename, "r") as fp:
        EMFModelGroupMeasurement.from_dict(json.load(fp))
