from library.jelka import Jelka, Color, Id, TimeMs
import math
import random as r
from library.patterns_lib import distance, normalize, vivid, random_color
from library.spheres import Sphere

# NAME: Rain

jelka = Jelka(file="data/lucke3d.csv")


sph = []

for i in range(0, 3):
    sph.append(Sphere((0.5, 0.5, 1.2), 0.2))
    sph[i].set_center((0.5 + r.uniform(-0.2, 0.2), 0.5 + r.uniform(-0.2, 0.2), 1 + r.uniform(0.0, 0.3)))
    sph[i].set_radius(0.1)
    sph[i].set_start(sph[i].get_center())
    sph[i].set_end((r.uniform(-1.0, 1.0), r.uniform(-1.0, 1.0), -0.5 + r.uniform(-2.0, 0.4)))
    # sph[i].set_end((0,0,0))
    sph[i].set_speed(0.01)


@jelka.run_shader_all
def update_colors(time: int, frame: int):
    colors = jelka.colors
    for i in range(len(sph)):
        sph[i].update_pos()

    for i in range(len(colors)):
        pos = jelka.get_position_normalized(i)
        colors[i] = (0, 255, 0)
        for j in range(len(sph)):
            if sph[j].isIn(pos):
                colors[i] = (0, 0, 255)
    return colors
