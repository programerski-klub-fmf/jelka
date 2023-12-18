import math

from library.jelka import Jelka
from library.patterns_lib import distance, normalize, vivid
from library.spheres import Sphere

# NAME: Sphere

jelka = Jelka(file="data/lucke3d.csv")


@jelka.run_shader_all
def update_colors(time: int, frame: int):
    colors = jelka.colors
    sph = Sphere((0.5, 0.5, 0.5), math.fabs(math.sin(frame / 50)) * 0.7 + 0.1)
    sphere_col = (255, 255, 255)

    positions = {}
    intensity = []

    for i in range(0, len(colors)):
        pos = list(jelka.get_position_normalized(i))
        if not sph.isIn(pos):
            intensity.append(0)
            positions[i] = sph.get_center()
        else:
            intensity.append(distance(sph.sphereDiff(pos)) / sph.get_rad())
            positions[i] = pos
            # positions.append([pos[0] - diff[0], pos[1] - diff[1], pos[2] - diff[2]])

    positions = normalize(positions)
    # print(positions)
    for i in range(0, len(colors)):
        colors[i] = [
            int(sphere_col[0] * positions[i][0] * intensity[i]),
            int(sphere_col[1] * positions[i][1] * intensity[i]),
            int(sphere_col[2] * positions[i][2] * intensity[i]),
        ]
        colors[i] = vivid(colors[i])

    return colors
