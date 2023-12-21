from .mode import Hardware
from collections import defaultdict
from typing import Any, Callable, cast
import time
from .mat import Matrix
from library.patterns_lib import normalize, distance
from library.types import Id, Color, PositionCm, PositionNormalized, PositionRelative, TimeMs


def nice_exit(func: Callable) -> Callable:
    def wrapper(*args: list, **kwargs: dict) -> Any:
        try:
            return func(*args, **kwargs)
        except InterruptedError:
            print("Interrupted.")

    return wrapper


def to_color(t: Any) -> Color:
    r = (int(t[0]), int(t[1]), int(t[2]))
    assert all(0 <= x <= 255 for x in r)
    return r


class Jelka:
    def __init__(self, file: str | None = None) -> None:
        # TODO : lastnosti smreke: višina, širina, število lučk, refresh rate, čas simulacije?
        self.count = 300
        self.refresh_rate = 20  # / s
        self.is_simulation = hasattr(Hardware, "is_simulation") and Hardware.is_simulation

        self._colors: list[Color] = [(0, 0, 0) for _ in range(self.count)]
        if file is None:
            if self.is_simulation:
                file = "data/random_tree.csv"
            else:
                file = "data/lucke3d.csv"
        self.hardware = Hardware(file=file)

        self.positions_cm: dict[Id, PositionCm] = {}
        with open(file) as f:
            for line in f.readlines():
                line = line.strip()
                if line == "":
                    continue
                i, x, y, z = line.split(",")
                self.positions_cm[int(i)] = (float(x), float(y), float(z))

        # calculate positions relative to the center of the tree whith max radius 1 and height 1
        max_r = max(distance(p[:2]) for p in self.positions_cm.values())
        max_h = max(p[2] for p in self.positions_cm.values())
        self.positions_relative: dict[Id, PositionRelative] = {
            i: (p[0] / max_r, p[1] / max_r, p[2] / max_h) for i, p in self.positions_cm.items()
        }
        # calculate positions normalized to [0,1]
        self.positions_normalized: dict[Id, PositionNormalized] = normalize(self.positions_cm)

        self.screen_mapping: dict[tuple[int, int], list[int]] = dict()
        self.screen_size: tuple[int, int] = (160, 160)
        self.new_screen_mapping()

    @property
    def colors(self) -> list[Color]:
        return [(color[0], color[1], color[2]) for color in self._colors]

    def if_exists(self, i: int, color: Color) -> Color:
        return color if i in self.positions_cm else (0, 0, 0)

    def set_colors(self, colors: dict[Id, Color] | list[Color] | defaultdict[Id, Color]) -> None:
        if isinstance(colors, list):
            if len(colors) != self.count:
                raise ValueError(f"Seznam barv mora imeti enako število lučk kot Jelka.count = {self.count}.")
            self._colors = [color for i, color in enumerate(colors)]
        elif isinstance(colors, defaultdict):
            self._colors = [colors[i] for i in range(self.count)]
        elif isinstance(colors, dict):
            self._colors = [colors[i] if i in colors else (0, 0, 0) for i in range(self.count)]
        else:
            raise ValueError(f"Unsuported type {type(colors)} for colors.")
        self.hardware.set_colors([self.if_exists(i, to_color(color)) for i, color in enumerate(self._colors)])

    def get_color(self, id: Id) -> Color:
        if id >= len(self._colors) or id < 0:
            return (0, 0, 0)
        return self._colors[id]

    def get_position_cm(self, id: Id) -> PositionCm:
        if id not in self.positions_cm:
            return (0, 0, 0)
        return self.positions_cm[id]

    def get_position_relative(self, id: Id) -> PositionRelative:
        if id not in self.positions_relative:
            return (0, 0, 0)
        return self.positions_relative[id]

    def get_position_normalized(self, id: Id) -> PositionNormalized:
        if id not in self.positions_normalized:
            return (0, 0, 0)
        return self.positions_normalized[id]

    def run_shader(self, shader: Callable[[Id, TimeMs, int], Color | None]) -> None:
        """Sprejme shader funkcijo, ki sprejme id lučke in čas v milisekundah od začetka simulacije in vrne barvo
        v obliki (r, g, b). Ko shader vrne None za vsaj eno lučko, se simulacija konča.
        """
        self.run_shader_all(lambda time, frame: [shader(i, time, frame) for i in range(self.count)])

    @nice_exit  # TODO pobriši in naredi lepo in malo bolj bug resistant
    def run_shader_all(
        self,
        multi_shader: Callable[[TimeMs, int], list[Color]],
    ) -> None:
        """enako kot run_shader, edino da poda "frame" info in pa da zahteva da nastavi vse lucke"""
        started_time = int(time.time() * 1000)
        frame = 0
        running = True
        colors = [(0, 0, 0) for i in range(self.count)]
        last_time = time.time()
        while running:
            if any(color is None for color in colors):
                running = False
                break
            self.set_colors(cast(list[Color], colors))
            tmp_last_time = time.time()
            colors = multi_shader(int(time.time() * 1000) - started_time, frame)
            time.sleep(max(1 / self.refresh_rate - (time.time() - last_time), 0.01))
            last_time = tmp_last_time
            frame += 1

    def new_screen_mapping(
        self,
        size: tuple[int, int] = (50, 50),
        rotation: tuple[float, float, float] = (0, 0, 0),
        translation: tuple[float, float, float] = (0, 0, 0),
        positive_only: bool = False,
    ) -> None:
        min_z = min(z for _, _, z in self.positions_cm.values())
        max_z = max(z for _, _, z in self.positions_cm.values())
        scale = size[1] / (max_z - min_z)

        self.screen_size = cast(tuple[int, int], tuple(size))
        tranformation = Matrix.rotation(*rotation)
        self.screen_mapping = {(x, y): [] for x in range(size[0]) for y in range(size[1])}

        # za vsako lučko izračunamo njeno pravokotno projekcijo na zaslon
        for i, (x, y, z) in self.positions_cm.items():
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
