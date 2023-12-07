from copy import deepcopy
from typing import Iterable, Union

import numpy as np
from numpy import float_
from numpy.typing import NDArray
from scipy.optimize import minimize

from lv_physics.core.rotations import rotate
from lv_physics.core.vectors import X_AXIS, Y_AXIS, Z_AXIS, mag, project_onto_axis, unit
from lv_physics.utils.helpers import ComplexUnsupportedError, complex_error_message


def catenary(
    s: Union[float, NDArray[float_]],
    curvature: float,
    height_a: float,
    height_b: float,
    span_length: float,
) -> Union[float, NDArray[float_]]:
    """
    Calculate the vertical position(s) of a catenary at horizontal positions. This function computes the z-values
    for given horizontal s-values of a catenary with a specified curvature and fixed endpoints. The catenary is defined
    between points (0, height_a) and (span_length, height_b). For theoretical background, refer to Alen Hatibovic's
    work on catenary equations.

    Args:
        s: Horizontal position(s) along the catenary.
        curvature: The curvature parameter of the catenary.
        height_a: The height of the catenary at the start (s=0).
        height_b: The height of the catenary at the end (s=span_length).
        span_length: The horizontal distance between the fixed ends of the catenary.

    Returns:
        The vertical position(s) of the catenary at specified horizontal position(s).

    Raises:
        AssertionError: When any of the parameters are of complex type.
    """
    try:
        real_kwargs = dict(
            s=s,
            curvature=curvature,
            height_a=height_a,
            height_b=height_b,
            span_length=span_length,
        )
        assert all([np.isrealobj(v) for k, v in real_kwargs.items()])
    except AssertionError as e:
        raise ComplexUnsupportedError(complex_error_message(**real_kwargs), e) from e

    # calculate the vertex point of the catenary
    s_vertex = catenary_vertex(
        curvature=curvature,
        height_a=height_a,
        height_b=height_b,
        span_length=span_length,
    )

    # the catenary (~eq.15)
    z = (
        2 * curvature * (np.sinh((s - s_vertex) / 2 / curvature) ** 2 - np.sinh(s_vertex / 2 / curvature) ** 2)
        + height_a
    )

    return z


def catenary_vertex(curvature: float, height_a: float, height_b: float, span_length: float) -> float:
    """
    Determine the horizontal position of the vertex of a catenary. This function calculates the position where the
    catenary curve attains its minimum height, based on the curvature and fixed heights at its endpoints. The theory
    behind this calculation is elaborated in Alen Hatibovic's work on catenary equations.

    Args:
        curvature: The curvature parameter of the catenary.
        height_a: The height of the catenary at the start.
        height_b: The height of the catenary at the end.
        span_length: The horizontal distance between the catenary's endpoints.

    Returns:
        The horizontal position of the catenary's vertex.
    """
    s_shift = curvature * np.arcsinh((height_b - height_a) / (2 * curvature * np.sinh(span_length / 2 / curvature)))

    return (span_length / 2) - s_shift


def catenary_length(
    curvature: float,
    height_a: float,
    height_b: float,
    span_length: float,
    bounds: Iterable[float] = None,
) -> float:
    """
    Calculate the parametric length of a catenary. This function determines the length of a catenary curve, given its
    curvature and fixed endpoints, over a specified horizontal segment. The method is based on Jim Emery's work on
    estimating catenary parameters.

    Args:
        curvature: The curvature parameter of the catenary.
        height_a: The height of the catenary at the start.
        height_b: The height of the catenary at the end.
        span_length: The horizontal distance between the catenary's endpoints.
        bounds: The horizontal segment for calculating the length. Defaults to the entire span.

    Returns:
        The length of the catenary over the specified segment.
    """
    s_vertex = catenary_vertex(
        curvature=curvature,
        height_a=height_a,
        height_b=height_b,
        span_length=span_length,
    )

    if bounds is None:
        bounds = (0.0, span_length)

    return curvature * np.sum([np.sinh(np.abs(s - s_vertex) / curvature) for s in bounds])


def catenary_sag(curvature: float, height_a: float, height_b: float, span_length: float) -> float:
    """
    Compute the maximum sag of a fixed-end catenary. This function calculates the greatest vertical distance between
    the catenary curve and the straight line connecting its endpoints. The theoretical foundation is based on Alen
    Hatibovic's study of catenary curves.

    Args:
        curvature: The curvature parameter of the catenary.
        height_a: The height of the catenary at the start.
        height_b: The height of the catenary at the end.
        span_length: The horizontal distance between the endpoints.

    Returns:
        The maximum vertical sag of the catenary.
    """
    try:
        real_kwargs = dict(
            curvature=curvature,
            height_a=height_a,
            height_b=height_b,
            span_length=span_length,
        )
        assert all([np.isrealobj(v) for k, v in real_kwargs.items()])
    except AssertionError as e:
        raise ComplexUnsupportedError(complex_error_message(**real_kwargs), e) from e

    d_height = height_b - height_a

    # these are taken from equations 11, 13, & 23 respectively
    s_vertex = catenary_vertex(
        curvature=curvature,
        height_a=height_a,
        height_b=height_b,
        span_length=span_length,
    )
    z_vertex = height_a - 2 * curvature * np.sinh(s_vertex / 2 / curvature) ** 2
    s_sag = s_vertex + curvature * np.arcsinh(d_height / span_length)

    # the sag is given by equation 37
    base_height = height_a + curvature - z_vertex
    sag = base_height + d_height * s_sag / span_length - curvature * np.cosh((s_sag - s_vertex) / curvature)

    return sag


def catenary_3d(
    span_points: NDArray[float_],
    curvature: float,
    end_point_a: NDArray[float_],
    end_point_b: NDArray[float_],
) -> NDArray[float_]:
    """
    Calculate 3D points of a catenary for given span coordinates. This function computes the 3D position of a catenary
    for each point in the span_points vector, considering only their horizontal components.

    Args:
        span_points: Coordinates for calculating the catenary's height values (z-component ignored).
        curvature: The curvature of the catenary.
        end_point_a: One fixed endpoint of the catenary.
        end_point_b: The other fixed endpoint of the catenary.

    Returns:
        A vector representing the 3D points of the catenary.

    Raises:
        AssertionError: When any of the inputs are of complex type.
    """
    try:
        real_kwargs = dict(
            span_points=span_points,
            curvature=curvature,
            end_point_a=end_point_a,
            end_point_b=end_point_b,
        )
        assert all([np.isrealobj(v) for k, v in real_kwargs.items()])
    except AssertionError as e:
        raise ComplexUnsupportedError(complex_error_message(**real_kwargs), e) from e

    # copy the points array into the output catenary array
    cat_points = deepcopy(span_points)

    # calculate the horizontal distance in the xy-plane of each point
    xy_distance = mag(span_points[:, :2] - end_point_a[:2])

    # fill the z-component of the catenary points with the catenary height calculated by the 2d catenary function
    cat_points[:, 2] = catenary(
        s=xy_distance,
        curvature=curvature,
        height_a=end_point_a[2],
        height_b=end_point_b[2],
        span_length=mag(end_point_b[:2] - end_point_a[:2]),
    )

    return cat_points


def gen_catenary_3d(
    n_points: int,
    curvature: float,
    end_point_a: NDArray[float_],
    end_point_b: NDArray[float_],
) -> NDArray[float_]:
    """
    Generate 3D catenary points between two fixed endpoints. This function creates a set of evenly spaced 3D points
    representing a catenary curve between two endpoints, using the `catenary_3d` function.

    Args:
        n_points: The number of points to generate.
        curvature: The curvature of the catenary.
        end_point_a: One fixed endpoint of the catenary.
        end_point_b: The other fixed endpoint of the catenary.

    Returns:
        A vector representing the 3D points of the catenary.

    Raises:
        AssertionError: When any of the inputs are of complex type.
    """
    try:
        real_kwargs = dict(
            n_points=n_points,
            curvature=curvature,
            end_point_a=end_point_a,
            end_point_b=end_point_b,
        )
        assert all([np.isrealobj(v) for k, v in real_kwargs.items()])
    except AssertionError as e:
        raise ComplexUnsupportedError(complex_error_message(**real_kwargs), e) from e

    span_points = np.linspace(end_point_a, end_point_b, n_points)

    return catenary_3d(
        span_points,
        curvature=curvature,
        end_point_a=end_point_a,
        end_point_b=end_point_b,
    )


def fit_catenary(
    s: Union[float, NDArray[float_]],
    z: Union[float, NDArray[float_]],
    height_a: float,
    height_b: float,
    span_length: float,
    method: str = "nelder-mead",
) -> float:
    """
    Optimize the catenary curvature for a given set of points. This function fits a catenary curve to a set of
    horizontal and vertical values using optimization, aligning with the catenary parameterization in the
    `lv_physics.core.catenaries.catenary`.

    Args:
        s: Horizontal span values for fitting the catenary.
        z: Vertical values corresponding to the horizontal span.
        height_a: The fixed height of the catenary at the start.
        height_b: The fixed height of the catenary at the end.
        span_length: The horizontal distance between the fixed endpoints.
        method: The optimization method for fitting. Defaults to 'nelder-mead'.

    Returns:
        The catenary curvature parameter for the optimal fit.

    Raises:
        AssertionError: When any of the parameters are of complex type.
    """
    try:
        real_kwargs = dict(s=s, z=z, height_a=height_a, height_b=height_b, span_length=span_length)
        assert all([np.isrealobj(v) for k, v in real_kwargs.items()])
    except AssertionError as e:
        raise ComplexUnsupportedError(complex_error_message(**real_kwargs), e) from e

    # define the error function
    def calc_error(curvature):
        z_model = catenary(
            s=s,
            curvature=curvature,
            height_a=height_a,
            height_b=height_b,
            span_length=span_length,
        )
        error = np.sqrt(np.sum([(z - z_model) ** 2]))
        return error

    # guess the curvature
    curvature_guess = 5.0 * span_length

    # use scipy minimize to optimize for the catenary curvature
    curvature_fit = minimize(calc_error, curvature_guess, method=method)["x"][0]

    return curvature_fit


def fit_blowout_angle(
    points: NDArray[float_],
    end_point_a: NDArray[float_],
    end_point_b: NDArray[float_],
) -> float:
    """
    Determine the optimal blowout angle for a set of 3D points. This function calculates the rotation angle needed
    to align a set of points with a catenary curve, considering the points' mean location and the axis formed by the
    catenary's endpoints.

    Args:
        points: 3D points for deriving the optimal catenary fit.
        end_point_a: One fixed endpoint of the catenary.
        end_point_b: The other fixed endpoint of the catenary.

    Returns:
        The blowout angle in radians.

    Raises:
        AssertionError: When any of the inputs are of complex type.
    """
    try:
        real_kwargs = dict(points=points, end_point_a=end_point_a, end_point_b=end_point_b)
        assert all([np.isrealobj(v) for k, v in real_kwargs.items()])
    except AssertionError as e:
        raise ComplexUnsupportedError(complex_error_message(**real_kwargs), e) from e

    # calculate the mean point
    point_mean = np.mean(points, axis=0)

    # project this point onto the end-to-end axis
    point_mean_projected = project_onto_axis(np.array([point_mean]), end_point_a, end_point_b)[0]

    # calculate the vector from the projected point to the mean point
    vector_diff = point_mean - point_mean_projected

    # solve for the rotation angle that maximizes the -z-compnent of the difference vector
    def rotated_vector_z(angle):
        rotation_axis = end_point_b - end_point_a
        vector_diff_rotated = rotate(vector_diff, angle=-angle, axis=rotation_axis)
        return vector_diff_rotated[2]

    return minimize(rotated_vector_z, 0.0, method="nelder-mead")["x"][0]


def fit_catenary_end(
    end_point: NDArray[float_],
    points: NDArray[float_],
    span_length: float_,
    z_offset: float_,
) -> NDArray[float_]:
    """
    Determine the opposite end point of a catenary from a given end point. This function calculates the position of the
    other end of a catenary, given one end point, a set of 3D points, the span length, and a vertical offset.

    Args:
        end_point: One fixed endpoint of the catenary.
        points: 3D points for deriving the catenary's other endpoint.
        span_length: The horizontal distance between the endpoints.
        z_offset: The vertical offset from the horizontal plane.

    Returns:
        The position of the opposite end of the catenary.

    Raises:
        AssertionError: When any of the inputs are of complex type.
    """
    try:
        real_kwargs = dict(
            end_point=end_point,
            points=points,
            span_lengh=span_length,
            z_offset=z_offset,
        )
        assert all([np.isrealobj(v) for k, v in real_kwargs.items()])
    except AssertionError as e:
        raise ComplexUnsupportedError(complex_error_message(**real_kwargs), e) from e

    # project the points onto the xy-plane coincident with the given end point
    points_xy = points * (X_AXIS + Y_AXIS) + end_point[2] * Z_AXIS

    # calculate the direction to the other endpoint
    span_direction = unit(np.mean(points_xy, axis=0) - end_point)

    return end_point + z_offset + span_length * span_direction


def fit_catenary_3d(
    points: NDArray[float_], end_point_a: NDArray[float_], end_point_b: NDArray[float_], method: str = "nelder-mead"
):
    """
    Optimize the blowout angle and catenary curvature to fit a set of 3D points. This function finds the angle and
    curvature that best represent the catenary curve fitting the given points, using the rotation about the axis formed
    from 'end_point_a' to 'end_point_b'.

    Args:
        points: The 3D points to fit the catenary to.
        end_point_a: One fixed end of the catenary.
        end_point_b: The other fixed end of the catenary.
        method: The optimization method to use.

    Returns:
        A tuple containing the optimized blowout angle and catenary curvature parameter.

    Raises:
        AssertionError: If any of the input parameters are complex.
    """
    try:
        real_kwargs = dict(points=points, end_point_a=end_point_a, end_point_b=end_point_b)
        assert all([np.isrealobj(v) for k, v in real_kwargs.items()])
    except AssertionError as e:
        raise ComplexUnsupportedError(complex_error_message(**real_kwargs), e) from e

    # fit the blowout angle beta
    blowout_angle_fit = fit_blowout_angle(points, end_point_a, end_point_b)

    # rotate the points by the blowout angle
    rotation_axis = end_point_b - end_point_a
    points_rotated = rotate(points, -blowout_angle_fit, point=end_point_a, axis=rotation_axis)

    # calculate the parametric value; distance in the tower-to-tower axis in the xy-plane
    xy_span = mag(points_rotated[:, :2] - end_point_a[:2])

    # fit 3d catenary curvature
    curvature_fit = fit_catenary(
        xy_span,
        points_rotated[:, 2],
        height_a=end_point_a[2],
        height_b=end_point_b[2],
        span_length=mag(end_point_b[:2] - end_point_a[:2]),
        method=method,
    )

    return blowout_angle_fit, curvature_fit


def fit_curvature_from_length(end_point_a: NDArray[float_], end_point_b: NDArray[float_], length: float) -> float:
    """
    Determine the catenary curvature parameter given the end points and the length of the conductor. This function
    calculates the curvature parameter that matches the given conductor length between the specified end points.

    Args:
        end_point_a: One end point of the conductor.
        end_point_b: The other end point of the conductor.
        length: The total length of the conductor.

    Returns:
        The catenary curvature parameter that fits the given conductor length.

    Raises:
        AssertionError: If the end points are complex.
    """
    span_length = mag((end_point_b - end_point_a) * (X_AXIS + Y_AXIS))

    def length_error(curvature: float):
        fit_length = catenary_length(
            curvature=curvature,
            height_a=end_point_a[2],
            height_b=end_point_b[2],
            span_length=span_length,
        )
        return (fit_length - length) ** 2

    curvature_guess = 3.0 * mag(end_point_b - end_point_a)

    return minimize(length_error, curvature_guess, method="nelder-mead")["x"][0]
