import math

from library.jelka import Color, Jelka
from library.patterns_lib import vivid

# NAME: Gradient

jelka = Jelka(file="data/lucke3d.csv")


@jelka.run_shader
def color_change(id: int, time: int, frame: int) -> Color:
    pos = list(jelka.get_position_normalized(id))
    return vivid(
        (
            (pos[0] * 255 + math.sin(time / 5000 + 1) * 255 + 256) % 256,
            (pos[1] * 255 + math.sin(time / 5000 + 2) * 255 + 256) % 256,
            (pos[2] * 255 + math.sin(time / 5000) * 255 + 256) % 256,
        )
    )
