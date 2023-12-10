from environment import Environment, StaticObstaclesEnvironment
from sensor import Sensor, PanoramaSensor
from plot import interactive_simulation
import numpy as np

"""
Configuration file for running the simulation of EKF-SLAM with known correspondence

To run the simulation, run this file with python3 from the workspace root directory:
python3 dev/simulate.py

To change the configuration, change the variables below. More information about each variable
can be found in the corresponding file.
"""

"""
Environment configuration (environment.py)

Sets the environment that the robot will be in. The environment determines the size of the map,
the obstacles, and the landmarks.
"""
ENVIRONMENT = StaticObstaclesEnvironment

"""
Movement configuration

Sets the noise model for the robot's movement. The noise model is a 3x3 matrix that represents
the covariance of the movement vector. The noise model is used to generate random movement vectors
for the robot in the simulation.

True movement noise is the noise model used to generate the true movement of the robot, and
EKF-SLAM movement noise is the noise model that the EKF-SLAM algorithm uses to estimate the
robot's movement.
"""
TRUE_MOVEMENT_NOISE = 0.05 * np.array([[1, 1, 0], [1, 1, 0], [0, 0, 0]])
EKF_SLAM_MOVEMENT_NOISE = TRUE_MOVEMENT_NOISE

"""
Sensor configuration (sensor.py)

Sets the sensor that the robot will use to sense the environment. The sensor determines how the
robot perceives the environment. The sensor can be changed to test different sensor models.

True sensor noise is the noise model used to generate the true sensor readings, and EKF-SLAM
sensor noise is the noise model that the EKF-SLAM algorithm uses to estimate the robot's sensor
readings.

Currently, the sensor noise model is a 2x2 matrix where
[0][0] = distance noise (units)
[1][1] = angle noise (radians)
"""
SENSOR = PanoramaSensor
TRUE_SENSOR_NOISE = np.array([[0.1, 0], [0, 0.05]])
EKF_SLAM_SENSOR_NOISE = TRUE_SENSOR_NOISE


# Do not change anything below this line unless you know what you are doing
assert issubclass(ENVIRONMENT, Environment)
assert issubclass(SENSOR, Sensor)
config = {
    "environment": ENVIRONMENT,
    "true_movement_noise": TRUE_MOVEMENT_NOISE,
    "ekf_slam_movement_noise": EKF_SLAM_MOVEMENT_NOISE,
    "sensor": SENSOR,
    "true_sensor_noise": TRUE_SENSOR_NOISE,
    "ekf_slam_sensor_noise": EKF_SLAM_SENSOR_NOISE,
}

interactive_simulation(config)
