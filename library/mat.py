# da ljudje ne rabijo nalagat numpyja samo za to, da dela simulacija
import math


class Matrix(list):
    def __mul__(self, other: "Matrix") -> "Matrix":  # type: ignore
        return Matrix(
            [
                [sum([self[i][m] * other[m][j] for m in range(len(self[0]))]) for j in range(len(other[0]))]
                for i in range(len(self))
            ]
        )

    def proj(self, cam: tuple[float, float, float]) -> tuple[float, float, float]:
        dy = self[1][0] - cam[1]
        if dy != 0:
            return ((self[0][0] - cam[0]) / dy, (self[2][0] - cam[2]) / dy, dy)
        else:
            return (0, 0, 1)

    @staticmethod
    def rotation(xy: float, yz: float, xz: float) -> "Matrix":
        r1 = Matrix([[math.cos(xy), -math.sin(xy), 0], [math.sin(xy), math.cos(xy), 0], [0, 0, 1]])
        r2 = Matrix([[1, 0, 0], [0, math.cos(yz), -math.sin(yz)], [0, math.sin(yz), math.cos(yz)]])
        r3 = Matrix([[math.cos(xz), 0, -math.sin(xz)], [0, 1, 0], [math.sin(xz), 0, math.cos(xz)]])
        return r3 * r2 * r1
