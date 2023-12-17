from library.jelka import Jelka, Color, Id, TimeMs
import math
import random as r
from library.patterns_lib import distance, normalize, vivid, random_color

# NAME: Pulse

jelka = Jelka(file="data/lucke3d.csv")

col = vivid(random_color())


@jelka.run_shader_all
def update_colors(time: int, frame: int):
    global col
    colors = jelka.colors
    sphere_center = [0.5, 0.5, 0.5]
    rad2 = (math.e ** (math.sin(frame / 20))) / 3
    rad1 = (math.e ** (math.cos(frame / 20))) / 3

    if frame % 10 == 0:
        col = vivid(random_color())

    for i in range(0, len(colors)):
        pos = jelka.get_position_normalized(i)
        diff = [sphere_center[0] - pos[0], sphere_center[1] - pos[1], sphere_center[2] - pos[2]]
        if distance(diff) <= rad1 and distance(diff) >= rad2:
            j = distance(diff) / rad1
            if colors[i] == (0, 0, 0):
                colors[i] = (j * col[0], j * col[1], j * col[2])
            else:
                colors[i] = (j * colors[i][0], j * colors[i][1], j * colors[i][2])
        else:
            colors[i] = (0, 0, 0)

    return colors
