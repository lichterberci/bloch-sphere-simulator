import sys
import os.path

# for being able to import from src
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)

from bloch_simulator.gate import Gate
from bloch_simulator.state import State

gate = Gate("X")
state = State("|0>")
