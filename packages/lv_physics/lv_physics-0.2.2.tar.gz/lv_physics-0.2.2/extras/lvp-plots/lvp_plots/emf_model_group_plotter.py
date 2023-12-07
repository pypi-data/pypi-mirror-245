import matplotlib.pyplot as plt
import numpy as np

from lv_physics.core.catenaries import gen_catenary_3d
from lv_physics.core.vectors import (
    X_AXIS,
    Y_AXIS,
    Z_AXIS,
    XYZ_FRAME,
    extrinsic_rotation_matrix,
    rotate_frame,
)
from lv_physics.emf.emf_const_objects import EMF_MODEL_GROUP_1
from lv_physics.emf.emf_objects import EmfModelGroup


CIRCUIT_COLORS = {n: f"C{n}" for n in range(10)}
PHASE_LINESTYLES = {"A": "solid", "B": "dotted", "C": "dashed"}


# ----------------------------------------------------------------------------------------------------------------------
# EMF MODEL GROUP PLOTTER


class EmfModelGroupPlotter:
    """
    A class dedicated to creating an EMF Model Group figure.
    """

    def __init__(
        self, figsize=(12, 8), title="EMF Model Group", view_azel=(30.0, 30.0), **kwargs
    ):
        """
        Initialize a 3d figure.
        """
        self.fig = plt.figure(figsize=figsize)

        self.ax = self.fig.add_subplot(111, projection="3d")
        self.ax.minorticks_on()
        self.ax.grid(False)
        self.ax.view_init(azim=view_azel[0], elev=view_azel[1])
        self.ax.set(xlabel="x [m]", ylabel="y [m]", zlabel="z [m]", title=title)
        self.ax.set(xlim=(-30, 30), ylim=(-30, 30), zlim=(-10, 20))
        self.ax.set(**kwargs)

    def plot_emf_model_group(self, model_group: EmfModelGroup):
        """
        Adds all EmfModelGroup features to the figure.
        """
        self.ax.set(title=f"EMF Model Group ID: {model_group.id}")

        for m, (_, circuit) in enumerate(model_group.circuits.items()):
            plot_circuit(self.ax, circuit, color=CIRCUIT_COLORS[m])

        for _, sensor in model_group.sensors.items():
            plot_sensor(self.ax, sensor)


# ---------------------------------------------------------------------------------------------------------------------
# HELPERS


def plot_curve(ax, X, alpha=1.0, color="black", ls="-", lw=1.0, **kwargs):

    ax.plot(
        X[..., 0],
        X[..., 1],
        X[..., 2],
        alpha=alpha,
        color=color,
        linestyle=ls,
        linewidth=lw,
    )


def plot_scatter(ax, X, alpha=1.0, color="black", marker="o", s=1.0):

    ax.scatter(
        X[..., 0], X[..., 1], X[..., 2], alpha=alpha, color=color, marker=marker, s=s
    )


def plot_quiver(ax, X, U, color="black"):

    ax.quiver(
        X[..., 0],
        X[..., 1],
        X[..., 2],
        U[..., 0],
        U[..., 1],
        U[..., 2],
        arrow_length_ratio=0.2,
        color=color,
    )


def plot_text(ax, point, label, color="black", offset=np.zeros(3)):

    ax.text(*(point + offset), label, color=color)


def plot_sensor(ax, sensor, color="black", marker="s", s=1.0):

    sensor_rotation_matrix = extrinsic_rotation_matrix(
        angles=sensor.ext_angles, axes=[0, 1, 2], order=sensor.rotation_order
    )
    sensor_frame = rotate_frame(
        rotation_matrix=sensor_rotation_matrix, coordinate_axes=XYZ_FRAME
    )

    plot_scatter(ax, sensor.position, color=color, marker=marker, s=10 * s)

    for color, axis in zip(["r", "g", "b"], sensor_frame):
        plot_quiver(ax, sensor.position, axis, color=color)

    label = f"{sensor.id}"
    offset = (X_AXIS + Y_AXIS + Z_AXIS) / 2
    plot_text(ax, sensor.position, label, offset=offset)


def plot_circuit(ax, circuit, n_points=1000, color="black", marker="s", s=1.0):

    for m, (_, circuit_span) in enumerate(circuit.spans.items()):
        for n, (_, conductor) in enumerate(circuit_span.conductors.items()):

            linestyle = PHASE_LINESTYLES[conductor.phase]

            # generate catenary
            cond_points = gen_catenary_3d(
                n_points=n_points,
                curvature=conductor.cat_curvature,
                end_point_a=conductor.mount_point_a,
                end_point_b=conductor.mount_point_b,
            )

            # conductor catenaries
            plot_curve(ax, cond_points, color=color, ls=linestyle, lw=s / 2)

            # conductor mount points
            plot_scatter(ax, conductor.mount_point_a, s=7 * s)
            plot_scatter(ax, conductor.mount_point_b, s=7 * s)

            # label
            label = f"{circuit.id}{conductor.phase}"
            offset = Z_AXIS * (1 + n / 3)
            plot_text(ax, conductor.mount_point_a, label, color="black", offset=offset)


# ----------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":

    mg_plotter_nie = EmfModelGroupPlotter()
    mg_plotter_nie.plot_emf_model_group(EMF_MODEL_GROUP_1)
    plt.show()
