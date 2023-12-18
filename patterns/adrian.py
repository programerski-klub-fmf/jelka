from library.jelka import Jelka, Color, Id, TimeMs
import random as r
from library.patterns_lib import vivid, random_color
from library.spheres import Sphere
import math

# NAME: adrian

jelka = Jelka(file="data/lucke3d.csv")

@jelka.run_shader_all
def update_colors(time: int, frame: int):
    colors = jelka.colors
    
    for i in range(len(jelka.colors)):
        pos = jelka.get_position_normalized(i)
        colors[i]=(255,0,0)if (math.atan2(pos[1]-.5,pos[0]-.5)*255*0.3+time/10+pos[2]*200)%255 > 127 else (255,255,255)

    return colors
