from library.jelka import Color, Jelka
from time import sleep

# NAME: DEBUG

jelka = Jelka(file="data/lucke3d.csv")

single = {
    44, 46, 48, 49, 50, 52, 55, 62, 98, 101, 120, 123, 165, 202, 222, 232, 244, 252, 269, 270, 299
}

l = 0
h = 299
sleep(1)
while l  < h:
    m = (l + h) // 2
    colors = []
    for i in range(jelka.count):
        if l <= i < m:
            colors.append((255, 0, 0))
        elif m <= i <= h:
            colors.append((0, 0, 255))
        else:
            colors.append((0, 0, 0))
    jelka.set_colors(colors)
    color = input(f"barva: [{l}:{h}] (r/b) ")
    if color == "r":
        h = m - 1
    elif color == "b":
        l = m
    else:
        print("napaka")
        break


    if l + 1 == h:
        jelka.set_colors({l: (255, 0, 0), h: (0, 0, 255)})
        color = input(f"barva: [{l}:{h}] (r/b) ")
        if color == "r":
            h = l
        elif color == "b":
            l = h
        else:
            print("napaka")

assert l == h

jelka.set_colors({l: (255, 255, 255)})
print(f"id = {l} = {h}")