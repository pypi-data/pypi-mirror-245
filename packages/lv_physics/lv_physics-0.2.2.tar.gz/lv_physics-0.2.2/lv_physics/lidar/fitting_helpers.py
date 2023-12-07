from typing import List

import numpy as np
from numpy import float_
from numpy.typing import NDArray
from scipy.optimize import Bounds

from lv_physics.core.dynamic_objects import Conductor
from lv_physics.core.rotations import solve_rotation_angle
from lv_physics.core.vectors import Z_AXIS, project_onto_axis, unit
from lv_physics.lidar.objects import ConductorFit


ALPHA_BOUND = np.pi / 4
BETA_BOUND = np.pi / 4
GAMMA_BOUND = np.pi / 32
CURVATURE_BOUND_FACTOR = 1.0


def estimate_bounds_and_values(conductor_md: Conductor, scan: NDArray[float_]):
    # create a vector pointing from the axis of rotation to the scan
    scan_point = np.median(scan, axis=0)
    scan_point_proj = project_onto_axis(
        scan_point,
        conductor_md.insulators[0].pivot_point,
        conductor_md.insulators[1].pivot_point,
    )
    scan_vector = unit(scan_point - scan_point_proj)

    # determine what rotation would be move -z-axis to the scan vector
    beta_guess = solve_rotation_angle(-Z_AXIS, scan_vector, axis=conductor_md.connect_axis)[0]

    # init values
    init_values = [
        beta_guess / 2,
        beta_guess,
        0.0,
        conductor_md.curvature,
    ]

    # alpha bounds
    alpha_bounds = np.sort([0.0, beta_guess])

    # set bounds
    bounds = Bounds(
        lb=[
            alpha_bounds[0],
            init_values[1] - BETA_BOUND / 2,
            init_values[2] - GAMMA_BOUND / 2,
            init_values[3] - CURVATURE_BOUND_FACTOR * init_values[3] / 2,
        ],
        ub=[
            alpha_bounds[1],
            init_values[1] + BETA_BOUND / 2,
            init_values[2] + GAMMA_BOUND / 2,
            init_values[3] + CURVATURE_BOUND_FACTOR * init_values[3] / 2,
        ],
    )

    return bounds, init_values


def check_blowout_bounds(bounds: Bounds):
    pass


def get_bounds_and_values(conductor_fit: ConductorFit):
    values = [
        conductor_fit.alpha,
        conductor_fit.beta,
        conductor_fit.gamma,
        conductor_fit.curvature,
    ]

    bounds = Bounds(
        lb=[
            values[0] - ALPHA_BOUND / 2,
            values[1] - BETA_BOUND / 2,
            values[2] - GAMMA_BOUND / 2,
            values[3] - CURVATURE_BOUND_FACTOR * values[3] / 2,
        ],
        ub=[
            values[0] + ALPHA_BOUND / 2,
            values[1] + BETA_BOUND / 2,
            values[2] + GAMMA_BOUND / 2,
            values[3] + CURVATURE_BOUND_FACTOR * values[3] / 2,
        ],
    )

    return bounds, values


def split_bounds(bounds: Bounds):
    blowout_bounds = Bounds(
        lb=bounds.lb[:-1],
        ub=bounds.ub[:-1],
    )

    curvature_bounds = Bounds(
        lb=bounds.lb[-1],
        ub=bounds.ub[-1],
    )

    return blowout_bounds, curvature_bounds


def split_values(values: List):
    b_values = values[:-1]
    c_value = values[-1]

    return b_values, c_value


def clean_scan(scan: NDArray[float_]):
    # NOTE: I'm still unsure if this is needed
    from sklearn.cluster import DBSCAN

    yz = scan[:, 1:]

    db = DBSCAN(eps=0.25, min_samples=1).fit(yz)

    labels = db.labels_
    unique_labels = set(labels)
    n_unique = len(unique_labels)

    core_mask = np.zeros_like(labels, dtype=bool)
    core_mask[db.core_sample_indices_] = True

    scan_cleaned = np.zeros((n_unique, 3), dtype=float_)

    for m, c in enumerate(unique_labels):
        class_mask = labels == c
        clean_scan_points = scan[class_mask & core_mask]
        scan_cleaned[m] = np.median(clean_scan_points, axis=0)

    return scan_cleaned
