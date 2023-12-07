from numpy import nan

from lv_physics.core.dynamic_objects import DynamicConductor
from lv_physics.core.ohl_objects import ConductorMaterial, ConductorState
from lv_physics.core.scene_objects import Air, Geography, Solar
from lv_physics.dlr.objects import DLRMCParams, DLRMCSigmas, DLRModelGroup


DLR_METHODS = "cigre", "generic"


IEEE_MOT = 100.0
MOT = 90.0


IEEE_AIR = Air(
    conductivity=nan,
    density=nan,
    heading=90.0,
    speed=1.5,
    temperature=25.0,
    viscosity=nan,
)


IEEE_STATIC_AIR = Air(
    conductivity=nan,
    density=nan,
    heading=90.0,
    speed=0.61,
    temperature=40.0,
    viscosity=nan,
)


IEEE_CONDUCTOR = DynamicConductor(
    id=-1,
    material=ConductorMaterial(
        name="IEEE-Drake",
        type="IEEE-ACSR",
        absorptivity=0.8,
        emissivity=0.8,
        diameter=0.0281432,
        mass=1.628,
        heat_capacity=1066.0 + 244.0,
        resistance_25c=7.283e-5,
        resistance_alpha=0.00385935,
        expansion_alpha=0.00000918141,
        youngs_modulus=77056.5363,
    ),
    state=ConductorState(
        loading=200.0,
        temperature=25.0,
    ),
)


IEEE_GEOGRAPHY = Geography(
    elevation=100,
    heading=0.0,
    latitude=30.0,
    longitude=30.0,
)


IEEE_SOLAR = Solar(
    altitude=74.8,
    azimuth=139.0,
    hour=-1.0,
    intensity=1027.0,
)


IEEE_STATIC_SOLAR = Solar(
    altitude=74.8,
    azimuth=139.0,
    hour=0.0,
    intensity=1025.0,
)


IEEE_DLR_MODEL_GROUP = DLRModelGroup(
    dttm=None,
    air=IEEE_AIR,
    conductor=IEEE_CONDUCTOR,
    geography=IEEE_GEOGRAPHY,
    solar=IEEE_SOLAR,
)


IEEE_SLR_MODEL_GROUP = DLRModelGroup(
    dttm=None,
    air=IEEE_STATIC_AIR,
    conductor=IEEE_CONDUCTOR,
    geography=IEEE_GEOGRAPHY,
    solar=IEEE_STATIC_SOLAR,
)


IEEE_MC_PARAMS = DLRMCParams(
    n_flops=5000,
    sigmas=DLRMCSigmas(
        air_speed=0.5,
        air_temperature=1.0,
        conductor_absorptivity=0.02,
        conductor_emissivity=0.02,
        conductor_loading=10.0,
        conductor_temperature=1.0,
        solar_intensity=50.0,
    ),
    method=DLR_METHODS[0],
)
