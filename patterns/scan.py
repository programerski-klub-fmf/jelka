import random as r
from library.jelka import Jelka, Color, Id, Position, Time
from typing import Any, Callable, cast
import math

jelka = Jelka(file="data/random_tree.csv")

def vivid(c : Color):
    c=list(c)
    m = min(c[0],c[1],c[2])
    if c[0] == m: return (0,c[1],c[2])
    if c[1] == m: return (c[0],0,c[2])
    return (c[0],c[1],0)


@jelka.run_shader_all
def update_colors(colors : list(Color),time: int, frame: int):
    zup = math.fabs(math.sin(frame/80))
    threshold = 0.12
    global col
    if frame == 0:
        col = [r.randint(0,255),r.randint(0,255),r.randint(0,255)]
        col = vivid(col)

    for i in range(0,len(colors)):
        pos = jelka.get_pos(i)
        if pos[2] <= zup and pos[2] >= zup - threshold:
            colors[i] = col
        else: colors[i] = (0,0,0)

    return colors
