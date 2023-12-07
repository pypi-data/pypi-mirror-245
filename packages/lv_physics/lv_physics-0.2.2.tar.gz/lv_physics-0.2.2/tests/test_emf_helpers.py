from collections import OrderedDict
from dataclasses import replace

import numpy as np

from lv_physics.emf.emf_const_objects import EMF_MEASUREMENT_1
from lv_physics.emf.helpers import (
    EMFDimension,
    EMFFaceCorners,
    correct_polaris_upside_downness,
    gen_missing_plane_point,
    gen_opposite_face_points,
)


def test_correct_polaris_upside_downness():
    corrected_meas_should_be = replace(EMF_MEASUREMENT_1, phasey=np.pi, phasez=5 * np.pi / 4)

    assert corrected_meas_should_be == correct_polaris_upside_downness(EMF_MEASUREMENT_1)


def test_gen_missing_plane_point():
    displacement_vector = np.array([1.2, 2.3, 3.4])

    test_corner_points = (
        np.array([[0.0, 0.0, 0.0], [0.0, 1.0, 0.0], [1.0, 1.0, 0.0]], dtype=np.float_) + displacement_vector
    )

    missing_plane_point_should_be = np.array([1.0, 0.0, 0.0]) + displacement_vector

    missing_plane_point = gen_missing_plane_point(test_corner_points)

    assert np.allclose(missing_plane_point, missing_plane_point_should_be)


def test_gen_opposite_face_points():
    face_points = np.array(
        [[0.0, 1.0, 0.0], [0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0]],
        dtype=np.float_,
    )

    # an EMFSensor laying on its back (and with the wrong dimensions, shhhhhh)
    corner_point_dict = {corner_name: face_points[i] for i, corner_name in enumerate(EMFFaceCorners.FRONT.value)}
    back_face_points_results = gen_opposite_face_points(
        face_name=EMFFaceCorners.FRONT.name,
        corner_points=OrderedDict(corner_point_dict),
    )
    back_face_points = np.array(list(back_face_points_results[1].values()), dtype=np.float_)
    back_face_points_should_be = np.array(
        [
            [1.0, 1.0, -EMFDimension.DEPTH.value],
            [1.0, 0.0, -EMFDimension.DEPTH.value],
            [0.0, 0.0, -EMFDimension.DEPTH.value],
            [0.0, 1.0, -EMFDimension.DEPTH.value],
        ],
        dtype=np.float_,
    )

    assert np.allclose(np.array(back_face_points), back_face_points_should_be)

    # as if it were a right face
    corner_point_dict = {corner_name: face_points[i] for i, corner_name in enumerate(EMFFaceCorners.RIGHT.value)}
    right_face_points_results = gen_opposite_face_points(
        face_name=EMFFaceCorners.RIGHT.name,
        corner_points=OrderedDict(corner_point_dict),
    )
    left_face_points = np.array(list(right_face_points_results[1].values()), dtype=np.float_)
    left_face_points_should_be = np.array(
        [
            [1.0, 1.0, -EMFDimension.WIDTH.value],
            [1.0, 0.0, -EMFDimension.WIDTH.value],
            [0.0, 0.0, -EMFDimension.WIDTH.value],
            [0.0, 1.0, -EMFDimension.WIDTH.value],
        ],
        dtype=np.float_,
    )

    assert np.allclose(left_face_points, left_face_points_should_be)

    # as if it were a top face
    corner_point_dict = {corner_name: face_points[i] for i, corner_name in enumerate(EMFFaceCorners.TOP.value)}
    bottom_face_points_results = gen_opposite_face_points(
        face_name=EMFFaceCorners.TOP.name, corner_points=OrderedDict(corner_point_dict)
    )
    bottom_face_points = np.array(list(bottom_face_points_results[1].values()), dtype=np.float_)
    bottom_face_points_should_be = np.array(
        [
            [0.0, 0.0, -EMFDimension.HEIGHT.value],
            [0.0, 1.0, -EMFDimension.HEIGHT.value],
            [1.0, 1.0, -EMFDimension.HEIGHT.value],
            [1.0, 0.0, -EMFDimension.HEIGHT.value],
        ],
        dtype=np.float_,
    )

    assert np.allclose(bottom_face_points, bottom_face_points_should_be)
