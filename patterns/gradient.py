from library.jelka import Jelka, Color, Id, Position, Time
import math

jelka = Jelka(file="data/random_tree.csv")

def vivid(c : Color):
    c=list(c)
    m = min(c[0],c[1],c[2])
    if c[0] == m: return (0,c[1],c[2])
    if c[1] == m: return (c[0],0,c[2])
    return (c[0],c[1],0)

@jelka.run_shader
def color_change(id: int, time: int) -> Color:
    pos = list(jelka.get_pos(id))
    return vivid(((pos[0] * 255 + math.sin(time/5000+1)*255 + 256) %256,(pos[1] * 255 + math.sin(time/5000 + 2)*255 + 256) %256,(pos[2] * 255 + math.sin(time/5000)*255 + 256) %256))
