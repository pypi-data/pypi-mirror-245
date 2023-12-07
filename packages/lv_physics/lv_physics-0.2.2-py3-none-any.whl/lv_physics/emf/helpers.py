"""
This module provides helpers not directly related to core EMF model calculations, but necessary for legacy
software/hardware bugs, and auxilliary processes like 3D survey processing.
"""
from collections import OrderedDict as ordered_dict
from dataclasses import replace
from enum import Enum, unique
from typing import Dict, OrderedDict, Tuple

import numpy as np
import numpy.typing as npt
from scipy.optimize import minimize

from lv_physics.core.rotations import (
    apply_rotation,
    extrinsic_angles_zyx,
    extrinsic_rotation_matrix,
    rotate,
    rotate_frame,
)
from lv_physics.core.vectors import XYZ_FRAME, Z_AXIS, cross, mag, unit
from lv_physics.emf.emf_objects import EMFMeasurement, EMFSensor


EMF_CORNER_POINT_NAMES = [
    f"{a}_{b}_{c}" for a in ["front", "back"] for b in ["top", "bottom"] for c in ["left", "right"]
]


@unique
class EMFFaceCorners(Enum):
    """
    Enum for getting the unique corner names (in right-handed order) for an EMF sensor box face.
    """

    FRONT = [
        "front_top_right",
        "front_bottom_right",
        "front_bottom_left",
        "front_top_left",
    ]
    BACK = ["back_top_left", "back_bottom_left", "back_bottom_right", "back_top_right"]
    TOP = ["front_top_right", "front_top_left", "back_top_left", "back_top_right"]
    BOTTOM = [
        "front_bottom_left",
        "front_bottom_right",
        "back_bottom_right",
        "back_bottom_left",
    ]
    LEFT = ["front_top_left", "front_bottom_left", "back_bottom_left", "back_top_left"]
    RIGHT = [
        "back_top_right",
        "back_bottom_right",
        "front_bottom_right",
        "front_top_right",
    ]


class EMFDimension(Enum):
    """
    Simple Enum for storing the dimensions of the EMF sensor box.  All values are in meters.
    """

    HEIGHT = 0.270
    WIDTH = 0.220
    DEPTH = 0.177


EMF_FACE_NAME_PAIRS = [
    {EMFFaceCorners.FRONT.name, EMFFaceCorners.BACK.name},
    {EMFFaceCorners.TOP.name, EMFFaceCorners.BOTTOM.name},
    {EMFFaceCorners.LEFT.name, EMFFaceCorners.RIGHT.name},
]


# ----------------------------------------------------------------------------------------------------------------------
# DATA PIPELINE


def correct_polaris_upside_downness(meas: EMFMeasurement) -> EMFMeasurement:
    """
    Takes a measurement assumed to be from a Polaris device, which has a right-handed but "upside down" coordinate
    frame internally, and corrects the Y and Z coils.  If the Polaris were placed with its door facing along a +x
    direction in an EMFModelGroup coordinate frame, the X coil would agree with this coordinate frame in phase, but the
    Y and Z coils would be opposite internally with the model group coordinate frame.

    :param meas: the EMFMeasurement which came from an "upsidedown" polaris

    :returns: EMFMeasurement object with corrected BY and BZ phases
    """

    def shift_phase_angle(phase_angle: float):
        # keeps the angle in [0., +2pi) radians
        return (phase_angle + np.pi) % (2.0 * np.pi)

    return replace(
        meas,
        phasey=shift_phase_angle(meas.phasey),
        phasez=shift_phase_angle(meas.phasez),
    )


# ----------------------------------------------------------------------------------------------------------------------
# 3D SURVEY


def gen_missing_plane_point(
    corner_points: npt.NDArray[np.float_],
) -> npt.NDArray[np.float_]:
    """
    Solves for the missing corner point of the emf-sensor in the same plane as the corner points provided.

    :param corner_points: N-vector of length 3 of emf-sensor corner points

    :returns: NDArray - the missing corner point vector
    """
    # find the "special" corner for which the other two corners are perpendicular.
    ab_cross_mags = np.zeros(3, np.float_)

    for n in range(3):
        this_corner_point = corner_points[n]
        other_corner_points = np.concatenate([corner_points[:n], corner_points[n + 1 :]])

        a_vector = unit(other_corner_points[0] - this_corner_point)
        b_vector = unit(other_corner_points[1] - this_corner_point)

        ab_cross_mags[n] = mag(cross(a_vector, b_vector))

    special_corner_index = np.argmax(ab_cross_mags)
    special_corner_point = corner_points[special_corner_index]

    # the missing corner is the special corner, plus the displacement vectors to the
    # other two corners.
    other_corner_points = np.concatenate(
        [
            corner_points[:special_corner_index],
            corner_points[special_corner_index + 1 :],
        ]
    )
    displacement_vectors = other_corner_points - special_corner_point
    missing_corner_point = special_corner_point + np.sum(displacement_vectors, axis=0)

    return missing_corner_point


def get_emf_face_corner_from_corner_names(
    corners_dict: Dict[str, npt.NDArray[np.float_]]
) -> Tuple[str, OrderedDict[str, npt.NDArray]]:
    """
    Get the right face name and (right-handed-wise) sorted dictionary of corner names and their positions.

    :param corners_dict: Dict of corner name and corresponding points
    :returns: Tuple of the name of the face, and the corresponding sorted dictionary of corner names and points
    """
    corner_names = corners_dict.keys()
    emf_face_corner = None
    for efc in list(EMFFaceCorners):
        if set(corner_names) == set(efc.value):
            emf_face_corner = efc
    if emf_face_corner:
        sorted_corner_points = [corners_dict[corner_name] for corner_name in emf_face_corner.value]
        return emf_face_corner.name, ordered_dict(
            {emf_face_corner.value[i]: sorted_corner_points[i] for i in range(len(emf_face_corner.value))}
        )

    else:
        raise Exception("Got unrecognized face name; unable to get an EMFFaceCorners member")


def gen_opposite_face_points(
    face_name: str, corner_points: OrderedDict[str, npt.NDArray[np.float_]]
) -> Tuple[str, OrderedDict[str, npt.NDArray[np.float_]]]:
    """
    Takes a name of a face and the associated corner points and generates the points of the opposite face.  The NDArray
    points MUST be provided in right-handed order of points (i.e., if looking directly at the face, the points should
    be given in a counter-clockwise order).

    :param name: unique name of the sensor face, for determining the magnitude of translation to the new face points
    :param corner_points: OrderedDict of the corner point names and NDArray's of positions of those points
                            (right-handed order!)
    :returns: a Tuple of the same form as the inputs but for the opposite face (a name and ordered dict of corners
                points)
    """
    # find the face-name pair we're dealing with
    face_name_pair = next((name_pair for name_pair in EMF_FACE_NAME_PAIRS if face_name in name_pair), None)
    if not face_name_pair:
        raise Exception("Got unrecognized face name; unable to generate EMFSensor's corner points")

    # get the EMFFaceCorners member for the face we're dealing with
    efc = [efc for efc in EMFFaceCorners if efc.name == face_name][0]

    # get the opposite face's name
    opposite_face_name = tuple(face_name_pair - {face_name})[0]

    # TODO: surely this block could already be known/made available when checking for which face_name_pair it is above
    dimension = None  # just so mypy doesn't complain for now

    # FRONT, BACK
    if face_name_pair == EMF_FACE_NAME_PAIRS[0]:
        dimension = EMFDimension.DEPTH.value
    # TOP, BOTTOM
    elif face_name_pair == EMF_FACE_NAME_PAIRS[1]:
        dimension = EMFDimension.HEIGHT.value
    # LEFT, RIGHT
    else:
        dimension = EMFDimension.WIDTH.value

    points = np.array(list(corner_points.values()))
    # create vectors from the ordered points forming a plane
    a = points[1] - points[0]
    b = points[3] - points[0]

    # create a normal vector for the face
    normal_vector = unit(cross(a, b))

    # get EMFFaceCorners member for opposite face and translate to get its corner points
    opposite_efc = [efc for efc in EMFFaceCorners if efc.name == opposite_face_name][0]
    opposite_points = points - normal_vector * dimension

    # form a dict of the points with correct corner names using string replacement
    opposite_face_corner_names_unordered = ordered_dict(
        {
            corner_name.replace(face_name.lower(), opposite_face_name.lower()): opposite_points[i]
            for i, corner_name in enumerate(efc.value)
        }
    )

    # sort the dict to ordered dict matching the order of the associated EMFFaceCorners member value
    sorted_corner_points = ordered_dict(
        {corner_name: opposite_face_corner_names_unordered[corner_name] for corner_name in opposite_efc.value}
    )

    return opposite_face_name, sorted_corner_points


def gen_emf_ext_angs_and_position_from_corner_points(
    sensor_id: int,
    model_group_id: int,
    corner_points: Dict[str, npt.NDArray[np.float_]],
) -> EMFSensor:
    """
    Takes a sensor id and dictionary of named EMF corner points and creates an EMFSensor object, calculating the
    ext_angles and position using the corner point positions.

    :param sensor_id: integer ID of the sensor
    :param corner_points: a dictionary of corner point names and positions
    :returns: EMFSensor object with correct orientation and position
    """
    front_face_points = np.array(
        [corner_points[corner_name] for corner_name in EMFFaceCorners.FRONT.value],
        dtype=np.float_,
    )
    sensor_y = unit(front_face_points[3] - front_face_points[0])
    sensor_z = unit(front_face_points[0] - front_face_points[1])
    sensor_x = cross(sensor_y, sensor_z)

    corner_point_positions = np.array(list(corner_points.values()), dtype=np.float_)

    sensor_local_frame = np.array([sensor_x, sensor_y, sensor_z])
    sensor_rotation_mat = (sensor_local_frame @ np.linalg.inv(XYZ_FRAME)).T
    ext_angles_xyz = extrinsic_angles_zyx(sensor_rotation_mat)
    return EMFSensor(
        id=sensor_id,
        model_group_id=model_group_id,
        position=np.mean(corner_point_positions, axis=0),
        ext_angles=ext_angles_xyz,
    )


def rotate_emf_sensor_about_z(emf_sensor: EMFSensor, angle_about_z: float) -> EMFSensor:
    """
    Takes an EMFSensor and returns a copy of it with the position and ext_angles updated to account for a rotation
    about the Z axis.  This is a common operation when normalizing 3d survey coordinates to LineVision's coordinate
    conventions, specifically that the +Y direction is ~along the front span direction.

    :emf_sensor: EMFSensor object to be rotated
    :angle_about_z: the angle around Z axis which the survey frame is rotated by to get to LV's frame
    :returns: EMFSensor object with updated ext_angles and position
    """
    # calculate the new position of the sensor
    rotated_position = rotate(emf_sensor.position, angle_about_z, axis=Z_AXIS, point=np.zeros(3))

    # calculate the new orientation of the sensor
    ext_rotation_matrix = extrinsic_rotation_matrix(angles=emf_sensor.ext_angles, axes=[0, 1, 2], order=[2, 1, 0])
    sensor_frame = rotate_frame(ext_rotation_matrix, XYZ_FRAME)
    sensor_frame_rot = rotate(
        vectors=sensor_frame, angle=angle_about_z, axis=Z_AXIS
    )  # NOTE: possibly the negative angle is needed

    new_ext_rotation_matrix = (sensor_frame_rot @ np.linalg.inv(XYZ_FRAME)).T
    new_ext_angles = extrinsic_angles_zyx(new_ext_rotation_matrix)

    return replace(emf_sensor, position=rotated_position, ext_angles=new_ext_angles)


BASE_FRONT_FACE_POINTS = ordered_dict(
    {
        "front_top_right": np.array(
            [
                0.5 * EMFDimension.DEPTH.value,
                -0.5 * EMFDimension.WIDTH.value,
                0.5 * EMFDimension.HEIGHT.value,
            ],
            dtype=np.float_,
        ),
        "front_bottom_right": np.array(
            [
                0.5 * EMFDimension.DEPTH.value,
                -0.5 * EMFDimension.WIDTH.value,
                -0.5 * EMFDimension.HEIGHT.value,
            ],
            dtype=np.float_,
        ),
        "front_bottom_left": np.array(
            [
                0.5 * EMFDimension.DEPTH.value,
                0.5 * EMFDimension.WIDTH.value,
                -0.5 * EMFDimension.HEIGHT.value,
            ],
            dtype=np.float_,
        ),
        "front_top_left": np.array(
            [
                0.5 * EMFDimension.DEPTH.value,
                0.5 * EMFDimension.WIDTH.value,
                0.5 * EMFDimension.HEIGHT.value,
            ],
            dtype=np.float_,
        ),
    }
)

_, BASE_BACK_FACE_POINTS = gen_opposite_face_points("FRONT", BASE_FRONT_FACE_POINTS)

BASE_LEFT_FACE_POINTS = ordered_dict(
    {
        "front_top_left": np.array(
            [
                0.5 * EMFDimension.DEPTH.value,
                0.5 * EMFDimension.WIDTH.value,
                0.5 * EMFDimension.HEIGHT.value,
            ],
            dtype=np.float_,
        ),
        "front_bottom_left": np.array(
            [
                0.5 * EMFDimension.DEPTH.value,
                0.5 * EMFDimension.WIDTH.value,
                -0.5 * EMFDimension.HEIGHT.value,
            ],
            dtype=np.float_,
        ),
        "back_bottom_left": np.array(
            [
                -0.5 * EMFDimension.DEPTH.value,
                0.5 * EMFDimension.WIDTH.value,
                -0.5 * EMFDimension.HEIGHT.value,
            ],
            dtype=np.float_,
        ),
        "back_top_left": np.array(
            [
                -0.5 * EMFDimension.DEPTH.value,
                0.5 * EMFDimension.WIDTH.value,
                0.5 * EMFDimension.HEIGHT.value,
            ],
            dtype=np.float_,
        ),
    }
)

_, BASE_RIGHT_FACE_POINTS = gen_opposite_face_points("LEFT", BASE_LEFT_FACE_POINTS)

BASE_TOP_FACE_POINTS = ordered_dict(
    {
        "front_top_right": np.array(
            [
                0.5 * EMFDimension.DEPTH.value,
                -0.5 * EMFDimension.WIDTH.value,
                0.5 * EMFDimension.HEIGHT.value,
            ],
            dtype=np.float_,
        ),
        "front_top_left": np.array(
            [
                0.5 * EMFDimension.DEPTH.value,
                0.5 * EMFDimension.WIDTH.value,
                0.5 * EMFDimension.HEIGHT.value,
            ],
            dtype=np.float_,
        ),
        "back_top_left": np.array(
            [
                -0.5 * EMFDimension.DEPTH.value,
                0.5 * EMFDimension.WIDTH.value,
                0.5 * EMFDimension.HEIGHT.value,
            ],
            dtype=np.float_,
        ),
        "back_top_right": np.array(
            [
                -0.5 * EMFDimension.DEPTH.value,
                -0.5 * EMFDimension.WIDTH.value,
                0.5 * EMFDimension.HEIGHT.value,
            ],
            dtype=np.float_,
        ),
    }
)

_, BASE_BOTTOM_FACE_POINTS = gen_opposite_face_points("TOP", BASE_TOP_FACE_POINTS)


def correct_emf_face_annotations(
    face_name: str, annotated_points: OrderedDict[str, npt.NDArray[np.float_]]
) -> Tuple[float, Tuple[str, OrderedDict[str, npt.NDArray[np.float_]]]]:
    """
    Takes an EMF face name and set of corner points annotated from a 3d survey and "corrects" them based on the known
    dimensions of the EMF sensor's faces.

    :param face_name: the name of the annotated face
    :param annotated_points: an ordered dictionary (by right-handedness) of corner point names and their positions
    :returns: a new ordered dictionary of the corner point names and their corrected positions
    """
    if face_name == "FRONT":
        ideal_points = BASE_FRONT_FACE_POINTS
    elif face_name == "BACK":
        ideal_points = BASE_BACK_FACE_POINTS
    elif face_name == "LEFT":
        ideal_points = BASE_LEFT_FACE_POINTS
    elif face_name == "RIGHT":
        ideal_points = BASE_RIGHT_FACE_POINTS
    elif face_name == "TOP":
        ideal_points = BASE_TOP_FACE_POINTS
    elif face_name == "BOTTOM":
        ideal_points = BASE_BOTTOM_FACE_POINTS
    else:
        raise Exception(f"Got unknown face name: {face_name}; can't correct the annotation points")

    # in this function context, we mostly just want the points as arrays, the names aren't as useful anymore
    ideal_points_array = np.array(list(ideal_points.values()), dtype=np.float_)
    annotated_points_array = np.array(list(annotated_points.values()), dtype=np.float_)

    # this just takes our "ideal" face and translates it to be at the center point of the actual annotated face
    # we do this first before getting into the rotation part
    annotated_centroid_point = np.mean(annotated_points_array, axis=0)
    ideal_centroid_point = np.mean(ideal_points_array, axis=0)
    translation = annotated_centroid_point - ideal_centroid_point
    translated_ideal_points = ideal_points_array + translation
    translated_ideal_centroid = np.mean(translated_ideal_points, axis=0)

    # we're going to look for a rotation of the "ideal" face that is closest on average to the actual annotated face
    def point_match_error(angles):
        rotation_mat = extrinsic_rotation_matrix(angles, axes=[0, 1, 2], order=[2, 1, 0])
        rotated_pts = apply_rotation(rotation_mat, translated_ideal_points, point=translated_ideal_centroid)

        pts_diff = rotated_pts - annotated_points_array
        pts_diff_mag = mag(pts_diff)
        pts_err = np.sum(pts_diff_mag**2)

        return pts_err

    angles_min_results = minimize(point_match_error, [0.0, 0.0, 0.0], method="nelder-mead")
    error = angles_min_results["fun"]
    ext_angles = angles_min_results["x"]

    # we're going to use the "ideal" face for the actual points, since it has accurate dimensions, but with the
    # rotation that causes the best match to the annotated points
    final_rotation_mat = extrinsic_rotation_matrix(ext_angles, axes=[0, 1, 2], order=[2, 1, 0])
    final_pts = apply_rotation(final_rotation_mat, translated_ideal_points, point=translated_ideal_centroid)

    corrected_pts = ordered_dict({key: final_pts[i] for i, key in enumerate(ideal_points.keys())})

    return error, (face_name, corrected_pts)
