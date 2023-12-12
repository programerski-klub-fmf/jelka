from library.patterns_lib import dist
from library.types import Position


class Sphere:
    def __init__(self, center: Position, radius: float) -> None:
        self.center = center
        self.radius = radius

    def sphereDiff(self, pt: Position) -> Position:
        return (self.center[0] - pt[0], self.center[1] - pt[1], self.center[2] - pt[2])

    def isIn(self, pt: Position) -> bool:
        if dist(self.sphereDiff(pt)) <= self.radius:
            return True
        return False

    def get_center(self) -> Position:
        return self.center

    def get_rad(self) -> float:
        return self.radius
