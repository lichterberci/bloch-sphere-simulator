Module bloch_simulator.gate
===========================

Classes
-------

`Gate(args)`
:   A class to represent a quantum gate. It is represented by a unitary matrix.
    
    Create a new gate.
    
    Args:
        args: The gate can be created in different ways:
            - With no arguments, the gate is the identity gate.
            - With a numpy array of size 2x2.
            - With a string representing the name of the gate: I, X, Y, Z, H.
    
    Raises:
        ValueError: If the arguments are invalid.

    ### Static methods

    `from_rotation(axis: numpy.ndarray, angle: float)`
    :   Create a gate that represents a rotation around an axis.
        
        Args:
            axis (np.ndarray): The axis of rotation.
            angle (float): The angle of rotation.
        
        Raises:
            AssertionError: If the axis does not have three components.
        
        Returns:
            Gate: The gate that represents the rotation.

    ### Instance variables

    `U`
    :   Return the matrix that represents the gate.
        
        Returns:
            np.ndarray: The matrix that represents the gate.

    `rotation_angle: float`
    :   Return the angle of rotation of the gate in the Bloch sphere.
        
        Raises:
            ValueError: If the matrix does not have two eigenvalues.
        
        Returns:
            float: The angle of rotation.

    `rotation_axis`
    :   Return the axis of rotation of the gate in the Bloch sphere.
        
        Returns:
            np.ndarray: The axis of rotation.

    ### Methods

    `apply(self, state: bloch_simulator.state.State) ‑> bloch_simulator.state.State`
    :   Apply the gate to a state. The state is a column vector of size 2, where the first element is the amplitude of |0> and the second element is the amplitude of |1>.
        
        Args:
            state (np.ndarray): The state to apply the gate to.
        
        Returns:
            np.ndarray: The new state after applying the gate.

    `calculate_trajectory(self, state_from: bloch_simulator.state.State, n_points: int)`
    :   Calculates the trajectory of a gate applied to a state in the Bloch sphere.
        
        Args:
            gate (Gate): The gate to apply.
            state_from (np.ndarray): The starting state.
            n_points (int): The number of points to calculate.
        
        Returns:
            np.ndarray: The points in the Bloch sphere. Each column is a point in Cartesian coordinates.

    `set_matrix(self, matrix: numpy.ndarray)`
    :   Set the matrix that represents the gate.