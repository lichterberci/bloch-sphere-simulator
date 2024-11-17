from typing import Self
import numpy as np


class State:
    """
    Class to represent a quantum state. It is represented by a column vector.
    """

    def __init__(self, *args):
        """
        Create a new state.

        Args:
            *args: The state can be given in different ways:
                - With no arguments, the state is |0>.
                - With a numpy array of size 2.
                - With another state.
                - With two numbers, the state is a column vector with those numbers as amplitudes.
                - With a string representing the name of the state: 0, 1, +, - (or |0>, |1>, |+>, |->).

        Raises:
            ValueError: If the arguments are invalid.
        """
        if isinstance(args[0], State):
            self._state = args[0].state.copy()
        elif args is None or len(args) == 0:
            self._state = np.array([1, 0])
        elif isinstance(args[0], np.ndarray):
            assert args[0].shape[0] == 2, "The state must be a column vector of size 2."
            self._state = args[0]
        elif len(args) == 2 and all(isinstance(x, (int, float, complex)) for x in args):
            assert (
                args == 0 or args == 1
            ), "The state must be a column vector of size 2."
            self._state = np.array([0, 1]) if args == 1 else np.array([1, 0])
        elif isinstance(args[0], str):
            match args[0]:
                case "0" | "|0>":
                    self._state = np.array([1, 0])
                case "1" | "|1>":
                    self._state = np.array([0, 1])
                case "+" | "|+>":
                    self._state = np.array([1 / np.sqrt(2), 1 / np.sqrt(2)])
                case "-" | "|->":
                    self._state = np.array([1 / np.sqrt(2), -1 / np.sqrt(2)])
                case _:
                    raise ValueError("Invalid state name.")
        else:
            raise ValueError("Invalid arguments.")

    @property
    def alpha(self) -> complex:
        """Return the amplitude of |0>.

        Returns:
            complex: The amplitude of |0>.
        """
        return self._state[0]

    @property
    def beta(self) -> complex:
        """
        Return the amplitude of |1>.

        Returns:
            complex: The amplitude of |1>.

        """
        return self._state[1]

    @property
    def state(self) -> np.ndarray[complex]:
        """
        Return the state.

        Returns:
            np.ndarray: The state.
        """
        return self._state

    @property
    def theta(self) -> float:
        """
        Return the angle of the state in the Bloch sphere.

        Returns:
            float: The angle of the state.
        """

        return 2 * np.arccos(np.abs(self.alpha))

    @property
    def phi(self) -> float:
        """
        Return the phase of the state in the Bloch sphere.

        Returns:
            float: The phase of the state.
        """
        return np.angle(self.beta) - np.angle(self.alpha)

    def set_state(self, new_state: np.ndarray | Self):
        """
        Set the state.

        Args:
            new_state (np.ndarray): The new state.
        """
        if isinstance(new_state, State):
            self._state = new_state.state
        else:
            assert (
                new_state.shape[0] == 2
            ), "The state must be a column vector of size 2."
            self._state = new_state

    @property
    def bloch_coordinates(self) -> np.ndarray[float]:
        """
        Return the Bloch coordinates of the state in Cartesian coordinates.

        Returns:
            np.ndarray[float]: The Bloch coordinates of the state in Cartesian coordinates.
        """
        return np.array(
            [
                2 * np.real(self[1] * np.conj(self[0])),
                2 * np.imag(self[1] * np.conj(self[0])),
                np.abs(self[0]) ** 2 - np.abs(self[1]) ** 2,
            ]
        )

    def __getitem__(self, index: int) -> complex:
        """
        Return the amplitude of the state.

        Args:
            index (int): The index of the amplitude to return.

        Raises:
            AssertionError: If the index is not 0 or 1.

        Returns:
            complex: The amplitude of the state.
        """
        assert index in [0, 1], "The index must be 0 or 1."

        return self._state[index]

    def __str__(self):
        if np.allclose(self._state, np.array([1, 0]), atol=1e-4):
            return "|0>"
        elif np.allclose(self._state, np.array([0, 1]), atol=1e-4):
            return "|1>"
        elif np.allclose(
            self._state, np.array([1 / np.sqrt(2), 1 / np.sqrt(2)]), atol=1e-4
        ):
            return "|+>"
        elif np.allclose(
            self._state, np.array([1 / np.sqrt(2), -1 / np.sqrt(2)]), atol=1e-4
        ):
            return "|->"

        return f"{self.alpha:.2f} |0> + {self.beta:.2f} |1>"

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, State):
            return False

        return np.allclose(self._state, value.state)

    def __hash__(self) -> int:
        return hash(tuple(self._state))

    def __repr__(self):
        return self.__str__()
