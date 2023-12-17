from position_calculator import Smreka, distance
import numpy as np
from itertools import product
import math

print("Reading data...")
data = []
with open("data/points2.csv") as f:
    for line in f.readlines():
        lucka, x, z, pogled = map(int, line.split(","))
        data.append((lucka, x, z, pogled))

# x = 0 je na levem robu slike
center_x = 880
# koordinatni sistem je obrnjen,
lowest_z = max(data, key=lambda x: x[2])[2]
height_on_image = abs(min(data, key=lambda x: x[2])[2] - lowest_z)
height = 200
scale = height / height_on_image
max_r2 = 0
pos2d = {}
for lucka, x, z, pogled in data:
    x -= center_x
    z = lowest_z - z
    if lucka not in pos2d:
        pos2d[lucka] = {}
    # if pogled == 2 and 0 in pos2d[lucka]: continue
    pos2d[lucka][pogled] = (x * scale, z * scale)
    max_r2 = max(max_r2, x**2 + z**2)

print("Calculating lucke...")
positions3d = {}
for lucka in sorted(pos2d.keys()):
    z = np.average(np.array([pos2d[lucka][pogled][1] for pogled in pos2d[lucka]]))
    x = 0
    if 0 in pos2d[lucka] and 2 in pos2d[lucka]:
        x = (pos2d[lucka][0][0] - pos2d[lucka][2][0]) / 2
    elif 0 in pos2d[lucka]:
        x = pos2d[lucka][0][0]
    elif 2 in pos2d[lucka]:
        x -= pos2d[lucka][2][0]

    y = 0
    if 1 in pos2d[lucka] and 3 in pos2d[lucka]:
        y = (pos2d[lucka][1][0] - pos2d[lucka][3][0]) / 2
    elif 1 in pos2d[lucka]:
        y = pos2d[lucka][1][0]
    elif 3 in pos2d[lucka]:
        y -= pos2d[lucka][3][0]

    positions3d[lucka] = (x, y, z)

with open("data/lucke3d.csv", "w") as f:
    for lucka in sorted(positions3d.keys()):
        f.write(f"{lucka},{positions3d[lucka][0]},{positions3d[lucka][1]},{positions3d[lucka][2]}\n")
