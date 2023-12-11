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
    pygame.draw.circle(screen, color, (w * lucka[0] * scale + w // 2, (-w * lucka[1] * scale + h // 2)), size)


class Simulation:
    def __init__(self, smreka=None) -> None:
        self.running = True
        self.phi, self.tau = 0, 0

        if smreka is None:
            self.smreka = list(random_tree())
        else:
            self.smreka = list(smreka)
        self.points = [Matrix([[p[0]], [p[1]], [p[2]]]) for p in self.smreka]
        self.colors = [(randint(0, 255), randint(0, 255), randint(0, 255)) for _ in self.smreka]

        self.scale = 1
        self.camera = (0, -500, 100)

    def set_colors(self, colors):
        if not self.running:
            raise InterruptedError("Simulation stopped.")
        self.colors = [tuple(color) for color in colors]

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
        for p, c in zip(map(lambda x: (r * x).proj(self.camera), self.points), self.colors):
            if p[2] > 0:
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
                smreka=[
                    tuple(map(float, (line.split(",")[1:])))
                    for line in open(file).read().split("\n")
                    if line != ""
                ]
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
        self.simulation.set_colors(colors)


if __name__ == "__main__":
    with open("data/random_tree.csv", "w+") as f:
        for i, (x, y, z) in enumerate(random_tree()):
            f.write(f"{i},{x},{y},{z}\n")
    h = Hardware(file=None)
