from library.jelka import Jelka, Color, Id, Position, Time
import math
import random as r
from library.patterns_lib import dist, normalize, vivid, random_color

# NAME: Pulse

jelka = Jelka(file="data/lucke3d.csv")


@jelka.run_shader_all
def update_colors(colors: list(Color), time: int, frame: int):
    colors = list(colors)
    sphere_center = [0.5, 0.5, 0.5]
    rad2 = (math.e ** (math.sin(frame / 20))) / 3
    rad1 = (math.e ** (math.cos(frame / 20))) / 3

    global col
    if frame % 10 == 0:
        col = vivid(random_color())

    for i in range(0, len(colors)):
        pos = jelka.get_pos(i)
        diff = [sphere_center[0] - pos[0], sphere_center[1] - pos[1], sphere_center[2] - pos[2]]
        if dist(diff) <= rad1 and dist(diff) >= rad2:
            j = dist(diff) / rad1
            if colors[i] == [0, 0, 0]:
                colors[i] = (j * col[0], j * col[1], j * col[2])
            else:
                colors[i] = (j * colors[i][0], j * colors[i][1], j * colors[i][2])
        else:
            colors[i] = [0, 0, 0]

    return colors
