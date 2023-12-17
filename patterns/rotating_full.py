from library.jelka import Jelka, Color, Id, Position, Time
import math
import random as r
from library.patterns_lib import dist, normalize, vivid, random_color

jelka = Jelka(file="data/lucke3d.csv")


@jelka.run_shader_all
def update_colors(colors: list(Color), time: int, frame: int):
    center = (0.5,0.5,0.5)
    normal = (math.sin(frame/40),0,math.cos(frame/40))
    d = normal[0] * center[0] + normal[1] * center[1] + normal[2] *center[2]
    threshold = 10

    global c1,c2
    if frame%150 == 0:
        c1 = vivid(random_color())
        c2 = vivid(random_color())

    for i in range(len(colors)):
        pos = jelka.get_pos(i)
        dcrtica = pos[0]*normal[0] + pos[1] * normal[1] + pos[2]*normal[2]
        if dcrtica >= d-threshold and dcrtica <= d:
            colors[i] = c1
        else:
            colors[i] = c2

    return colors