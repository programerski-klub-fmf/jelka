from library.jelka import Color, Jelka

# NAME: DEBUG

jelka = Jelka(file="data/lucke3d.csv")
single = {
    44, 46, 48, 49, 50, 52, 55, 62, 98, 101, 120, 123, 165, 202, 222, 232, 244, 252, 269, 270, 299
}


@jelka.run_shader
def color_change(id: int, time: int, frame: int) -> Color:
    x, y, z = jelka.get_position_cm(id)
    if (x, y, z) == (0, 0, 0):
        return (0, 0, 100)
    if id in single:
        return (0, 255, 0)
    # if id in sus:
    #     return (255, 0, 0)
    # if id in lil_sus:
    #     return (255, 255, 0)
    return (0, 0, 150)