from library.jelka import Color, Jelka

jelka = Jelka(file="data/lucke3d.csv")


very_sus = {148, 152, 27, 157, 285, 34, 36, 37, 166, 295, 40, 41, 169, 296, 297, 176, 202, 89, 217, 218, 95, 97, 102, 103, 104, 106, 110, 246, 249}
sus = {7, 11, 23, 24, 25, 27, 28, 30, 32, 33, 34, 36, 37, 38, 40, 41, 42, 43, 45, 46, 47, 50, 51, 60, 64, 71, 77, 78, 79, 80, 82, 83, 84, 85, 86, 88, 89, 90, 92, 93, 94, 95, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 109, 110, 111, 112, 113, 114, 115, 116, 118, 119, 120, 126, 138, 141, 146, 148, 150, 151, 152, 153, 154, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 168, 169, 171, 172, 174, 176, 188, 194, 201, 202, 212, 213, 214, 215, 216, 217, 218, 221, 223, 224, 226, 234, 240, 241, 242, 244, 245, 246, 247, 248, 249, 251, 252, 253, 254, 255, 262, 263, 264, 265, 268, 270, 271, 272, 273, 283, 284, 285, 286, 293, 295, 296, 297, 299}
lil_sus = {267, 19, 20, 152, 153, 282, 27, 284, 29, 157, 285, 34, 291, 37, 166, 167, 40, 41, 169, 295, 296, 45, 297, 54, 202, 210, 89, 217, 218, 220, 93, 95, 96, 97, 228, 102, 103, 104, 106, 108, 110, 245, 246, 125}

single = {0, 1, 2, 6, 8, 9, 10, 13, 15, 19, 29, 33, 38, 39, 44, 46, 47, 51, 54, 56, 57, 58, 59, 61, 62, 63, 64, 66, 96, 98, 99, 101, 105, 108, 111, 112, 113, 114, 115, 118, 119, 120, 121, 122, 124, 125, 128, 132, 135, 140, 167, 172, 174, 178, 181, 189, 205, 210, 220, 222, 223, 224, 226, 228, 229, 230, 244, 251, 253, 270, 271, 272, 274, 286, 289, 290, 292, 298, 299}

@jelka.run_shader
def color_change(id: int, time: int) -> Color:
    x, y, z = jelka.get_real_pos(id)
    if (x, y, z) == (0, 0, 0):
        return (0, 0, 100)
    if id in single:
        return (0, 255, 0)
    # if id in sus:
    #     return (255, 0, 0)
    # if id in lil_sus:
    #     return (255, 255, 0)
    return (0, 0, 150)