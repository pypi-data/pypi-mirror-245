from typing import List, Tuple

class Environment:
    """
    Environment classes are used to define the environment

    All obstacles are defined in terms of lines to make collision detection safer and easier
    """
    WIDTH = 100
    HEIGHT = 100

    WALLS = []
    STATIC_OBSTACLES = []
    DYNAMIC_OBSTACLES = []


"""
Obstacles in the environment, composed of 4-tuples of (x1, y1, x2, y2) denoting lines in the environment
"""


class Rectangle:
    """
    Class for rectangle obstacles that do not move
    """

    def __init__(self, x1: int, y1: int, x2: int, y2: int) -> None:
        self.walls = [
            (x1, y1, x1, y2),
            (x1, y2, x2, y2),
            (x2, y2, x2, y1),
            (x2, y1, x1, y1),
        ]

    def landmarks(self) -> List[Tuple[int, int]]:
        landmarks = []
        # since walls are closed, we can just use 1 vertex per wall
        for wall in self.walls:
            landmarks.append((wall[0], wall[1]))
        return landmarks

    def state(self) -> List[Tuple[int, int, int, int]]:
        return self.walls


class DynamicRectangle(Rectangle):
    """
    Class for rectangles that move in a path defined by dx dy waypoints

    (for future development)
    """

    def __init__(self, x1: int, y1: int, x2: int, y2: int, waypoints: list) -> None:
        # Format of waypoints: [(dx1, dy1, t1), (dx2, dy2, t2), ...] where t is the time it takes to
        # reach the next waypoint. Waypoints are in cycle, i.e. the last waypoint is connected to
        # the first waypoint
        super().__init__(x1, y1, x2, y2)
        self.waypoints = waypoints

    def tick(self) -> None:
        pass

    def state(self) -> List[Tuple[int, int, int, int]]:
        pass


"""
ENVIRONMENT 1: Room

Simple environment with a single square room
"""


class RoomEnvironment(Environment):
    STATIC_OBSTACLES = [
        Rectangle(25, 25, 75, 75),
    ]


"""
ENVIRONMENT 2: Static obstacles

Simple environment with static rectangle obstacles
"""


class StaticObstaclesEnvironment(Environment):
    STATIC_OBSTACLES = [
        Rectangle(20, 20, 80, 30),
        Rectangle(30, 30, 45, 45),
        Rectangle(70, 25, 80, 35),
        Rectangle(30, 70, 50, 100),
        Rectangle(70, 70, 80, 100),
    ]


"""
ENVIRONMENT 3: Dynamic obstacles (not implemented)

Simple environment with dynamic obstacles
"""


class DynamicObstaclesEnvironment(Environment):
    pass
