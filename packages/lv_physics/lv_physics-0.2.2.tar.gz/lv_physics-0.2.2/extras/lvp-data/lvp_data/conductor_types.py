from dataclasses import dataclass
from typing import Dict, Union

from dataclasses_json import dataclass_json

from lv_physics.core.ohl_objects import ConductorMaterial


@dataclass_json
@dataclass
class ConductorType:
    core: str
    outer: str


@dataclass_json
@dataclass
class MaterialProperty:
    youngs_modulus: Union[float, Dict[int, float]]
    expansion_alpha: float
    specific_heat: float


def ym_to_metric(v: float) -> float:
    """elastic modulus: [MPSI] -> [MPa]"""
    return v * 6894.76


def sh_to_metric(v: float) -> float:
    """specific heat: [cal/g/C] -> [J/kg/C]"""
    return v * 4186.80


CONDUCTOR_TYPES = {
    "ACSR": ConductorType("Galvanized Steel", "1350-H19 Aluminum"),
    "ACSS": ConductorType("Mischmetal-Coated Steel", "1350-O Aluminium"),
    "Copper": ConductorType(None, "Hard-Drawn Copper"),
    "ACCR": ConductorType(
        "Fiber-Reinforced Aluminum Matrix", "Hardened Aluminum-Zirconium Alloy"
    ),
    "ACSS_TW": ConductorType("Mischmetal-Coated Steel", "1350-O Aluminium"),
    "ACSS/TW": ConductorType("Mischmetal-Coated Steel", "1350-O Aluminium"),
    "ACSR_SD": ConductorType("Aluminum-Clad Steel", "1350-H19 Aluminum"),
    "ACSR/SD": ConductorType("Aluminum-Clad Steel", "1350-H19 Aluminum"),
    "SCACAR": ConductorType(
        "Galvanized Steel", "(30) 1350-H19 Aluminum & (24) 6201-T81 Aluminum Alloy"
    ),
    "AAC": ConductorType("1350-H19 Aluminum", "1350-H19 Aluminum"),
    "ACAR": ConductorType("6201-T81 Aluminum Alloy", "1350-H19 Aluminum"),
    "AAAC": ConductorType("6201-T81 Aluminum Alloy", "6201-T81 Aluminum Alloy"),
    "AAAC-Custom-1": ConductorType(
        "Aluminum Alloy-Custom-1", "Aluminum Alloy-Custom-1"
    ),
    "TACSR": ConductorType("Galvanized Steel", "Aluminum-Zirconium Alloy"),
}


MATERIAL_PROPERTIES = {
    "1350-H19 Aluminum": MaterialProperty(
        youngs_modulus={
            0: ym_to_metric(8.6),
        },
        expansion_alpha=23.04 * 1e-6,
        specific_heat=sh_to_metric(0.2151),
    ),
    "Galvanized Steel": MaterialProperty(
        youngs_modulus={
            1: ym_to_metric(27.5),
            7: ym_to_metric(27),
            19: ym_to_metric(26.5),
            37: ym_to_metric(26.0),
        },
        expansion_alpha=11.52 * 1e-6,
        specific_heat=sh_to_metric(0.1198),
    ),
    "Hard-Drawn Copper": MaterialProperty(
        youngs_modulus={
            7: ym_to_metric(16.8),
            19: ym_to_metric(16.8),
            37: ym_to_metric(15.4),
            61: ym_to_metric(15.4),
        },
        expansion_alpha=16.92 * 1e-6,
        specific_heat=sh_to_metric(0.0914),
    ),
    "Hardened Aluminum-Zirconium Alloy": MaterialProperty(
        youngs_modulus={
            0: ym_to_metric(8.6),
        },
        expansion_alpha=23.04 * 1e-6,
        specific_heat=sh_to_metric(0.2284),
    ),
    "Fiber-Reinforced Aluminum Matrix": MaterialProperty(
        youngs_modulus={
            0: ym_to_metric(0.2049),
        },
        expansion_alpha=6.3 * 1e-6,
        specific_heat=sh_to_metric(32.96),
    ),
    "Mischmetal-Coated Steel": MaterialProperty(
        youngs_modulus={
            1: ym_to_metric(27.5),
            7: ym_to_metric(27),
            19: ym_to_metric(26.5),
        },
        expansion_alpha=11.52 * 1e-6,
        specific_heat=sh_to_metric(0.1198),
    ),
    "1350-O Aluminium": MaterialProperty(
        youngs_modulus={
            0: ym_to_metric(8.6),
        },
        expansion_alpha=23.04 * 1e-6,
        specific_heat=sh_to_metric(0.2151),
    ),
    "Aluminum-Clad Steel": MaterialProperty(
        youngs_modulus={
            1: ym_to_metric(23.5),
            7: ym_to_metric(23),
            19: ym_to_metric(22.5),
        },
        expansion_alpha=12.96 * 1e-6,
        specific_heat=sh_to_metric(0.1292),
    ),
    "(30) 1350-H19 Aluminum & (24) 6201-T81 Aluminum Alloy": MaterialProperty(
        youngs_modulus={
            0: ym_to_metric(8.6),
        },
        expansion_alpha=23.04 * 1e-6,
        specific_heat=sh_to_metric(0.2144),
    ),
    "6201-T81 Aluminum Alloy": MaterialProperty(
        youngs_modulus={
            0: ym_to_metric(8.6),
        },
        expansion_alpha=23.04 * 1e-6,
        specific_heat=sh_to_metric(0.2139),
    ),
    "Aluminum Alloy-Custom-1": MaterialProperty(
        youngs_modulus={
            0: ym_to_metric(7.832037),
        },
        expansion_alpha=23.04 * 1e-6,
        specific_heat=sh_to_metric(0.2151),
    ),
    "Aluminum-Zirconium Alloy": MaterialProperty(
        youngs_modulus={
            0: ym_to_metric(8.6),
        },
        expansion_alpha=23.04 * 1e-6,
        specific_heat=sh_to_metric(0.2173),
    ),
    None: MaterialProperty(
        youngs_modulus={0: 0.0},
        expansion_alpha=0.0,
        specific_heat=0.0,
    ),
}


class ConductorPropertiesMD:
    """A phony class to represent Ops data."""
    pass


def calc_conductor_material(
    cp: ConductorPropertiesMD, absorptivity: float = 0.8, emissivity: float = 0.8
):

    ct = CONDUCTOR_TYPES[cp.type]

    # In ops code, the young's modulus is either a float or a Dict[int, float].  The
    # logic in ops uses if/else to get multiple values based on whether or not the
    # young's modulus is a dict or not.  Here we handle that slightly differently.
    if cp.stranding_core in MATERIAL_PROPERTIES[ct.core].youngs_modulus.keys():
        sc = cp.stranding_core
    else:
        sc = 0
    if cp.stranding_outer in MATERIAL_PROPERTIES[ct.outer].youngs_modulus.keys():
        so = cp.stranding_outer
    else:
        so = 0

    area = cp.area_core + cp.area_outer

    mass_core = cp.weight_core / 9.807
    mass_outer = cp.weight_outer / 9.807
    mass = mass_core + mass_outer

    specific_heat_core = MATERIAL_PROPERTIES[ct.core].specific_heat
    specific_heat_outer = MATERIAL_PROPERTIES[ct.outer].specific_heat

    heat_capacity_core = specific_heat_core * mass_core
    heat_capacity_outer = specific_heat_outer * mass_outer
    heat_capacity = heat_capacity_core + heat_capacity_outer

    expansion_alpha_core = MATERIAL_PROPERTIES[ct.core].expansion_alpha
    expansion_alpha_outer = MATERIAL_PROPERTIES[ct.outer].expansion_alpha

    youngs_modulus_core = MATERIAL_PROPERTIES[ct.core].youngs_modulus[sc]
    youngs_modulus_outer = MATERIAL_PROPERTIES[ct.outer].youngs_modulus[so]

    resistance_alpha = cp.resistance_slope / cp.resistance_25c

    # IEEE - Eq. 14.22
    youngs_modulus = (
        youngs_modulus_core * cp.area_core + youngs_modulus_outer * cp.area_outer
    ) / area

    # IEEE - Eq. 14.23
    # TODO: Something seems wrong about this value.
    expansion_alpha = (
        youngs_modulus_core * expansion_alpha_core * cp.area_outer
        + youngs_modulus_outer * expansion_alpha_outer * cp.area_outer
    ) / (youngs_modulus * area)

    return ConductorMaterial(
        name=cp.name,
        type=cp.type,
        absorptivity=absorptivity,
        emissivity=absorptivity,
        diameter=cp.diameter,
        heat_capacity=heat_capacity,
        mass=mass,
        resistance_25c=cp.resistance_25c,
        resistance_alpha=resistance_alpha,
        expansion_alpha=expansion_alpha,
        youngs_modulus=youngs_modulus,
    )
