from library.jelka import Jelka, Color, Id, Position, Time
import math
from typing import Any, Callable, cast
import time
import random as r

jelka = Jelka(file="data/random_tree.csv")

frame = 0
running = True
colors = [(0,0,0) for i in range(jelka.count)]
lineLength = 10
spawnRate = 25
last_time = time.time()
jelka.refresh_rate = 8
col = (r.randint(0,255),r.randint(0,255),r.randint(0,255)) 
while running:
    if any(color is None for color in colors):
        running = False
        break  
    if (frame%spawnRate) < lineLength: colors[0] = col
    else: 
        colors[0] = (0,0,0)
        col = (r.randint(0,255),r.randint(0,255),r.randint(0,255)) 
    
    for i in reversed(range(1,len(colors))):
        colors[i] = colors[i-1]
    jelka.set_colors(cast(list[Color], colors))
    tmp_last_time = time.time()
    time.sleep(max(1 / jelka.refresh_rate - (time.time() - last_time), 0.01))
    last_time = tmp_last_time
    frame += 1