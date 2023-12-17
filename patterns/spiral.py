from library.jelka import Jelka, Color, Id, Position, Time
import random as r
from library.patterns_lib import vivid, random_color
from library.spheres import Sphere

# NAME: Spiral

jelka = Jelka(file="data/lucke3d.csv")



@jelka.run_shader_all
def update_colors(colors: list(Color), time: int, frame: int):
    global bruh
    if frame == 0:
        bruh = [Sphere([0.5,0.5,0.5],1.0)]
        for i in range(len(colors)):
            colors[i] =[0,0,0]


    for i in range(len(colors)):
        pos = jelka.get_pos(i)
        for b in range(len(bruh)):
            if bruh[b].isIn(pos):
                if colors[i] == [0,0,0]:
                    colors[i] = vivid(random_color())
            else:
                colors[i] = [0,0,0]

    return colors

