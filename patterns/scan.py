import random as r
from library.jelka import Jelka, Color, Id, Position, Time
from typing import Any, Callable, cast
import math
from library.patterns_lib import vivid, random_color

jelka = Jelka(file="data/lucke3d.csv")


@jelka.run_shader_all
def update_colors(colors: list(Color), time: int, frame: int):
    zup = math.sin(frame / 80)/2 + 0.5
    threshold = 0.1
    
    global col
    global change
    if frame == 0: change = 0
    if (frame == 0 or zup < 0.01 or zup > 0.99) and change == 0:
        change = 1
        col = vivid(random_color())
    elif zup > 0.01 and zup < 0.99: change = 0

    for i in range(0, len(colors)):
        pos = jelka.get_pos(i)
        if pos[2] <= zup and pos[2] >= zup - threshold:
            colors[i] = col
        else:
            colors[i] = (0, 0, 0)

    return colors
