from copy import deepcopy
from dataclasses import replace

import numpy as np
from numpy import array, float_, nan, ones, zeros
from numpy.typing import NDArray

from lv_physics.dlr.const_objects import DLR_METHODS
from lv_physics.dlr.distributions import weibull_reverse_samples, weibull_samples
from lv_physics.dlr.ieee_calcs import calc_air_speed_eff, calc_dlr, calc_heat
from lv_physics.dlr.objects import (
    Distribution,
    DLRMCDistributions,
    DLRMCParams,
    DLRModelGroup,
)
from lv_physics.dlr.thermalization import solve_conductor_temperature_ss


def gen_dlr_model_group_flops(
    model_group: DLRModelGroup,
    params: DLRMCParams,
) -> DLRMCDistributions:
    """
    Returns the results from a DLR Monte Carlo run, using the model group as a source
    of "truth", and stochastically varying the model group by parameters sepcified in
    the params.
    """
    if params.method.lower() not in DLR_METHODS:
        raise ValueError(f"Method '{params.method}' is not recognized.")

    # PART I: SETUP

    mg = deepcopy(model_group)

    # Define the truth air state
    mg.air.heading = mg.geography.heading + 90.0

    # Define the initial conductor temperature
    mg.conductor.state.temperature = solve_conductor_temperature_ss(model_group=model_group)

    # PART II: Creating the stochastic variable distributions

    # Distributions
    if params.method.lower() == "generic":
        air_speed_fraction = abs(mg.air.speed) / 3.0
        air_speed_flops = weibull_samples(
            n_samples=params.n_flops,
            mean=mg.air.speed,
            sigma=params.sigmas.air_speed * air_speed_fraction,
        )
    elif params.method.lower() == "cigre":
        air_speed_flops = nan * ones(params.n_flops)

    air_temperature_flops = np.random.normal(
        size=params.n_flops,
        loc=mg.air.temperature,
        scale=params.sigmas.air_temperature,
    )

    conductor_absorptivity_flops = weibull_reverse_samples(
        n_samples=params.n_flops,
        mean=mg.conductor.material.absorptivity,
        sigma=params.sigmas.conductor_absorptivity,
    )

    conductor_emissivity_flops = weibull_reverse_samples(
        n_samples=params.n_flops,
        mean=mg.conductor.material.emissivity,
        sigma=params.sigmas.conductor_emissivity,
    )

    conductor_loading_flops = np.random.normal(
        size=params.n_flops,
        loc=mg.conductor.state.loading,
        scale=params.sigmas.conductor_loading,
    )

    conductor_temperature_flops = np.random.normal(
        size=params.n_flops,
        loc=mg.conductor.temperature,
        scale=params.sigmas.conductor_temperature,
    )

    solar_intensity_fraction = mg.solar.intensity / 1300.0
    solar_intensity_flops = np.abs(
        weibull_samples(
            n_samples=params.n_flops,
            mean=mg.solar.intensity,
            sigma=params.sigmas.solar_intensity * solar_intensity_fraction,
        )
    )

    # PART III: Running the Monte Carlo

    # Initialize the output arrays
    model_group_flops = zeros(params.n_flops, dtype=DLRModelGroup)

    # Loop through monte carlo flops
    for n in range(params.n_flops):
        # Create thermal objects with mc flop values
        air_flop = deepcopy(mg.air)
        air_flop.temperature = air_temperature_flops[n]

        conductor_flop = deepcopy(mg.conductor)
        conductor_flop.material.absorptivity = conductor_absorptivity_flops[n]
        conductor_flop.material.emissivity = conductor_emissivity_flops[n]
        conductor_flop.state.loading = conductor_loading_flops[n]
        conductor_flop.state.temperature = conductor_temperature_flops[n]

        solar_flop = deepcopy(mg.solar)
        solar_flop.intensity = solar_intensity_flops[n]

        # Create the model group flop
        model_group_flop = DLRModelGroup(
            air=air_flop,
            conductor=conductor_flop,
            geography=mg.geography,
            solar=solar_flop,
        )

        # The air flop
        if params.method.lower() == "generic":
            model_group_flop.air.heading = mg.geography.heading + 90.0
            model_group_flop.air.speed = air_speed_flops[n]

        elif params.method.lower() == "cigre":
            model_group_flop.air.heading = mg.geography.heading + 90.0
            model_group_flop.air.speed = calc_air_speed_eff(
                model_group=model_group_flop,
                temperature_rate=0.0,
            )

        # Store the model group flop
        model_group_flops[n] = model_group_flop

    return model_group_flops


def run_dlr_monte_carlo(model_group_flops: NDArray[DLRModelGroup]) -> DLRMCDistributions:
    """
    Runs the DLR calculations on each model group in the array.
    """
    for mg in model_group_flops:
        mg.heat = calc_heat(mg)
        mg.dlr = calc_dlr(mg)

    return gen_dlrmc_distributions(model_group_flops)


def run_thermalization_monte_carlo(
    model_group_flops: NDArray[DLRModelGroup],
    rating: float,
) -> Distribution:
    """
    Returns the distribution of temperatures the conductor would equilibriate
    to, given a distribution of loadings.
    """
    temperature_flops = zeros(len(model_group_flops), dtype=float_)

    for n, mg in enumerate(model_group_flops):
        mg_at_rating = replace(
            mg,
            conductor=replace(
                mg.conductor,
                state=replace(
                    mg.conductor.state,
                    loading=rating,
                ),
            ),
        )

        temperature_flops[n] = solve_conductor_temperature_ss(mg_at_rating)

    return Distribution(temperature_flops)


def gen_dlrmc_distributions(model_group_flops: NDArray[DLRModelGroup]) -> DLRMCDistributions:
    """
    Generates a DLRMCResults object with populated Distributions from the
    input model_group_flops and results_flops.
    """
    air_speed_values = array([mg.air.speed for mg in model_group_flops])
    air_temperature_values = array([mg.air.temperature for mg in model_group_flops])
    conductor_temperature_values = array([mg.conductor.state.temperature for mg in model_group_flops])

    q_convective_values = array([mg.heat.convective for mg in model_group_flops])
    q_radiative_values = array([mg.heat.radiative for mg in model_group_flops])
    q_resistive_values = array([mg.heat.resistive for mg in model_group_flops])
    q_solar_values = array([mg.heat.solar for mg in model_group_flops])

    q_convective_rating_values = array([mg.dlr.heat.convective for mg in model_group_flops])
    q_radiative_rating_values = array([mg.dlr.heat.radiative for mg in model_group_flops])
    q_resistive_rating_values = array([mg.dlr.heat.resistive for mg in model_group_flops])
    q_solar_rating_values = array([mg.dlr.heat.solar for mg in model_group_flops])

    rating_values = array([mg.dlr.loading for mg in model_group_flops])

    return DLRMCDistributions(
        air_speed=Distribution(air_speed_values),
        air_temperature=Distribution(air_temperature_values),
        conductor_temperature=Distribution(conductor_temperature_values),
        conductor_temperature_ss=None,
        q_convective=Distribution(q_convective_values),
        q_radiative=Distribution(q_radiative_values),
        q_resistive=Distribution(q_resistive_values),
        q_solar=Distribution(q_solar_values),
        q_convective_rating=Distribution(q_convective_rating_values),
        q_radiative_rating=Distribution(q_radiative_rating_values),
        q_resistive_rating=Distribution(q_resistive_rating_values),
        q_solar_rating=Distribution(q_solar_rating_values),
        rating=Distribution(rating_values),
    )
