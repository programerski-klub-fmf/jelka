import random as r
from library.jelka import Jelka, Color, Id, Position, Time
from typing import Any, Callable, cast

jelka = Jelka(file="data/random_tree.csv")

 
@jelka.run_shader_all
def update_colors(colors : list(Color),time: int, frame: int):
    if frame == 0:
        global col
        global spawnRate
        global lineLength
        col = Color((r.randint(0,255),r.randint(0,255),r.randint(0,255)))
        spawnRate=25
        lineLength=10
        jelka.refresh_rate = 8

    if (frame%spawnRate) < lineLength:
        colors[0] = col
    else:
        colors[0] = (0,0,0)
        col = Color((r.randint(0,255),r.randint(0,255),r.randint(0,255)))
    for i in reversed(range(1,len(colors))):
        colors[i] = colors[i-1]
    return colors
