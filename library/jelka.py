from .mode import Hardware
from collections import defaultdict
from typing import Any, Callable, cast
import time
from .mat import Matrix

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
        self.count = 300
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

        self.screen_mapping: dict[tuple[int, int], list[int]] = dict()
        self.screen_size: tuple[int, int] = (160, 160)
        self.new_screen_mapping()

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

    def get_pos(self, id: Id) -> Position:
        return self.positions[id]

    @nice_exit
    def run_shader(self, shader: Callable[[Id, Time], Color | None]) -> None:
        """Sprejme shader funkcijo, ki sprejme id lučke in čas v milisekundah od začetka simulacije in vrne barvo
        v obliki (r, g, b). Ko shader vrne None za vsaj eno lučko, se simulacija konča.
        """
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

    def new_screen_mapping(
        self,
        size: tuple[int, int] = (160, 160),
        rotation: tuple[float, float, float] = (0, 0, 0),
        translation: tuple[float, float, float] = (0, 0, 0),
        positive_only: bool = False,
    ) -> None:
        min_z = min(z for _, _, z in self.positions.values())
        max_z = max(z for _, _, z in self.positions.values())
        scale = size[1] / (max_z - min_z)

        self.screen_size = cast(tuple[int, int], tuple(size))
        tranformation = Matrix.rotation(*rotation)
        self.screen_mapping = {(x, y): [] for x in range(size[0]) for y in range(size[1])}

        # za vsako lučko izračunamo njeno pravokotno projekcijo na zaslon
        for i, (x, y, z) in self.positions.items():
            moved = tranformation * Matrix([[x], [y], [z]])
            moved = (moved[0][0] + translation[0], moved[1][0] + translation[1], moved[2][0] + translation[2])
            if positive_only and moved[1] < 0:
                continue
            projected = int(moved[0] * scale), int(moved[2] * scale)
            if projected in self.screen_mapping:
                self.screen_mapping[projected].append(i)

    def screen_draw(self, image: dict[tuple[int, int], Color] | list[list[Color]]) -> None:
        if isinstance(image, dict):
            self.set_colors(
                {
                    i: cast(Color, tuple(image[pixel]))
                    for pixel in image
                    for i in self.screen_mapping[pixel]
                    if pixel in self.screen_mapping
                }
            )
        elif isinstance(image, list):
            new_colors = {}
            for y in range(self.screen_size[1]):
                for x in range(self.screen_size[0]):
                    if y < len(image) and x < len(image[y]):
                        new_colors.update(
                            {
                                i: cast(Color, tuple(image[y][x]))
                                for i in self.screen_mapping[(x, y)]
                                if (x, y) in self.screen_mapping
                            }
                        )
            self.set_colors(new_colors)
        else:
            raise ValueError(f'Unsuported type "{type(image)}" for image.')
