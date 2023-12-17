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
width, height = 200, 200
scale = height / height_on_image
smreka = Smreka(0, 200, 0, height=height, width=width)
max_r2 = 0
for lucka, x, z, pogled in data:
    x -= center_x
    z = lowest_z - z
    smreka.rotate_to(pogled * math.pi / 4)
    smreka.add_line(x * scale, z * scale, lucka)
    max_r2 = max(max_r2, x**2 + z**2)

max_r = int(math.sqrt(max_r2))
print(f"{max_r} -> {max_r ** 2} moznosti / lucko")
# print(*smreka.lines.items(), sep="\n")
print("Calculating lucke...")
for i, lucka in enumerate(sorted(smreka.lines)):  # [40, 41, 42, 43, 89, 104, 106, 110]
    print(f"{i}/{len(smreka.lines)}", end=" " * 10 + "\r")
    lines = smreka.lines[lucka]
    lines = [[p1.flatten(), p2.flatten()] for p1, p2 in lines]
    z = np.average([p1[2] for p1, p2 in lines] + [p1[2] for p1, p2 in lines])
    xy_lines = [(np.array([p1[0], p1[1], z]), np.array([p2[0], p2[1], z])) for p1, p2 in lines]
    points = ((x, y, z) for x, y in product(range(-max_r, max_r + 1), range(-max_r, max_r + 1)))
    smreka.lucke[lucka] = min(points, key=lambda p: distance(p, xy_lines))

    with open("data/bf_lucke3d.csv", "a+") as f:
        f.write(
            f"round 2: {lucka},{smreka.lucke[lucka][0]},{smreka.lucke[lucka][1]},{smreka.lucke[lucka][2]}\n"
        )
