from library.jelka import Jelka, Color, Id, Position, Time
import math

jelka = Jelka(file="data/random_tree.csv")


@jelka.run_shader
def color_change(id: int, time: int) -> Color:
    #offset = math.fabs(math.sin(time))*255 #max +-1
    offset = 0
    
    mnz = min(z for _, _, z in jelka.positions.values())
    mxz = max(z for _, _, z in jelka.positions.values())
    mxz -= mnz

    mny = min(y for _, y, _  in jelka.positions.values())
    mxy = max(y for _, y, _  in jelka.positions.values())
    mxy -= mny

    mnx = min(x for x, _, _ in jelka.positions.values())
    mxx = max(x for x, _, _ in jelka.positions.values())
    mxx -= mnx
    
    pos = list(jelka.get_pos(id))
    pos[0] -= mnx
    pos[1] -= mny
    pos[2] -= mnz
    
    pos[0] += offset
    pos[1] += offset
    pos[2] += offset
    
    mxx += offset
    mxy += offset 
    mxz += offset
    # med 0 in 1
    pos[0] /= mxx
    pos[1] /= mxy
    pos[2] /= mxz
    #print(offset)
    #if pos[0] < 0 or pos[0] > 1 or pos[1] < 0 or pos[1] > 1 or pos[2] < 0 or pos[2] > 1:
    #    print(pos)
    return (pos[0] * 255,pos[1] * 255,pos[2] * 255)