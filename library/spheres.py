from library.patterns_lib import dist
from library.types import Position


class Sphere:
    def __init__(self, center: Position, radius: float, startpos : Position =(0.5,0.5,0.5), endpos : Position =(0.5,0.5,0.5),speed : float = 0.1) -> None:
        self.center = center
        self.radius = radius
        self.startpospos = startpos
        self.endpos = endpos
        self.speed = speed

    def sphereDiff(self, pt: Position) -> Position:
        return (self.center[0] - pt[0], self.center[1] - pt[1], self.center[2] - pt[2])

    def isIn(self, pt: Position) -> bool:
        if dist(self.sphereDiff(pt)) <= self.radius:
            return True
        return False

    def set_center(self,center : Position) -> None:
        self.center = center

    def set_radius(self,radius : float) -> None:
        self.radius = radius

    def get_center(self) -> Position:
        return self.center

    def get_rad(self) -> float:
        return self.radius

    def set_start(self, start: Position) -> None:
        self.startpos = start

    def set_end(self, end: Position) -> None:
        self.endpos = end
        
    def get_start(self) -> Position:
        return self.startpos

    # dist per frame
    def set_speed(self, speed: float) -> None:
        self.speed = speed

    def update_pos(self) -> None:
        vec = (self.endpos[0] - self.startpos[0], self.endpos[1] - self.startpos[1], self.endpos[2] - self.startpos[2])
        self.center = (
            self.center[0] + vec[0] * self.speed,
            self.center[1] + vec[1] * self.speed,
            self.center[2] + vec[2] * self.speed,
        )
        if dist(self.sphereDiff(self.startpos)) > dist((self.startpos[0]-self.endpos[0],self.startpos[1]-self.endpos[1],self.startpos[2]-self.endpos[2])):
            self.center = self.startpos