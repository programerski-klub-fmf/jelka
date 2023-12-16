import random as r
from library.jelka import Jelka, Color, Id, Position, Time
from typing import Any, Callable, cast
from library.patterns_lib import random_color, vivid

# NAME: Lines

jelka = Jelka(file="data/lucke3d.csv")


@jelka.run_shader_all
def update_colors(colors: list(Color), time: int, frame: int):
    if frame == 0:
        global col
        global spawnRate
        global lineLength
        col = vivid(random_color())
        spawnRate = 25
        lineLength = 10
        jelka.refresh_rate = 8

    if (frame % spawnRate) < lineLength:
        colors[0] = col
    else:
        colors[0] = (0, 0, 0)
        col = vivid(random_color())
    for i in reversed(range(1, len(colors))):
        colors[i] = colors[i - 1]
    return colors
