from dataclasses import dataclass, field
from typing import List, Optional

from dataclasses_json import dataclass_json
from numpy import array, float_, int_, nan, zeros
from numpy.typing import NDArray

from lv_physics.core.rotations import extrinsic_rotation_matrix, rotate_frame
from lv_physics.core.vectors import XYZ_FRAME
from lv_physics.utils.dataclass_helpers import array_field


@dataclass_json
@dataclass
class Sensor:
    """
    Represents a sensor with an identifier, position, orientation, and rotation order.

    Attributes:
        id: Unique identifier of the sensor.
        position: 3D position of the sensor as an NDArray.
        ext_angles: Extrinsic orientation angles of the sensor as an NDArray.
        rotation_order: Order of rotations for the sensor's orientation as an NDArray.
    """

    id: int
    position: NDArray[float_] = array_field(lambda: zeros(3, float_))
    ext_angles: NDArray[float_] = array_field(lambda: zeros(3, float_))
    rotation_order: NDArray[int_] = array_field(lambda: array([2, 1, 0], int_))

    @property
    def frame(self):
        """
        Returns the coordinate frame of the sensor.
        """
        # Calculate the rotation matrix based on the extensive orientation angles
        ext_matrix = extrinsic_rotation_matrix(
            self.ext_angles,
            axes=[0, 1, 2],
            order=self.rotation_order,
        )

        # Rotate the xyz-coordinate frame to the sensor frame
        frame = rotate_frame(ext_matrix, XYZ_FRAME)

        return frame


@dataclass_json
@dataclass
class ConductorBundle:
    """
    Represents a bundle of conductors, specifying offsets for each conductor.

    Attributes:
        offsets: Offsets for each conductor in the bundle as an NDArray.
    """

    offsets: NDArray[float_] = array_field(lambda: zeros((1, 3), float_))

    @property
    def count(self) -> int:
        return len(self.offsets)


@dataclass_json
@dataclass
class ConductorMaterial:
    """
    Describes the material properties of a conductor.

    Attributes:
        name: Name of the conductor material.
        type: Type of the conductor material.
        absorptivity: Absorptivity coefficient.
        emissivity: Emissivity coefficient.
        diameter: Diameter of the conductor.
        mass: Mass per unit length of the conductor.
        heat_capacity: Heat capacity of the material.
        resistance_25c: Electrical resistance at 25 degrees Celsius.
        resistance_alpha: Temperature coefficient of resistance.
        expansion_alpha: Coefficient of thermal expansion.
        youngs_modulus: Young's modulus of the material.
    """

    name: str = "Drake"
    type: str = "ACSR"
    absorptivity: float = 0.8
    emissivity: float = 0.8
    diameter: float = 0.0281432
    mass: float = 1.628
    heat_capacity: float = 1280.069
    resistance_25c: float = 0.000382546
    resistance_alpha: float = 0.000385935
    expansion_alpha: float = 0.00000918141
    youngs_modulus: float = 77056.5363


@dataclass_json
@dataclass
class ConductorShape:
    """
    Defines the shape characteristics of a conductor.

    Attributes:
        curvature: Curvature parameter of the conductor.
        swing_angle: Swing angle of the conductor.
    """

    curvature: float = nan
    swing_angle: float = nan


@dataclass_json
@dataclass
class ConductorState:
    """
    Represents the state of a conductor in terms of loading and temperature.

    Attributes:
        loading: The loading on the conductor.
        temperature: The temperature of the conductor.
    """

    loading: float = nan
    temperature: float = nan


@dataclass_json
@dataclass
class Insulator:
    """
    Describes an insulator, including its mount points and connection points.

    Attributes:
        mounts: Mount points of the insulator as an NDArray.
        connect: Connection points of the insulator as an NDArray.
        rest_connect: Resting connection points of the insulator as an NDArray.
    """

    mounts: NDArray[float_] = array_field(lambda: array([[nan, nan, nan]], float_))
    connect: NDArray[float_] = array_field(lambda: array([nan, nan, nan], float_))
    rest_connect: NDArray[float_] = array_field(lambda: array([nan, nan, nan], float_))


@dataclass_json
@dataclass
class Conductor:
    """
    Represents a conductor with its unique identifier, bundle configuration, insulators, material, physical points,
    shape, and state.

    Attributes:
        id: Unique identifier of the conductor.
        bundle: Configuration of the conductor bundle.
        insulators: List of insulators associated with the conductor.
        material: Material properties of the conductor.
        points: Physical points defining the conductor's geometry.
        shape: Shape characteristics of the conductor.
        state: State of the conductor in terms of loading and temperature.
    """

    id: int
    bundle: Optional[ConductorBundle] = field(default_factory=ConductorBundle)
    insulators: Optional[List[Insulator]] = None
    material: Optional[ConductorMaterial] = None
    points: Optional[NDArray] = None
    shape: Optional[ConductorShape] = None
    state: Optional[ConductorState] = None

    @property
    def connects(self) -> NDArray[float_]:
        """
        Returns a (2 x 3)-array of the points of the conductor which connect to the insulator.
        """
        return array([insulator.connect for insulator in self.insulators])
