import re

import numpy as np
import pytest

from lv_physics.core.vectors import (
    KRONECKER,
    LEVI_CIVITA,
    X_AXIS,
    Y_AXIS,
    Z_AXIS,
    angle_between,
    cartesian_transform,
    cross,
    dot,
    mag,
    project_onto_axis,
    spherical_transform,
    unit,
)
from lv_physics.utils.helpers import ComplexUnsupportedError, complex_error_message


N_VECTOR_LENGTH = 5

A_VECTOR = np.array([1.0, 1.0, 1.0])
B_VECTOR = np.array([2.0, 2.0, 2.0])
C_VECTOR = np.array([3.0, 4.0, 0.0])
D_VECTOR = np.array([137.0, 0.0, 0.0])

A_VECTORS = np.array([A_VECTOR for n in range(N_VECTOR_LENGTH)])
B_VECTORS = np.array([B_VECTOR for n in range(N_VECTOR_LENGTH)])
C_VECTORS = np.array([C_VECTOR for n in range(N_VECTOR_LENGTH)])
D_VECTORS = np.array([D_VECTOR for n in range(N_VECTOR_LENGTH)])

X_AXES = np.array([X_AXIS for n in range(N_VECTOR_LENGTH)])
Y_AXES = np.array([Y_AXIS for n in range(N_VECTOR_LENGTH)])
Z_AXES = np.array([Z_AXIS for n in range(N_VECTOR_LENGTH)])

HALF_PI = np.pi / 2
HALF_PIS = np.array([np.pi / 2 for n in range(N_VECTOR_LENGTH)])


def test_levi_civita():
    """
    Tests that the levi-civita tensor const is generated correctly.
    """
    levi_civita_should_be = np.array(
        [
            [[0, 0, 0], [0, 0, 1], [0, -1, 0]],
            [[0, 0, -1], [0, 0, 0], [1, 0, 0]],
            [[0, 1, 0], [-1, 0, 0], [0, 0, 0]],
        ],
        dtype=np.int_,
    )

    assert np.array_equal(LEVI_CIVITA, levi_civita_should_be)


def test_kronecker_delta():
    """
    Tests that the kronecker delta in 3D const is generated correctly.
    """
    kronecker_delta_3d_should_be = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])

    assert np.array_equal(KRONECKER, kronecker_delta_3d_should_be)


def test_dot():
    """
    Tests the dot function.
    """
    error_message_1 = re.escape(complex_error_message(u=A_VECTOR, v=B_VECTOR + 1.0j))
    with pytest.raises(ComplexUnsupportedError, match=error_message_1):
        dot(A_VECTOR, B_VECTOR + 1.0j)

    error_message_2 = re.escape(complex_error_message(u=A_VECTOR + 1.0j, v=B_VECTOR + 1.0j))
    with pytest.raises(ComplexUnsupportedError, match=error_message_2):
        dot(A_VECTOR + 1.0j, B_VECTOR + 1.0j)

    assert dot(A_VECTOR, B_VECTOR) == 6.0
    assert np.allclose(dot(A_VECTOR, B_VECTORS), 6.0 * np.ones(5))
    assert np.allclose(dot(A_VECTORS, B_VECTOR), 6.0 * np.ones(5))
    assert np.allclose(dot(A_VECTORS, B_VECTORS), 6.0 * np.ones(5))


def test_mag():
    """
    Tests the mag function.
    """
    assert mag(C_VECTOR) == mag(C_VECTOR * 1.0j) == 5.0
    assert np.allclose(mag(C_VECTORS), 5.0 * np.ones(5))


def test_unit():
    """
    Tests the unit function.
    """
    assert np.allclose(unit(D_VECTOR), X_AXIS)
    assert np.allclose(unit(D_VECTORS), X_AXES)


def test_cross():
    """
    Tests the cross function.
    """
    error_message_1 = re.escape(complex_error_message(u=X_AXIS, v=Y_AXIS + 1.0j))
    with pytest.raises(ComplexUnsupportedError, match=error_message_1):
        cross(X_AXIS, Y_AXIS + 1.0j)

    error_message_2 = re.escape(complex_error_message(u=X_AXIS + 1.0j, v=Y_AXIS + 1.0j))
    with pytest.raises(ComplexUnsupportedError, match=error_message_2):
        cross(X_AXIS + 1.0j, Y_AXIS + 1.0j)

    assert np.allclose(cross(X_AXIS, Y_AXIS), Z_AXIS)
    assert np.allclose(cross(X_AXES, Y_AXIS), Z_AXES)
    assert np.allclose(cross(X_AXIS, Y_AXES), Z_AXES)
    assert np.allclose(cross(X_AXES, Y_AXES), Z_AXES)


def test_angle_between():
    """
    Tests the angle function.
    """
    error_message_1 = re.escape(complex_error_message(u=X_AXIS, v=Y_AXIS + 1.0j))
    with pytest.raises(ComplexUnsupportedError, match=error_message_1):
        angle_between(X_AXIS, Y_AXIS + 1.0j)

    error_message_2 = re.escape(complex_error_message(u=X_AXIS + 1.0j, v=Y_AXIS + 1.0j))
    with pytest.raises(ComplexUnsupportedError, match=error_message_2):
        angle_between(X_AXIS + 1.0j, Y_AXIS + 1.0j)

    assert angle_between(X_AXIS, Y_AXIS) == np.pi / 2
    assert np.allclose(angle_between(X_AXIS, Y_AXIS), HALF_PIS)


def test_project_onto_axis():
    """
    Tests the project_onto_axis function.
    """
    vector = np.array([1.0, 5.0, 1.0])
    vectors = np.array([vector for n in range(N_VECTOR_LENGTH)])

    axis_start = np.zeros(3)
    axis_end = 7.0 * Y_AXIS

    projected_vector = np.array([0.0, 5.0, 0.0])
    projected_vectors = np.array([projected_vector for n in range(N_VECTOR_LENGTH)])

    assert np.array_equal(project_onto_axis(vector, axis_start, axis_end), projected_vector)
    assert np.allclose(project_onto_axis(vectors, axis_start, axis_end), projected_vectors)


def test_transforms():
    """
    Tests the cartesian_transform and spherical_transform functions.
    """
    cartesian_vector = np.array([-(1.0 / np.sqrt(2)), 0.0, 1.0 / np.sqrt(2)])
    cartesian_vectors = np.array([cartesian_vector for n in range(N_VECTOR_LENGTH)])

    spherical_vector = np.array([1.0, np.pi / 2, np.pi / 4])
    spherical_vectors = np.array([spherical_vector for n in range(N_VECTOR_LENGTH)])

    erm = re.escape(complex_error_message(vectors=cartesian_vector + 1.0j))
    with pytest.raises(ComplexUnsupportedError, match=erm):
        spherical_transform(vectors=cartesian_vector + 1.0j)

    erm = re.escape("Unsupported")
    with pytest.raises(ComplexUnsupportedError):
        cartesian_transform(vectors=spherical_vector + 1.0j)

    erm = re.escape("Unsupported")
    with pytest.raises(ComplexUnsupportedError):
        cartesian_transform(vectors=spherical_vector + 1.0j)

    assert np.allclose(spherical_transform(cartesian_vector), spherical_vector)
    assert np.allclose(cartesian_transform(spherical_vector), cartesian_vector)
    assert np.allclose(spherical_transform(cartesian_vectors), spherical_vectors)
    assert np.allclose(cartesian_transform(spherical_vectors), cartesian_vectors)
