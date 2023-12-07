from dataclasses import dataclass
from typing import Iterable, List

import numpy as np
from dataclasses_json import dataclass_json
from numpy import float_, zeros
from numpy.typing import NDArray

from lv_physics.core.catenaries import (
    catenary_length,
    catenary_sag,
    catenary_vertex,
    fit_catenary,
    fit_curvature_from_length,
    gen_catenary_3d,
)
from lv_physics.core.ohl_objects import Conductor, Insulator
from lv_physics.core.rotations import rotate
from lv_physics.core.vectors import X_AXIS, Y_AXIS, Z_AXIS, cross, mag, unit
from lv_physics.utils.dataclass_helpers import array_field


# NOTE: Areas where improvement are needed:
# 1. The optional attributes of the class are not handled.
# 2. The temperature of the conductor could be related to the length of the conductor.


@dataclass_json
@dataclass
class DynamicInsulator(Insulator):
    """
    A specialized Insulator class with additional methods for manipulating insulator orientation and calculating
    geometrical properties.
    """

    def __post_init__(self):
        """
        Initializes the DynamicInsulator instance by setting the rest position of the insulator.
        """
        self.rest_connect = self.connect + 0.0

    @property
    def length(self) -> NDArray[float_]:
        """
        Calculate the length of the insulator between its end-points.

        Returns:
            The length of the insulator as an NDArray.
        """
        return self.pivot_point - self.connect

    @property
    def pivot_point(self) -> NDArray[float_]:
        """
        Determine the pivot point of the insulator, currently defined as the mean of its mount points.

        Returns:
            The pivot point of the insulator as an NDArray.
        """
        return self.mounts.mean(axis=0)

    def set(self, angles: List[float], axes: List[NDArray[float_]]) -> None:
        """
        Set the orientation of the insulator by rotating the connect-point and storing the new angles.

        Args:
            angles: A list of rotation angles.
            axes: A list of rotation axes corresponding to the angles.
        """
        self.connect[:] = self.rest_connect[:] + 0.0

        for k in range(len(angles)):
            self.connect[:] = rotate(
                self.connect,
                angle=angles[k],
                axis=axes[k],
                point=self.pivot_point,
            )

    def reset(self) -> None:
        """
        Reset the insulator to its rest position.
        """
        self.connect = self.rest_connect + 0.0


@dataclass_json
@dataclass
class DynamicConductor(Conductor):
    """
    Extends the Conductor class with additional properties and methods for dynamic operations.

    Attributes:
        insulators: A list of Insulators associated with the conductor.
        points: An NDArray representing the physical points defining the conductor's geometry.
    """

    insulators: List[Insulator]
    points: NDArray[float_] = array_field(default_factory=lambda: zeros((0, 3), float_))

    @property
    def n_points(self) -> int:
        """
        Determine the number of points in the conductor's points array.

        Returns:
            The count of points in the conductor's points array.
        """
        return len(self.points)

    @property
    def curvature(self) -> float:
        """
        Retrieve the curvature of the conductor's shape.

        Returns:
            The curvature of the conductor.
        """
        return self.shape.curvature

    @property
    def swing_angle(self) -> float:
        """
        Obtain the swing angle of the conductor's shape.

        Returns:
            The swing angle of the conductor.
        """
        return self.shape.swing_angle

    @property
    def loading(self) -> float:
        """
        Access the loading state of the conductor.

        Returns:
            The loading value of the conductor.
        """
        return self.state.loading

    @property
    def resistance(self) -> float:
        """
        Calculate the electrical resistance of the conductor based on its temperature.

        Returns:
            The calculated resistance of the conductor.
        """
        return (
            self.material.resistance_25c
            * (1.0 + self.material.resistance_alpha * (self.state.temperature - 25.0))
            / self.bundle.count**2
        )

    @property
    def temperature(self) -> float:
        """
        Get the current temperature of the conductor.

        Returns:
            The temperature of the conductor.
        """
        return self.state.temperature

    @property
    def connect_axis(self) -> NDArray[float_]:
        """
        Determine the axis spanned by the conductor's end-points.

        Returns:
            An NDArray representing the axis spanned by the conductor's end-points.
        """
        return unit(self.connects[1] - self.connects[0])

    @property
    def normal_axis(self) -> NDArray[float_]:
        """
        Calculate the axis perpendicular to both the span axis and the z-axis.

        Returns:
            An NDArray representing the normal axis.
        """
        return unit(cross(self.span_axis, Z_AXIS))

    @property
    def span_axis(self) -> NDArray[float_]:
        """
        Determine the axis spanned by the conductor's end-points, projected onto the xy-plane.

        Returns:
            An NDArray representing the span axis.
        """
        return self.connect_axis * (X_AXIS + Y_AXIS)

    @property
    def chord_length(self) -> float:
        """
        Calculate the straight-line length between the conductor's connect-points.

        Returns:
            The chord length of the conductor.
        """
        return mag(self.connects[1] - self.connects[0])

    @property
    def length(self) -> float:
        """
        Compute the parametric length of the conductor between its end-points.

        Returns:
            The parametric length of the conductor.
        """
        return catenary_length(
            self.shape.curvature,
            self.connects[0, 2],
            self.connects[1, 2],
            self.span_length,
        )

    @property
    def length_to_vertex(self, n: int = 0) -> float:
        """
        Calculate the length of the conductor from the n-th end-point to its vertex.

        Args:
            n: Index of the end-point (0 or 1).

        Returns:
            The length from the specified end-point to the catenary vertex.
        """
        s_vertex = catenary_vertex(
            self.shape.curvature,
            self.connects[0, 2],
            self.connects[1, 2],
            self.span_length,
        )

        bounds = [0, s_vertex] if n == 0 else [s_vertex, self.span_length]

        return catenary_length(
            self.shape.curvature,
            self.connects[0, 2],
            self.connects[1, 2],
            self.span_length,
            bounds=bounds,
        )

    @property
    def span_length(self) -> float:
        """
        Determine the horizontal span length between the conductor's connect-points.

        Returns:
            The horizontal span length of the conductor.
        """
        return mag((self.connects[1] - self.connects[0]) * (X_AXIS + Y_AXIS))

    @property
    def sag(self) -> float:
        """
        Calculate the maximum resting sag of the conductor.

        Returns:
            The maximum sag of the conductor.
        """
        return catenary_sag(
            self.shape.curvature,
            self.connects[0, 2],
            self.connects[1, 2],
            self.span_length,
        )

    @property
    def net_mass(self) -> float:
        """
        Compute the net mass of the conductor from end-to-end.

        Returns:
            The net mass of the conductor.
        """
        return self.material.mass * self.length

    @property
    def mass_to_vertex(self, n: int = 0) -> float:
        """
        Calculate the mass of the conductor from the n-th end-point to the vertex.

        Args:
            n: Index of the end-point (0 or 1).

        Returns:
            The mass of the conductor from the specified end-point to the vertex.
        """
        return self.material.mass * self.length_to_vertex(n)

    @property
    def tension_at_connect(self, n: int = 0) -> NDArray[float_]:
        """
        Calculate the tension vector through the conductor from the n-th end-point.

        Args:
            n: Index of the end-point (0 or 1).

        Returns:
            The tension vector at the specified end-point.
        """
        tension_h = self.shape.curvature * self.material.mass * 9.80665 * self.span_axis
        tension_v = self.mass_to_vertex(n) * 9.80665 * Z_AXIS

        return tension_h + tension_v

    def get_wind_speed(self, air_density: float = 1.225, drag_coeff: float = 1.2) -> float:
        """
        Calculate the wind speed component normal to the conductor's span axis.

        Args:
            air_density: The air density in kg/m^3. Defaults to 1.225.
            drag_coeff: The drag coefficient. Defaults to 1.2.

        Returns:
            The wind speed normal to the span axis of the conductor.
        """
        force_g = -self.material.mass * 9.80665
        force_w = force_g * np.tan(self.shape.swing_angle)

        return np.sign(force_w) * np.sqrt(2 * np.abs(force_w) / self.material.diameter / air_density / drag_coeff)

    def rotate(self, angle: float) -> None:
        """
        Rotate the conductor points about its end-point axis by a specified angle.

        Args:
            angle: The rotation angle in radians.
        """
        self.points[:] = rotate(
            self.points[:],
            angle,
            axis=self.connect_axis,
            point=self.connects[0],
        )

    def set_blowout(self, swing_angle: float, insulator_swing_factor: float = 0.0) -> None:
        """
        Set the swing angle of the conductor and rotate its points accordingly. Also rotates the insulators by a
        fraction of the conductor's swing angle.

        Args:
            swing_angle: The swing angle in radians.
            insulator_swing_factor: The factor by which the insulators will swing relative to the conductor.
                Defaults to 0.0.
        """
        if insulator_swing_factor > 0.0:
            for n in range(len(self.insulators)):
                insulator_swing_angle = insulator_swing_factor * swing_angle
                self.set_insulator(n=n, angles=[insulator_swing_angle, 0.0], fix_length=True)

        self.rotate(swing_angle - self.shape.swing_angle)
        self.shape.swing_angle = swing_angle + 0.0

    def set_curvature(self, curvature: float) -> None:
        """
        Update the curvature value of the conductor.

        Args:
            curvature: The new curvature value to be set.
        """
        self.shape.curvature = curvature + 0.0
        self.set_points(self.n_points)

    def set_curvature_from_length(self, length: float) -> None:
        """
        Adjust the curvature parameter of the conductor based on a given length.

        Args:
            length: The target length for the conductor.
        """
        self.set_curvature(
            fit_curvature_from_length(
                end_point_a=self.connects[0],
                end_point_b=self.connects[1],
                length=length,
            )
        )

    def set_thermal_expansion(self, temperature_delta: float) -> None:
        """
        Adjust the curvature of the conductor to account for thermal length expansion due to a temperature change.

        Args:
            temperature_delta: The change in temperature.
        """
        if self.state is not None:
            self.state.temperature += temperature_delta

        self.set_curvature_from_length(self.length * (1.0 + self.material.expansion_alpha * temperature_delta))

    def set_insulator(self, n: int, angles: Iterable[float], fix_length: bool = True) -> None:
        """
        Rotate the n-th insulator and update conductor properties dependent on the end-point. The 'angles' list
        specifies the rotation about the span axis and the axis normal to both the span and z axes.

        Args:
            n: Index of the insulator to be rotated.
            angles: A list of angles for rotation.
            fix_length: Flag to maintain the conductor's length after rotation.
        """
        if fix_length:
            length_0 = self.length

        self.insulators[n].set(angles=angles, axes=[self.span_axis, self.normal_axis])

        if fix_length:
            self.set_curvature_from_length(length_0)

        self.set_points(self.n_points)

    def set_points(self, n_points: int) -> None:
        """
        Generate a set of points along the conductor, evenly spaced along the span axis.

        Args:
            n_points: The number of points to generate along the conductor.
        """
        self.points = gen_catenary_3d(
            n_points=n_points,
            curvature=self.shape.curvature,
            end_point_a=self.connects[0],
            end_point_b=self.connects[1],
        )

        if np.abs(self.shape.swing_angle) > 0.0:
            self.rotate(self.shape.swing_angle)

    def set_curvature_from_midspan_sag(self, midspan_sag: float) -> None:
        """
        Determine the curvature of a catenary that aligns with both connect points and a specified midspan sag.

        Args:
            midspan_sag: The sag at the midpoint of the span.
        """
        midspan_straight_line_height = self.insulators[0].connect[2] + (
            (self.insulators[1].connect[2] - self.insulators[0].connect[2]) / 2
        )
        midspan_sag_height = midspan_straight_line_height - midspan_sag
        curvature = fit_catenary(
            s=(self.span_length / 2),
            z=midspan_sag_height,
            height_a=self.connects[0, 2],
            height_b=self.connects[1, 2],
            span_length=self.span_length,
        )
        self.set_curvature(curvature)
