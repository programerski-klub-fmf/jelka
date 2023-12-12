import math

from library.jelka import Color, Jelka
from library.patterns_lib import random_color, vivid

jelka = Jelka(file="data/lucke3d.csv")

axis = 1
threshold = 0.1


@jelka.run_shader_all
def update_colors(colors: list[Color], time: int, frame: int):
    coord = math.sin(frame / 80) / 1.8 + 0.55

    global color
    global change

    if frame == 0:
        change = 0

    if (frame == 0 or coord < 0 or coord > 1.1) and change == 0:
        color = vivid(random_color())
        change = 1
    elif 0.01 < coord < 0.99:
        change = 0

    for i in range(0, len(colors)):
        pos = jelka.get_pos(i)
        if coord >= pos[axis] >= coord - threshold:
            colors[i] = color
        else:
            colors[i] = (0, 0, 0)

    return colors
