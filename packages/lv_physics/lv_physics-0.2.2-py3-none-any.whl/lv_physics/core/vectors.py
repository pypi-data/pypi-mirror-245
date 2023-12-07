"""
This module provides the core utility functions for the lv-physics framework for performing operations on or between
vectors, tensors, and general matrices.

This module heavily uses the function `numpy.einsum()`, which makes use of the Einstein summation convention.  This
convention may seem strange to the reader, and more information can be found in the following links:
    - https://en.wikipedia.org/wiki/Einstein_notation
    - https://ajcr.net/Basic-guide-to-einsum/
"""
import numpy as np
from numpy import complex_, float_, int_
from numpy.typing import NDArray

from lv_physics.utils.helpers import ComplexUnsupportedError, complex_error_message


def kronecker_delta(n: int = 3) -> NDArray[int_]:
    """
    Generate a Kronecker delta matrix with specified dimensions. This function creates a square matrix of size `n x n`,
    where the diagonal elements are 1, and all off-diagonal elements are 0. It's a fundamental entity in linear algebra
    and tensor calculus.

    Args:
        n: The dimension of the square matrix. Defaults to 3.

    Returns:
        A square matrix representing the Kronecker delta, with dimensions `n x n`.
    """
    return np.diag(np.ones(n, dtype=int_))


def levi_civita_tensor() -> NDArray[int_]:
    """
    Create the 3D Levi-Civita tensor.

    This tensor is an essential component in vector and tensor analysis, especially in three dimensions.  It is
    characterized by its elements being 1 for cyclic permutations of indices, -1 for anti-cyclic permutations,  and 0
    when any indices are repeated. The mathematical representation of this concept is:

        ε_ijk = -ε_ikj = 1          and
        ε_iik = ε_ijj = ε_iji = 0

    Returns:
        The 3D Levi-Civita tensor.
    """
    levi_civita = np.zeros((3, 3, 3), dtype=int_)
    for i in range(3):
        for l in range(3):
            for m in range(l + 1, 3):
                for n in range(m + 1, 3):
                    L, M, N = (i + l) % 3, (i + m) % 3, (i + n) % 3
                    levi_civita[L, M, N] = +1
                    levi_civita[N, M, L] = -1

    return levi_civita


X_AXIS = np.array([1.0, 0.0, 0.0])
Y_AXIS = np.array([0.0, 1.0, 0.0])
Z_AXIS = np.array([0.0, 0.0, 1.0])
XYZ_FRAME = np.array([X_AXIS + 0.0, Y_AXIS + 0.0, Z_AXIS + 0.0])
# TODO: The XYZ_FRAME should be XYZ_FRAME.T.  This is why the rotations get the anomalous transpose.

KRONECKER = kronecker_delta(3)
LEVI_CIVITA = levi_civita_tensor()


def dot(u: NDArray[float_], v: NDArray[float_]) -> float_:
    """
    Compute the dot product of two vectors.

    This function calculates the dot product of vectors `u` and `v`. It is not applicable to complex vectors due to
    specific requirements in complex phase space. For more information on complex vectors, refer to:
    https://en.wikipedia.org/wiki/Dot_product#Complex_vectors

    Args:
        u: The first vector.
        v: The second vector.

    Returns:
        The scalar dot product of `u` and `v`.

    Raises:
        ComplexUnsupportedError: If either `u` or `v` is of complex data type.
    """
    try:
        assert np.isrealobj(u) and np.isrealobj(v)
    except AssertionError as e:
        raise ComplexUnsupportedError(complex_error_message(u=u, v=v), e) from e

    return np.einsum("...i, ...i", u, v)


def mag(v: NDArray[float_ | complex_]) -> float_:
    """
    Calculate the magnitude of a vector.

    The function computes the magnitude of vector `v`. For complex vectors, the full phasor magnitude is taken.

    Args:
        v: The vector to compute the magnitude of.

    Returns:
        The scalar magnitude of the vector.
    """
    # The abs() calls ensure expected behavior when dealing with complex types
    return np.sqrt(dot(np.abs(v), np.abs(v)))


def unit(v: NDArray[float_ | complex_]) -> NDArray[float_ | complex_]:
    """
    Generate a unit vector in the direction of the given vector. This function creates a unit vector along the direction
    of vector `v`. For more details on unit vectors, see: https://en.wikipedia.org/wiki/Unit_vector

    Args:
        v: The vector to create a unit vector of.

    Returns:
        A unit vector with magnitude 1 in the same direction as `v`.
    """
    # If the magnitude of the vector is zero, the unit vector is zero
    with np.errstate(divide="ignore"):
        u = np.einsum("...j, ... -> ...j", v, 1 / mag(v))
        u[np.isnan(u)] = 0.0

    return u


def cross(u: NDArray[float_], v: NDArray[float_]) -> NDArray[float_]:
    """
    Calculate the cross product of two vectors. This function computes the cross product of vectors `u` and `v`. It does
    not support complex vectors, similar to the dot function.

    Args:
        u: The first vector.
        v: The second vector.

    Returns:
        The resulting vector from the cross product of `u` and `v`.

    Raises:
        ComplexUnsupportedError: If either `u` or `v` is of complex data type.
    """
    try:
        assert np.isrealobj(u) and np.isrealobj(v)
    except AssertionError as e:
        raise ComplexUnsupportedError(complex_error_message(u=u, v=v), e) from e

    return np.einsum("ijk, ...j, ...k", LEVI_CIVITA, u, v)


def angle_between(u: NDArray[float_], v: NDArray[float_]) -> float_:
    """
    Determine the angle between two vectors. This function calculates the absolute value of the angle between vectors
    `u` and `v` in radians.

    Args:
        u: The first vector.
        v: The second vector.

    Returns:
        The angle between vectors `u` and `v` in radians.

    Raises:
        ComplexUnsupportedError: If either vector is of complex data type.
    """
    try:
        assert np.isrealobj(u) and np.isrealobj(v)
    except AssertionError as e:
        raise ComplexUnsupportedError(complex_error_message(u=u, v=v), e) from e

    return np.arccos(dot(u, v) / mag(u) / mag(v))


def project_onto_axis(
    vectors: NDArray[float_],
    a: NDArray[float_],
    b: NDArray[float_],
) -> NDArray[float_]:
    """
    Project vectors onto a specified axis. This function projects the given vector or array of vectors onto the axis
    formed by vectors `a` and `b`.

    Args:
        vectors: The vector or array of vectors to project.
        a: The starting point of the axis.
        b: The ending point of the axis.

    Returns:
        The projected vector or array of vectors.
    """
    axis = unit(b - a)

    return a + np.einsum("..., i", dot(vectors - a, axis), axis)


def spherical_transform(vectors: NDArray[float_]) -> NDArray[float_]:
    """
    Convert cartesian coordinates to spherical coordinates. This function transforms vectors from cartesian (x, y, z) to
    spherical coordinates (r, azimuth, elevation) using the right-hand coordinate system. Azimuth is measured from the
    y-axis leftward, and elevation from the y-axis upward.

    Args:
        vectors: The vector or array of vectors in cartesian coordinates to be transformed.

    Returns:
        The same vectors in spherical coordinates.

    Raises:
        ComplexUnsupportedError: If the input vectors are of complex data type.
    """
    try:
        assert np.isrealobj(vectors)
    except AssertionError as e:
        raise ComplexUnsupportedError(complex_error_message(vectors=vectors), e) from e

    return np.array(
        [
            mag(vectors[..., :]),
            np.arctan2(vectors[..., 1], vectors[..., 0]) - np.pi / 2,
            np.pi / 2 - np.arctan2(mag(vectors[..., :2]), vectors[..., 2]),
        ]
    ).T


def cartesian_transform(vectors: NDArray[float_]) -> NDArray[float_]:
    """
    Convert spherical coordinates to cartesian coordinates. This function transforms vectors from spherical
    (r, azimuth, elevation) to cartesian coordinates (x, y, z).

    Args:
        vectors: The vector or array of vectors in spherical coordinates to be transformed.

    Returns:
        The same vectors in cartesian coordinates.
    """
    try:
        assert np.isrealobj(vectors)
    except AssertionError as e:
        raise ComplexUnsupportedError(complex_error_message(vectors=vectors), e) from e

    return np.array(
        [
            -vectors[..., 0] * np.sin(vectors[..., 1]) * np.cos(vectors[..., 2]),
            vectors[..., 0] * np.cos(vectors[..., 1]) * np.cos(vectors[..., 2]),
            vectors[..., 0] * np.sin(vectors[..., 2]),
        ]
    ).T
