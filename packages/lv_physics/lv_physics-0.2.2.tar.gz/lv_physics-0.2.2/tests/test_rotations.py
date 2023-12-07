import re

import numpy as np
import pytest

from lv_physics.core.rotations import (
    apply_rotation,
    extrinsic_angles_zyx,
    extrinsic_rotation_matrix,
    intrinsic_rotation_matrix,
    rotate,
    rotate_frame,
    rotation_matrix,
    solve_rotation_angle,
)
from lv_physics.core.vectors import X_AXIS, XYZ_FRAME, Y_AXIS, Z_AXIS
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

ROTATION_MATRIX_X = np.array([[1.0, 0.0, 0.0], [0.0, 0.0, -1.0], [0.0, 1.0, 0.0]])
ROTATION_MATRIX_Y = np.array([[0.0, 0.0, 1.0], [0.0, 1.0, 0.0], [-1.0, 0.0, 0.0]])
ROTATION_MATRIX_Z = np.array([[0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]])


def test_rotation_matrix():
    """
    Tests the rotation matrix function.
    """
    erm = re.escape(complex_error_message(angle=HALF_PI + 1.0j, axis=Z_AXIS))
    with pytest.raises(ComplexUnsupportedError, match=erm):
        rotation_matrix(angle=HALF_PI + 1.0j, axis=Z_AXIS)

    erm = re.escape(complex_error_message(angle=HALF_PI + 1.0j, axis=Z_AXIS + 1.0j))
    with pytest.raises(ComplexUnsupportedError, match=erm):
        rotation_matrix(angle=HALF_PI + 1.0j, axis=Z_AXIS + 1.0j)

    assert np.allclose(rotation_matrix(angle=HALF_PI, axis=X_AXIS), ROTATION_MATRIX_X)
    assert np.allclose(rotation_matrix(angle=HALF_PI, axis=Y_AXIS), ROTATION_MATRIX_Y)
    assert np.allclose(rotation_matrix(angle=HALF_PI, axis=Z_AXIS), ROTATION_MATRIX_Z)


def test_rotate():
    """
    Tests the rotate function.
    """
    erm = re.escape(complex_error_message(X_AXIS=X_AXIS, angle=HALF_PI + 1.0j, point=Y_AXIS, axis=Z_AXIS))
    with pytest.raises(ComplexUnsupportedError, match=erm):
        rotate(X_AXIS, angle=HALF_PI + 1.0j, point=Y_AXIS, axis=Z_AXIS)

    erm = re.escape(complex_error_message(X_AXIS=X_AXIS, angle=HALF_PI, point=Y_AXIS + 1.0j, axis=Z_AXIS))
    with pytest.raises(ComplexUnsupportedError, match=erm):
        rotate(X_AXIS, angle=HALF_PI, point=Y_AXIS + 1.0j, axis=Z_AXIS)

    erm = re.escape(complex_error_message(X_AXIS=X_AXIS, angle=HALF_PI, point=Y_AXIS, axis=Z_AXIS + 1.0j))
    with pytest.raises(ComplexUnsupportedError, match=erm):
        rotate(X_AXIS, angle=HALF_PI, point=Y_AXIS, axis=Z_AXIS + 1.0j)

    assert np.allclose(rotate(X_AXIS, angle=HALF_PI, axis=Z_AXIS), Y_AXIS)
    assert np.allclose(rotate(Y_AXIS, angle=HALF_PI, axis=X_AXIS), Z_AXIS)
    assert np.allclose(rotate(Z_AXIS, angle=HALF_PI, axis=Y_AXIS), X_AXIS)

    assert np.allclose(rotate(X_AXES, angle=HALF_PI, axis=Z_AXIS), Y_AXES)
    assert np.allclose(rotate(Y_AXES, angle=HALF_PI, axis=X_AXIS), Z_AXES)
    assert np.allclose(rotate(Z_AXES, angle=HALF_PI, axis=Y_AXIS), X_AXES)


def test_apply_rotation():
    """
    Tests the apply rotation function.
    """
    rotation_matrix_ = np.array([[0.0, 1.0, 0.0], [-1.0, 0.0, 0.0], [0.0, 0.0, 1.0]]).T

    erm = re.escape("Unsupported")
    with pytest.raises(ComplexUnsupportedError, match=erm):
        apply_rotation(rotation_matrix_ + 1.0j, X_AXIS)

    erm = re.escape(complex_error_message(rotation_matrix_=rotation_matrix_, X_AXIS=X_AXIS, point=X_AXIS + 1.0j))
    with pytest.raises(ComplexUnsupportedError, match=erm):
        apply_rotation(rotation_matrix_, X_AXIS, point=X_AXIS + 1.0j)

    assert np.allclose(apply_rotation(rotation_matrix_, X_AXIS), Y_AXIS)


def test_solve_rotation_angle():
    """
    Tests the solve rotation angle function.
    """
    erm = re.escape(complex_error_message(X_AXIS=X_AXIS, Y_AXIS=Y_AXIS, axis=Z_AXIS + 1.0j))
    with pytest.raises(ComplexUnsupportedError, match=erm):
        solve_rotation_angle(X_AXIS, Y_AXIS, axis=Z_AXIS + 1.0j)

    assert np.allclose(solve_rotation_angle(X_AXIS, Y_AXIS, axis=Z_AXIS), HALF_PI)


def test_rotate_frame():
    """
    Tests the rotation of a full coordinate frame.
    """
    rotation_matrix_x = ROTATION_MATRIX_X
    rotation_matrix_xy = ROTATION_MATRIX_Y @ ROTATION_MATRIX_X
    rotation_matrix_xyz = ROTATION_MATRIX_Z @ ROTATION_MATRIX_Y @ ROTATION_MATRIX_X

    coords_after_x = np.array([X_AXIS, Z_AXIS, -Y_AXIS])
    coords_after_xy = np.array([-Z_AXIS, X_AXIS, -Y_AXIS])
    coords_after_xyz = np.array([-Z_AXIS, Y_AXIS, X_AXIS])

    erm = re.escape(complex_error_message(rotation_matrix=ROTATION_MATRIX_X + 1.0j, coordinate_axes=XYZ_FRAME))
    with pytest.raises(ComplexUnsupportedError, match=erm):
        rotate_frame(ROTATION_MATRIX_X + 1.0j, XYZ_FRAME)

    assert np.allclose(rotate_frame(rotation_matrix_x, XYZ_FRAME), coords_after_x)
    assert np.allclose(rotate_frame(rotation_matrix_xy, XYZ_FRAME), coords_after_xy)
    assert np.allclose(rotate_frame(rotation_matrix_xyz, XYZ_FRAME), coords_after_xyz)


def test_extrinsic_angles_zyx():
    """
    Tests that extrinsic rotation angles in the rotation order of zyx are extracted from a rotation matrix.
    """
    angles_xyz = np.array([HALF_PI, HALF_PI / 2, HALF_PI / 3])
    axes = [0, 1, 2]
    order = [2, 1, 0]

    rotation_matrix = extrinsic_rotation_matrix(angles=angles_xyz, axes=axes, order=order)
    angles_solved = extrinsic_angles_zyx(rotation_matrix)

    assert np.allclose(angles_solved, angles_xyz)


def test_extrinsic_rotation_matrix():
    """
    Tests that an extrinsinc rotation matrix is generated correctly.
    """
    angles = np.array([HALF_PI, HALF_PI, HALF_PI])
    axes = np.array([0, 1, 2], dtype=np.int_)
    order = [0, 1, 2]

    net_rotation_matrix = ROTATION_MATRIX_Z @ ROTATION_MATRIX_Y @ ROTATION_MATRIX_X

    erm = re.escape(complex_error_message(angles=angles + 1.0j, axes=axes, order=order))
    with pytest.raises(ComplexUnsupportedError, match=erm):
        extrinsic_rotation_matrix(angles=angles + 1.0j, axes=axes, order=order)

    assert np.allclose(
        extrinsic_rotation_matrix(angles=angles, axes=axes, order=order),
        net_rotation_matrix,
    )


def test_intrinsic_rotation_matrix():
    """
    Tests that an intrinsinc rotation matrix is generated correctly.
    """
    angles = np.array([HALF_PI, HALF_PI, HALF_PI])
    axes = np.array([0, 2, 0], dtype=np.int_)
    order = [0, 1, 2]

    net_rotation_matrix = ROTATION_MATRIX_X @ ROTATION_MATRIX_Z @ ROTATION_MATRIX_X

    erm = re.escape(complex_error_message(angles=angles + 1.0j, axes=axes, order=order))
    with pytest.raises(ComplexUnsupportedError, match=erm):
        intrinsic_rotation_matrix(angles=angles + 1.0j, axes=axes, order=order)

    assert np.allclose(
        intrinsic_rotation_matrix(angles=angles, axes=axes, order=order),
        net_rotation_matrix,
    )
