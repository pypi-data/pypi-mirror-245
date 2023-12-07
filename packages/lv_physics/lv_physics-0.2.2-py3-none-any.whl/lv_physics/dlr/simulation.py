from copy import deepcopy
from dataclasses import replace

from numpy.typing import NDArray

from lv_physics.dlr.const_objects import MOT
from lv_physics.dlr.ieee_calcs import calc_dlr, calc_heat
from lv_physics.dlr.monte_carlo import gen_dlr_model_group_flops, run_dlr_monte_carlo
from lv_physics.dlr.objects import DLRMCParams, DLRModelGroup
from lv_physics.dlr.thermalization import (
    evolve_conductor_temperature,
    sim_thermalization_time,
)
from lv_physics.utils.helpers import progress_bar


def sim_dlr_series(
    mg_series: NDArray[DLRModelGroup],
    time_step: float = 1.0,
    mc_params: DLRMCParams = None,
) -> None:
    """
    Simulates the evolution of Dynamic Line Rating.
    """
    # Initialize the conductor temperature
    mg_series[0].conductor.state.temperature = mg_series[0].air.temperature

    # Iterate through the series, beginning with the second time element
    for n in range(1, len(mg_series)):
        progress_bar(n, len(mg_series))

        # Get relevant model groups
        mg_m = mg_series[n - 1]
        mg_n = mg_series[n]

        # Get datetimes and evolution duration
        dttm_m = mg_m.dttm
        dttm_n = mg_n.dttm
        duration = (dttm_n - dttm_m).total_seconds()

        # Evolve the conductor temperature (evolve from the time m)
        mg_n.conductor.state.temperature = evolve_conductor_temperature(
            model_group=mg_m,
            duration=duration,
            time_step=time_step,
        )

        # Calculate the line rating results (calculate for time n)
        mg_n.dlr = calc_dlr(mg_n)
        mg_n.heat = calc_heat(mg_n)

        # Model group for thermalization time
        mg_r = deepcopy(mg_n)
        mg_r.conductor.state = replace(
            mg_r.conductor.state,
            loading=mg_n.dlr.loading,
        )

        # Calculate the thermalization time
        thermalization_time = sim_thermalization_time(
            mg_r,
            temperature_max=MOT,
            threshold=2.0,
            time_step=time_step,
            duration_max=100.0,
        )
        mg_n.dlr.thermalization_time = thermalization_time + 0.0

        # Monte Carlo
        if mc_params is not None:
            model_group_flops = gen_dlr_model_group_flops(mg_n, mc_params)
            mg_n.dists = run_dlr_monte_carlo(model_group_flops)

        # Write conductor temperature into the model group
        mg_series[n] = mg_n

    # Set the 0th time
    mg_series[0].dlr = mg_series[1].dlr
    mg_series[0].heat = mg_series[1].heat
    mg_series[0].dists = mg_series[1].dists
