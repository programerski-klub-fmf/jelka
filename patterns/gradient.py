from library.jelka import Jelka, Color, Id, Position, Time
import math

jelka = Jelka(file="data/random_tree.csv")


@jelka.run_shader
def color_change(id: int, time: int) -> Color:
    #offset = math.fabs(math.sin(time))*255 #max +-1
    offset = 0
    pos = list(jelka.get_pos(id))
    return (pos[0] * 255,pos[1] * 255,pos[2] * 255)