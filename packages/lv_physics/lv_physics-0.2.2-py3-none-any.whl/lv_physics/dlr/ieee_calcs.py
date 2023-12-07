"""
Provides functions for IEEE-2012 calculations.
"""
from copy import deepcopy

import numpy as np

from lv_physics.core.dynamic_objects import DynamicConductor
from lv_physics.core.scene_objects import Air, Geography, Solar
from lv_physics.dlr.const_objects import MOT
from lv_physics.dlr.objects import DLR, DLRModelGroup, Heat


# ----------------------------------------------------------------------------------------------------------------------
# Basic Calculations ---------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------


def calc_air_conductivity(air_temperature: float, cond_temperature: float) -> float:
    """
    Returns the thermal conductivity of air.
    """
    c_0 = +2.424e-2
    c_1 = +7.477e-5
    c_2 = -4.407e-9

    film_temperature = np.max([-270.0, (air_temperature + cond_temperature) / 2])

    return c_0 + c_1 * film_temperature + c_2 * film_temperature**2


def calc_air_density(air_temperature: float, cond_temperature: float, elevation: float) -> float:
    """
    Returns the density of air.
    """
    c_0 = +1.293
    c_1 = -1.525e-4
    c_2 = +6.379e-9
    c_3 = +0.00367

    film_temperature = np.max([-270.0, (air_temperature + cond_temperature) / 2])

    numerator = c_0 + c_1 * elevation + c_2 * elevation**2
    denomenator = 1.0 + np.max([-0.99, c_3 * film_temperature])

    return numerator / denomenator


def calc_air_viscosity(air_temperature: float, cond_temperature: float) -> float:
    """
    Returns the viscosity of air.
    """
    c_1 = 1.458e-6
    c_2 = 383.4

    film_temperature = np.max([-270.0, (air_temperature + cond_temperature) / 2])

    numerator = c_1 * (film_temperature + 273.0) ** 1.5
    denomenator = film_temperature + c_2

    return numerator / denomenator


def calc_reynolds_number(
    air_speed: float,
    air_temperature: float,
    cond_diameter: float,
    cond_temperature: float,
    elevation: float,
) -> float:
    """
    Returns the Reynolds number for a given air flow across a conductor.
    """
    air_density = calc_air_density(
        air_temperature=air_temperature,
        cond_temperature=cond_temperature,
        elevation=elevation,
    )

    air_viscosity = calc_air_viscosity(air_temperature=air_temperature, cond_temperature=cond_temperature)

    return cond_diameter * air_density * air_speed / air_viscosity


def calc_k_angle(air_heading: float, cond_heading: float, base_value: float = 0.194) -> float:
    """
    Returns the k-angle of wind against a conductor.
    """
    amplitude = 1.0 - base_value
    wind_angle = np.radians(air_heading - cond_heading)

    return base_value + amplitude * np.sin(wind_angle) ** 4


def calc_solar_altitude(latitude: float, longitude: float, sol_declination: float, sol_hour: float) -> float:
    """
    Returns the altitude [rad] of the sun for the given geographic location and sun position.
    """
    omega = sol_hour * np.radians(15.0)

    return np.arcsin(
        np.cos(omega) * np.cos(np.radians(latitude)) * np.cos(np.radians(sol_declination))
        + np.sin(np.radians(latitude)) * np.sin(np.radians(sol_declination))
    )


def calc_solar_attenuation(elevation: float) -> float:
    """
    Returns the atmospheric attenuation factor to the sun's intensity.
    """
    a_0 = +1.0
    a_1 = +1.148e-4
    a_2 = -1.108e-8

    return a_0 + a_1 * elevation + a_2 * elevation**2


# ----------------------------------------------------------------------------------------------------------------------
# CIGRE TB-498 Prescription --------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------


def calc_air_speed_eff_from_convection(
    q_convective: float,
    air_temperature: float,
    cond_diameter: float,
    cond_temperature: float,
    elevation: float,
) -> float:
    """
    Returns the effective air speed required to produce a given convective cooling.
    """
    air_conductivity = calc_air_conductivity(air_temperature=air_temperature, cond_temperature=cond_temperature)
    air_density = calc_air_density(air_temperature, cond_temperature, elevation)
    air_viscosity = calc_air_viscosity(air_temperature, cond_temperature)
    temperature_delta = np.abs(air_temperature - cond_temperature)
    k_angle = 1.0

    # Return 0.0 if any of the necessary parameters are 0.0
    if air_density == 0.0 or air_viscosity == 0.0 or temperature_delta == 0.0:
        return 0.0

    # Calculate effective reynolds
    n_reynolds_eff_1 = np.abs((q_convective / k_angle / air_conductivity / temperature_delta) - 1.01) / 1.135

    n_reynolds_eff_2 = np.abs(q_convective / 0.754 / k_angle / air_conductivity / temperature_delta)

    # Calculate possible wind speeds
    air_speed_1 = n_reynolds_eff_1 ** (1.0 / 0.52) * air_viscosity / cond_diameter / air_density
    air_speed_2 = n_reynolds_eff_2 ** (1.0 / 0.60) * air_viscosity / cond_diameter / air_density

    return np.min([air_speed_1, air_speed_2])


def calc_air_speed_eff(
    model_group: DLRModelGroup,
    temperature_rate: float = 0.0,
    temperature_max: float = MOT,
) -> float:
    """
    Returns the DLR after solving for the convective cooling term.

    This makes the steady-state assumption:
        0 = mc δT/δt = ql + qs + qr + qc
    """
    mg = deepcopy(model_group)

    # Calculate heating terms
    q_mass = mg.conductor.material.heat_capacity * temperature_rate
    q_radiative = calc_q_radiative(air=mg.air, conductor=mg.conductor)
    q_resistive = calc_q_resistive(conductor=mg.conductor)
    q_solar = calc_q_solar(conductor=mg.conductor, geography=mg.geography, solar=mg.solar)
    q_convective = q_mass - np.abs(q_resistive + q_solar + q_radiative)

    # Use convective heating to derive wind speed
    air_speed_eff = calc_air_speed_eff_from_convection(
        q_convective=q_convective,
        air_temperature=mg.air.temperature,
        cond_diameter=mg.conductor.material.diameter,
        cond_temperature=mg.conductor.temperature,
        elevation=mg.geography.elevation,
    )

    return air_speed_eff


# ----------------------------------------------------------------------------------------------------------------------
# Heat Calculations ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------


def calc_q_convective(
    air: Air,
    conductor: DynamicConductor,
    geography: Geography,
) -> float:
    """
    Returns the convective heat.
    """
    temperature_delta = np.min([0.0, air.temperature - conductor.temperature])

    air_conductivity = calc_air_conductivity(air_temperature=air.temperature, cond_temperature=conductor.temperature)

    air_density = calc_air_density(
        air_temperature=air.temperature,
        cond_temperature=conductor.temperature,
        elevation=geography.elevation,
    )

    k_angle = calc_k_angle(air_heading=air.heading, cond_heading=geography.heading)

    n_reynolds = calc_reynolds_number(
        air_speed=air.speed,
        air_temperature=air.temperature,
        cond_diameter=conductor.material.diameter,
        cond_temperature=conductor.temperature,
        elevation=geography.elevation,
    )

    q_0 = np.abs(3.645 * air_density**0.5 * conductor.material.diameter**0.75 * np.abs(temperature_delta) ** 1.25)

    q_1 = np.abs(k_angle * (1.01 + 1.35 * n_reynolds**0.52) * air_conductivity * np.abs(temperature_delta))

    q_2 = np.abs(k_angle * 0.754 * n_reynolds**0.6 * air_conductivity * np.abs(temperature_delta))

    return -np.max([q_0, q_1, q_2])


def calc_q_radiative(air: Air, conductor: DynamicConductor) -> float:
    """
    Returns the radiative heat.
    """
    a_1 = 17.8
    temperature_delta_4 = ((air.temperature + 273.0) ** 4 - (conductor.temperature + 273.0) ** 4) / 100.0**4

    return a_1 * conductor.material.diameter * conductor.material.emissivity * temperature_delta_4


def calc_q_resistive(conductor: DynamicConductor) -> float:
    """
    Returns the resistive heat.
    """
    return conductor.resistance * conductor.loading**2


def calc_q_solar(conductor: DynamicConductor, geography: Geography, solar: Solar) -> float:
    """
    Returns the solar heat.
    """
    theta = np.arccos(np.cos(np.radians(solar.altitude)) * np.cos(np.radians(solar.azimuth - geography.heading)))

    return conductor.material.absorptivity * solar.intensity * conductor.material.diameter * np.sin(theta)


def calc_heat(model_group: DLRModelGroup) -> Heat:
    """
    Returns the heat object that descibes the interaction between conductor and environment.
    """
    # Unpack the model group
    air = model_group.air
    conductor = model_group.conductor
    geography = model_group.geography
    solar = model_group.solar

    # Calculate all heating terms
    heat = Heat(
        convective=calc_q_convective(air=air, conductor=conductor, geography=geography),
        radiative=calc_q_radiative(air=air, conductor=conductor),
        resistive=calc_q_resistive(conductor=conductor),
        solar=calc_q_solar(conductor=conductor, geography=geography, solar=solar),
    )

    return heat


def calc_dlr(model_group: DLRModelGroup, temperature_max: float = MOT) -> DLR:
    """
    Returns the DLR provided all factors.
    """
    mg = deepcopy(model_group)

    # Establish the conductor at rating (at maximumum operating temperature)
    mg.conductor.state.temperature = temperature_max

    # Calculate heating terms
    q_convective = calc_q_convective(
        air=mg.air,
        conductor=mg.conductor,
        geography=mg.geography,
    )

    q_radiative = calc_q_radiative(air=mg.air, conductor=mg.conductor)

    q_solar = calc_q_solar(
        conductor=mg.conductor,
        geography=mg.geography,
        solar=mg.solar,
    )

    q_resistive = np.max([0.0, -np.nansum([q_convective, q_radiative, q_solar])])

    # Calculate rating
    loading = np.sqrt(q_resistive / mg.conductor.resistance)

    # Create DLR object
    dlr = DLR(
        heat=Heat(
            convective=q_convective,
            radiative=q_radiative,
            resistive=q_resistive,
            solar=q_solar,
        ),
        loading=loading,
    )

    return dlr


def calc_air_speed_from_dlr(model_group: DLRModelGroup, rating: float):
    # Create the model group with the rated loading
    mg = deepcopy(model_group)
    mg.conductor.state.loading = rating
    mg.conductor.state.temperature = MOT

    # Calculate heating terms
    q_radiative = calc_q_radiative(air=mg.air, conductor=mg.conductor)
    q_solar = calc_q_solar(
        conductor=mg.conductor,
        geography=mg.geography,
        solar=mg.solar,
    )
    q_resistive = calc_q_resistive(mg.conductor)
    q_convective = -(q_radiative + q_solar + q_resistive)

    # Calculate the effective wind speed
    air_speed_eff = calc_air_speed_eff_from_convection(
        q_convective,
        mg.air.temperature,
        mg.conductor.material.diameter,
        mg.conductor.state.temperature,
        mg.geography.elevation,
    )

    return air_speed_eff
