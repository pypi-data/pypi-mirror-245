import matplotlib.pyplot as plt
from sensor import Sensor
from map import Map
import ekf_slam
import numpy as np
from typing import Dict, List


class Agent:
    """
    Agent class that represents the robot in the simulation.

    The agent is responsible for maintaining its own state and updating it based on user input.

    Note that this is meant for simulation purposes and is not abstracted like a real robot would be,
    since it tracks both the true and perceived state of the robot.
    """
    SPEED = 15  # ticks per waypoint

    TRUE_COLOR = "lightblue"
    PERCEIVED_COLOR = "dodgerblue"

    def __init__(self, config: Dict, ax: plt.Axes, map: Map) -> None:
        self.ax = ax
        self.map = map
        self.config = config

        # true robot state
        self.x = config["environment"].WIDTH / 2
        self.y = config["environment"].HEIGHT / 2

        # perceived robot state
        self.perceived_x = self.x
        self.perceived_y = self.y
        self.corrective_angle = 0

        # waypoints
        self.pathx = [self.x]
        self.pathy = [self.y]

        # waypoint-based traversal
        self.cur_interval_time = 0
        self.next_waypoint_idx = 1

        # plotting
        self.true_circle = plt.Circle((self.x, self.y), 2, color=self.TRUE_COLOR)
        self.perceived_circle = plt.Circle((self.x, self.y), 2, color=self.PERCEIVED_COLOR)

        # sensor
        self.sensor: Sensor = config["sensor"](self.x, self.y, ax, map, config)
        self.landmarks = []

        # EKF-SLAM
        self.ekf_slam = ekf_slam.KnownCorrespondence(
            init=[self.x, self.y, 0],
            Qt=config["ekf_slam_sensor_noise"],
            Rt=config["ekf_slam_movement_noise"],
            num_landmarks=len(self.map.all_landmarks()),  # assume no landmarks are added after initialization
        )

    def move(self, x, y) -> None:
        """Moves the agent to the specified location

        :param x: the x coordinate of the new location
        :param y: the y coordinate of the new location
        """
        self.x = x
        self.y = y

        self.sensor.move(x, y)

    def tick(self) -> None:
        """Executes one tick of the simulation, updating the state of the agent (and all its children)
        by moving it to the next waypoint"""
        if self.next_waypoint_idx < len(self.pathx):
            # calculate the corrective distance and angle once per waypoint
            # can't compute this before the movement to the waypoint starts because it
            # depends on where the robot is at the start of the movement after noisy movement
            if self.cur_interval_time == 0:
                cur_x = self.perceived_x
                cur_y = self.perceived_y
                next_x = self.pathx[self.next_waypoint_idx]
                next_y = self.pathy[self.next_waypoint_idx]

                self.corrective_angle = (np.arctan2(next_y - cur_y, next_x - cur_x) + 2 * np.pi) % (2 * np.pi)
                self.corrective_dist = np.sqrt((next_x - cur_x) ** 2 + (next_y - cur_y) ** 2)

            self.cur_interval_time += 1

            if self.cur_interval_time >= self.SPEED:
                self.cur_interval_time = 0
                self.next_waypoint_idx += 1

                # perform correction step
                self.ekf_slam.predict(np.array([self.corrective_dist, self.corrective_angle]))

                # update based on observations
                sensor_state = np.array(self.sensor.state())
                self.ekf_slam.update(sensor_state)
                self.landmarks = self.ekf_slam.mean[3:]

                self.perceived_x = self.ekf_slam.mean[0]
                self.perceived_y = self.ekf_slam.mean[1]

        if self.next_waypoint_idx < len(self.pathx):
            next_waypt_x = self.pathx[self.next_waypoint_idx]
            next_waypt_y = self.pathy[self.next_waypoint_idx]

            cur_waypt_x = self.perceived_x
            cur_waypt_y = self.perceived_y

            # slow bot down as it approaches waypoint
            dx = (next_waypt_x - cur_waypt_x) * self.cur_interval_time / self.SPEED
            dy = (next_waypt_y - cur_waypt_y) * self.cur_interval_time / self.SPEED

            self.perceived_x += dx
            self.perceived_y += dy

            # add noise to true movement, scaled to distance moved
            dist_moved = np.sqrt(dx**2 + dy**2)
            motion_noise = dist_moved * np.matmul(np.random.randn(1, 3), self.config["true_movement_noise"])[0]

            self.move(self.x + dx + motion_noise[0], self.y + dy + motion_noise[1])

        self.sensor.tick()

    def click(self, x, y) -> None:
        """Adds a waypoint at the clicked location for the robot to move to

        :param x: the x coordinate of the click
        :param y: the y coordinate of the click
        """
        self.pathx.append(x)
        self.pathy.append(y)

    def plot(self) -> None:
        """Plot the current state of the agent"""
        self.true_circle.set_center((self.x, self.y))
        self.ax.add_patch(self.true_circle)

        self.perceived_circle.set_center((self.perceived_x, self.perceived_y))
        self.ax.add_patch(self.perceived_circle)

        self.ax.plot(self.pathx, self.pathy, color=self.TRUE_COLOR, linestyle="dashed", linewidth=1)

        for i in range(len(self.landmarks) // 2):
            self.ax.plot(self.landmarks[2 * i], self.landmarks[2 * i + 1], marker="o", color="red", alpha=0.15)

        self.sensor.plot()
