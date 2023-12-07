import numpy as np
from pytest import approx

from lv_physics.emf.emf_const_objects import (
    EMF_CIRCUIT_1,
    EMF_MODEL_GROUP_1,
    EMF_SENSOR_1,
)
from lv_physics.emf.emf_functions import (
    Phase,
    calc_h_matrix,
    calc_h_vector,
    stitch_conductor_phases,
)


def test_calc_h_vector():
    straight_overhead_conductor = np.linspace(
        np.array([0.0, -100.0, 2.0]), np.array([0.0, 100.0, 2.0]), 200, dtype=np.float_
    )
    sensor_position = np.array([0.0, 0.0, 0.0], dtype=np.float_)

    h_vector_from_straight_overhead = np.array([-1.0 + 0.0j, 0.0j, 0.0j], dtype=np.complex_)

    assert np.allclose(
        calc_h_vector(x=sensor_position, Y=straight_overhead_conductor),
        h_vector_from_straight_overhead,
        rtol=1e-03,
    )

    stitched_conds = stitch_conductor_phases(EMF_CIRCUIT_1)

    h_vector_from_a = calc_h_vector(x=EMF_SENSOR_1.position, Y=stitched_conds["A"], phase=Phase.A.value)
    h_vector_from_b = calc_h_vector(x=EMF_SENSOR_1.position, Y=stitched_conds["B"], phase=Phase.B.value)
    h_vector_from_c = calc_h_vector(x=EMF_SENSOR_1.position, Y=stitched_conds["C"], phase=Phase.C.value)

    # =================================A PHASE ASSERTIONS=================================
    # A phase is directly overhead so only has contribution in the X direction,
    # and 0 imag component since it's the A phase in snapshot when A is peak amplitude
    assert h_vector_from_a[1] == h_vector_from_a[2] == 0.0 + 0.0j
    assert h_vector_from_a[0].real == approx(-0.14041287)
    assert h_vector_from_a[0].imag == 0.0

    # =================================B & C ASSERTIONS===================================
    # B and C are same distance apart in opposite directions, so there is a natural symmetry
    # both in their vectoral directions and the "phase-ness" timing in the A-peak snapshot

    # their real components are equivalent in X
    assert h_vector_from_b[0].real == approx(h_vector_from_c[0].real) == approx(6.72897700e-02)

    # their imag components are equal but opposite in X
    assert np.abs(h_vector_from_b[0].imag) == approx(np.abs(h_vector_from_c[0].imag)) == approx(0.1165493003839844)
    assert np.sign(h_vector_from_b[0].imag) == -np.sign(h_vector_from_c[0].imag)

    # it's the reverse in Z
    assert h_vector_from_b[2].real == approx(np.abs(h_vector_from_c[2].real)) == approx(0.0137953509207929)
    assert np.sign(h_vector_from_b[2].real) == -np.sign(h_vector_from_c[2].real)
    assert h_vector_from_b[2].imag == approx(h_vector_from_c[2].imag) == approx(0.0238942487030554)

    # their imag components are larger than their reals, because they are more between peak
    # amplitude whenever A is at peak amplitude
    assert np.abs(h_vector_from_b[0].imag) > np.abs(h_vector_from_b[0].real)
    assert np.abs(h_vector_from_b[2].imag) > np.abs(h_vector_from_b[2].real)
    assert np.abs(h_vector_from_c[0].imag) > np.abs(h_vector_from_c[0].real)
    assert np.abs(h_vector_from_c[2].imag) > np.abs(h_vector_from_c[2].real)

    # their Y components are approximately 0 (just floating point precision spillage)
    assert np.abs(h_vector_from_b[1]) == approx(np.abs(h_vector_from_c[1])) == approx(0.0, abs=1e-5)


def test_calc_h_matrix():
    h_matrix_should_be = np.array(
        [
            [
                [
                    -5.83333326e-03 + 4.16333634e-17j,
                    3.81164826e-21 - 9.80694451e-06j,
                    -1.90819582e-17 + 4.77884974e-02j,
                ]
            ]
        ],
        dtype=np.complex_,
    )

    assert np.allclose(calc_h_matrix(EMF_MODEL_GROUP_1), h_matrix_should_be)
