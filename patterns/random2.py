from library.jelka import Jelka, Color, Id, Position, Time
import random as r

jelka = Jelka(file="data/random_tree.csv")


@jelka.run_shader
def color_change(id: int, time: int) -> Color:
    cur = jelka.get_color(id)
    if time % 5 == 0: return Color((r.randint(0,255), r.randint(0,255), r.randint(0,255)))
    return cur
