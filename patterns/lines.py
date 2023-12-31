from library.jelka import Jelka
from library.patterns_lib import random_color, vivid

# NAME: Lines

jelka = Jelka(file="data/lucke3d.csv")


@jelka.run_shader_all
def update_colors(time: int, frame: int):
    colors = jelka.colors
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
