from library.jelka import Jelka, Color, Id, Position, Time
import math
import random as r
from library.patterns_lib import dist, normalize
from library.spheres import Sphere

jelka = Jelka(file="data/lucke3d.csv")


@jelka.run_shader_all
def update_colors(colors: list(Color), time: int, frame: int):
    colors = list(colors)
    sph = Sphere([0.5,0.5,0.5],math.fabs(math.sin(frame / 50)) * 0.7 + 0.1)
    sphere_col = (255, 255, 255)

    positions = []
    intensity = []

    for i in range(0, len(colors)):
        pos = list(jelka.get_pos(i))
        if not sph.isIn(pos):
            intensity.append(0)
            positions.append(sph.get_center())
        else:
            intensity.append(dist(sph.sphereDiff(pos)) / sph.get_rad())
            positions.append(pos)
            #positions.append([pos[0] - diff[0], pos[1] - diff[1], pos[2] - diff[2]])

    positions = normalize(positions,sph.get_center())
    for i in range(0, len(colors)):
        colors[i] = [
            sphere_col[0] * positions[i][0] * intensity[i],
            sphere_col[1] * positions[i][1] * intensity[i],
            sphere_col[2] * positions[i][2] * intensity[i],
        ]

    return colors
