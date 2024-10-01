from tkinter import *
from customtkinter import *
from application_state import gate, state
from gate import Gate
import numpy as np

from state import State


def render_settings_bar_frame(root, rerender_bloch_frame):
    settings_bar = CTkFrame(master=root)
    settings_bar.pack(side=RIGHT, fill="both", expand=True)

    matrix_form = CTkFrame(master=settings_bar)
    matrix_form.pack(side=TOP, fill="both", expand=True)
    matrix_form.grid_rowconfigure(tuple(range(5)), weight=1)
    matrix_form.grid_columnconfigure(tuple(range(2)), weight=1)

    matrix_label = CTkLabel(master=matrix_form, text="Unitary matrix:")
    matrix_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="news")

    matrix_entries = [
        CTkEntry(
            master=matrix_form,
            width=120,
        )
        for i in range(4)
    ]

    for i, entry in enumerate(matrix_entries):
        entry.bind(
            "<Return>",
            lambda _: save_and_rerender(),
        )
        entry.bind("<FocusOut>", lambda _: save_and_rerender)
        entry.insert(0, f"{gate.U[i % 2, i // 2]:.5f}")
        entry.grid(row=i // 2 + 1, column=i % 2, padx=5, pady=5, sticky="news")

    predefined_matrices = [
        Gate("X").U,
        Gate("Y").U,
        Gate("Z").U,
        Gate("H").U,
    ]

    def set_matrix(matrix):
        gate.set_matrix(matrix)
        for i, entry in enumerate(matrix_entries):
            entry.delete(0, END)
            entry.insert(0, f"{matrix[i % 2, i // 2]:.5f}")

        save_and_rerender()

    predefined_matrix_btns = [
        CTkButton(
            master=matrix_form,
            text=f"{Gate(matrix)}",
            command=lambda matrix=matrix: set_matrix(matrix),
        )
        for matrix in predefined_matrices
    ]

    for i, btn in enumerate(predefined_matrix_btns):
        btn.grid(row=3 + i % 2, column=i // 2, padx=5, pady=5, sticky="news")

    state_form = CTkFrame(master=settings_bar)
    state_form.pack(side=TOP, fill="both", expand=True)
    state_form.grid_rowconfigure(tuple(range(5)), weight=1)
    state_form.grid_columnconfigure(tuple(range(2)), weight=1)

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
        gate.set_matrix(new_matrix)

        state_entry_values = list(map(lambda entry: entry.get(), state_entries))
        state_entry_filled_values = list(
            map(
                lambda val: (
                    complex(val[0]) if val[0] is not None and val[0] != "" else val[1]
                ),
                zip(state_entry_values, state.state),
            )
        )
        new_state = np.array(state_entry_filled_values)

        state.set_state(new_state)

        rerender_bloch_frame()

    state_label = CTkLabel(master=state_form, text="State:")
    state_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="news")

    state_entries = [
        CTkEntry(
            master=state_form,
            width=120,
        )
        for i in range(2)
    ]

    for i, entry in enumerate(state_entries):
        entry.bind(
            "<Return>",
            lambda _: save_and_rerender(),
        )
        entry.bind(
            "<FocusOut>",
            lambda _: save_and_rerender(),
        )
        entry.insert(0, f"{state[i]:.5f}")
        entry.grid(row=i // 2 + 1, column=i % 2, padx=5, pady=5, sticky="news")

    predefined_states = [
        State(np.array([1, 0])),
        State(np.array([0, 1])),
        State(np.array([1 / np.sqrt(2), 1 / np.sqrt(2)])),
        State(np.array([1 / np.sqrt(2), -1 / np.sqrt(2)])),
    ]

    def set_state(state):
        state.set_state(state.state)

        for i, entry in enumerate(state_entries):
            entry.delete(0, END)
            entry.insert(0, f"{state[i]:.5f}")

        save_and_rerender()

    predefined_state_btns = [
        CTkButton(
            master=state_form,
            text=f"{_state}",
            command=lambda s=_state: set_state(s),
        )
        for _state in predefined_states
    ]

    for i, btn in enumerate(predefined_state_btns):
        btn.grid(row=3 + i % 2, column=i // 2, padx=5, pady=5, sticky="news")

    def apply_gate():

        state.set_state(gate * state)

        for i, entry in enumerate(state_entries):
            entry.delete(0, END)
            entry.insert(0, f"{state[i]:.5f}")
            entry.grid(row=i // 2 + 1, column=i % 2, padx=5, pady=5, sticky="news")

        rerender_bloch_frame()

    button_apply = CTkButton(master=settings_bar, text="Apply", command=apply_gate)
    button_apply.pack(side=BOTTOM)

    button_rerender = CTkButton(
        master=settings_bar, text="Rerender", command=rerender_bloch_frame
    )
    button_rerender.pack(side=BOTTOM)
