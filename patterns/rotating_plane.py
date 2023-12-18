import math
import random
from colorsys import hsv_to_rgb, rgb_to_hsv

from library.jelka import Jelka
from library.patterns_lib import random_color, vivid

# NAME: Rotating Plane

jelka = Jelka(file="data/lucke3d.csv")


@jelka.run_shader_all
def update_colors(time: int, frame: int):
    colors = jelka.colors
    center = (0.5, 0.5, 0.5)
    normal = (math.sin(frame / 40), 0, math.cos(frame / 40))
    d = normal[0] * center[0] + normal[1] * center[1] + normal[2] * center[2]
    threshold = 0.1

    global c1, c2
    if frame % 150 == 0:
        c1 = vivid(random_color())
        c1hsv = rgb_to_hsv(*[comp / 255.0 for comp in c1])
        c2hsv = ((c1hsv[0] * 360 + random.randint(80, 280) % 360) / 360.0, c1hsv[1], c1hsv[2])
        c2 = vivid(tuple(comp * 255 for comp in hsv_to_rgb(*c2hsv)))

    for i in range(len(colors)):
        pos = jelka.get_position_normalized(i)
        dcrtica = pos[0] * normal[0] + pos[1] * normal[1] + pos[2] * normal[2]
        if d - threshold <= dcrtica <= d + threshold:
            colors[i] = c1
        else:
            colors[i] = c2

    return colors
