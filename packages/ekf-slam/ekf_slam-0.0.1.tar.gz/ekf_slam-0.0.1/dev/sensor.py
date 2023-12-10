import numpy as np
from typing import Tuple, Optional, Dict, List
import matplotlib.pyplot as plt
from map import Map

def line_intersection(line1: Tuple[Tuple[int, int], Tuple[int, int]], line2: Tuple[Tuple[int, int], Tuple[int, int]]) -> Optional[Tuple]:
    """Snippet from https://gist.github.com/kylemcdonald/6132fc1c29fd3767691442ba4bc84018

    Returns the intersection point of two line segments

    :param line1: the first line segment, a 2-tuple of 2-tuples of (x, y) coordinates
    :param line2: the second line segment, a 2-tuple of 2-tuples of (x, y) coordinates
    :return: the intersection point if the lines intersect, otherwise None
    """
    x1, y1 = line1[0]
    x2, y2 = line1[1]
    x3, y3 = line2[0]
    x4, y4 = line2[1]
    denom = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
    if denom == 0:  # parallel
        return None
    ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / denom
    if ua < 0 or ua > 1:  # out of range
        return None
    ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / denom
    if ub < 0 or ub > 1:  # out of range
        return None
    x = x1 + ua * (x2 - x1)
    y = y1 + ua * (y2 - y1)
    return (x, y)


class Sensor:
    """Base class for the sensor API"""
    def sense(self):
        pass

    def move(self, x, y):
        pass

    def tick(self):
        pass

    def plot(self):
        pass


class PanoramaSensor(Sensor):
    """Senses everything in a 360 degree radius around the robot, and returns the visible landmarks and their
    distances and angles relative to the sensor"""

    EPSILON = 1e-6

    def __init__(self, x: int, y: int, ax: plt.Axes, map: Map, config: Dict) -> None:
        """Initializes a panorama sensor

        :param x: starting x value of the sensor
        :param y: starting y value of the sensor
        :param ax: matplotlib axes to plot the sensor visualization on
        :param map: map object to sense
        :param config: configuration dictionary for the simulation
        """
        self.x = x
        self.y = y
        self.ax = ax
        self.map = map
        self.prev_state = None
        self.updated = True

        noise = config["true_sensor_noise"]
        self.range_noise = noise[0][0]
        self.bearing_noise = noise[1][1]

    def state(self) -> List:
        """Returns the state of the sensor, a list of 3-tuples of (distance, angle, landmark)"""

        if not self.updated:
            return self.prev_state
        all_landmarks = self.map.all_landmarks()
        all_walls = self.map.all_walls()

        sensed_landmarks = []

        for i in range(len(all_landmarks)):
            landmark = all_landmarks[i]
            dx = landmark[0] - self.x
            dy = landmark[1] - self.y

            # offset the landmark by a small amount to avoid self-intersection
            landmark_x = self.x + dx * (1 - self.EPSILON)
            landmark_y = self.y + dy * (1 - self.EPSILON)

            intersected = False
            for wall in all_walls:
                intersection = line_intersection(
                    [(self.x, self.y), (landmark_x, landmark_y)], [(wall[0], wall[1]), (wall[2], wall[3])]
                )
                if intersection is not None:
                    intersected = True
                    break

            if not intersected:
                dist = np.linalg.norm(np.array(landmark) - np.array((self.x, self.y)))
                angle = np.arctan2(landmark[1] - self.y, landmark[0] - self.x)

                # add noise
                dist += self.range_noise * np.random.randn(1).item()
                angle += (self.bearing_noise * np.random.randn(1).item() + 2 * np.pi) % (2 * np.pi)

                sensed_landmarks.append([dist, angle, i])

        self.prev_state = sensed_landmarks
        self.updated = False
        return sensed_landmarks

    def move(self, x: int, y: int) -> None:
        """Move the (true) sensor to a new location

        :param x: the x value to move the sensor to
        :param y: the y value to move the sensor to
        """
        self.x = x
        self.y = y
        self.updated = True
        self.state()

    def tick(self) -> None:
        """This method is called to update the internal state of the sensor.

        Currently, it does nothing since the sensor behavior between ticks is the same, but it can be overridden
        in subclasses to provide custom behavior.
        """
        return

    def plot(self) -> None:
        """Plots the noisy measurement of the sensor on the map"""
        if self.prev_state is None:
            self.state()
        for landmark in self.prev_state:
            landmark_x = landmark[0] * np.cos(landmark[1]) + self.x
            landmark_y = landmark[0] * np.sin(landmark[1]) + self.y
            self.ax.plot([self.x, landmark_x], [self.y, landmark_y], color="grey", linewidth=0.5)
            self.ax.plot([landmark_x], [landmark_y], marker="o", markersize=3, color="red")
