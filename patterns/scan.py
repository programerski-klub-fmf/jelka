import random as r
from library.jelka import Jelka, Color, Id, Position, Time
from typing import Any, Callable, cast
import math

jelka = Jelka(file="data/random_tree.csv")


@jelka.run_shader_all
def update_colors(colors : list(Color),time: int, frame: int):
    zup = math.fabs(math.sin(frame/80))
    threshold = 0.12
    col = [69,210,210]

    for i in range(0,len(colors)):
        pos = jelka.get_pos(i)
        if pos[2] <= zup and pos[2] >= zup - threshold:
            colors[i] = col
        else: colors[i] = (0,0,0)
    
    return colors
