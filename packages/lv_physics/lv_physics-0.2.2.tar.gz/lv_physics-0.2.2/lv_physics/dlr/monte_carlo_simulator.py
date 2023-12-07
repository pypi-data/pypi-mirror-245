from numpy.typing import NDArray

from lv_physics.dlr.const_objects import (
    IEEE_DLR_MODEL_GROUP,
    IEEE_MC_PARAMS,
    IEEE_SLR_MODEL_GROUP,
    MOT,
)
from lv_physics.dlr.ieee_calcs import calc_dlr, calc_heat
from lv_physics.dlr.monte_carlo import (
    gen_dlr_model_group_flops,
    run_dlr_monte_carlo,
    run_thermalization_monte_carlo,
)
from lv_physics.dlr.objects import DLRMCDistributions, DLRMCParams, DLRModelGroup
from lv_physics.dlr.thermalization import sim_thermalization_time


class DLRMCSimulator:
    dlr_model_group: DLRModelGroup
    slr_model_group: DLRModelGroup
    params: DLRMCParams
    flops: NDArray[DLRModelGroup]
    dists: DLRMCDistributions

    def __init__(
        self,
        params: DLRMCParams = IEEE_MC_PARAMS,
        dlr_model_group: DLRModelGroup = IEEE_DLR_MODEL_GROUP,
        slr_model_group: DLRModelGroup = IEEE_SLR_MODEL_GROUP,
    ):
        self.params = params
        self.dlr_model_group = dlr_model_group
        self.slr_model_group = slr_model_group
        self.flops = None
        self.dists = None

    def gen_dlr_model_group_flops(self):
        """
        Generate the DLR conditions for each flop.
        """
        self.flops = gen_dlr_model_group_flops(
            model_group=self.dlr_model_group,
            params=self.params,
        )

    def run_dlr_monte_carlo(self):
        """
        Generate the DLR for each flop.
        """
        self.dists = run_dlr_monte_carlo(self.flops)

    def run_thermalization_monte_carlo(self, percentile: float = 1.0):
        """
        Generate the steady state temperatures for each flop.
        """
        if False:
            # Exploratory
            from copy import deepcopy

            from lv_physics.dlr.ieee_calcs import calc_air_speed_from_dlr

            # from lv_physics.dlr.distributions import weibull_samples
            # Calculate the air speed for this rating
            dlr_p = self.dists.rating.percentile(percentile)
            air_speed_eff = calc_air_speed_from_dlr(self.dlr_model_group, rating=dlr_p)

            # Create distribution
            # air_speed_fraction = abs(air_speed_eff) / 5.0
            # air_speed_flops = weibull_samples(
            #     n_samples=self.params.n_flops,
            #     mean=air_speed_eff,
            #     sigma=self.params.sigmas.air_speed * air_speed_fraction,
            # )

            # Create new flops
            flops = deepcopy(self.flops)
            for n in range(len(flops)):
                flops[n].air.speed = air_speed_eff

            # Compute the steady-state
            self.dists.conductor_temperature_ss = run_thermalization_monte_carlo(
                model_group_flops=flops,
                rating=self.dists.rating.percentile(percentile),
            )

        else:
            # Compute the steady-state
            self.dists.conductor_temperature_ss = run_thermalization_monte_carlo(
                model_group_flops=self.flops,
                rating=self.dists.rating.percentile(percentile),
            )

    def run_dlr(self, thermalization_time: bool = False):
        """
        Generates the static rating for the DLR model group.
        """
        self.dlr_model_group.dlr = calc_dlr(self.dlr_model_group)
        self.dlr_model_group.heat = calc_heat(self.dlr_model_group)

        if thermalization_time is True:
            self.dlr_model_group.dlr.thermalization_time = sim_thermalization_time(
                model_group=self.dlr_model_group,
                temperature_max=MOT,
            )

    def run_slr(self):
        """
        Generates the static rating for the SLR model group.
        """
        self.slr_model_group.dlr = calc_dlr(self.slr_model_group)
        self.slr_model_group.heat = calc_heat(self.slr_model_group)


if __name__ == "__main__":
    sim = DLRMCSimulator()
    sim.gen_dlr_model_group_flops()
    sim.run_dlr()
    sim.run_slr()
    sim.run_dlr_monte_carlo()
    sim.run_thermalization_monte_carlo()
