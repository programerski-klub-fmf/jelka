from library.jelka import Jelka, Color, Id, Position, Time

jelka = Jelka(file="data/lucke3d.csv")


@jelka.run_shader
def color_change(id: int, time: int) -> Color:
    # TODO: Kaj sploh dela ta vzorec ker ne zgleda prav?
    # color = jelka.get_color(id)
    x, y, z = jelka.get_pos(id)
    z *= 256
    return (z % 256, z % 256, z % 256)
