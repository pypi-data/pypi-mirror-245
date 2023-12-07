import numpy as np
import pytest

from lv_physics.core.catenaries import (
    catenary,
    catenary_3d,
    catenary_sag,
    fit_blowout_angle,
    fit_catenary,
    fit_catenary_3d,
    fit_catenary_end,
    gen_catenary_3d,
)
from lv_physics.core.rotations import rotate
from lv_physics.core.vectors import X_AXIS, Y_AXIS, Z_AXIS, mag
from lv_physics.utils.helpers import ComplexUnsupportedError


N_POINTS = 1000
HEIGHT = 10.0
SPAN_LENGTH = 50.0
END_POINT_A = np.array([0.0, 0.0, HEIGHT])
END_POINT_B = np.array([0.0, SPAN_LENGTH, HEIGHT])
END_POINT_C = END_POINT_B + 3 * Z_AXIS
CURVATURE = 5 * SPAN_LENGTH
BLOWOUT_ANGLE = np.pi / 16
SPAN_POINTS = np.linspace(END_POINT_A, END_POINT_B, N_POINTS)


def test_catenary():
    """
    Tests the 1d catenary function.
    """
    # test unsupported compelx error message
    kwargs = dict(
        s=np.linspace(0, SPAN_LENGTH, 10) + 1.0j,
        curvature=CURVATURE + 1.0j,
        height_a=END_POINT_A[2] + 1.0j,
        height_b=END_POINT_B[2] + 1.0j,
        span_length=SPAN_LENGTH + 1.0j,
    )
    with pytest.raises(ComplexUnsupportedError):
        catenary(**kwargs)

    # generate a simple catenary
    s_cat = np.linspace(END_POINT_A[1], END_POINT_B[1], N_POINTS)
    z_cat = catenary(s_cat, CURVATURE, END_POINT_A[2], END_POINT_B[2], SPAN_LENGTH)

    # make most basic catenary assertions
    assert z_cat[0] == END_POINT_A[2]
    assert z_cat[-1] == END_POINT_B[2]
    assert (z_cat <= END_POINT_A[2]).all()


def test_catenary_sag():
    """
    Tests the calculation of the catenary sag.
    """
    # test unsupported compelx error message
    kwargs = dict(
        curvature=CURVATURE + 1.0j,
        height_a=END_POINT_A[2] + 1.0j,
        height_b=END_POINT_C[2] + 1.0j,
        span_length=SPAN_LENGTH + 1.0j,
    )
    with pytest.raises(ComplexUnsupportedError):
        catenary_sag(**kwargs)

    # generate a simple catenary
    s_cat = np.linspace(END_POINT_A, END_POINT_C, 100 * N_POINTS)
    z_cat = catenary(s_cat[:, 1], CURVATURE, END_POINT_A[2], END_POINT_C[2], SPAN_LENGTH)
    numerical_sag = np.max(s_cat[:, 2] - z_cat)

    # make simple sag calculation
    sag = catenary_sag(CURVATURE, END_POINT_A[2], END_POINT_C[2], SPAN_LENGTH)

    # assert roughly equivalent values; there is no gauruntee that numerical value will be at point of max sag
    assert np.abs(sag - numerical_sag) / sag < 0.01


def test_catenary_3d():
    """
    Tests the 3d catenary function.
    """
    # test unsupported compelx error message
    kwargs = dict(
        span_points=SPAN_POINTS,
        curvature=CURVATURE + 1.0j,
        end_point_a=END_POINT_A + 1.0j,
        end_point_b=END_POINT_B + 1.0j,
    )
    with pytest.raises(ComplexUnsupportedError):
        catenary_3d(**kwargs)

    # generate a simple catenary
    s_cat = np.linspace(END_POINT_A[1], END_POINT_B[1], N_POINTS)
    z_cat = catenary(s_cat, CURVATURE, END_POINT_A[2], END_POINT_B[2], SPAN_LENGTH)

    # generate a catenary in 3d
    cat_points = catenary_3d(SPAN_POINTS, CURVATURE, END_POINT_A, END_POINT_B)

    # shift and rotate the catenary, and generate a new catenary to match it
    trans_cat_points = rotate(cat_points, np.pi / 8, axis=Z_AXIS, point=3 * X_AXIS) - 3 * Z_AXIS
    new_span_points = np.linspace(trans_cat_points[0], trans_cat_points[-1], N_POINTS)
    new_cat_points = catenary_3d(new_span_points, CURVATURE, trans_cat_points[0], trans_cat_points[-1])

    assert np.allclose(cat_points[:, 2], z_cat)
    assert np.allclose(trans_cat_points, new_cat_points)


def test_gen_catenary_3d():
    """
    Tests the generate catenary 3d convenience function.
    """
    # test unsupported compelx error message
    kwargs = dict(
        n_points=N_POINTS + 1.0j,
        curvature=CURVATURE + 1.0j,
        end_point_a=END_POINT_A + 1.0j,
        end_point_b=END_POINT_B + 1.0j,
    )
    with pytest.raises(ComplexUnsupportedError):
        gen_catenary_3d(**kwargs)

    # generate a catenary to check against
    cat_points = catenary_3d(
        SPAN_POINTS,
        curvature=CURVATURE,
        end_point_a=END_POINT_A,
        end_point_b=END_POINT_B,
    )

    # generate a catenary using the method to test
    gen_points = gen_catenary_3d(N_POINTS, curvature=CURVATURE, end_point_a=END_POINT_A, end_point_b=END_POINT_B)

    assert np.allclose(cat_points, gen_points)
    assert np.allclose(gen_points[0], END_POINT_A)
    assert np.allclose(gen_points[-1], END_POINT_B)


def test_fit_catenary():
    """
    Tests the fit catenary function.
    """
    # test unsupported compelx error message
    kwargs = dict(
        s=SPAN_POINTS[:, 1] + 1.0j,
        z=SPAN_POINTS[:, 2] + 1.0j,
        height_a=HEIGHT + 1.0j,
        height_b=HEIGHT + 1.0j,
        span_length=SPAN_LENGTH + 1.0j,
    )
    with pytest.raises(ComplexUnsupportedError):
        fit_catenary(**kwargs)

    # create a set of points, using the ends and one point between
    mid = int(N_POINTS / 2)
    mid_point = SPAN_POINTS[mid]
    span_points = np.array([END_POINT_A, mid_point, END_POINT_B])

    # create a model catenary to check against
    z_cat_model = catenary(
        span_points[:, 1],
        CURVATURE,
        height_a=END_POINT_A[2],
        height_b=END_POINT_B[2],
        span_length=SPAN_LENGTH,
    )

    # fit a catenary to this point
    curvature_fit = fit_catenary(
        span_points[:, 1],
        z_cat_model,
        height_a=END_POINT_A[2],
        height_b=END_POINT_B[2],
        span_length=SPAN_LENGTH,
    )

    assert np.allclose(curvature_fit, CURVATURE)


def test_fit_blowout_angle():
    """
    Tests the fit blowout angle function.
    """
    # test unsupported compelx error message
    kwargs = dict(
        points=SPAN_POINTS[:, 1] + 1.0j,
        end_point_a=END_POINT_A,
        end_point_b=END_POINT_B,
    )
    with pytest.raises(ComplexUnsupportedError):
        fit_blowout_angle(**kwargs)

    # create a model catenary to check against
    cat_points = catenary_3d(SPAN_POINTS, CURVATURE, END_POINT_A, END_POINT_B)

    # rotate rotate an angle
    rotation_axis = END_POINT_B - END_POINT_A
    cat_points_rotated = rotate(cat_points, BLOWOUT_ANGLE, axis=rotation_axis, point=END_POINT_A)

    # solve for the rotation angle
    blowout_angle_fit = fit_blowout_angle(cat_points_rotated, END_POINT_A, END_POINT_B)

    assert np.abs(blowout_angle_fit - BLOWOUT_ANGLE) / BLOWOUT_ANGLE < 0.001


def test_fit_catenary_end():
    """
    Tests the fit_catenary_end function.
    """
    # test unsupported compelx error message
    kwargs = dict(
        end_point=END_POINT_A + 1.0j,
        points=SPAN_POINTS[:, 1] + 1.0j,
        span_length=1.0,
        z_offset=1.0,
    )
    with pytest.raises(ComplexUnsupportedError):
        fit_catenary_end(**kwargs)

    # create a model catenary to check against
    cat_points = gen_catenary_3d(N_POINTS, curvature=CURVATURE, end_point_a=END_POINT_A, end_point_b=END_POINT_B)

    # take only some of the points
    span_points = cat_points[int(N_POINTS / 5) : int(N_POINTS / 2)]

    # calculate the span length and vertical offset
    end_point_a_xy = END_POINT_A * (X_AXIS + Y_AXIS)
    end_point_b_xy = END_POINT_B * (X_AXIS + Y_AXIS)
    span_length = mag(end_point_b_xy - end_point_a_xy)
    z_offset = END_POINT_B[2] - END_POINT_A[2]

    # find the missing end point
    missing_end_point = fit_catenary_end(END_POINT_A, span_points, span_length, z_offset)

    assert np.allclose(missing_end_point, END_POINT_B)


def test_fit_catenary_3d():
    """
    Tests the fit catenary 3d function.
    """
    # test unsupported compelx error message
    kwargs = dict(
        points=SPAN_POINTS[:, 1] + 1.0j,
        end_point_a=END_POINT_A,
        end_point_b=END_POINT_B,
    )
    with pytest.raises(ComplexUnsupportedError):
        fit_catenary_3d(**kwargs)

    # create a model catenary to check against
    cat_points = catenary_3d(SPAN_POINTS, CURVATURE, END_POINT_A, END_POINT_B)

    # rotate rotate an angle
    rotation_axis = END_POINT_B - END_POINT_A
    cat_points_rotated = rotate(cat_points, BLOWOUT_ANGLE, axis=rotation_axis, point=END_POINT_A)

    # fit catenary 3d
    blowout_angle_fit, curvature_fit = fit_catenary_3d(cat_points_rotated, END_POINT_A, END_POINT_B)

    assert np.abs(blowout_angle_fit - BLOWOUT_ANGLE) / BLOWOUT_ANGLE < 0.001
    assert np.allclose(curvature_fit, CURVATURE)
