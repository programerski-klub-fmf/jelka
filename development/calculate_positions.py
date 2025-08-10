from position_calculator import Cam, calculate, total_error
import math

def main():
    print("Reading data...")
    data = []
    max_pogled = 0
    vse_lucke = set()
    with open("../data/points3.csv") as f:
        for line in f.readlines():
            lucka, x, z, pogled = map(int, line.split(","))
            vse_lucke.add(lucka)
            data.append((lucka, x, z, pogled))
            max_pogled = max(max_pogled, pogled)
    ok_pos = {}
    with open("../data/test.csv", "r") as f:
        for line in f.readlines():
            lucka, x, y, z = line.split(",")
            ok_pos[int(lucka)] = (float(x), float(y) - 40, float(z))

    # x = 0 je na levem robu slike
    center_x = [920] * 8  # zares je sredina smreke na 920, ampak tkole so boljši rezultati
    lowest_z = min(data, key=lambda x: x[2])[2]
    max_z = max(data, key=lambda x: x[2])[2]
    height_on_image = max(data, key=lambda x: x[2])[2] - lowest_z
    print(f"Lowest Z: {lowest_z}, Height on image: {height_on_image}")
    # koordinatni sistem je obrnjen, necentriran
    data = [(lucka, x - center_x[pogled], (- z + max_z - height_on_image * 0.4), pogled) for lucka, x, z, pogled in data]
    lowest_z = min(data, key=lambda x: x[2])[2]
    max_z = max(data, key=lambda x: x[2])[2]
    min_x = min(data, key=lambda x: x[1])[1]
    max_x = max(data, key=lambda x: x[1])[1]
    angles = [-n * 45 for n in range(8)]
    # center_x = [0] * 4
    f = height_on_image
    print(f"{f=}")
    print(f"{lowest_z=}")
    print(f"{max_z=}")
    print(f"{min_x=} {max_x=} avg_x={sum(x for _, x, _, _ in data) / len(data)}")
    
    cams = []
    for pogled in range(max_pogled + 1):
        lucke = {lucka: (x, z) for lucka, x, z, p in data if p == pogled}
        cams.append(Cam(d=200, angle=angles[pogled], f=f, lucke=lucke))

    # cams = [cams[0]]
    positions = []
    sug_fs_x = []
    sug_fs_y = []
    good_errs = []
    for lucka in sorted(vse_lucke):
        print(f"Lucka {lucka}")
        this_cams = [cam for cam in cams if lucka in cam.lucke]
        pos3d = calculate(this_cams, lucka)
        # print(pos3d)
        print(f"3D Position for Lucka {lucka}: {pos3d.success=} {pos3d.x=} total_error={total_error(pos3d.x, this_cams, lucka)}")
        positions.append([lucka, pos3d.x[0], pos3d.x[1], pos3d.x[2]])

        calced = ok_pos[lucka]
        # print("lucka uv", cams[0].lucke[lucka])
        for cam in this_cams:
            uvt = cam.pos_to_uv(calced)
            sug_fs_x.append(f / (uvt[0][0] / cam.lucke[lucka][0]))
            sug_fs_y.append(f / (uvt[1][0] / cam.lucke[lucka][1]))
        # print("Good position:", calced)
        good_errs.append(total_error(calced, this_cams, lucka))
    print("Good errors:", good_errs)
    # print("Suggested focal lengths:", sug_fs_x, "\n"+"#"*100+"\n", sug_fs_y)

    positions.sort()
    with open("../data/positions_test2.csv", "w") as f:
        for pos in positions:
            f.write(f"{pos[0]},{pos[1]},{pos[2]},{pos[3]}\n")
    print("Done writing positions to ../data/positions_test2.csv")

main()