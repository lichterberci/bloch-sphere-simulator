from tkinter import *
from customtkinter import *
from application_state import gate, state, update_gate, update_state, reset_last_app_state, history, previous_inputs
import numpy as np
from math import *
import re

import sys
import os.path

# for being able to import from src
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)

from bloch_simulator.gate import Gate
from bloch_simulator.state import State

PRIMARY_BTN_BG_COLOR = "#007090"
SECONDARY_BTN_BG_COLOR = "#0050c0"

def _sanitize_complex_number_str(val: str) -> str:
    val = val.replace("i", "j")
    val = re.sub(r"(?<!\d)j", "1j", val)
    val = val.replace(" ", "")
    return val

def _sanitize_complex_output(val: complex) -> str:
    real = val.real
    imag = val.imag
    
    if np.isclose(real, 0, atol=1e-5) and np.isclose(imag, 0, atol=1e-5):
        return "0"
    
    def _is_int(val: float) -> bool:
       return np.isclose(val, np.rint(val), atol=1e-4)
    
    def _sanitize_number(val: float) -> str:
        if _is_int(val):
            return str(int(np.rint(val)))
        # elif _is_int(val * np.sqrt(2)):
        #     n = int(np.rint((val * np.sqrt(2))))
        #     if n == 1:
        #         return "sqrt(2)"
        #     elif n == -1:
        #         return "-sqrt(2)"
        #     else:
        #         return f"{n}*sqrt(2)"
        else:
            return f"{val:.5f}"
    
    real_str = _sanitize_number(real) if real != 0 else ""
    imag_str = ((_sanitize_number(imag) + "i") if abs(imag) != 1 else ("i" if imag == 1 else "-i")) if imag != 0 else ""
    
    imag_str = imag_str.replace(")i", ")*1i")
    
    if real_str == "":
        return imag_str
    elif imag_str == "":
        return real_str
    else:
        if imag_str[0] == "-":
            return f"{real_str} - {imag_str[1:]}"
        else:
            return f"{real_str} + {imag_str}"
    
    
def _convert_to_complex(val: str) -> complex:
    try:
        val = " " + val + " "
        sanitized_val = _sanitize_complex_number_str(val)
        evaluated_result = eval(sanitized_val, {}, {"sqrt": np.sqrt, "sin": np.sin, "cos": np.cos, "tan": np.tan, "np": np})
        if isinstance(evaluated_result, complex):
            return evaluated_result
        elif isinstance(evaluated_result, (int, float)):
            return complex(evaluated_result)
        elif isinstance(evaluated_result, np.ndarray):
            return complex(evaluated_result[0])
        elif isinstance(evaluated_result, (list, tuple)):
            return complex(evaluated_result[0])
        else:
            return None
    except Exception as e:
        print(e)
        return None

def render_settings_bar_frame(root, rerender_bloch_frame):
    settings_bar = CTkFrame(master=root)
    settings_bar.pack(side=RIGHT, fill="both", expand=True)

    matrix_form = CTkFrame(master=settings_bar)
    matrix_form.pack(side=TOP, fill="both", expand=True)
    matrix_form.grid_rowconfigure(tuple(range(7)), weight=1)
    matrix_form.grid_columnconfigure(tuple(range(2)), weight=1)

    matrix_label = CTkLabel(master=matrix_form, text="Unitary matrix:")
    matrix_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="news")

    matrix_entries = [
        CTkEntry(
            master=matrix_form,
            width=120,
        )
        for _ in range(4)
    ]

    for i, entry in enumerate(matrix_entries):
        entry.bind(
            "<Return>",
            lambda _: save_and_rerender(),
        )
        # entry.bind("<FocusOut>", lambda _: save_and_rerender)
        entry.insert(0, _sanitize_complex_output(gate.U[i % 2, i // 2]))
        entry.grid(row=i // 2 + 1, column=i % 2, padx=5, pady=5, sticky="news")

    predefined_matrices = [
        Gate("X").U,
        Gate("Y").U,
        Gate("Z").U,
        Gate("H").U,
        Gate("S").U,
        Gate("T").U,
        Gate("S^†").U,
        Gate("T^†").U,
    ]

    def set_matrix(matrix):
        # gate.set_matrix(matrix)
        update_gate(matrix)
        
        for i, entry in enumerate(matrix_entries):
            entry.delete(0, END)
            entry.insert(0, _sanitize_complex_output(matrix[i % 2, i // 2]))

        save_and_rerender()

    predefined_matrix_btns = [
        CTkButton(
            master=matrix_form,
            text=f"{Gate(matrix)}",
            command=lambda matrix=matrix: set_matrix(matrix),
            fg_color=SECONDARY_BTN_BG_COLOR,
        )
        for matrix in predefined_matrices
    ]

    for i, btn in enumerate(predefined_matrix_btns):
        btn.grid(row=3 + i // 2, column=i % 2, padx=5, pady=5, sticky="news")

    def apply_gate():
        # state.set_state(gate * state)
        update_state(gate(state), update_history=True)

        for i, entry in enumerate(state_entries):
            entry.delete(0, END)
            entry.insert(0, _sanitize_complex_output(state[i]))
            entry.grid(row=i // 2 + 1, column=i % 2, padx=5, pady=5, sticky="news")

        rerender_bloch_frame()
        
    def undo():
        global history
        if len(history) == 0:
            return

        reset_last_app_state()
        
        for i, entry in enumerate(matrix_entries):
            entry.delete(0, END)
            entry.insert(0, _sanitize_complex_output(gate.U[i % 2, i // 2]))
            entry.grid(row=i // 2 + 1, column=i % 2, padx=5, pady=5, sticky="news")
        
        for i, entry in enumerate(state_entries):
            entry.delete(0, END)
            entry.insert(0, _sanitize_complex_output(state[i]))
            entry.grid(row=i // 2 + 1, column=i % 2, padx=5, pady=5, sticky="news")
        
        rerender_bloch_frame()
        
    matrix_btn_panel = CTkFrame(master=settings_bar)
    matrix_btn_panel.pack(side=TOP, fill="x")
    matrix_btn_panel.grid_rowconfigure(0, weight=1)
    matrix_btn_panel.grid_columnconfigure(tuple(range(2)), weight=1)

    button_apply = CTkButton(
        master=matrix_btn_panel,
        text="APPLY GATE",
        command=apply_gate,
        width=190,
        height=50,
        fg_color=PRIMARY_BTN_BG_COLOR,
    )
    button_apply.grid(row=0, column=0, padx=5, pady=5, sticky="news")
    
    button_undo = CTkButton(
        master=matrix_btn_panel,
        text="UNDO",
        command=undo,
        width=190,
        height=50,
        fg_color=PRIMARY_BTN_BG_COLOR
    )
    button_undo.grid(row=0, column=1, padx=5, pady=5, sticky="news")

    state_form = CTkFrame(master=settings_bar)
    state_form.pack(side=TOP, fill="both", expand=True)
    state_form.grid_rowconfigure(tuple(range(5)), weight=1)
    state_form.grid_columnconfigure(tuple(range(2)), weight=1)

    state_label = CTkLabel(master=state_form, text="State:")
    state_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="news")

    state_entries = [
        CTkEntry(
            master=state_form,
            width=120,
        )
        for _ in range(2)
    ]

    def save_and_rerender():

        if previous_inputs["unitary_matrix"] == list(map(lambda entry: entry.get(), matrix_entries)) and previous_inputs["state"] == list(map(lambda entry: entry.get(), state_entries)):
            for entry in matrix_entries:
                entry.configure(require_redraw=True, text_color="white")
            return
        
        matrix_entry_values = list(map(lambda entry: entry.get(), matrix_entries))
        matrix_entry_filled_values = list(
            map(
                lambda val: (
                    _convert_to_complex(val[0]) if val[0] is not None and val[0] != "" else val[1]
                ),
                zip(matrix_entry_values, gate.U.flatten()),
            )
        )

        new_matrix = np.array(matrix_entry_filled_values).reshape(2, 2)

        # check if the matrix is unitary
        if None in matrix_entry_filled_values or not np.allclose(np.eye(2), new_matrix @ new_matrix.conj().T, rtol=1e-4):
            for i, entry in enumerate(matrix_entries):
                entry.configure(require_redraw=True, text_color="red")
            return
        else:
            for entry in matrix_entries:
                entry.configure(require_redraw=True, text_color="white")

        # gate.set_matrix(new_matrix)
        update_gate(new_matrix)

        state_entry_values = list(map(lambda entry: entry.get(), state_entries))
        state_entry_filled_values = list(
            map(
                lambda val: (
                    _convert_to_complex(val[0]) if val[0] is not None and val[0] != "" else val[1]
                ),
                zip(state_entry_values, state.state),
            )
        )
        
        if None in state_entry_filled_values:
            for i, entry in enumerate(state_entries):
                entry.configure(require_redraw=True, text_color="red")               
            return
        else:
            for entry in state_entries:
                entry.configure(require_redraw=True, text_color="white")       

        new_state = np.array(state_entry_filled_values)
        
        # check if the state is normalized
        if not np.allclose(1, np.linalg.norm(new_state), rtol=1e-4):
            new_state /= np.linalg.norm(new_state)

            for i, entry in enumerate(state_entries):
                entry.delete(0, END)
                entry.insert(0, _sanitize_complex_output(new_state[i]))
                entry.configure(require_redraw=True, text_color="lightblue")
        else:
            for entry in state_entries:
                entry.configure(require_redraw=True, text_color="white")          

        # state.set_state(new_state)
        update_state(new_state)

        previous_inputs["unitary_matrix"] = list(map(lambda entry: entry.get(), matrix_entries))
        previous_inputs["state"] = list(map(lambda entry: entry.get(), state_entries))

        for entry in matrix_entries:
            entry.configure(require_redraw=True, text_color="white")
        # for entry in state_entries:
        #     entry.configure(require_redraw=True, text_color="white")

        rerender_bloch_frame()

    for i, entry in enumerate(state_entries):
        entry.bind(
            "<Return>",
            lambda _: save_and_rerender(),
        )
        # entry.bind(
        #     "<FocusOut>",
        #     lambda _: save_and_rerender(),
        # )
        entry.insert(0, _sanitize_complex_output(state[i]))
        entry.grid(row=i // 2 + 1, column=i % 2, padx=5, pady=5, sticky="news")

    predefined_states = [
        State(np.array([1, 0])),
        State(np.array([0, 1])),
        State(np.array([1 / np.sqrt(2), 1 / np.sqrt(2)])),
        State(np.array([1 / np.sqrt(2), -1 / np.sqrt(2)])),
    ]

    def set_state(state):
        # state.set_state(state.state)
        update_state(State(state.state))

        for i, entry in enumerate(state_entries):
            entry.delete(0, END)
            entry.insert(0, _sanitize_complex_output(state[i]))

        save_and_rerender()

    predefined_state_btns = [
        CTkButton(
            master=state_form,
            text=f"{_state}",
            command=lambda s=_state: set_state(s),
            fg_color=SECONDARY_BTN_BG_COLOR,
        )
        for _state in predefined_states
    ]

    for i, btn in enumerate(predefined_state_btns):
        btn.grid(row=3 + i % 2, column=i // 2, padx=5, pady=5, sticky="news")

    button_rerender = CTkButton(
        master=settings_bar,
        text="RERENDER",
        command=rerender_bloch_frame,
        width=200,
        height=50,
        fg_color=PRIMARY_BTN_BG_COLOR
    )
    button_rerender.pack(side=BOTTOM, pady=5)
