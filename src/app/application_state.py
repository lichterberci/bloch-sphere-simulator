from collections import deque
import sys
import os.path
import numpy as np

# for being able to import from src
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)

from bloch_simulator.gate import Gate
from bloch_simulator.state import State

previous_inputs = {
    "unitary_matrix": [""] * 4,
    "state": [""] * 2,
}

gate = Gate("X")
state = State("|0>")

MAX_HISTORY_LENGTH = 4

def update_state(new_state: State | np.ndarray, update_history: bool = False):
    
    if update_history:
        history.append({
            # copy the current state
            "gate": Gate(gate),
            "state": State(state)
        })
    
    if isinstance(new_state, State):
        state.set_state(new_state.state)
    else:
        state.set_state(new_state)
        
def update_gate(new_gate: Gate | str, update_history: bool = False):
    
    if update_history :
        history.append({
            # copy the current state
            "gate": Gate(gate),
            "state": State(state)
        })
    
    if isinstance(new_gate, Gate):
        gate.set_matrix(new_gate.U)
    else:
        gate.set_matrix(new_gate)

def reset_last_app_state():
    if len(history) > 0:
        previous_state = history.pop()
        
        update_gate(Gate(previous_state["gate"]))
        update_state(State(previous_state["state"]))    

history = deque(maxlen=MAX_HISTORY_LENGTH)
