from library.jelka import Jelka, Color, Id, Position, Time
import math
import random as r
from library.patterns_lib import dist, normalize, vivid, random_color
from library.spheres import Sphere

jelka = Jelka(file="data/lucke3d.csv")

sph = Sphere((0.5, 0.5, 1), 0.2)
sph.set_start(sph.center)
sph.set_end((0.2, 0., 0))
sph.set_speed(0.01)


@jelka.run_shader_all
def update_colors(colors: list[Color], time: int, frame: int):
    sph.update_pos(frame)

    for i in range(len(colors)):
        pos = jelka.get_pos(i)
        if sph.isIn(pos):
            colors[i] = (0, 0, 255)
        else:
            colors[i] = (0,255, 0)
    return colors
