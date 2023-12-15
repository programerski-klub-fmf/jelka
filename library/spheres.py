from library.patterns_lib import dist
from library.types import Position


class Sphere:
    def __init__(self, center: Position, radius: float) -> None:
        self.center = center
        self.radius = radius
        self.startpos = center
        self.endpos = center
        self.speed = 0

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

    def set_start(self,start : Position):
        self.start = start
    
    def set_end(self,end : Position):
        self.end = end
        
    # dist per frame
    def set_speed(self,speed : float):
        self.speed = speed
        
    def update_pos(self,frame : int):
        vec = (self.end[0] - self.start[0],self.end[1] - self.start[1],self.end[2] - self.start[2])
        self.center = (self.start[0] + vec[0]*self.speed*frame,self.start[1] + vec[1]*self.speed*frame,self.start[2] + vec[2]*self.speed*frame)