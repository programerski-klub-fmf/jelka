import math

from library.jelka import Jelka
from library.patterns_lib import random_color, vivid
from library.spheres import Sphere

# NAME: Spiral

jelka = Jelka(file="data/lucke3d.csv")


@jelka.run_shader_all
def update_colors(time: int, frame: int):
    colors = jelka.colors
    global col

    height = 1 - 0.005 * (frame % 220)
    if height == 1:
        col = vivid(random_color())
    rad = 1 / 2 - height / 2
    x = 0.5 + rad * math.cos(height * 20)
    y = 0.5 + rad * math.sin(height * 20)

    sph = Sphere((x, y, height), 0.1)

    for i in range(len(colors)):
        pos = jelka.get_position_normalized(i)
        if sph.isIn(pos):
            colors[i] = col
        else:
            colors[i] = (0, 0, 0)

    return colors
