from library.jelka import Jelka, Color, Id, Position, Time
import random as r
from library.patterns_lib import vivid, random_color

# NAME: Random

jelka = Jelka(file="data/lucke3d.csv")


@jelka.run_shader_all
def update_colors(colors: list(Color), time: int, frame: int):
    if frame % 20 == 0:
        for i in range(0, len(colors)):
            colors[i] = vivid(random_color())
    return colors
