Module bloch_simulator.state
============================

Classes
-------

`State(*args)`
:   Class to represent a quantum state. It is represented by a column vector.

Create a new state.

Args:
    *args: The state can be given in different ways:
        - With no arguments, the state is |0>.
        - With a numpy array of size 2.
        - With two numbers, the state is a column vector with those numbers as amplitudes.
        - With a string representing the name of the state: 0, 1, +, - (or |0>, |1>, |+>, |->).

Raises:
    ValueError: If the arguments are invalid.

### Instance variables

`alpha: complex`
:   Return the amplitude of |0>.
    
    Returns:
        complex: The amplitude of |0>.

`beta: complex`
:   Return the amplitude of |1>.
    
    Returns:
        complex: The amplitude of |1>.

`bloch_coordinates: numpy.ndarray[float]`
:   Return the Bloch coordinates of the state in Cartesian coordinates.
    
    Returns:
        np.ndarray[float]: The Bloch coordinates of the state in Cartesian coordinates.

`phi: float`
:   Return the phase of the state in the Bloch sphere.
    
    Returns:
        float: The phase of the state.

`state: numpy.ndarray[complex]`
:   Return the state.
    
    Returns:
        np.ndarray: The state.

`theta: float`
:   Return the angle of the state in the Bloch sphere.
    
    Returns:
        float: The angle of the state.

### Methods

    `set_state(self, new_state: Union[numpy.ndarray, Self])`
    :   Set the state.
        
        Args:
            new_state (np.ndarray): The new state.
