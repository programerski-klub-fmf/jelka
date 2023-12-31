import math
from random import uniform, randint
from threading import Thread, Lock


class Matrix(list):
    def __mul__(self, other):
        return Matrix(
            [
                [sum([self[i][m] * other[m][j] for m in range(len(self[0]))]) for j in range(len(other[0]))]
                for i in range(len(self))
            ]
        )

    def proj(self, cam):
        dy = self[1][0] - cam[1]
        if dy != 0:
            return ((self[0][0] - cam[0]) / dy, (self[2][0] - cam[2]) / dy, dy)
        else:
            return (0, 0, 1)

    @staticmethod
    def rotation(phi, tau):
        xy = Matrix([[math.cos(phi), -math.sin(phi), 0], [math.sin(phi), math.cos(phi), 0], [0, 0, 1]])
        yz = Matrix([[1, 0, 0], [0, math.cos(tau), -math.sin(tau)], [0, math.sin(tau), math.cos(tau)]])
        return yz * xy


def random_tree(n=300, origin=(0, 0, 0), height=200, max_width=120, min_width=60):
    count = 0
    while count < n:
        x = uniform(-max_width, max_width)
        y = uniform(-max_width, max_width)
        h = uniform(0, height)
        max_w = (height - h) / height * max_width
        min_w = max(max_w - max_width + min_width, 0)
        if min_w**2 <= x**2 + y**2 <= max_w**2:
            count += 1
            yield (x + origin[0], y + origin[1], origin[2] + h)


def draw_lucka(pygame, lucka, screen, size, color, scale):
    w, h = pygame.display.get_surface().get_size()
    pygame.draw.circle(
        screen, color, (w * lucka[0] * scale + w // 2, (-w * lucka[1] * scale + h // 2)), size + 3
    )


def draw_line(pygame, p1, p2, screen, color, scale):
    w, h = pygame.display.get_surface().get_size()
    pygame.draw.line(
        screen,
        color,
        (w * p1[0] * scale + w // 2, (-w * p1[1] * scale + h // 2)),
        (w * p2[0] * scale + w // 2, (-w * p2[1] * scale + h // 2)),
    )


class Simulation:
    def __init__(self, smreka=None) -> None:
        self.running = True
        self.phi, self.tau = 0, 0

        if smreka is None:
            self.smreka = {i: pos for i, pos in enumerate(random_tree())}
        else:
            self.smreka = smreka.copy()
        self.points = {i: Matrix([[p[0]], [p[1]], [p[2]]]) for i, p in self.smreka.items()}
        self.colors = {i: (randint(0, 255), randint(0, 255), randint(0, 255)) for i in self.smreka}

        self.scale = 1
        self.camera = (0, -500, 100)

    def set_colors(self, colors):
        if not self.running:
            raise InterruptedError("Simulation stopped.")
        try:
            for i, c in colors.items():
                assert all(isinstance(c[i], int) for i in range(3))
                assert all(0 <= c[i] <= 255 for i in range(3))
        except AssertionError:
            self.running = False
            raise ValueError(f"Wrong shape for color: ({i}: {c})") from None
        self.colors = {pk: tuple(color) for pk, color in colors.items()}

    def init(self):
        import pygame

        self.pygame = pygame
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        pygame.mouse.get_rel()

    def frame(self):
        pygame = self.pygame
        self.w, self.h = pygame.display.get_surface().get_size()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEWHEEL:
                self.camera = (self.camera[0], self.camera[1] + event.y * 5, self.camera[2])
            elif event.type == pygame.VIDEORESIZE:
                old_surface_saved = self.screen
                self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                self.screen.blit(old_surface_saved, (0, 0))
                del old_surface_saved

        mouse_pressed = pygame.mouse.get_pressed(num_buttons=3)
        key_pressed = pygame.key.get_pressed()
        if mouse_pressed[0] and not key_pressed[pygame.K_LCTRL] and not key_pressed[pygame.K_RCTRL]:
            dphi, dtau = pygame.mouse.get_rel()
            self.phi += dphi / 100
            self.tau += dtau / 100 if dphi == 0 or dtau / dphi > 0.69 else 0
        elif mouse_pressed[0] and (key_pressed[pygame.K_LCTRL] or key_pressed[pygame.K_RCTRL]):
            dx, dz = pygame.mouse.get_rel()
            self.camera = (self.camera[0] - dx / 2, self.camera[1], self.camera[2] + dz / 2)
        else:
            pygame.mouse.get_rel()

        self.screen.fill("black")

        r = Matrix.rotation(self.phi, self.tau)
        prev = None
        projected = {i: (r * p).proj(self.camera) for i, p in self.points.items()}

        for _, p in sorted(projected.items()):
            if p[2] > 0 and prev and prev[2] > 0:
                draw_line(pygame, p, prev, self.screen, (10, 10, 10), self.scale)
            prev = p

        for i, p in projected.items():
            c = self.colors.get(i, (0, 0, 0))
            draw_lucka(pygame, (p[0], p[1]), self.screen, max(20 / p[2], 1), c, self.scale)

        p = (r * Matrix([[0], [0], [0]])).proj(self.camera)
        draw_lucka(pygame, (p[0], p[1]), self.screen, max(20 / p[2], 1), (0, 255, 0), self.scale)
        pygame.display.flip()
        # self.clock.tick(60)  # limits FPS to 60

    def quit(self):
        self.running = False
        self.pygame.quit()


class Hardware:
    is_simulation = True

    def __init__(self, file: str | None = "data/random_tree.csv") -> None:
        if file is None:
            self.simulation = Simulation()
        else:
            self.simulation = Simulation(
                smreka={
                    int(line.split(",")[0]): tuple(map(float, (line.split(",")[1:])))
                    for line in open(file).read().split("\n")
                    if line != ""
                }
            )

        self.thread = Thread(target=self._run)
        self.thread.start()

    def _run(self) -> None:
        try:
            self.simulation.init()
            while self.simulation.running:
                with Lock():
                    self.simulation.frame()
            self.simulation.quit()
        finally:
            self.simulation.quit()

    def set_colors(self, colors: list[tuple[int, int, int]]) -> None:
        self.simulation.set_colors({i: color for i, color in enumerate(colors)})


if __name__ == "__main__":
    rt = list(random_tree())
    with open("data/random_tree.csv", "w+") as f:
        for i, (x, y, z) in enumerate(rt):
            f.write(f"{i},{x},{y},{z}\n")
    rt = {
        int(line.split(",")[0]): tuple(map(float, (line.split(",")[1:])))
        for line in open("data/lucke3d.csv").read().split("\n")
        if line != ""
    }
    scale = 0.2372479240806643
    lz = 1068
    cx = 880
    with open("data/3d_to_2d.csv", "w+") as f:
        for i, (x, y, z) in ((i, rt[i]) for i in rt):
            for pogled in range(4):
                rot = Matrix.rotation(pogled * math.pi / 2, 0)
                v = rot * Matrix([[x], [y], [z]])
                xp = v[0][0]  # / scale + cx
                zp = lz - v[2][0] / scale
                f.write(f"{i},{int(xp)},{int(zp)},{pogled}\n")
    h = Hardware(file=None)
