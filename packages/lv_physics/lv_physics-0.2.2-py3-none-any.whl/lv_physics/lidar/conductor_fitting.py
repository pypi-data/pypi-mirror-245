from copy import deepcopy
from typing import List

import numpy as np
from numpy import float_
from numpy.typing import NDArray
from scipy.optimize import Bounds, minimize

from lv_physics.core.catenaries import catenary_3d
from lv_physics.core.dynamic_objects import Conductor
from lv_physics.core.rotations import rotate
from lv_physics.core.vectors import X_AXIS, Y_AXIS, mag, project_onto_axis
from lv_physics.lidar.fitting_helpers import (
    ALPHA_BOUND,
    BETA_BOUND,
    CURVATURE_BOUND_FACTOR,
    GAMMA_BOUND,
    clean_scan,
    estimate_bounds_and_values,
    get_bounds_and_values,
    split_bounds,
    split_values,
)
from lv_physics.lidar.objects import ConductorFit


def fit_and_set_conductor(
    conductor_md: Conductor,
    scan: NDArray[float_],
    fit_type: str = "2-step",
    bounds: Bounds = None,
    init_values: List = None,
    iterate: bool = False,
    clean: bool = True,
):
    conductor = deepcopy(conductor_md)

    if len(scan) < 10:
        conductor_fits = [ConductorFit()]

    else:
        if clean is True:
            scan_points = clean_scan(float_(scan))
        else:
            scan_points = scan

        if fit_type.lower() == "1-step":
            conductor_fits = fit_conductor_4d(
                conductor_md,
                scan_points,
                bounds=bounds,
                init_values=init_values,
                iterate=iterate,
            )

        elif fit_type.lower() == "2-step":
            conductor_fits = fit_conductor_2_step(
                conductor_md,
                scan_points,
                bounds=bounds,
                init_values=init_values,
                iterate=iterate,
            )

        elif fit_type.lower() == "forced":
            conductor_fits = fit_conductor_forced_insulator(
                conductor_md=conductor_md,
                scan=scan_points,
                bounds=bounds,
                init_values=init_values,
            )

        else:
            conductor_fits = [ConductorFit()]

        conductor.set_points(len(conductor_md.points))
        conductor.set_blowout(conductor_fits[-1].beta)
        conductor.set_curvature(conductor_fits[-1].curvature)
        conductor.set_insulator(0, angles=[conductor_fits[-1].alpha, conductor_fits[-1].gamma])

    return conductor, conductor_fits


def fit_conductor_4d(
    conductor_md: Conductor,
    scan: NDArray[float_],
    bounds: List = None,
    init_values: List = None,
    iterate: bool = False,
):
    """
    Returns the insulator orientation angles (alpha, gamma), conductor blowout angle (beta), and the
    catenary curvature constant (c) fit to a set of (N x 3)-points, fit to the geometry defined in the
    conductor object.
    """
    conductor_fits_4d = []

    def fit_error_4d(fit_params_4d):
        alpha, beta, gamma, curvature = fit_params_4d

        # create a conductor that hangs vertically with no blowout
        conductor_f = deepcopy(conductor_md)
        conductor_f.set_points(0)
        conductor_f.set_curvature(curvature)
        conductor_f.set_insulator(0, angles=[alpha, gamma])

        # rotate the scan points underneath the conductor
        scan_rotated = rotate(
            scan,
            angle=-beta,
            axis=conductor_f.connect_axis,
            point=conductor_f.connects[0],
        )

        # project the scan points onto the xy-plane
        scan_rotated_xy = project_onto_axis(
            scan_rotated,
            conductor_f.end_points[0] * (X_AXIS + Y_AXIS),
            conductor_f.end_points[1] * (X_AXIS + Y_AXIS),
        )

        # use the positions of those points to get catenary values
        fit_points = catenary_3d(
            scan_rotated_xy,
            curvature=curvature,
            end_point_a=conductor_f.connects[0],
            end_point_b=conductor_f.connects[1],
        )

        # calculate the mean distance squared to points
        distance = np.median(mag(fit_points - scan_rotated))

        # write to the conductor fits list
        conductor_fits_4d.append(
            ConductorFit(
                alpha=alpha,
                beta=beta,
                gamma=gamma,
                curvature=curvature,
                error=distance,
            )
        )

        return 1e6 * distance**2

    # initialize values and bounds if not provided
    if init_values is None:
        init_values = [0.01, 0.01, 0.01, conductor_md.curvature]

    if bounds is None:
        bounds = Bounds(
            lb=[
                -ALPHA_BOUND,
                -BETA_BOUND,
                -GAMMA_BOUND,
                conductor_md.curvature - CURVATURE_BOUND_FACTOR * conductor_md.curvature,
            ],
            ub=[
                +ALPHA_BOUND,
                +BETA_BOUND,
                +GAMMA_BOUND,
                conductor_md.curvature + CURVATURE_BOUND_FACTOR * conductor_md.curvature,
            ],
        )

    # use minimize to solve for the conductor shape
    _ = minimize(
        fit_error_4d,
        init_values,
        bounds=bounds,
        method="nelder-mead",
    )

    # iterative running
    if iterate is True:
        bounds, init_values = get_bounds_and_values(conductor_fits_4d[-1])

        _ = minimize(
            fit_error_4d,
            init_values,
            bounds=bounds,
            method="nelder-mead",
        )

    return np.array(conductor_fits_4d)


def fit_conductor_2_step(
    conductor_md: Conductor,
    scan: NDArray[float_],
    bounds: Bounds = None,
    init_values: List = None,
    iterate: bool = False,
):
    if bounds is None or init_values is None:
        bounds, init_values = estimate_bounds_and_values(conductor_md, scan)

    blowout_bounds = None
    curvature_bounds = None
    if bounds is not None:
        blowout_bounds, curvature_bounds = split_bounds(bounds)

    blowout_values = None
    curvature_value = None
    if init_values is not None:
        blowout_values, curvature_value = split_values(init_values)

    blowout_fits = fit_conductor_blowout(
        conductor_md,
        scan,
        bounds=blowout_bounds,
        init_values=blowout_values,
        iterate=False,
    )

    catenary_fits = fit_conductor_catenary(
        conductor_md,
        scan,
        blowout_angles=[
            blowout_fits[-1].alpha,
            blowout_fits[-1].beta,
            blowout_fits[-1].gamma,
        ],
        bounds=curvature_bounds,
        init_value=curvature_value,
        iterate=False,
    )

    conductor_fits = np.concatenate([blowout_fits, catenary_fits])

    if iterate is True:
        bounds, init_values = get_bounds_and_values(conductor_fits[-1])

        conductor_fits_2 = fit_conductor_2_step(
            conductor_md,
            scan,
            bounds=bounds,
            init_values=init_values,
            iterate=False,
        )

        conductor_fits = np.concatenate([conductor_fits, conductor_fits_2])

    return conductor_fits


def fit_conductor_blowout(
    conductor_md: Conductor,
    scan: NDArray[float_],
    bounds: Bounds = None,
    init_values: List[float] = None,
    iterate: bool = False,
):
    blowout_fits: List[ConductorFit] = []

    def blowout_fit_error(blowout_fit_params):
        alpha, beta, gamma = blowout_fit_params

        # create a copy of the conductor to manipulate
        conductor_f = deepcopy(conductor_md)
        conductor_f.set_blowout(0.0)
        conductor_f.set_insulator(0, angles=[alpha, gamma], fix_length=False)

        # rotate the scan points underneath the conductor
        scan_rotated = rotate(
            scan,
            angle=-beta,
            axis=conductor_f.connect_axis,
            point=conductor_f.connects[0],
        )

        # project the scan points onto the xy-plane
        scan_rotated_xy = scan_rotated * (X_AXIS + Y_AXIS)

        # project the connect points onto the xy-plane
        connect_points_xy = conductor_f.connects * (X_AXIS + Y_AXIS)

        # project the xy-plane scan points to the xy-plane connect axis
        scan_projected_xy = project_onto_axis(
            scan_rotated_xy,
            connect_points_xy[0],
            connect_points_xy[1],
        )

        # calculate the mean distance squared to points
        distance_xy = np.median(mag(scan_rotated_xy - scan_projected_xy))

        # write to the conductor_fits list
        blowout_fits.append(
            ConductorFit(
                alpha=alpha,
                beta=beta,
                gamma=gamma,
                error=distance_xy,
            )
        )

        return 1e6 * distance_xy**2

    # initialize values and bounds if not provided
    if init_values is None:
        init_values = [0.01, 0.01, 0.01]

    if bounds is None:
        bounds = Bounds(
            lb=[-ALPHA_BOUND, -BETA_BOUND, -GAMMA_BOUND],
            ub=[+ALPHA_BOUND, +BETA_BOUND, +GAMMA_BOUND],
        )

    # use minimize to solve for the conductor shape
    _ = minimize(
        blowout_fit_error,
        init_values,
        bounds=bounds,
        method="nelder-mead",
    )

    # iterative running
    if iterate is True:
        bounds, init_values = get_bounds_and_values(blowout_fits[-1])
        blowout_bounds, _ = split_bounds(bounds)
        blowout_values, _ = split_values(init_values)

        _ = minimize(
            blowout_fit_error,
            blowout_values,
            bounds=blowout_bounds,
            method="nelder-mead",
        )

    return np.array(blowout_fits)


def fit_conductor_catenary(
    conductor_md: Conductor,
    scan: NDArray[float_],
    blowout_angles: NDArray[float_] = np.zeros(3, float_),
    bounds: Bounds = None,
    init_value: float = None,
    iterate: bool = False,
):
    catenary_fits: List[ConductorFit] = []

    def catenary_fit_error(curvature):
        alpha, beta, gamma = blowout_angles

        # create a copy of the conductor to manipulate
        conductor_f = deepcopy(conductor_md)
        conductor_f.set_insulator(0, angles=[alpha, gamma], fix_length=False)

        # rotate the scan points underneath the conductor
        scan_rotated = rotate(
            scan,
            angle=-beta,
            axis=conductor_f.connect_axis,
            point=conductor_f.connects[0],
        )

        # provide the projected points with a catenary value in the z-axis
        scan_cat = catenary_3d(
            scan_rotated,
            curvature=curvature[0],
            end_point_a=conductor_f.connects[0],
            end_point_b=conductor_f.connects[1],
        )

        # calculate the mean distance squared to points
        distance = np.median(mag(scan_cat - scan_rotated))

        # write to the conductor_fits list
        catenary_fits.append(
            ConductorFit(
                alpha=alpha,
                beta=beta,
                gamma=gamma,
                curvature=curvature[0],
                error=distance,
            )
        )

        return 1e6 * distance**2

    # initialize values and bounds if not provided
    if init_value is None:
        init_value = conductor_md.curvature

    if bounds is None:
        bounds = Bounds(
            lb=init_value - CURVATURE_BOUND_FACTOR * init_value,
            ub=init_value + CURVATURE_BOUND_FACTOR * init_value,
        )

    # use minimize to solve for the conductor shape
    _ = minimize(
        catenary_fit_error,
        init_value,
        bounds=bounds,
        method="nelder-mead",
    )

    # iterative running
    if iterate is True:
        bounds, init_values = get_bounds_and_values(catenary_fits[-1])
        _, curvature_bounds = split_bounds(bounds)
        _, curvature_value = split_values(init_values)

        _ = minimize(
            catenary_fit_error,
            curvature_value,
            bounds=curvature_bounds,
            method="nelder-mead",
        )

    return np.array(catenary_fits)


def fit_conductor_forced_insulator(
    conductor_md: Conductor,
    scan: NDArray[float],
    bounds: List = None,
    init_values: List = None,
):
    """
    Returns the insulator and conductor blowout fit.
    """
    conductor_fits = []

    global m
    m = 0

    def fit_error_forced(fit_params):
        global m

        beta, curvature = fit_params

        # create a conductor that hangs vertically with no blowout
        conductor_f = deepcopy(conductor_md)
        conductor_f.set_points(0)
        conductor_f.set_curvature(curvature)
        conductor_f.set_insulator(0, angles=[beta, 0.0])

        # rotate the scan points underneath the conductor
        scan_rotated = rotate(
            scan,
            angle=-beta,
            axis=conductor_f.connect_axis,
            point=conductor_f.connects[0],
        )

        # project the scan points onto the xy-plane
        scan_rotated_xy = project_onto_axis(
            scan_rotated,
            conductor_f.end_points[0] * (X_AXIS + Y_AXIS),
            conductor_f.end_points[1] * (X_AXIS + Y_AXIS),
        )

        # use the positions of those points to get catenary values
        fit_points = catenary_3d(
            scan_rotated_xy,
            curvature=curvature,
            end_point_a=conductor_f.connects[0],
            end_point_b=conductor_f.connects[1],
        )

        # calculate the mean distance squared to points
        distance = np.median(mag(fit_points - scan_rotated))

        # write to the conductor fits list
        conductor_fits.append(
            ConductorFit(
                alpha=beta,
                beta=beta,
                gamma=0.0,
                curvature=curvature,
                error=distance,
            )
        )

        m += 1

        return 1e6 * distance**2

    # initialize values and bounds if not provided
    if init_values is None:
        init_values = [0.01, conductor_md.curvature]

    if bounds is None:
        bounds = Bounds(
            lb=[
                -BETA_BOUND,
                conductor_md.curvature - CURVATURE_BOUND_FACTOR * conductor_md.curvature,
            ],
            ub=[
                +BETA_BOUND,
                conductor_md.curvature + CURVATURE_BOUND_FACTOR * conductor_md.curvature,
            ],
        )

    # use minimize to solve for the conductor shape
    _ = minimize(
        fit_error_forced,
        init_values,
        bounds=bounds,
        method="nelder-mead",
    )

    return np.array(conductor_fits)
