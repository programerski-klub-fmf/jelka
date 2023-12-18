from library.jelka import Color, Jelka

# NAME: DEBUG

jelka = Jelka(file="data/lucke3d.csv")

w = 100


@jelka.run_shader
def color_change(id: int, time: int, frame: int) -> Color:
    target_x = w * (time / 1000 / 10) % (2 * w) - w
    x, y, z = jelka.get_position_cm(id)
    if (x, y, z) == (0, 0, 0):
        return (0, 0, 50)
    if abs(x - target_x) < 10:
        return (0, 255, 0)
    return (50, 0, 0)
