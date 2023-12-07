"""
This module provides the core utility functions for the lv-physics framework for performing operations on or between
vectors, tensors, and general matrices.

This module heavily uses the function `numpy.einsum()`, which makes use of the Einstein summation convention.  This
convention may seem strange to the reader, and more information can be found in the following links:
    - https://en.wikipedia.org/wiki/Einstein_notation
    - https://ajcr.net/Basic-guide-to-einsum/
"""
from typing import Iterable

import numpy as np
from numpy import complex_, float_
from numpy.typing import NDArray
from scipy.optimize import fsolve

from lv_physics.core.vectors import KRONECKER, LEVI_CIVITA, XYZ_FRAME, mag, unit
from lv_physics.utils.helpers import ComplexUnsupportedError, complex_error_message


def rotation_matrix(angle: float_, axis: NDArray[float_] = np.array([0.0, 0.0, 1.0], dtype=float_)) -> NDArray[float_]:
    """
    Create a rotation matrix for rotating by a specified angle about a given axis. This function constructs a 3x3
    rotation matrix based on the axis-angle representation, as detailed in:
    https://en.wikipedia.org/wiki/Rotation_matrix#Rotation_matrix_from_axis_and_angle.

    Args:
        angle: The angle of rotation in radians.
        axis: The axis of rotation represented as a vector. Defaults to the z-axis.

    Returns:
        A 3x3 rotation matrix.

    Raises:
        AssertionError: When either the angle or axis is of complex type.
    """
    try:
        assert np.isrealobj(angle) and np.isrealobj(axis)
    except AssertionError as e:
        raise ComplexUnsupportedError(complex_error_message(angle=angle, axis=axis), e) from e

    ku = unit(axis)
    kx = np.einsum("ijk, j", LEVI_CIVITA, ku)
    kij = np.einsum("i, j -> ij", ku, ku)

    return np.cos(angle) * KRONECKER + np.sin(angle) * kx + (1 - np.cos(angle)) * kij


def rotate(
    vectors: NDArray[float_ | complex_],
    angle: float_,
    axis: NDArray[float_] = np.array([0.0, 0.0, 1.0], dtype=float_),
    point: NDArray[float_] = np.array([0.0, 0.0, 0.0], dtype=float_),
) -> NDArray[float_ | complex_]:
    """
    Rotate vectors by a specified angle around an axis originating from a point. This function applies a rotational
    transformation to a vector or an array of vectors.

    Args:
        vectors: The vector or array of vectors to be rotated.
        angle: The angle in radians by which to rotate.
        axis: The axis of rotation.
        point: The origin point of the axis of rotation.

    Returns:
        The rotated vector or array of vectors.

    Raises:
        AssertionError: When the angle, axis, or point is of complex type.
    """
    try:
        assert np.isrealobj(angle) and np.isrealobj(axis) and np.isrealobj(point)
    except AssertionError as e:
        raise ComplexUnsupportedError(complex_error_message(angle=angle, axis=axis, point=point), e) from e

    return (
        np.einsum(
            "...ij, ...j",
            rotation_matrix(angle=angle, axis=unit(axis)),
            vectors - point,
        )
        + point
    )


def apply_rotation(
    rotation_matrix: NDArray[float_],
    vectors: NDArray[float_ | complex_],
    point: NDArray[float_] = np.zeros(3, dtype=float_),
) -> NDArray[float_ | complex_]:
    """
    Apply a given rotation matrix to vectors. This function rotates vectors using a specified rotation matrix and a
    reference point.

    Args:
        rotation_matrix: The rotation matrix to be used for rotation.
        vectors: The vector or array of vectors to rotate.
        point: The reference point for rotation. Defaults to the origin.

    Returns:
        The rotated vector or array of vectors.

    Raises:
        AssertionError: When the rotation matrix or point is of complex type.
    """
    try:
        assert np.isrealobj(rotation_matrix) and np.isrealobj(point)
    except AssertionError as e:
        raise ComplexUnsupportedError(complex_error_message(rotation_matrix=rotation_matrix, point=point), e) from e

    return np.einsum("...ij, ...j", rotation_matrix, vectors - point) + point


def solve_rotation_angle(u: NDArray[float_ | complex_], v: NDArray[float_ | complex_], axis: NDArray[float_]) -> float_:
    """
    Calculate the rotation angle required to rotate vector 'u' to 'v' about a given axis. This function computes the
    angle needed for such a rotation using numerical methods.

    Args:
        u: The original vector.
        v: The vector after rotation.
        axis: The axis of rotation.

    Returns:
        The angle in radians required to rotate 'u' to 'v' about the specified axis.

    Raises:
        AssertionError: When the axis is of complex type.
    """

    def rotation_err(angle):
        return mag(rotate(u, angle, axis=axis) - v)

    try:
        assert np.isrealobj(axis)
    except AssertionError as e:
        raise ComplexUnsupportedError(complex_error_message(axis=axis), e) from e

    return fsolve(rotation_err, 0)


def rotate_frame(rotation_matrix: NDArray[float_], coordinate_axes: NDArray[float_]) -> NDArray[float_]:
    """
    Rotate a set of coordinate axes using a given rotation matrix. This function applies the rotation matrix to
    transform a coordinate frame.

    Args:
        rotation_matrix: The rotation matrix.
        coordinate_axes: A set of vectors forming a coordinate frame.

    Returns:
        The rotated coordinate frame.

    Raises:
        AssertionError: When the rotation matrix is of complex type.
    """
    try:
        assert np.isrealobj(rotation_matrix)
    except AssertionError as e:
        raise ComplexUnsupportedError(complex_error_message(rotation_matrix=rotation_matrix), e) from e

    return np.einsum("mn, an -> am", rotation_matrix, coordinate_axes)


def extrinsic_angles_zyx(rotation_matrix: NDArray[float_]) -> NDArray[float_]:
    """
    Determine the extrinsic rotation angles from a given rotation matrix, specifically in the zyx order. This function
    extracts the angles about the x, y, and z axes that produce the given rotation matrix when applied extrinsically in
    the zyx order. The method is detailed under 'Conversions to other orientation representations' at:
    https://en.wikipedia.org/wiki/Euler_angles.

    Args:
        rotation_matrix: A 3x3 array representing a rotation matrix.

    Returns:
        An array of rotation angles in radians for the zyx order: [angle_about_x, angle_about_y, angle_about_z].
    """
    angle_about_x = np.arctan2(-rotation_matrix[1, 2], rotation_matrix[2, 2])
    angle_about_y = np.arctan2(+rotation_matrix[0, 2], np.sqrt(1.0 - rotation_matrix[0, 2] ** 2))
    angle_about_z = np.arctan2(-rotation_matrix[0, 1], rotation_matrix[0, 0])

    return np.array([angle_about_x, angle_about_y, angle_about_z])


def extrinsic_rotation_matrix(angles: Iterable[float], axes: Iterable[int], order: Iterable[int]) -> NDArray[float_]:
    """
    Construct a rotation matrix from a set of angles and axes indices, applied in a specified order, with respect to a
    fixed coordinate frame. This function builds a rotation matrix using the provided angles and axes, considering
    rotations as applied extrinsically.

    Args:
        angles: A sequence of angles in radians for rotation.
        axes: The indices of axes about which to rotate.
        order: The order in which to apply the rotations.

    Returns:
        A rotation matrix constructed from the specified angles and axes.

    Raises:
        AssertionError: When any of the inputs are of complex type.
    """
    try:
        assert np.isrealobj(angles) and np.isrealobj(axes) and np.isrealobj(order)
    except AssertionError as e:
        raise ComplexUnsupportedError(complex_error_message(angles=angles, axes=axes, order=order), e) from e

    rotated_coordinate_axes = np.array([x for x in XYZ_FRAME])

    for k in order:
        rotation_mat = rotation_matrix(angles[k], axis=XYZ_FRAME[axes[k]])
        rotated_coordinate_axes = rotate_frame(rotation_mat, rotated_coordinate_axes)

    net_rotation_matrix = (rotated_coordinate_axes @ np.linalg.inv(XYZ_FRAME)).T

    return net_rotation_matrix


def intrinsic_rotation_matrix(angles: Iterable[float], axes: Iterable[int], order: Iterable[int]) -> NDArray[float_]:
    """
    Create a rotation matrix from a set of angles and axes indices, applied in a specified order, with respect to a
    co-moving coordinate frame. This function generates a rotation matrix considering the rotations as applied
    intrinsically.

    Args:
        angles: A sequence of angles in radians for rotation.
        axes: The indices of axes about which to rotate.
        order: The order in which to apply the rotations.

    Returns:
        A rotation matrix built from the given angles and axes, considering intrinsic rotations.

    Raises:
        AssertionError: When any of the inputs are of complex type.
    """
    try:
        assert np.isrealobj(angles) and np.isrealobj(axes) and np.isrealobj(order)
    except AssertionError as e:
        raise ComplexUnsupportedError(complex_error_message(angles=angles, axes=axes), e) from e

    rotated_coordinate_axes = np.array([x for x in XYZ_FRAME])

    for k in order:
        rotation_mat = rotation_matrix(angles[k], axis=rotated_coordinate_axes[axes[k]])
        rotated_coordinate_axes = rotate_frame(rotation_mat, rotated_coordinate_axes)

    net_rotation_matrix = (rotated_coordinate_axes @ np.linalg.inv(XYZ_FRAME)).T

    return net_rotation_matrix
