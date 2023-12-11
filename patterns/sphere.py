from library.jelka import Jelka, Color, Id, Position, Time
import math
import random as r

jelka = Jelka(file="data/random_tree.csv")

def clamp(c : Color):
    return (min(255,max(c[0],0)), min(255,max(c[1],0)),min(255,max(c[1],0)))

def dist(p):
    return math.sqrt(p[0] ** 2 + p[1]**2 + p[2]**2)

def abs(p):
    return [math.fabs(p[0]), math.fabs(p[1]),math.fabs(p[2])]

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


@jelka.run_shader_all
def update_colors(colors : list(Color),time: int, frame: int):
    colors = list(colors)
    sphere_center = [0.5,0.5,0.5]
    sphere_col = (255,255,255)
    sphere_rad = math.fabs(math.sin(frame / 50))*0.7+0.1
    positions = []
    intensity = []

    for i in range(0,len(colors)):
        pos = list(jelka.get_pos(i))
        diff =  [sphere_center[0] - pos[0],sphere_center[1] - pos[1],sphere_center[2] - pos[2]]
        if dist(diff) > sphere_rad :
            intensity.append(0)
            positions.append(sphere_center)
        else :
            #intensity.append(1)
            intensity.append(dist(diff)/sphere_rad)
            positions.append([pos[0] - diff[0], pos[1] - diff[1], pos[2] - diff[2]])
        #colors[i] = (pos[0] * sphere_col[0] ,sphere_col[1] * pos[1] ,pos[2] * sphere_col[2])


    positions = normalize(positions)
    for i in range(0,len(colors)):
        #print(sphere_col[0] * positions[i][0] * intensity[i])
       # print(positions[i])
        colors[i] = [sphere_col[0] * positions[i][0] * intensity[i],sphere_col[1] * positions[i][1] * intensity[i],sphere_col[2] * positions[i][2] * intensity[i] ]

    return colors


