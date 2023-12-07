"""
Provides functions for simulating more envolved thermal calculations for the DLRModelGroup.
"""
from copy import deepcopy
from typing import Tuple

import numpy as np
from numpy import array, float_
from numpy.typing import NDArray
from scipy.optimize import fsolve

from lv_physics.dlr.ieee_calcs import calc_heat
from lv_physics.dlr.objects import DLRModelGroup


# ----------------------------------------------------------------------------------------------------------------------


def solve_conductor_temperature_ss(model_group: DLRModelGroup) -> float:
    """
    Returns the steady-state conductor temperature.
    """
    mg = deepcopy(model_group)

    # Define the steady state function to solve to zero
    def steady_state_heat(temperature, mg):
        mg.conductor.state.temperature = float(temperature)
        return calc_heat(model_group=mg).net

    Tc = fsolve(
        steady_state_heat,
        x0=model_group.air.temperature,
        args=(mg),
    )[0]

    return Tc


def evolve_conductor_temperature(
    model_group: DLRModelGroup,
    duration: float,
    time_step: float,
) -> float:
    """
    Evolve the thermal state of the conductor for a single time interval.
    """
    mg = deepcopy(model_group)

    for t in np.arange(0.0, duration, time_step):
        heat = calc_heat(model_group=mg)
        mg.conductor.state.temperature += time_step * heat.net / mg.conductor.material.heat_capacity

    return mg.conductor.state.temperature


def sim_thermalization_time(
    model_group: DLRModelGroup,
    temperature_max: float,
    threshold: float = 2.0,
    time_step: float = 1.0,
    duration_max: float = 72000.0,
) -> float:
    """
    Returns the time for the conductor to reach within the threshold of
    the maximum temperature.
    """
    mg = deepcopy(model_group)

    thermalization_time = 0.0

    while mg.conductor.temperature < temperature_max - threshold:
        thermalization_time += time_step
        mg.conductor.state.temperature = evolve_conductor_temperature(
            model_group=mg,
            duration=time_step,
            time_step=time_step,
        )

    return thermalization_time


def sim_thermalization(
    model_group: DLRModelGroup,
    temperature_max: float,
    threshold: float = 2.0,
    time_step: float = 1.0,
    duration_max: float = 7200.0,
    iters_max: int = 10000,
) -> Tuple[NDArray[float_], NDArray[float_]]:
    """
    Returns the array of conductor temperature evolution.
    """
    mg = deepcopy(model_group)

    thermalization_time = 0.0
    times = [thermalization_time]
    temperatures = [mg.conductor.temperature]

    iters = 0
    while mg.conductor.temperature < temperature_max - threshold:
        iters += 1
        if iters > iters_max:
            break

        thermalization_time += time_step
        mg.conductor.state.temperature = evolve_conductor_temperature(
            model_group=mg,
            duration=time_step,
            time_step=time_step,
        )

        times.append(thermalization_time)
        temperatures.append(mg.conductor.temperature)

    return array(times), array(temperatures)
