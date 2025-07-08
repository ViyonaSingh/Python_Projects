import pygame
import math
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1000, 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
FPS = 60
GRAVITY = 0.4

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Drawing Physics")
clock = pygame.time.Clock()


class Ball:
    def __init__(self):
        self.radius = 10
        self.x = 50
        self.y = 50
        self.vx = 0
        self.vy = 0
        self.released = False
        self.mode = "rubber"  # "rubber" or "steel"

    def update(self, lines):
        if not self.released:
            return

        # Apply gravity
        self.vy += GRAVITY if self.mode == "rubber" else GRAVITY * 0.5

        steps = 8  # more sub steps = better accuracy
        for _ in range(steps):
            self.x += self.vx / steps
            self.y += self.vy / steps

            for line in lines:
                (x1, y1), (x2, y2) = line
                collision, nx, ny = self._check_collision(x1, y1, x2, y2)
                if collision:
                    self._resolve_collision(nx, ny)

    def _check_collision(self, x1, y1, x2, y2):
        px, py = self.x, self.y
        dx, dy = x2 - x1, y2 - y1
        line_len_sq = dx ** 2 + dy ** 2

        if line_len_sq == 0:
            return False, 0, 0

        # Closest point on segment to ball
        t = max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / line_len_sq))
        nearest_x = x1 + t * dx
        nearest_y = y1 + t * dy

        dist = math.hypot(px - nearest_x, py - nearest_y)
        if dist <= self.radius:
            # Normal vector (from line to ball center)
            nx = px - nearest_x
            ny = py - nearest_y
            mag = math.hypot(nx, ny)
            if mag == 0:
                return True, 0, -1  # Fallback
            return True, nx / mag, ny / mag
        return False, 0, 0

    def _resolve_collision(self, nx, ny):
        # Velocity dot normal
        dot = self.vx * nx + self.vy * ny

        # Reflect the velocity across the surface normal
        self.vx -= 2 * dot * nx
        self.vy -= 2 * dot * ny

        # Coefficient of restitution (bounciness)
        if self.mode == "rubber":
            restitution = 0.4
            friction = 0.85
        else:  # steel
            restitution = 0.1
            friction = 0.95

        # Apply energy loss
        self.vx *= friction
        self.vy *= restitution

        # Kill small velocities to avoid jitter
        if abs(self.vx) < 0.05:
            self.vx = 0
        if abs(self.vy) < 0.05:
            self.vy = 0

        # Push ball slightly out of the surface
        self.x += nx * (self.radius * 1.01)
        self.y += ny * (self.radius * 1.01)

    def draw(self, surface):
        color = RED if self.mode == "rubber" else BLUE
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.radius)


# Variables
ball = Ball()
lines = []
current_line = []

# Main loop
running = True
while running:
    screen.fill(WHITE)
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ball.released = True
            elif event.key == pygame.K_s:
                ball.mode = "steel"
            elif event.key == pygame.K_r:
                ball.mode = "rubber"

        elif event.type == pygame.MOUSEBUTTONDOWN and not ball.released:
            current_line = [event.pos]

        elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0] and not ball.released:
            current_line.append(event.pos)

        elif event.type == pygame.MOUSEBUTTONUP and not ball.released:
            if len(current_line) > 1:
                for i in range(len(current_line) - 1):
                    lines.append((current_line[i], current_line[i + 1]))
            current_line = []

    for line in lines:
        pygame.draw.line(screen, BLACK, line[0], line[1], 10)
    if len(current_line) > 1:
        for i in range(len(current_line) - 1):
            pygame.draw.line(screen, BLACK, current_line[i], current_line[i + 1], 10)

    ball.update(lines)
    ball.draw(screen)

    pygame.display.flip()
print(lines)
pygame.quit()
sys.exit()
