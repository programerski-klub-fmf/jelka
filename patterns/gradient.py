from library.jelka import Jelka, Color, Id, Position, Time
import math

jelka = Jelka(file="data/random_tree.csv")


@jelka.run_shader
def color_change(id: int, time: int) -> Color:
    pos = list(jelka.get_pos(id))
    return ((pos[0] * 255 + math.sin(time/5000+1)*255 + 256) %256,(pos[1] * 255 + math.sin(time/5000 + 2)*255 + 256) %256,(pos[2] * 255 + math.sin(time/5000)*255 + 256) %256)
