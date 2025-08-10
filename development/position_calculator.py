import numpy as np
import scipy


def distance(point, lines):
    point = np.array(point)

    return np.sum(
        np.array(
            [
                np.linalg.norm(
                    np.cross(point - line[0], line[0] - line[1]) / np.linalg.norm(line[0] - line[1])
                )
                ** 2
                for line in lines
            ]
        )
    )


def jac(point, lines):
    point = np.array(point)

    return 2 * np.sum(
        np.array(
            [
                [
                    (point - line[0])
                    - (line[0] - line[1])
                    * np.dot(point - line[0], line[0] - line[1])
                    / np.linalg.norm(line[0] - line[1]) ** 2
                    for line in lines
                ]
            ]
        ),
        axis=1,
    )


class Smreka:
    def __init__(self, x, y, z, height=200, width=200) -> None:
        self.origin = np.array([[0], [0], [0]])
        self.camera = np.array([[-x], [-y], [-z]])

        # končni rezultati (lucka -> OptimizeResult), OptimizeResult.x = [x, y, z], OptimizeResult.success = True/False
        self.lucke = {}

        self.inverse_rotation = np.identity(3)
        self.angle = 0
        self.height = height
        self.width = width

        self.lines = {}  # lucka -> [(point1, point2), ...]

    def rotate_to(self, angle):
        self.angle = angle
        self.angle %= np.pi * 2
        self.inverse_rotation = np.array(
            [
                [np.cos(-self.angle), -np.sin(-self.angle), 0],
                [np.sin(-self.angle), np.cos(-self.angle), 0],
                [0, 0, 1],
            ]
        )

    def add_line(self, x: float, z: float, lucka=0):
        # pravokotno na ravnino kamere (y = y_camera)
        point1 = np.array([[x], [-self.camera[1, 0]], [z]]) + self.camera
        point2 = point1 + np.array([[0], [self.height], [0]])
        pointa = self.inverse_rotation @ self.camera
        pointb = self.inverse_rotation @ point2

        if lucka not in self.lines:
            self.lines[lucka] = []
        self.lines[lucka].append((pointa, pointb))

    def calculate(self):
        # Sanja se mi ne zakaj, ampak če uporabljam bounds gre vse v (0, 0, 0)
        # bounds = ((-self.width, -self.width, 0), (self.width, self.width, self.height))
        for lucka in self.lines:
            lines = [(line[0].flatten(), line[1].flatten()) for line in self.lines[lucka]]
            # print(lucka, lines)
            yield lucka, scipy.optimize.least_squares(
                distance,
                np.array([0, 0, 0]),
                args=(lines,),
            )

    def calculate_lucke(self):
        self.lucke = dict(self.calculate())


class Cam:
    def __init__(self, d, angle, f, lucke: dict[int, tuple[float, float]]):
        ''' d = distance camera - center of rotation
        f = focal length in pixel/cm
        '''
        self.d = d
        self.f = f
        self.angle = angle % (2 * np.pi)
        self.lucke = {lucka: np.array([[x], [z]]) for lucka, (x, z) in lucke.items()}
        self.inverse_rotation = np.array(
            [
                [np.cos(-self.angle), -np.sin(-self.angle), 0],
                [np.sin(-self.angle), np.cos(-self.angle), 0],
                [0, 0, 1],
            ]
        )
    
    def pos_to_uv(self, r: np.array):
        xyz = self.inverse_rotation @ np.array([[r[0]], [r[1]], [r[2]]]) + np.array([[0], [self.d], [0]])
        return self.f / xyz[1] * np.array([
            [1, 0, 0],
            [0, 0, 1],
        ]) @ xyz

    def uv_to_err2(self, uv: np.array, led: int):
        err = uv - self.lucke[led]
        err2 = np.sum(err ** 2)
        return err2

def total_error(pos: np.array, cams: list[Cam], led: int):
    te = sum(cam.uv_to_err2(cam.pos_to_uv(pos), led) for cam in cams)
    # print("total_error", te)
    return te

def calculate(cams: list[Cam], led: int):
    return scipy.optimize.minimize(
        total_error,
        np.array([0, 0, 0]),
        args=(cams, led),
    )