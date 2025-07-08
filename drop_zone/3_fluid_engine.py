import pygame
import math
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1000, 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
FPS = 80
GRAVITY = 0.4

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drop Drawing Physics 💧")
clock = pygame.time.Clock()


class Drop:
    def __init__(self, start_x, start_y, radius=10):
        self.radius = radius
        self.x = start_x
        self.y = start_y
        self.vx = random.uniform(-1, 1)  # Slight random velocity
        self.vy = random.uniform(-1, 1)  # Slight random velocity
        self.released = False

    def update(self, lines):
        if not self.released:
            return

        # Apply gravity
        self.vy += GRAVITY

        steps = 8  # more sub steps = better accuracy
        for _ in range(steps):
            self.x += self.vx / steps
            self.y += self.vy / steps

            for line in lines:
                (x1, y1), (x2, y2) = line
                collision, nx, ny = self._check_collision(x1, y1, x2, y2)
                if collision:
                    # Get the nearest point on the line
                    t = max(0, min(1, ((self.x - x1) * (x2 - x1) + (self.y - y1) * (y2 - y1)) / ((x2 - x1)**2 + (y2 - y1)**2)))
                    nearest_x = x1 + t * (x2 - x1)
                    nearest_y = y1 + t * (y2 - y1)

                    # Resolve the collision with the nearest point and normal
                    self._resolve_collision(nx, ny, nearest_x, nearest_y)

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

    def _resolve_collision(self, nx, ny, nearest_x, nearest_y):
        # Correct position so the drop doesn't sink into the surface
        dx = self.x - nearest_x
        dy = self.y - nearest_y
        dist = math.hypot(dx, dy)
        penetration = self.radius - dist
        if dist != 0 and penetration > 0:
            self.x += (dx / dist) * (penetration + 0.1)
            self.y += (dy / dist) * (penetration + 0.1)

        # Project velocity onto the surface tangent to simulate rolling
        tangent_x = -ny
        tangent_y = nx

        # Velocity along the tangent
        tangent_speed = self.vx * tangent_x + self.vy * tangent_y

        # Set new velocity along the tangent only (no normal component)
        self.vx = tangent_speed * tangent_x
        self.vy = tangent_speed * tangent_y

        # Apply friction to slow it down
        friction = 0.98
        self.vx *= friction
        self.vy *= friction

        # Kill tiny velocities to prevent jitter
        if abs(self.vx) < 0.05:
            self.vx = 0
        if abs(self.vy) < 0.05:
            self.vy = 0

    def draw(self, surface):
        pygame.draw.circle(surface, (0, 150, 255), (self.x, self.y), self.radius)


# Variables
drops = []
lines = []
current_line = []

# Create multiple drops with slightly different starting positions
for i in range(50):
    drops.append(Drop(start_x=50 + i * 5, start_y=50))

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
                for drop in drops:
                    drop.released = True

        elif event.type == pygame.MOUSEBUTTONDOWN and not any(drop.released for drop in drops):
            current_line = [event.pos]

        elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0] and not any(drop.released for drop in drops):
            current_line.append(event.pos)

        elif event.type == pygame.MOUSEBUTTONUP and not any(drop.released for drop in drops):
            if len(current_line) > 1:
                for i in range(len(current_line) - 1):
                    lines.append((current_line[i], current_line[i + 1]))
            current_line = []

    for line in lines:
        pygame.draw.line(screen, BLACK, line[0], line[1], 10)
    if len(current_line) > 1:
        for i in range(len(current_line) - 1):
            pygame.draw.line(screen, BLACK, current_line[i], current_line[i + 1], 10)

    for drop in drops:
        drop.update(lines)
        drop.draw(screen)

    pygame.display.flip()
pygame.quit()
sys.exit()
