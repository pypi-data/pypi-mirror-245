import numpy as np

from lv_physics.dlr.const_objects import IEEE_MOT, IEEE_SLR_MODEL_GROUP
from lv_physics.dlr.ieee_calcs import calc_dlr


# ----------------------------------------------------------------------------------------------------------------------


IEEE_LINE_RATING = 1025
IEEE_Q_CONVECTIVE = -81.93
IEEE_Q_RADIATIVE = -39.10
IEEE_Q_RESISTIVE = 9.390e-5 * IEEE_LINE_RATING**2
IEEE_Q_SOLAR = +22.44


def test_calc_dlr():
    """
    Tests `calc_dlr`.
    """
    ERROR_THRESHOLD = 0.03

    dlr = calc_dlr(model_group=IEEE_SLR_MODEL_GROUP, temperature_max=IEEE_MOT)

    line_rating_error = np.abs((dlr.loading - IEEE_LINE_RATING) / IEEE_LINE_RATING)
    assert line_rating_error < ERROR_THRESHOLD

    q_convective_error = np.abs((dlr.heat.convective - IEEE_Q_CONVECTIVE) / IEEE_Q_CONVECTIVE)
    assert q_convective_error < ERROR_THRESHOLD

    q_radiative_error = np.abs((dlr.heat.radiative - IEEE_Q_RADIATIVE) / IEEE_Q_RADIATIVE)
    assert q_radiative_error < ERROR_THRESHOLD

    q_resistive_error = np.abs((dlr.heat.resistive - IEEE_Q_RESISTIVE) / IEEE_Q_RESISTIVE)
    assert q_resistive_error < ERROR_THRESHOLD

    q_solar_error = np.abs((dlr.heat.solar - IEEE_Q_SOLAR) / IEEE_Q_SOLAR)
    assert q_solar_error < ERROR_THRESHOLD
