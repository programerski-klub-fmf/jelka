#!/usr/bin/env python3
# API za umetnike -- produkcija
from mmap import mmap
from sys import stdout, argv
from io import FileIO
shmf = open("/dev/shm/jelka", mode="r+b")
buffer = mmap(shmf.fileno(), 0)
w = FileIO(int(argv[1]), mode="w", closefd=False)
def nastavi(luč, barva):
    buffer[luč*3] = int(barva[0])
    buffer[luč*3+1] = int(barva[1])
    buffer[luč*3+2] = int(barva[2])
def pokaži(tupli):
    idx = 0
    for rgb in tupli:
        nastavi(idx, rgb)
        idx += 1
def izriši():
    w.write(b'\n')
class Hardware:
    def __init__(self, file) -> None:
        pass
    def set_colors(self, colors: list[tuple[int, int, int]]) -> None:
        pokaži(colors)
        izriši()
