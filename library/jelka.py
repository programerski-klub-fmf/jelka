from .mode import Hardware
from collections import defaultdict
from typing import Any, NewType, Callable, cast
import time

Color = tuple[int, int, int]
Id = int
Position = tuple[float, float, float]
Time = int


def nice_exit(func: Callable) -> Callable:
    def wrapper(*args: list, **kwargs: dict) -> Any:
        try:
            return func(*args, **kwargs)
        except InterruptedError:
            print("Interrupted.")

    return wrapper


class Jelka:
    def __init__(self, file: str | None = None) -> None:
        # TODO : lastnosti smreke: višina, širina, število lučk, refresh rate, čas simulacije?
        self.count = 500
        self.refresh_rate = 20  # / s

        self.colors: list[Color] = [(0, 0, 0) for _ in range(self.count)]
        if file is None:
            if hasattr(Hardware, "is_simulation") and Hardware.is_simulation:
                file = "data/random_tree.csv"
            else:
                file = "data/lucke3d.csv"
        self.hardware = Hardware(file=file)

        self.positions = {}
        with open(file) as f:
            for line in f.readlines():
                line = line.strip()
                if line == "":
                    continue
                i, x, y, z = line.split(",")
                self.positions[int(i)] = (float(x), float(y), float(z))

    def set_colors(self, colors: dict[Id, Color] | list[Color] | defaultdict[Id, Color]) -> None:
        if isinstance(colors, list):
            if len(colors) != self.count:
                raise ValueError(f"Seznam barv mora biti enak številu lučk Jelka.count = {self.count}.")
            self.colors = [cast(Color, color) for color in colors]
            self.hardware.set_colors(self.colors)
        elif isinstance(colors, defaultdict):
            self.colors = [colors[i] for i in range(self.count)]
            self.hardware.set_colors(self.colors)
        elif isinstance(colors, dict):
            self.colors = [colors[i] if i in colors else (0, 0, 0) for i in range(self.count)]
            self.hardware.set_colors(self.colors)
        else:
            raise ValueError(f"Unsuported type {type(colors)} for colors.")

    def get_color(self, id: Id) -> Color:
        return self.colors[id]

    @nice_exit
    def run_shader(self, shader: Callable[[Id, Time], Color | None]) -> None:
        started_time = int(time.time() * 1000)
        running = True
        colors = [shader(i, 0) for i in range(self.count)]
        last_time = time.time()
        while running:
            if any(color is None for color in colors):
                running = False
                break
            self.set_colors(cast(list[Color], colors))
            tmp_last_time = time.time()
            colors = [shader(i, int(time.time() * 1000) - started_time) for i in range(self.count)]
            time.sleep(max(1 / self.refresh_rate - (time.time() - last_time), 0.01))
            last_time = tmp_last_time
