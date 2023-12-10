# Development

## Installation
We use flit as our package management, so you can install the package for local development via:

`flit install -s`

after cloning the repo and creating a new virtual/conda environment.

## Flit
Since we use flit, you also have access to the following on `flit install`:
- black
- flake8
- pylint
- pytest

Flit is also used for publishing, with `flit publish`. CI/CD will be configured to do this in the future.

## Tests
We use pytest for our tests (located in `/tests`), which can be invoked with the `pytest` command.


## Simulation
We provide some helper scripts to interactively visualize EKF-SLAM, better understand behavior, and assist with development.

The various parameters used in simulation is configurable from `simulate.py` and can be ran from the project root using:

`python dev/simulate.py`

whereupon an interactive simulation will pop up as a matplotlib window. Clicking will create "waypoints" for the simulated bot to follow, and at the end of each waypoint the bot will perform an EKF-SLAM predict and update.