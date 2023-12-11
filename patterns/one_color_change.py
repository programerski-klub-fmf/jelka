from colorsys import hsv_to_rgb, rgb_to_hsv

from library.jelka import Color, Jelka

jelka = Jelka(file="data/lucke3d.csv")


@jelka.run_shader
def color_change(id: int, time: int) -> Color:
    hue = rgb_to_hsv(*jelka.get_color(id))[0] * 360
    hue = (hue + 1) % 360

    color = hsv_to_rgb(hue / 360.0, 1.0, 1.0)
    color = tuple(map(lambda x: int(x * 255), color))

    return Color(color)
