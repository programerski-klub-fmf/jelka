import math
from library.types import Color, PositionCm, Position, PositionNormalized, Id
from typing import Iterable, cast
from random import randint


def clamp(c: Color) -> Color:
    """Clamps color into valid range (0-255)."""
    return min(255, max(c[0], 0)), min(255, max(c[1], 0)), min(255, max(c[1], 0))


def distance(p: Iterable[float]) -> float:
    """Calculates absolute value of a point."""
    return math.sqrt(sum(x**2 for x in p))


def get_max(positions: Iterable[Position]) -> tuple[float, ...]:
    """Gets the maximum position in iterable."""
    return tuple(max(pos[axis] for pos in positions) for axis in range(3))


def get_min(positions: Iterable[Position]) -> tuple[float, ...]:
    """Gets the minimum position in iterable."""
    return tuple(min(pos[axis] for pos in positions) for axis in range(3))


def normalize(
    positions: dict[Id, PositionCm], offset: PositionCm = (0, 0, 0)
) -> dict[Id, PositionNormalized]:
    max_coords = get_max(positions.values())
    min_coords = get_min(positions.values())
    difference = tuple(max_coords[axis] - min_coords[axis] for axis in range(3))
    difference = tuple(d if d != 0 else 1 for d in difference)
    return {
        i: cast(
            PositionNormalized,
            tuple((p[axis] - offset[axis] - min_coords[axis]) / difference[axis] for axis in range(3)),
        )
        for i, p in positions.items()
    }


def vivid(c: Color) -> Color:
    """Makes color more vivid."""
    m = min(c[0], c[1], c[2])
    if c[0] == m:
        return (0, c[1], c[2])
    if c[1] == m:
        return (c[0], 0, c[2])
    return (c[0], c[1], 0)


def random_color() -> Color:
    """Generates a random color."""
    return randint(0, 255), randint(0, 255), randint(0, 255)
