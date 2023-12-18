from library.jelka import Jelka, Color, Id, TimeMs
import random as r
from library.patterns_lib import vivid, random_color
from library.spheres import Sphere
import math

# NAME: Barbers

jelka = Jelka(file="data/lucke3d.csv")

@jelka.run_shader_all
def update_colors(time: int, frame: int):
    colors = jelka.colors

    cols = [(255,0,0),(0,0,255),(255,255,255)]
    height = [1 - 0.005 *(frame%210),1 - 0.005 *((frame+70)%210),1 - 0.005 *((frame+140)%210)]

    rad =  [ (1-height[0])/2,(1-height[1])/2,(1-height[2])/2]
    x = [0.5 + rad[0]*math.cos(height[0]*20),0.5 + rad[1]*math.cos(height[1]*20),0.5 + rad[2]*math.cos(height[2]*20)]
    y = [0.5 + rad[0]*math.sin(height[0]*20),0.5 + rad[1]*math.sin(height[1]*20),0.5 + rad[2]*math.sin(height[2]*20)]

    sph = [Sphere((x[0],y[0],height[0]),0.2),Sphere((x[1],y[1],height[1]),0.2),Sphere((x[2],y[2],height[2]),0.2)]

    for i in range(len(colors)):
        pos = jelka.get_position_normalized(i)
        for j in range(0,3):
            if sph[j].isIn(pos) :
                colors[i] = cols[j]

    return colors
