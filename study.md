# Bloch sphere simulator

*Made by: Bertalan Lichter, 13. 10. 2024.*  

## The goal of this project

This is my work for a university assignment and aims to create a simple Bloch-sphere simulator as a standalone python application.

## An overview of a few Bloch-sphere simulators

### [Konstantin Herb's Bloch-sphere simulator](https://bloch.kherb.io/)

This is the work of a student at ETH Zürich, called Konstantin Herb. It is freely available online and has a very nice user interface with a clean, interactive visualization of what you are doing. The project is open-source with the source-code being available on [github](https://github.com/kherb27/Blochy).

### Main features

- the user can apply...
  - any rotation, defined by angles around the $x$, $y$ and $z$ axis
  - any rotation around a custom axis
  - popular quantum gates
    - $X$
    - $Y$
    - $Z$
    - $H$
    - $S$
    - $S^{\dagger}$
    - $T$
    - $T^{\dagger}$
  - pulses
- the user can rotate the sphere around freely and always see the axis, the current state and the history (represented by curves on the surface of the sphere)

### Upsides

- very clean, intuitive interface
- open-source
- the ability to do any operation

### Drawbacks

- the user cannot directly set a state without resetting the page
- the user cannot see the axis around which we rotate at each step

## [Bits and electronics' Bloch sphere simulator](https://bits-and-electrons.github.io/bloch-sphere-simulator/)

This is yet another open-source project with a farily intuitive UI. The interface and the visualization is a bit less refined than the first project, we looked at, but nothing to be ashamed of.

This site presents us with a bit more information about the current state (such as the polar coordinates $\theta$ and $phi$, the Cartesian coordinates and the probability amplitudes $\alpha$ and $\beta$).

### Main features

- the user can apply...
    - half-turn, quarter-turn and eighth-turn gates
      - eg.: $H$, $P_X$, $P_X^{1/2}$, $P_X^{1/4}$
    - custom gates that can be defined either by
      - a matrix
      - a rotation around a custom axis
    - lambda gates, defined by two angles:
      - $\theta$ - polar angle
      - $\phi$ - azimuthal angle
- URL-based state sharing

### Upsides

- open-source
- the ability to do any operation
- the user can easily read the current state in multiple ways
- the user can share the current state via neat URLs

### Drawbacks

- the user cannot directly set a state without resetting the page
- the visualization is a bit less refined

## [Attila Kun's Bloch-sphere simulator](https://attilakun.net/bloch/)

This is a pet project of Attila Kun, a full-stack developer and BME alumnus. The project is open-source and available on [github](https://github.com/attila-kun/bloch). 

Although the UI is very simple with a very old style, the Bloch-sphere (to be more precise, only the axis, the state and the current operation's parameters) is very well put together. The user can see the axis around which we rotate at each step, as well as the path the state has taken. One very nice feature is the ability to directly set the state by entering the amplitudes or by dragging the state around.

### Main features

- the user can apply...
  - any rotation, defined by a unitary matrix
  - popular quantum gates
    - $X$
    - $Y$
    - $Z$
    - $H$
- the user can set the state directly by...
  - $\ket{0}$, $\ket{1}$, $\ket{+}$ and $\ket{-}$ buttons 
  - dragging the state vector around
  - entering the amplitudes directly
- save the current visualization as a .png

### Upsides

- open-source
- the user can...
  - see much more information about the current operation
  - directly set the state
  - save the current visualization as a .png
  - apply any operation via a unitary matrix

### Drawbacks

- the UI is very simple and old-fashioned
- the user cannot use many predefined operations
- it is limited in the ways the user can define a rotation