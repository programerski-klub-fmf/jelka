import math
from library.types import Color, Position
import random as r


def clamp(c: Color) -> Color:
    return (min(255, max(c[0], 0)), min(255, max(c[1], 0)), min(255, max(c[1], 0)))


def dist(p: Position) -> float:
    return math.sqrt(p[0] ** 2 + p[1] ** 2 + p[2] ** 2)


def abs(p: Position) -> Position:
    return (math.fabs(p[0]), math.fabs(p[1]), math.fabs(p[2]))


def get_max(positions: list[Position]) -> list[float]:
    mxx = [-1e9, -1e9, -1e9]
    mxx[0] = max(x for x, _, _ in positions)
    mxx[1] = max(y for _, y, _ in positions)
    mxx[2] = max(z for _, _, z in positions)
    return mxx


def get_min(positions: list[Position]) -> list[float]:
    mnn = [1e9, 1e9, 1e9]
    mnn[0] = min(x for x, _, _ in positions)
    mnn[1] = min(y for _, y, _ in positions)
    mnn[2] = min(z for _, _, z in positions)
    return mnn


def normalize(positions: list[Position], offset: Position = (0, 0, 0)) -> list[Position]:
    positions = list(positions)
    for i in range(0, len(positions)):
        positions[i] = (
            2 * positions[i][0] - offset[0],
            2 * positions[i][1] - offset[1],
            2 * positions[i][2] - offset[2],
        )

    mx = get_max(positions)
    mn = get_min(positions)
    mx[0] -= mn[0]
    mx[1] -= mn[1]
    mx[2] -= mn[2]
    for i in range(0, len(positions)):
        try:
            positions[i] = (
                (positions[i][0] - mn[0]) / mx[0],
                (positions[i][1] - mn[1]) / mx[1],
                (positions[i][2] - mn[2]) / mx[2],
            )
        except ZeroDivisionError:
            positions[i] = (0, 0, 0)
    return positions


def vivid(c: Color) -> Color:
    c = list(c)
    m = min(c[0], c[1], c[2])
    if c[0] == m:
        return (0, c[1], c[2])
    if c[1] == m:
        return (c[0], 0, c[2])
    return (c[0], c[1], 0)


def random_color() -> Color:
    return (r.randint(0, 255), r.randint(0, 255), r.randint(0, 255))
