"""
This module provides the functions used with the emf_objects module dataclasses to produce a physics model of the
loading of 3-phase circuits given EMF measurements by sensors near those circuits.
"""
from enum import Enum, unique
from typing import Dict, Optional

import numpy as np
import numpy.typing as npt
from scipy.linalg import lstsq

from lv_physics.core.catenaries import gen_catenary_3d
from lv_physics.core.vectors import cross, mag
from lv_physics.emf.emf_objects import (
    EMFCircuit,
    EMFModelGroup,
    EMFModelGroupMeasurement,
    EMFModelResult,
)


# ----------------------------------------------------------------------------------------------------------------------


NUM_CATENARY_POINTS = 1000


@unique
class Phase(Enum):
    A = 0.0 * np.pi / 180.0
    B = -120.0 * np.pi / 180.0
    C = -240.0 * np.pi / 180.0


def stitch_conductor_phases(circuit: EMFCircuit) -> Dict[str, npt.NDArray[np.float_]]:
    """
    Takes the EMFCircuitSpan and lower EMFConductors from the EMFCircuit object, generates the catenary shapes for each
    EMFConductor, and then "stitches" together the same-phase conductors in each span for the circuit.

    :param circuit: the EMFCircuit object for which to stitch together continuous conductor paths
    :returns: a Dict keyed by the phase name ('A', 'B', or 'C') w/ vals as arrays of points representing the continuous
                conductor (electrically, not mechanically)
    """
    spans = circuit.spans

    # first generate the catenaries for each conductor on a per-span basis
    catenaries_by_phase = {"A": [], "B": [], "C": []}
    for span_id, span in spans.items():
        for cond in span.conductors.values():
            # generate the catenary for the conductor and add to the correct phase container
            cat = gen_catenary_3d(
                NUM_CATENARY_POINTS,
                cond.shape.curvature,
                cond.connects[0],
                cond.connects[1],
            )
            catenaries_by_phase[cond.phase].append(cat)

    # now create continuous conductors for each phase of the circuit, or "stitch" the conductors in each span together
    a_phase = np.concatenate(
        sorted(catenaries_by_phase["A"], key=lambda x: x[0][1])
    )  # sort the a phase cats by the y values & concatenate
    b_phase = np.concatenate(sorted(catenaries_by_phase["B"], key=lambda x: x[0][1]))  # "        b phase      "
    c_phase = np.concatenate(sorted(catenaries_by_phase["C"], key=lambda x: x[0][1]))  # "        c phase      "

    return {"A": a_phase, "B": b_phase, "C": c_phase}


def calc_h_vector(x: npt.NDArray[np.float_], Y: npt.NDArray[np.float_], phase=0.0) -> npt.NDArray[np.complex_]:
    """
    Calculates the geometric component of Biot-Savart's law at point x by integrating over a line Y, in the milligauss
    system of units.

    :param x: Vector representing the position x at which to solve for the h_vector
    :param Y: N-Vector of points representing a line of current which cause a magnetic field at position x
    :param phase: phase of the line of current (coming from A, B, or C convention)
    :returns: a phasor Vector representing the magnetic field component at point x due to the line of current Y
    """
    dY = Y[1:] - Y[:-1]
    R = x - Y[1:]

    return np.exp(1.0j * phase) * np.einsum("j, jk -> k", 1.0 / mag(R) ** 3, np.complex_(cross(dY, R)))


def calc_h_matrix(model_group: EMFModelGroup) -> npt.NDArray[np.complex_]:
    """
    Creates the coefficient matrix, or "h-matrix", for a specific EMFModelGroup.  This is equivalent to solving for the
    EMFs at each EMFSensor location when each EMFCircuit is at 1-amp loading and all other EMFCircuits are at 0 loading.
    We happen to use the instant when the A-phase conductor of the EMFCircuit is all-real and roughly in the positive-y
    direction (accounting for conductors which are not purely in a yz-plane).

    :param model_group: EMFModelGroup object for which to calculate an "h-matrix"
    :returns: NDArray object representing the "h-matrix"
    """
    sensors = model_group.sensors
    circuits = model_group.circuits

    # First generate arrays of continuous points for each conductor in each circuit
    cond_arrays_by_circ_id = {circ.id: stitch_conductor_phases(circ) for circ in circuits.values()}

    # The h_matrix will have M-sensors rows, N-circuits columns, and be 3-"deep"
    # due to each sensor having 3 axes of magnetic field measurements
    h_matrix = np.zeros((len(sensors), len(circuits), 3), dtype=np.complex_)

    for s, sensor in enumerate(sensors.values()):
        for c, circuit in enumerate(circuits.values()):
            for phase, points in cond_arrays_by_circ_id[circuit.id].items():
                if phase not in Phase.__members__.keys():
                    raise Exception("Unrecognized conductor phase name")
                elif phase == "A":
                    phase = Phase.A.value
                elif phase == "B":
                    phase = Phase.B.value
                else:
                    phase = Phase.C.value

                h_matrix[s, c, :] += calc_h_vector(sensor.position, points, phase=phase)

    return h_matrix


def devectorize_matrix(matrix: npt.NDArray[np.complex_]) -> npt.NDArray[np.complex_]:
    """
    Takes an (M x N x D)-matrix, with D-vector components, and flattens to a (D*M x N)-matrix.  Specifically for use
    setting up the h matrix for the EMF model.

    :param matrix: the matrix to flatten
    :returns: a flattened matrix
    """
    M, N, D = matrix.shape

    flat_matrix = np.zeros((D * M, N), dtype=matrix.dtype)

    for m in range(M):
        for n in range(N):
            for k in range(D):
                flat_matrix[D * m + k, n] = matrix[m, n, k]

    return flat_matrix


def vectorize_matrix(matrix: npt.NDArray[np.complex_], D=3) -> npt.NDArray[np.complex_]:
    """
    Takes a flattened (D*M x N)-matrix, vectorizes it to a (M x N x D)-matrix.  Specifically for use in vectorizing
    results of the EMF model, the loading_matrix.

    :param matrix: the flat matrix to re-vectorize
    :returns: a flattened matrix
    """
    Mp, N = matrix.shape

    matrix_vectorized = np.zeros((Mp // D, N, D), dtype=matrix.dtype)

    for m in range(Mp // D):
        for n in range(N):
            for k in range(D):
                matrix_vectorized[m, n, k] = matrix[D * m + k, n]

    return matrix_vectorized


def calc_loading_from_emf(
    model_group: EMFModelGroup,
    emg_measurement: EMFModelGroupMeasurement,
    magnitude_only: Optional[bool] = False,
) -> EMFModelResult:
    """
    The main entry function for the EMF model.  Takes a full EMFModelGroup object and a full EMFModelGroupMeasurement
    object corresponding to that model group, and produces a loading result per circuit in the model group contained in
    an EMFModelResult object.

    :param model_group: EMFModelGroup that will be calculated against
    :param measurement: EMFModelGroupMeasurement for which corresponding loading results are desired
    :param magnitude_only: optional argument to return only the absolute value of loading as opposed to the phasor form
    :returns: an EMFModelResult object, where main attribute is a Dict keyed by circuit id, with loadings as values
    """
    # calc h_matrix for this model group's geometric configuration
    h_matrix = calc_h_matrix(model_group)

    # arrange the measurements into a b_matrix of phasor vectors
    b_matrix = np.array(
        [
            model_group.sensors[sensor_id].rotate_phasor_vector(measurement.phasor_vector)
            for sensor_id, measurement in emg_measurement.measurements.items()
        ]
    )

    # use scipy's lstsq method to calculate the loading and residuals
    loading_matrix, residuals, _, _ = lstsq(devectorize_matrix(h_matrix), b_matrix.flatten())

    loading_matrix = np.abs(loading_matrix) if magnitude_only else loading_matrix

    return EMFModelResult(
        model_group_id=model_group.id,
        dttm=emg_measurement.dttm,
        loading_by_circ_id={circ.id: loading_matrix[i] for i, circ in enumerate(model_group.circuits.values())},
    )
