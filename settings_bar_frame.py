from tkinter import *
from customtkinter import *
from application_state import gate, state
from gate import Gate
import numpy as np


def render_settings_bar_frame(root, rerender_bloch_frame):
    settings_bar = CTkFrame(master=root)
    settings_bar.pack(side=RIGHT, fill="both", expand=True)

    matrix_form = CTkFrame(master=settings_bar)
    matrix_form.pack(side=TOP, fill="both", expand=True)

    matrix_label = CTkLabel(master=matrix_form, text="Matrix:")
    matrix_label.pack(side=LEFT)

    matrix_entries = [
        CTkEntry(
            master=matrix_form,
            width=5,
            placeholder_text=f"{gate.U[i % 2, i // 2]:.2f}",
        )
        for i in range(4)
    ]

    for i, entry in enumerate(matrix_entries):
        entry.bind(
            "<Return>",
            lambda _: save_and_rerender(),
        )
        entry.pack(side=LEFT)

    state_form = CTkFrame(master=settings_bar)
    state_form.pack(side=TOP, fill="both", expand=True)

    def save_and_rerender():

        matrix_entry_values = list(map(lambda entry: entry.get(), matrix_entries))
        matrix_entry_filled_values = list(
            map(
                lambda val: (
                    complex(val[0]) if val[0] is not None and val[0] != "" else val[1]
                ),
                zip(matrix_entry_values, gate.U.flatten()),
            )
        )

        new_matrix = np.array(matrix_entry_filled_values).reshape(2, 2)
        new_matrix /= np.linalg.norm(new_matrix)
        # gate = Gate(new_matrix)
        gate.set_matrix(new_matrix)
        rerender_bloch_frame()

    state_label = CTkLabel(master=state_form, text="State:")
    state_label.pack(side=LEFT)

    button_rerender = CTkButton(
        master=settings_bar, text="Rerender", command=rerender_bloch_frame
    )
    button_rerender.pack(side=BOTTOM)
