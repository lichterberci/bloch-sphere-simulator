from typing import Any
import numpy as np
from state import State


class Gate:
    """
    A class to represent a quantum gate. It is represented by a unitary matrix.
    """

    def __init__(self, args):
        """
        Create a new gate.

        Args:
            args: The gate can be created in different ways:
                - With no arguments, the gate is the identity gate.
                - With a numpy array of size 2x2.
                - With a string representing the name of the gate: I, X, Y, Z, H.

        Raises:
            ValueError: If the arguments are invalid.

        """

        if args is None or len(args) == 0:
            self._matrix = np.eye(2)
        elif isinstance(args, np.ndarray):
            assert args.shape[0] == 2 and args.shape[1] == 2, "The matrix must be 2x2"
            # assert np.allclose(
            #     np.eye(2), args @ args.conj().T
            # ), "The matrix is not unitary"

            self._matrix = args
        elif isinstance(args, str):
            if args == "I":
                self._matrix = np.eye(2)
            elif args == "X":
                self._matrix = np.array([[0, 1], [1, 0]])
            elif args == "Y":
                self._matrix = np.array([[0, -1j], [1j, 0]])
            elif args == "Z":
                self._matrix = np.array([[1, 0], [0, -1]])
            elif args == "H":
                self._matrix = np.sqrt(0.5) * np.array([[1, 1], [1, -1]])
            elif args == "S":
                self._matrix = np.array([[1, 0], [0, 1j]])
            elif args == "T":
                self._matrix = np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]])
            elif args == "S^†":
                self._matrix = np.array([[1, 0], [0, -1j]])
            elif args == "T^†":
                self._matrix = np.array([[1, 0], [0, np.exp(-1j * np.pi / 4)]])
            else:
                raise ValueError("Invalid gate name.")
        else:
            raise ValueError("Invalid arguments.")

    def apply(self, state: State) -> State:
        """Apply the gate to a state. The state is a column vector of size 2, where the first element is the amplitude of |0> and the second element is the amplitude of |1>.

        Args:
            state (np.ndarray): The state to apply the gate to.

        Returns:
            np.ndarray: The new state after applying the gate.
        """
        return State(self._matrix @ state.state)

    def set_matrix(self, matrix: np.ndarray):
        """
        Set the matrix that represents the gate.
        """

        self._matrix = matrix

    def __mul__(self, state: State) -> State:
        """Apply the gate to a state using the * operator.

        Args:
            state (State): The state to apply the gate to.

        Returns:
            State: The new state after applying the gate.
        """

        assert isinstance(state, State), "The state must be a State object."

        return self.apply(state)

    def __matmul__(self, state: State) -> State:
        """Apply the gate to a state using the @ operator.

        Args:
            state (State): The state to apply the gate to.

        Returns:
            State: The new state after applying the gate.
        """

        assert isinstance(state, State), "The state must be a State object."

        return self.apply(state)

    def __call__(self, *args: State) -> State:
        """Apply the gate to a state using the () operator.

        Returns:
            State: The new state after applying the gate.
        """

        assert len(args) == 1, "The gate must be applied to a single state."
        assert isinstance(args[0], State), "The state must be a State object."

        return self.apply(args[0])

    @property
    def U(self):
        """
        Return the matrix that represents the gate.

        Returns:
            np.ndarray: The matrix that represents the gate.
        """
        return self._matrix

    @property
    def rotation_axis(self):
        """Return the axis of rotation of the gate in the Bloch sphere.

        Returns:
            np.ndarray: The axis of rotation.
        """

        _, eigenvectors = np.linalg.eig(self._matrix)

        a = eigenvectors[:, 0][0]
        b = eigenvectors[:, 0][1]
        c = eigenvectors[:, 1][0]
        d = eigenvectors[:, 1][1]

        off_diagonal = c * np.conj(d) - a * np.conj(b)

        x = np.real(off_diagonal)
        y = -1 * np.imag(off_diagonal)
        z = np.abs(c) ** 2 - np.abs(a) ** 2

        return np.array([x, y, z])

    @property
    def rotation_angle(self) -> float:
        """
        Return the angle of rotation of the gate in the Bloch sphere.

        Raises:
            ValueError: If the matrix does not have two eigenvalues.

        Returns:
            float: The angle of rotation.
        """

        eigenvalues, _ = np.linalg.eig(self._matrix)

        if eigenvalues is None or len(eigenvalues) != 2:
            raise ValueError("The matrix must have two eigenvalues!")

        return float(np.angle(eigenvalues[0]) - np.angle(eigenvalues[1]))

    def calculate_trajectory(self, state_from: State, n_points: int):
        """Calculates the trajectory of a gate applied to a state in the Bloch sphere.

        Args:
            gate (Gate): The gate to apply.
            state_from (np.ndarray): The starting state.
            n_points (int): The number of points to calculate.

        Returns:
            np.ndarray: The points in the Bloch sphere. Each column is a point in Cartesian coordinates.
        """

        t = np.linspace(0, self.rotation_angle, n_points)

        points = list(
            map(
                lambda p: p.bloch_coordinates,
                [
                    Gate.from_rotation(self.rotation_axis, _t).apply(state_from)
                    for _t in t
                ],
            )
        )

        return np.array(points).T

    @staticmethod
    def from_rotation(axis: np.ndarray, angle: float):
        """Create a gate that represents a rotation around an axis.

        Args:
            axis (np.ndarray): The axis of rotation.
            angle (float): The angle of rotation.

        Raises:
            AssertionError: If the axis does not have three components.

        Returns:
            Gate: The gate that represents the rotation.
        """

        assert len(axis) == 3, "The axis must have three components."

        # normalize the axis
        normalized_axis = axis / np.linalg.norm(axis)

        x, y, z = normalized_axis

        sigma = np.array(
            [
                np.array([[0, 1], [1, 0]]),
                np.array([[0, -1j], [1j, 0]]),
                np.array([[1, 0], [0, -1]]),
            ]
        )

        return Gate(
            np.cos(angle / 2) * np.eye(2)
            - 1j * np.sin(angle / 2) * (x * sigma[0] + y * sigma[1] + z * sigma[2])
        )

    def __repr__(self) -> str:
        if np.allclose(self.U, np.eye(2), atol=1e-4):
            return "I"
        if np.allclose(self.U, np.array([[0, 1], [1, 0]]), atol=1e-4):
            return "X"
        if np.allclose(self.U, np.array([[0, -1j], [1j, 0]]), atol=1e-4):
            return "Y"
        if np.allclose(self.U, np.array([[1, 0], [0, -1]]), atol=1e-4):
            return "Z"
        if np.allclose(self.U, np.sqrt(0.5) * np.array([[1, 1], [1, -1]]), atol=1e-4):
            return "H"
        if np.allclose(self.U, np.array([[1, 0], [0, 1j]]), atol=1e-4):
            return "S"
        if np.allclose(
            self.U, np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]]), atol=1e-4
        ):
            return "T"
        if np.allclose(self.U, np.array([[1, 0], [0, -1j]]), atol=1e-4):
            return "S^†"
        if np.allclose(
            self.U, np.array([[1, 0], [0, np.exp(-1j * np.pi / 4)]]), atol=1e-4
        ):
            return "T^†"
        return f"U({self.U})"
