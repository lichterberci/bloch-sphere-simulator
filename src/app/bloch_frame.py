from typing import Deque, Dict, Union
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib import animation
from tkinter import *
from customtkinter import *

from application_state import gate, state, history

import sys
import os.path

# for being able to import from src
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)

from bloch_simulator.state import State
from bloch_simulator.gate import Gate

HISTORY_COLOR = (0.7, 0.3, 0)

canvas = None
transform_animation = None
prev_elevation, prev_azimuth = 30, -45
fig = None

def draw_bloch_figure(
    gate: Gate,
    state: State,
    history: Deque[Dict[str, Union[Gate, State]]],
    figsize=(7, 7),
    figure_background_color="#202020",
    figure_foreground_color="white",
    from_arrow_color="red",
    to_arrow_color="green",
    rotation_axis_color="blue",
    path_color="blue",
):

    fig = Figure(figsize=figsize, dpi=100)

    ax = fig.add_subplot(111, projection="3d")

    fig.patch.set_facecolor(figure_background_color)

    ax.set_facecolor(figure_background_color)
    # set foreground color
    ax.xaxis.label.set_color(figure_foreground_color)
    ax.yaxis.label.set_color(figure_foreground_color)
    ax.zaxis.label.set_color(figure_foreground_color)
    ax.xaxis.set_pane_color((0.1, 0.1, 0.1, 0.0))
    ax.yaxis.set_pane_color((0.1, 0.1, 0.1, 0.0))
    ax.zaxis.set_pane_color((0.1, 0.1, 0.1, 0.0))
    ax.tick_params(axis="x", colors=figure_foreground_color)
    ax.tick_params(axis="y", colors=figure_foreground_color)
    ax.tick_params(axis="z", colors=figure_foreground_color)
    ax.grid(False)
    ax.xaxis._axinfo["grid"]["color"] = figure_foreground_color
    ax.yaxis._axinfo["grid"]["color"] = figure_foreground_color
    ax.zaxis._axinfo["grid"]["color"] = figure_foreground_color
    ax.xaxis._axinfo["tick"]["color"] = figure_foreground_color
    ax.yaxis._axinfo["tick"]["color"] = figure_foreground_color
    ax.zaxis._axinfo["tick"]["color"] = figure_foreground_color
    ax.xaxis._axinfo["axisline"]["linewidth"] = 1
    ax.yaxis._axinfo["axisline"]["linewidth"] = 1
    ax.zaxis._axinfo["axisline"]["linewidth"] = 1
    ax.xaxis.line.set_color((1, 1, 1, 0.5))
    ax.yaxis.line.set_color((1, 1, 1, 0.5))
    ax.zaxis.line.set_color((1, 1, 1, 0.5))

    def draw_wireframe_sphere(figure_foreground_color, ax):
        num_lines_in_wireframe = 30

        # draw the bloch sphere
        u = np.linspace(0, 2 * np.pi, num_lines_in_wireframe)
        v = np.linspace(0, np.pi, num_lines_in_wireframe)
        x = np.outer(np.cos(u), np.sin(v))
        y = np.outer(np.sin(u), np.sin(v))
        z = np.outer(np.ones(np.size(u)), np.cos(v))
        ax.plot_wireframe(x, y, z, color=figure_foreground_color, alpha=0.1)

    draw_wireframe_sphere(figure_foreground_color, ax)

    p_from = state.bloch_coordinates
    p_to = gate(state).bloch_coordinates

    num_pts = 100


    def draw_history_line(_gate: Gate, _state: State, color, linestyle="-"):
        t = np.linspace(0, _gate.rotation_angle, num_pts)
        _points = list(
            map(
                lambda p: p.bloch_coordinates,
                [Gate.from_rotation(_gate.rotation_axis, _t).apply(_state) for _t in t],
            )
        )    
        
        ax.plot(*np.array(_points).T, color=color, linestyle=linestyle, lw=3) 
    
    num_history_lines = len(history)
    
    for i, history_state in enumerate(history):
        min_alpha = 0.3
        alpha = min_alpha + ((i + 1) / (num_history_lines)) * (1 - min_alpha)
        c = (*HISTORY_COLOR, alpha)
        draw_history_line(history_state["gate"], history_state["state"], c, linestyle="--")
    
    t = np.linspace(0, gate.rotation_angle, num_pts)
    points = list(
        map(
            lambda p: p.bloch_coordinates,
            [Gate.from_rotation(gate.rotation_axis, _t).apply(state) for _t in t],
        )
    )

    ax.quiver(0, 0, 0, *p_from, color=from_arrow_color, label="Initial State", lw=3)
    ax.quiver(0, 0, 0, *p_to, color=to_arrow_color, label="Final State", lw=3)
    ax.quiver(
        0,
        0,
        0,
        *(gate.rotation_axis / np.linalg.norm(gate.rotation_axis)),
        color=rotation_axis_color,
        label="Rotation Axis",
        alpha=0.5,
        linestyle="--",
        lw=3,
    )

    ax.set_xlabel("X", fontsize=15)
    ax.set_ylabel("Y", fontsize=15)
    ax.set_zlabel("Z", fontsize=15)
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(-1, 1)
    ax.set_xticks([-1, 0, 1])
    ax.set_yticks([-1, 0, 1])
    ax.set_zticks([-1, 0, 1])

    ax.set_box_aspect([1, 1, 1])
    ax.set_aspect("equal")
    ax.set_title(f"Bloch sphere", color=figure_foreground_color, fontsize=20)

    leg = ax.legend(
        loc="upper center", fancybox=True, bbox_to_anchor=(0.5, -0.05), ncol=4
    )
    leg.get_frame().set_facecolor(figure_background_color)
    leg.get_frame().set_linewidth(0)
    
    # reset camera
    ax.view_init(elev=prev_elevation, azim=prev_azimuth)

    for text in leg.get_texts():
        text.set_color(figure_foreground_color)

    [line] = ax.plot([], [], [], color=path_color, lw=3, linestyle="-")
    return fig, num_pts, points, line


def render_bloch_frame(root: CTk):
    to_color = (1, 1, 0, 0.5)
    from_color = (1, 0, 0, 1)

    global fig, prev_elevation, prev_azimuth

    if fig is not None:
        prev_elevation = fig.axes[0].elev
        prev_azimuth = fig.axes[0].azim
        plt.close(fig)

    global history

    fig, num_pts, points, line = draw_bloch_figure(
        gate,
        state,
        history,
        figsize=(7, 7),
        figure_background_color="#202020",
        path_color="magenta",
        rotation_axis_color="cyan",
        from_arrow_color=from_color,
        to_arrow_color=to_color,
    )

    global canvas
    if canvas is not None:
        canvas.get_tk_widget().pack_forget()

    canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
    canvas.draw()

    def update(i):
        interpolated_color = tuple(
            i / num_pts * np.array(to_color) + (1 - i / num_pts) * np.array(from_color)
        )
        line.set_data_3d(*np.array(points[: i + 1]).T)
        line.set_color(interpolated_color)
        return line

    animation_time = 2000
    delay_time = 1000

    global transform_animation
    if transform_animation is not None:
        transform_animation.event_source.stop()

    transform_animation = animation.FuncAnimation(
        fig,
        update,
        frames=num_pts,
        interval=animation_time / num_pts,
        blit=False,
        repeat=True,
        repeat_delay=delay_time,
    )

    # start the animation
    transform_animation.event_source.start()

    # pack_toolbar=False will make it easier to use a layout manager later on.
    toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
    toolbar.update()

    canvas.get_tk_widget().pack(side=LEFT, fill="both", expand=True)
