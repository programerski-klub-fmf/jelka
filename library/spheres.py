from library.patterns_lib import dist

class Sphere:
    def __init__(self, center, radius) -> None:
        self.center = center
        self.radius = radius
    
    def sphereDiff(self,pt):
        return [self.center[0] - pt[0],self.center[1]-pt[1],self.center[2]-pt[2]]
    
    def isIn(self, pt):
        return dist(self.sphereDiff(pt)) <= self.radius
    
    def get_center(self):
        return self.center
    
    def get_rad(self):
        return self.radius