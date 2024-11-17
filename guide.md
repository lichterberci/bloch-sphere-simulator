# User manual

## Table of contents

- [User manual](#user-manual)
  - [Table of contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Overview](#overview)
    - [Applying operations](#applying-operations)
      - [Applying known gates](#applying-known-gates)
      - [Applying custom gates](#applying-custom-gates)
    - [Setting the state](#setting-the-state)
    - [Evaluation of the text boxes](#evaluation-of-the-text-boxes)
    - [History and undo](#history-and-undo)

## Installation 

To install the software, follow these steps:

  - download the software from [github](https://github.com/lichterberci/bloch-sphere-simulator). Use the Releases tab to download the latest version.
  - open a terminal and navigate to the folder where you downloaded the software
  - run the following command: `pip install DOWNLOADED.gz` where `DOWNLOADED.gz` is the name of the downloaded file
  - navigate to `/src/app/` and run the following command: `python app_main.py`
  - you should now see the app open up!

## Usage

### Overview

On the left side of the screen, you will see the Bloch sphere. You can rotate the sphere by clicking and dragging. The sphere will rotate around the axis that is perpendicular to the screen. The current state of the qubit is represented by a point on the sphere (red arrow).
The state after the current operation is represented by a yellow arrow. The axis around which the rotation is performed is shown as blue dashed arrow. The transition between the two states is shown as an animated line that fades from red to yellow. The history is shown as fading dashed orange lines.

On the right side of the screen, you will see the controls. You can apply various operations to the qubit. You can also reset the qubit to a specific state.

### Applying operations

#### Applying known gates

To apply a known gate, click on the corresponding button. The gate's matrix will be loaded up and will be ready to use. After selecting the desired gate, click on the "APPLY" button to apply the gate to the current state.

#### Applying custom gates

To apply a custom gate, simply modify the unitary matrix of the gate in the text box. The matrix should be a valid unitary matrix. After entering the matrix, click on the "APPLY" button to apply the gate to the current state. If the matrix is not valid, the matrix's text will be colored red.

### Setting the state

To set the state, click on the corresponding button. The state will be set to the desired state. You can also enter the amplitudes directly in the text boxes. If the input is not a valid number, the text box will be colored red. If the input is a number for each component but the resulting vector is not normalized, the application will normalize the vector and highlight the state-vector's text in light blue to notify the user of the modification. 

### Evaluation of the text boxes

The text in the text boxes (for the matrix and the state vector) is evaluated upon hitting enter. The program tries to evaluate it using python's `eval` function. All `i`s are replaced with `j`s and the following locals are set for easier use:

  - `np` - numpy (default import)
  - `sqrt` - numpy.sqrt
  - `sin` - numpy.sin
  - `cos` - numpy.cos
  - `tan` - numpy.tan

If the program cannot evaluate the text, the text box will be colored red.

### History and undo

All operations along with their corresponding states are saved in the history. You can undo the last operation by clicking on the "UNDO" button. The history is saved in a stack, so you can undo multiple operations. The history is only updated upon hitting the "APPLY" button. The history stack is maximum 4 elements long. This is due to the fact that the history is shown on the Bloch sphere and the screen would get cluttered if the history was too long. 

The history is shown as dashed orange lines. The older a line is, the more faded it is.
