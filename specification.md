# My Bloch Sphere Simulator

My aim is to create a library that can be independently used in other projects,  alongside a simple Bloch-sphere simulator as a standalone python application.
This project is open-source and available on [github](
https://github.com/lichterberci/bloch-sphere-simulator).

## Specification

### Main features

- the user can apply...
  - predefined gates
    - eg.: $H$, $X$, $S^{\dagger}$
    - custom gates, defined by a unitary matrix
- the user can set the state directly by defining the amplitudes (they are normalized automatically)
- the user can save the current visualization as a .png
- the visualization includes...
  - the Bloch sphere
  - the state vector
  - the current operation's parameters (path, axis, from and to states)
- the user can easily read...
  - the current state
  - the current operation's matrix

### Third-party libraries

- numpy - for linear algebra operations
- matplotlib - for visualization
- tkinter - as the base for the GUI
- customtkinter - for nicer widgets (better looking UI)

### Main implementation details

#### Backend

##### States

The state is a column vector of size 2, where the first element is the amplitude of $|0\rangle$ and the second element is the amplitude of $|1\rangle$.

##### Gates

Every gate is a wrapper for a unitary matrix. The user can apply predefined gates or custom gates defined by a matrix.
Applying a gate to a state is a simple matrix multiplication. Determining the axis and angle of rotation is done by finding the eigenvectors and eigenvalues of the gate's matrix.

#### Frontend

##### Visualizing the Bloch sphere

The Bloch sphere is visualized by a 3D plot in matplotlib. I chose this library due to familiarity, but one has to realize that drawing a Bloch-sphere only involves drawing spheres, parts of circles, arrows and axis (lines or arrows). The states (before and after the operation) and the axis of operation are quivers, and the path by a curve. The animation is also handled by matplotlib with the in-between states calculated by linear interpolation of the angle around the given axis.
