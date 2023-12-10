import matplotlib.pyplot as plt
from typing import Dict, List, Tuple

class Map:
    """Map class that manages all objects in the simulation"""

    def __init__(self, config: Dict, ax: plt.Axes) -> None:
        self.environment = config["environment"]
        self.ax = ax

        self.static_walls = []
        self.static_landmarks = []
        self.dynamic_walls = []
        self.dynamic_landmarks = []

        # initialize obstacles
        for obstacle in self.environment.STATIC_OBSTACLES:
            self.static_walls.extend(obstacle.state())
            self.static_landmarks.extend(obstacle.landmarks())

        for obstacle in self.environment.DYNAMIC_OBSTACLES:
            self.dynamic_walls.extend(obstacle.state())
            self.dynamic_landmarks.extend(obstacle.landmarks())

    def all_walls(self) -> List[Tuple[int, int, int, int]]:
        """Returns the current locations of all walls in the environment

        :return: List of 4-tuples of (x1, y1, x2, y2) denoting walls from (x1, y1) to (x2, y2) in the environment
        """
        return self.static_walls + self.dynamic_walls

    def all_landmarks(self) -> List[Tuple[int, int]]:
        """Returns the current locations of all landmarks in the environment

        :return: List of 2-tuples of (x, y) denoting the locations of all landmarks in the environment
        """
        return self.static_landmarks + self.dynamic_landmarks

    def tick(self) -> None:
        """Executes one tick of the simulation, updating the state of all dynamic children"""
        new_dynamic_walls = []
        new_dynamic_landmarks = []
        for obstacle in self.environment.DYNAMIC_OBSTACLES:
            obstacle.tick()
            new_dynamic_walls.extend(obstacle.state())
            self.dynamic_landmarks.extend(obstacle.landmarks())
        self.dynamic_walls = new_dynamic_walls
        self.dynamic_landmarks = new_dynamic_landmarks

    def click(self, x, y) -> None:
        """Handles a click event on the map by the user

        (Does nothing by default)

        :param x: the x coordinate of the click
        :param y: the y coordinate of the click
        """
        pass

    def plot(self) -> None:
        """Plots the current state of the map, currently just the walls"""
        for wall in self.all_walls():
            self.ax.plot([wall[0], wall[2]], [wall[1], wall[3]], color="black")
