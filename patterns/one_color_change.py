from library.jelka import Jelka, Color, Id, Position, Time

jelka = Jelka(file="data/random_tree.csv")


@jelka.run_shader
def color_change(id: int, time: int) -> Color:
    color = jelka.get_color(id)
    return Color(((color[0] + 1) % 256, (color[1] + 2) % 256, (color[2] + 3) % 256))
