# DCS Pylote

DCS Pylote is a Python application designed to bridge DCS World simulation data with a virtual joystick controller. By acting as a bridge between the DCS-BIOS data stream and the vJoy virtual device driver, it enables flight simulation enthusiasts to create highly customized input setups.

## Features

- **DCS-BIOS to vJoy Integration**: Translates real-time data from DCS World into control inputs for a virtual joystick.
- **Flexible Mapping**: Configure how DCS-BIOS data points map to vJoy axes, buttons, or POVs.
- **Low-Latency Performance**: Implements a responsive, non-blocking loop for real-time updates.
- **Custom Control Logic**: Supports advanced setups like combining multiple inputs into a single axis or modifying inputs based on aircraft state.

## Use Cases

- Map aircraft trim positions to dedicated vJoy axes for precise control.
- Combine separate inputs (e.g., left and right rudder pedals) into a single virtual axis.
- Use external scripts or peripherals to directly control vJoy inputs.
- Modify joystick inputs dynamically based on the aircraft's state in the simulation.

## Technical Overview

### Core Functionality

- **Bridge DCS-BIOS Output to Virtual Input**: Reads specific data outputs from the cockpit of a DCS World aircraft and translates them into control inputs for a virtual joystick.
- **Example Use Case**: Map the aircraft's throttle position to a vJoy axis, allowing external hardware or scripts to stay in sync with the aircraft's internal state.

### Implementation Goals

1. **Utilize Existing Python Libraries**: Leverage libraries like `dcs-bios-connector` and `pyvjoy` for low-level communication.
2. **Flexible Mapping/Logic Layer**: Develop a configurable layer to define how DCS-BIOS data points map to vJoy inputs.
3. **Responsive Loop**: Implement a non-blocking main loop to ensure low-latency performance.

## Installation

_coming soon..._

## Contributing

_coming soon..._

## Acknowledgements

_coming soon..._
