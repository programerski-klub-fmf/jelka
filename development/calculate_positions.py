from position_calculator import Smreka
import math

print("Reading data...")
data = []
with open("data/points3.csv") as f:
    for line in f.readlines():
        lucka, x, z, pogled = map(int, line.split(","))
        data.append((lucka, x, z, pogled))

# x = 0 je na levem robu slike
center_x = [880] * 8  # zares je sredina smreke na 920, ampak tkole so boljši rezultati
angles = [-n * 45 for n in range(8)]
# center_x = [0] * 4
# koordinatni sistem je obrnjen,
lowest_z = max(data, key=lambda x: x[2])[2]
height_on_image = abs(min(data, key=lambda x: x[2])[2] - lowest_z)
width, height = 200, 200
scale = height / height_on_image
print(f"{scale=}")
print(f"{lowest_z=}")
print(f"{center_x=}")
smreka = Smreka(0, 200, 0, height=height, width=width)
lp = {}
for lucka, x, z, pogled in data:
    x -= center_x[pogled]
    z = lowest_z - z
    smreka.rotate_to(math.radians(angles[pogled]))
    if lucka not in lp:
        lp[lucka] = []
    if True:  # pogled != 2 or 0 not in lp[lucka]:
        smreka.add_line(x * scale, z * scale, lucka)
        lp[lucka].append(pogled)

# print(*smreka.lines.items(), sep="\n")
print("Calculating lucke...")
smreka.calculate_lucke()
for lucka in smreka.lucke:
    if not smreka.lucke[lucka].success:
        print(
            f"{lucka=}: result={smreka.lucke[lucka].x} cost={smreka.lucke[lucka].cost} success={smreka.lucke[lucka].success}"
        )

print("Writing data...")
with open("data/lucke3d.csv", "w") as f:
    for lucka in sorted(smreka.lucke.keys()):
        f.write(
            f"{lucka},{smreka.lucke[lucka].x[0]},{-smreka.lucke[lucka].x[1]},{smreka.lucke[lucka].x[2]}\n"
        )
