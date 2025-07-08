import json
import pygame
import math
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1000, 700
WHITE = (255, 255, 255)
# Colors
blue = (15, 82, 186)
pastel_blue = (211, 237, 250)
turquoise = (64, 224, 208)
dark_blue = (0, 0, 128)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
DARK_GREEN = (0, 100, 0)
FPS = 60
GRAVITY = 0.4

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Drawing Physics")
clock = pygame.time.Clock()

# Progress file
SAVE_FILE = "progress.json"


def save_progress(level):
    with open(SAVE_FILE, 'w') as f:
        json.dump({"level": level}, f)


def load_progress():
    try:
        with open(SAVE_FILE) as f:
            return json.load(f).get("level", 1)
    except:
        return 1


def load_level(level_number):
    with open("levels.json", "r") as f:
        levels = json.load(f)

    level_data = levels.get(str(level_number), {})
    lines = []
    slippery_lines = []
    magnet_lines = []
    slime_lines = []
    bounce_lines = []

    for line in level_data.get("lines", []):
        start = tuple(line["start"])
        end = tuple(line["end"])
        line_type = line.get("type", "normal")  # Default to normal if missing

        if line_type == "normal":
            lines.append((start, end))
        elif line_type == "slippery":
            slippery_lines.append((start, end))
        elif line_type == "magnetic":
            magnet_lines.append((start, end))
        elif line_type == "slime":
            slime_lines.append((start, end))
        elif line_type == "bounce":
            bounce_lines.append((start, end))

    target = level_data.get("target")
    print(f" Loaded level {level_number} with:")
    print(f"  - {len(lines)} normal lines")
    print(f"  - {len(slippery_lines)} slippery lines")
    print(f"  - {len(magnet_lines)} magnet lines")
    print(f"  - {len(slime_lines)} slime lines")
    print(f"  - {len(bounce_lines)} bounce lines")

    return lines, slippery_lines, magnet_lines, slime_lines, bounce_lines, target


class Ball:
    def __init__(self):
        self.radius = 10
        self.x = 50
        self.y = 80
        self.vx = 0
        self.vy = 0
        self.released = False
        self.mode = "rubber"

    def reset(self):
        self.__init__()

    def update(self, p_lines, p_slippery_lines, p_magnet_lines, p_slime_lines, p_bounce_lines):
        if self.released:
            self.vy += GRAVITY if self.mode == "rubber" else GRAVITY * 0.5

            steps = 1

            dx = self.vx / steps
            dy = self.vy / steps

            for iii in range(steps):
                self.x += dx
                self.y += dy

                for line in p_lines:
                    (x1, y1), (x2, y2) = line
                    collision, nx, ny = self._check_collision(x1, y1, x2, y2)
                    if collision:
                        self._resolve_collision(nx, ny, "normal")
                for line in p_slippery_lines:
                    (x1, y1), (x2, y2) = line
                    collision, nx, ny = self._check_collision(x1, y1, x2, y2)
                    if collision:
                        self._resolve_collision(nx, ny, "slippery")
                for line in p_magnet_lines:
                    (x1, y1), (x2, y2) = line
                    collision, nx, ny = self._check_collision(x1, y1, x2, y2)
                    if collision:
                        self._resolve_collision(nx, ny, "magnetic")
                for line in p_slime_lines:
                    (x1, y1), (x2, y2) = line
                    collision, nx, ny = self._check_collision(x1, y1, x2, y2)
                    if collision:
                        self._resolve_collision(nx, ny, "slime")
                for line in p_bounce_lines:
                    (x1, y1), (x2, y2) = line
                    collision, nx, ny = self._check_collision(x1, y1, x2, y2)
                    if collision:
                        self._resolve_collision(nx, ny, "bounce")

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

    def _resolve_collision(self, nx, ny, line_type):
        # Velocity dot normal
        dot = self.vx * nx + self.vy * ny

        # Reflect the velocity across the surface normal
        self.vx -= 2 * dot * nx
        self.vy -= 2 * dot * ny

        # Coefficient of restitution (bounciness)
        if self.mode == "rubber":
            restitution = 0.3
            friction = 0.85
        else:  # steel
            restitution = 0.05
            friction = 0.95

        # Line reactions
        if line_type == "slippery":
            friction = 0.99
        elif line_type == "magnetic":
            self.vx += -nx * 1.5
            self.vy += -ny * 1.5
        elif line_type == "slime":
            friction = 0.05
            restitution = 0
        elif line_type == "bounce":
            restitution = 0.9

        # Apply energy loss
        self.vx *= friction
        self.vy *= restitution

        # Kill small velocities to avoid jitter
        if abs(self.vx) < 0.05:
            self.vx = 0
        if abs(self.vy) < 0.05:
            self.vy = 0

        # Push ball slightly out of the surface
        self.x += nx * (self.radius * 1.00001)
        self.y += ny * (self.radius * 1.00001)

    def draw(self, surface):
        color = RED if self.mode == "rubber" else BLUE
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.radius)


def check_target_hit(ball, target):
    if not target:
        return False
    tx, ty = target
    return math.hypot(ball.x - tx, ball.y - ty) < 20


def get_total_levels():
    try:
        with open("levels.json") as f:
            all_levels = json.load(f)
            return len(all_levels)
    except Exception as e:
        print(f" Failed to load levels: {e}")
        return 0


def draw_lines():
    for line in lines:
        pygame.draw.line(screen, (0, 0, 0), line[0], line[1], 5)  # normal = black
    for line in slippery_lines:
        pygame.draw.line(screen, (0, 255, 255), line[0], line[1], 5)  # slippery = cyan

    for line in magnet_lines:
        pygame.draw.line(screen, (255, 0, 0), line[0], line[1], 5)  # magnet = red

    for line in slime_lines:
        pygame.draw.line(screen, (0, 255, 0), line[0], line[1], 5)  # slime = green

    for line in bounce_lines:
        pygame.draw.line(screen, (255, 0, 255), line[0], line[1], 5)  # bounce = purple


LEVELS_TOTAL = get_total_levels()

# Game state
current_level = load_progress()
lines, slippery_lines, magnet_lines, slime_lines, bounce_lines, target = load_level(current_level)
ball = Ball()
current_line = []
transitioning = False
transition_alpha = 0

# Main loop
running = True
while running:
    screen.fill(pastel_blue)
    pygame.draw.rect(screen, blue, (0, 0, WIDTH, HEIGHT), 10)
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ball.released = True
            elif event.key == pygame.K_r:
                ball = Ball()
                lines, slippery_lines, magnet_lines, slime_lines, bounce_lines, target = load_level(current_level)
            elif event.key == pygame.K_c:
                ball.mode = "rubber" if ball.mode != "rubber" else "steel"  # "steel" as placeholder

        elif event.type == pygame.MOUSEBUTTONDOWN and not ball.released:
            current_line = [event.pos]

        elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0] and not ball.released:
            current_line.append(event.pos)

        elif event.type == pygame.MOUSEBUTTONUP and not ball.released:
            if len(current_line) > 1:
                for i in range(len(current_line) - 1):
                    lines.append((current_line[i], current_line[i + 1]))
            current_line = []

    draw_lines()
    if len(current_line) > 1:
        for i in range(len(current_line) - 1):
            pygame.draw.line(screen, BLACK, current_line[i], current_line[i + 1], 4)

    ball.update(lines, slippery_lines, magnet_lines, slime_lines, bounce_lines)
    ball.draw(screen)

    if target:
        pygame.draw.circle(screen, DARK_GREEN, target, 12)

    if check_target_hit(ball, target) and not transitioning:
        transitioning = True
        transition_alpha = 0

    if transitioning:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(transition_alpha)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        transition_alpha += 5
        if transition_alpha >= 255:
            current_level += 1
            if current_level > LEVELS_TOTAL:
                font = pygame.font.Font(None, 72)
                win_text = font.render("You Won! All levels completed", True, (0, 255, 0))
                screen.blit(win_text,
                            (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - win_text.get_height() // 2))
                pygame.display.flip()
                pygame.time.wait(2000)
                running = False
            else:
                save_progress(current_level)
                lines, slippery_lines, magnet_lines, slime_lines, bounce_lines, target = load_level(current_level)
                ball = Ball()
                transitioning = False

    font = pygame.font.Font(None, 36)
    text = font.render(f"Level: {current_level}", True, (0, 0, 0))
    screen.blit(text, (WIDTH - 110, 20))

    progress = int((current_level - 1) / max(1, LEVELS_TOTAL) * 100)
    progress_text = font.render(f"Progress: {progress} %", True, (0, 0, 0))
    screen.blit(progress_text, (20, 20))

    pygame.display.flip()

pygame.quit()
sys.exit()
