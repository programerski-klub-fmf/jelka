from library.jelka import Jelka, Color, Id, Position, Time
import math
import random as r

jelka = Jelka(file="data/random_tree.csv")

def dist(p):
    return math.sqrt(p[0] ** 2 + p[1]**2 + p[2]**2)

def get_max(positions) :
        mxx = [-1e9,-1e9,-1e9]
        mxx[0] = max(x for x, _, _ in positions)
        mxx[1] = max(y for _, y, _ in positions)
        mxx[2] = max(z for _, _, z in positions)
        return mxx

def get_min(positions):
        mnn = [1e9,1e9,1e9]
        mnn[0] = min(x for x, _, _ in positions)
        mnn[1] = min(y for _, y, _ in positions)
        mnn[2] = min(z for _, _, z in positions)
        return mnn

def normalize(positions):
    mx = get_max(positions)
    mn = get_min(positions)
    mx[0] -= mn[0]
    mx[1] -= mn[1]
    mx[2] -= mn[2]
    for i in range(0,len(positions)):
        positions[i] = [(positions[i][0] - mn[0])/mx[0] , (positions[i][1] -mn[1])/mx[1], (positions[i][2] - mn[2])/mx[2]]
    return positions

def vivid(c : Color):
    c=list(c)
    m = min(c[0],c[1],c[2])
    if c[0] == m: return (0,c[1],c[2])
    if c[1] == m: return (c[0],0,c[2])
    return (c[0],c[1],0)

@jelka.run_shader_all
def update_colors(colors : list(Color),time: int, frame: int):
    colors = list(colors)
    sphere_center = [0.5,0.5,0.5]
    rad2 = (math.e ** (math.sin(frame/20))) /3
    rad1 = (math.e ** (math.cos(frame/20))) /3

    global col
    if frame%10==0:
        rd = r.randint(0,2)
        col = [r.randint(0,255),r.randint(0,255),r.randint(0,255)]


    for i in range(0,len(colors)):
        pos = jelka.get_pos(i)
        diff =  [sphere_center[0] - pos[0],sphere_center[1] - pos[1],sphere_center[2] - pos[2]]
        if dist(diff) <= rad1 and dist(diff) >= rad2:
            j = dist(diff)/rad1
            if colors[i] == [0,0,0]:
                colors[i] = (j*col[0], j*col[1],j*col[2])
                colors[i] = vivid(colors[i])
            else : colors[i] = (j*colors[i][0], j*colors[i][1], j*colors[i][2])
        else: colors[i] = [0,0,0]

    return colors


