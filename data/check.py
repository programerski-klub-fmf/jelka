import numpy as np

def read_pos(filename):
    with open(filename, "r") as file:
        return {
            int(line.split(",")[0]): tuple(map(float, (line.split(",")[1:])))
            for line in file.read().split("\n")
            if line != ""
        }
    

old = read_pos("lucke3d.csv")
new = read_pos("test.csv")
new = {key: (x * 2, y * 2.6, z * 2) for key, (x, y, z) in new.items()}

moy = min(old.values(), key=lambda x: x[1])[1]
mny = min(new.values(), key=lambda x: x[1])[1]
ky = moy / mny

mox = min(old.values(), key=lambda x: x[0])[0]
mnx = min(new.values(), key=lambda x: x[0])[0]
kx = mox / mnx

moz = min(old.values(), key=lambda x: x[2])[2]
mnz = min(new.values(), key=lambda x: x[2])[2]
kz = moz / mnz

print(f"y: {ky}, x: {kx}, z: {kz}")

v1 = []
v2 = []
for key, (x, y, z) in old.items():
    if key in new:
        x2, y2, z2 = new[key]
        v1.append(np.array([x, y, z]))
        v2.append(np.array([x2, y2, z2]))

v1 = np.array(v1)
v2 = np.array(v2)
print(f"std: {np.std(v1 - v2, axis=0)}")
print(f"avg: {np.average(np.abs(v1 - v2), axis=0)}")
print(f"max: {np.max(np.abs(v1 - v2), axis=0)}")
print(f"<1: {(np.sum(np.abs(v1 - v2) < 1)) / len(v1) * 100 / 3} %")
print(f"<5: {(np.sum(np.abs(v1 - v2) < 5)) / len(v1) * 100 / 3} %")
print(f"<10: {(np.sum(np.abs(v1 - v2) < 10)) / len(v1) * 100 / 3} %")
