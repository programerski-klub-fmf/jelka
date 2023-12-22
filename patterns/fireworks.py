import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["GOTO_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"

import math
import random
import numpy as np

from library.jelka import Jelka
from library.patterns_lib import random_color, vivid
from library.spheres import Sphere

# NAME: Fireworks
# play around with these parameters
firework_count = 3  # number of fireworks visible at the same time
lifetime = 42 # number of frames that a single firework is visible for
expand_speed = 5 # not linear increase in speed
disapper_speed = 1.1 # how fast the center disappears (is a linear multiplier)
radius = 0.4 # size of fireworks in range [0, 1]

spawn_offset = lifetime // firework_count # frames between two spawns of fireworks
fireworks = [(0, 0)] * firework_count
firework_colors = [(0, 0, 0)] * firework_count

jelka = Jelka(file="data/lucke3d.csv")

# scale up all values so that at least one of the components is 255
def brighten_color(color):
    x = 255 / max(color)
    color = tuple(map(lambda x, s : int(x * s), color, (x, x, x)))
    return color

@jelka.run_shader_all
def update_colors(time: int, frame: int):
    colors = jelka.colors

    global fireworks
    global firework_colors
    
    rad_func = lambda z : 1 / 2 - z / 2
    # pass a tuple of height and angle around vertical,
    # it will calculate the firework position on the surface of the tree
    firework_pos = lambda za : (0.5 + rad_func(za[0]) * math.cos(za[1] * 20), 
                                 0.5 + rad_func(za[0]) * math.sin(za[1] * 20), 
                                 za[0])
    firework_rad_func = lambda t : 1 / (1 + math.exp(-t * expand_speed)) * radius
    firework_small_rad_func = lambda t : t * radius * disapper_speed

    looped_frames = [0] * firework_count
    for i in range(firework_count):
        looped_frames[i] = (frame + i * spawn_offset) % lifetime + 1  # +1 to skip size 0
        if looped_frames[i] == 1:
            fireworks[i] = (np.random.normal(loc=0.42, scale=0.3), random.uniform(-1, 1))
            firework_colors[i] = brighten_color(vivid(random_color()))
    
    # spheres expand with time
    spheres = [Sphere(firework_pos(fireworks[i]), firework_rad_func(looped_frames[i] / lifetime)) for i in range(firework_count)]
    # smaller sphere for a disappearing center
    spheres_small = [Sphere(firework_pos(fireworks[i]), firework_small_rad_func(looped_frames[i] / lifetime)) for i in range(firework_count)]

    for i in range(len(colors)):
        pos = jelka.get_position_normalized(i)

        sumed_count = 0
        color_sum = (0, 0, 0)
        for j in range(firework_count):
            if spheres[j].isIn(pos) and not spheres_small[j].isIn(pos):
                color_sum = tuple(map(lambda x, y : x + y, color_sum, firework_colors[j]))
                sumed_count += 1

        if sumed_count > 0:
            # average together colors from fireworks that intersect
            color_sum = (int(color_sum[0] / sumed_count), 
                         int(color_sum[1] / sumed_count), 
                         int(color_sum[2] / sumed_count))
        colors[i] = color_sum

    return colors
