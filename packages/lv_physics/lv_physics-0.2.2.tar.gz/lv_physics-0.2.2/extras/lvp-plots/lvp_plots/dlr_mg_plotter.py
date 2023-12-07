from typing import Dict

import numpy as np
from matplotlib import pyplot as plt
from numpy import array
from numpy.typing import NDArray

from lv_physics.dlr.objects import DLRModelGroup
from lv_physics.general.objects import CircuitSpan


class DLRModelGroupFigure:

    fig: plt.Figure
    axes: Dict[str, plt.Axes]

    def __init__(self):

        fig: plt.Figure = plt.figure(figsize=(14, 8))
        axes: Dict[str, plt.Axes] = {}

        axes["time"] = fig.add_subplot(511)
        axes["time"].set(ylabel="Time [min.]")

        axes["temp"] = fig.add_subplot(512, sharex=axes["time"])
        axes["temp"].set(ylabel="Temperature [$^{\\circ} C$]")

        axes["heat"] = fig.add_subplot(513, sharex=axes["time"])
        axes["heat"].set(ylabel="Heat [W/m]")

        axes["load"] = fig.add_subplot(514, sharex=axes["time"])
        axes["load"].set(ylabel="Loading [A]")

        axes["wx"] = fig.add_subplot(515, sharex=axes["time"])
        axes["wx"].set(xlabel="Hour", ylabel="Weather")

        for ax in axes.values():
            # ax.tick_params(axis="both", labelrotation=20)
            ax.set_ylabel(ax.get_ylabel(), rotation=45)
            ax.yaxis.set_label_coords(-0.10, 0.25)
            ax.grid()

        self.fig = fig
        self.axes = axes

    def shades(self):
        """
        Shade the time axis.
        """
        t_array = np.arange(-1000, 1000)
        a_array = np.zeros(len(t_array))
        b_array = np.ones(len(t_array)) * 10.0
        c_array = np.ones(len(t_array)) * 60.0
        d_array = np.ones(len(t_array)) * 1000.0

        self.axes["time"].fill_between(t_array, a_array, b_array, color="red", alpha=0.2)
        self.axes["time"].fill_between(t_array, b_array, c_array, color="yellow", alpha=0.2)
        self.axes["time"].fill_between(t_array, c_array, d_array, color="green", alpha=0.2)

    def plot_mg_series(self, circuit_span: CircuitSpan, mg_series: NDArray[DLRModelGroup], title: bool = False) -> None:

        if title is True:
            self.fig.suptitle(circuit_span.name)

        # get values
        dttms = array([mg.dttm for mg in mg_series])
        hours = array([(dttm - dttms[0]).total_seconds() / 3600 for dttm in dttms])
        hours_delta = hours[-1] - hours[0]

        thermalization_time = array([mg.dlr.thermalization_time for mg in mg_series]) / 60.0

        temperature_a = array([mg.air.temperature for mg in mg_series])
        temperature_c = array([mg.conductor.temperature for mg in mg_series])

        loading = array([mg.conductor.loading for mg in mg_series])

        rating = array([mg.dlr.loading for mg in mg_series])
        rating_p1 = array([mg.dists.rating.percentile(1) for mg in mg_series])
        rating_p10 = array([mg.dists.rating.percentile(10) for mg in mg_series])
        rating_p50 = array([mg.dists.rating.percentile(50) for mg in mg_series])
        rating_p90 = array([mg.dists.rating.percentile(90) for mg in mg_series])
        rating_p99 = array([mg.dists.rating.percentile(99) for mg in mg_series])

        q_convective = array([mg.heat.convective for mg in mg_series])
        q_radiative = array([mg.heat.radiative for mg in mg_series])
        q_resistive = array([mg.heat.resistive for mg in mg_series])
        q_solar = array([mg.heat.solar for mg in mg_series])
        q_net = array([mg.heat.net for mg in mg_series])

        air_speed = array([mg.air.speed for mg in mg_series])
        geography = circuit_span.geography
        air_heading = geography.heading - array([mg.air.heading for mg in mg_series])
        air_speed_perp = np.abs(air_speed * np.sin(air_heading))

        solar = array([mg.solar.intensity for mg in mg_series]) / 100.0  # 10 kW / cm / m

        # plots
        self.axes["time"].plot(hours, thermalization_time, color="black", label="Thermalization")
        self.axes["time"].plot(hours, np.zeros_like(hours) + 30.0, "r--", linewidth=1)
        self.axes["time"].plot(hours, np.zeros_like(hours) + 60.0, "r--", linewidth=1)
        self.axes["time"].plot(hours, np.zeros_like(hours) + 90.0, "r--", linewidth=1)
        self.axes["time"].set(ylim=(0.0, 105))  # 1.5 * np.nanmax(thermalization_time)))
        self.axes["time"].legend()

        self.axes["temp"].plot(hours, temperature_a, color="skyblue", label="Air")
        self.axes["temp"].plot(hours, temperature_c, color="black", label="Conductor")
        self.axes["temp"].legend()

        self.axes["heat"].plot(hours, q_convective, color="skyblue", label="Convective")
        self.axes["heat"].plot(hours, q_radiative, color="magenta", label="Radiative")
        self.axes["heat"].plot(hours, q_resistive, color="red", label="Resistive")
        self.axes["heat"].plot(hours, q_solar, color="orange", label="Solar")
        self.axes["heat"].plot(hours, q_net, color="black", label="Total")
        self.axes["heat"].legend()

        self.axes["load"].fill_between(hours, rating_p1, rating_p99, color="red", alpha=0.2)
        self.axes["load"].fill_between(hours, rating_p10, rating_p90, color="red", alpha=0.2)
        self.axes["load"].plot(hours, loading, color="black", label="Loading")
        self.axes["load"].plot(hours, rating, color="red", label="Rating")
        self.axes["load"].plot(hours, rating_p50, color="red", ls="--", label="P-50 DLR")
        self.axes["load"].set(ylim=(0.0, 2.0 * np.nanmax(rating)))
        self.axes["load"].legend()

        self.axes["wx"].plot(hours, air_speed_perp, color="skyblue", label="Perp. Wind Speed [m/s]")
        self.axes["wx"].plot(hours, solar, color="orange", label="Solar [10 kW/(cm x m)]")
        self.axes["wx"].legend()

        # datetime limits
        self.axes["time"].set(
            xlim=(
                hours[0] - 0.02 * hours_delta,
                hours[-1] + 0.20 * hours_delta,
            )
        )
