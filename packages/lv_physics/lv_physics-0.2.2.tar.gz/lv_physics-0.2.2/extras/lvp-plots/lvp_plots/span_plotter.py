import numpy as np
from matplotlib.pyplot import Axes, Figure, GridSpec, figure, Polygon
from numpy.linalg import inv
from numpy.typing import NDArray

from lv_physics.core.dynamic_objects import DynamicConductor, DynamicInsulator
from lv_physics.core.ohl_objects import Sensor
from lv_physics.core.rotations import extrinsic_rotation_matrix, rotate_frame
from lv_physics.core.vectors import XYZ_FRAME
from lv_physics.general.objects import CircuitSpan


FIGSIZE = 10, 9
X_LIM = -10, 10
Y_LIM = -5, 35
Z_LIM = 0, 20

CONDUCTOR_COLORS = "firebrick", "forestgreen", "steelblue"


def cs_title(cs: CircuitSpan):
    return f"Site Group {cs.id}: {cs.name}"


class SpanFigure3D:

    fig: Figure
    gsp: GridSpec
    ax: Axes

    def __init__(self):

        fig = figure(figsize=FIGSIZE)
        gsp = fig.add_gridspec(1, 1)

        ax = fig.add_subplot(gsp[0, 0], projection="3d")
        ax.set(xlabel="x [m]", ylabel="y [m]", zlabel="z [m]")
        ax.set(xlim=X_LIM, ylim=Y_LIM, zlim=Z_LIM)
        ax.minorticks_on()
        ax.grid(False)

        fig.subplots_adjust(left=0, bottom=0, right=1, top=1)

        self.fig = fig
        self.gsp = gsp
        self.ax = ax

    # HELPERS

    def set(self, **kwargs):
        self.ax.set(**kwargs)

    def plot_curve(self, curve: NDArray[float], alpha=1.0, color="black", ls=1.0, lw=1.0):
        self.ax.plot(
            curve[..., 0],
            curve[..., 1],
            curve[..., 2],
            alpha=alpha,
            color=color,
            linestyle=ls,
            linewidth=lw,
        )

    def plot_scatter(self, points: NDArray[float], alpha=1.0, color="black", marker="o", s=1.0):
        self.ax.scatter(
            points[..., 0],
            points[..., 1],
            points[..., 2],
            alpha=alpha,
            color=color,
            marker=marker,
            s=s,
        )

    def plot_quiver(self, points: NDArray[float], vectors: NDArray[float], color="black", s=2.0):
        self.ax.quiver(
            points[..., 0],
            points[..., 1],
            points[..., 2],
            vectors[..., 0],
            vectors[..., 1],
            vectors[..., 2],
            color=color,
            arrow_length_ratio=s / 10,
        )

    def plot_text(self, point, label, color="black", offset=np.zeros(3)):
        self.ax.text(*(point + offset), label, color=color)

    # MAIN PLOTS

    def plot_circuit_span(self, circuit_span: CircuitSpan):

        self.fig.suptitle(cs_title(circuit_span))

        for cond_id, conductor in circuit_span.conductors.items():
            self.plot_conductor(
                conductor,
                color=CONDUCTOR_COLORS[conductor.id % 3],
                label=f"{conductor.id}"
            )

        for sensor_id, sensor in circuit_span.sensors.items():
            self.plot_sensor(sensor)

    def plot_sensor(self, sensor: Sensor, color="black", marker="s", s=1.0, label=None):
        label = f"{sensor.id}"
        offset = XYZ_FRAME[0] / 2

        sensor_rotation_matrix = extrinsic_rotation_matrix(
            angles=sensor.ext_angles, axes=[0, 1, 2], order=sensor.rotation_order
        )

        sensor_frame = rotate_frame(
            rotation_matrix=sensor_rotation_matrix, coordinate_axes=XYZ_FRAME
        )

        for color, axis in zip(["r", "g", "b"], sensor_frame):
            self.plot_quiver(sensor.position, axis, color=color)
        self.plot_scatter(sensor.position, color=color, marker=marker, s=10 * s)
        self.plot_text(sensor.position, label, offset=offset)

    def plot_fov(self, sensor: Sensor, fov: NDArray[float], R: float = 100.0, color='lightgreen', alpha=0.2):
        """
        Plots the field of view of a camera in 3D.
        """
        # Determine the rotation of the sensor frame
        rotation = sensor.frame @ inv(XYZ_FRAME)

        # Define the corners of the pyramid in the camera's coordinate system
        corners = np.array([
            [R, -R * np.tan(fov[0]/2), -R * np.tan(fov[1]/2)],  # lower left
            [R,  R * np.tan(fov[0]/2), -R * np.tan(fov[1]/2)],  # lower right
            [R,  R * np.tan(fov[0]/2),  R * np.tan(fov[1]/2)],  # upper right
            [R, -R * np.tan(fov[0]/2),  R * np.tan(fov[1]/2)],   # upper left
        ])

        # Transform the corners to the world coordinate system
        corners_world = np.einsum("mn, ...n -> ...m", rotation, corners) + sensor.position

        # Plot the edges of the pyramid
        self.ax.plot([0, corners_world[0, 0]], [0, corners_world[0, 1]], [0, corners_world[0, 2]], color=color)
        self.ax.plot([0, corners_world[1, 0]], [0, corners_world[1, 1]], [0, corners_world[1, 2]], color=color)
        self.ax.plot([0, corners_world[2, 0]], [0, corners_world[2, 1]], [0, corners_world[2, 2]], color=color)
        self.ax.plot([0, corners_world[3, 0]], [0, corners_world[3, 1]], [0, corners_world[3, 2]], color=color)

        # Connect the corners to form the base of the pyramid
        self.ax.plot([corners_world[0, 0], corners_world[1, 0]], [corners_world[0, 1], corners_world[1, 1]], [corners_world[0, 2], corners_world[1, 2]], color=color)
        self.ax.plot([corners_world[1, 0], corners_world[2, 0]], [corners_world[1, 1], corners_world[2, 1]], [corners_world[1, 2], corners_world[2, 2]], color=color)
        self.ax.plot([corners_world[2, 0], corners_world[3, 0]], [corners_world[2, 1], corners_world[3, 1]], [corners_world[2, 2], corners_world[3, 2]], color=color)
        self.ax.plot([corners_world[3, 0], corners_world[0, 0]], [corners_world[3, 1], corners_world[0, 1]], [corners_world[3, 2], corners_world[0, 2]], color=color)

        # Plot
        for point in corners_world:
            self.ax.plot(
                [sensor.position[0], point[0]],
                [sensor.position[1], point[1]],
                [sensor.position[2], point[2]],
                color="lightgreen",
                alpha=0.25,
                lw=3,
            )

        # Create vertices
        # x = np.append(corners_world[:, 0], 0)
        # y = np.append(corners_world[:, 1], 0)
        # z = np.append(corners_world[:, 2], 0)
        # verts = [list(zip(x, y, z))]

        # # Fill the pyramid with color
        # self.ax.add_collection3d(Polygon(verts, color=color, alpha=alpha, linewidth=1))

    def plot_scan(self, scan, alpha=0.8, color="black", s=2.0, label=None):
        self.ax.scatter(*scan.T, alpha=alpha, color=color, s=s, label=label)

    def plot_conductor(
        self,
        conductor: DynamicConductor,
        alpha=1.0,
        color="black",
        ls="-",
        lw=1.0,
        label=None,
    ):

        # plot the conductor points
        for n, offset in enumerate(conductor.bundle.offsets):
            b_label = label if n == 0 else None
            self.ax.plot(
                conductor.points[:, 0] + offset[0],
                conductor.points[:, 1] + offset[1],
                conductor.points[:, 2] + offset[2],
                alpha=alpha,
                color=color,
                ls=ls,
                lw=lw,
                label=b_label,
            )

        # plot the insulator points
        self.plot_insulator(
            conductor.insulators[0], alpha=alpha, color=color, ls=ls, lw=3 * lw
        )
        self.plot_insulator(
            conductor.insulators[1], alpha=alpha, color=color, ls=ls, lw=3 * lw
        )

        if label is not None:
            self.ax.legend()

    def plot_insulator(
        self,
        ins: DynamicInsulator,
        alpha=1.0,
        color="black",
        ls="-",
        lw=1.0,
        label=None,
    ):

        ins_points = np.array([ins.mounts[0], ins.connect])

        self.ax.plot(
            *ins_points.T,
            alpha=alpha,
            color=color,
            lw=lw,
            marker="D",
            ms=lw,
        )


if __name__ == "__main__":
    span_fig = SpanFigure3D()
    span_fig.fig.show()
