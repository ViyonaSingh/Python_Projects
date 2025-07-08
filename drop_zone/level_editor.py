import pygame
import json
import os

pygame.init()
screen = pygame.display.set_mode((1000, 700))
clock = pygame.time.Clock()

pen_types = ['normal', 'slippery', 'magnetic', 'slime', 'bounce']
current_pen = 'normal'
lines = []
target = None
placing_target = False

# Colors
blue = (15, 82, 186)
pastel_blue = (211, 237, 250)
turquoise = (64, 224, 208)
dark_blue = (0, 0, 128)

WIDTH, HEIGHT = 1000, 700
pygame.display.set_caption("Level Editor")
screen.fill(pastel_blue)
pygame.draw.rect(screen, blue, (0, 0, WIDTH, HEIGHT), 10)


drawing = False
start_pos = None
level = 1
font = pygame.font.SysFont("None", 24)

# Trash button
TRASH_RECT = pygame.Rect(WIDTH - 80, 20, 50, 30)


def load_level(level_number):
    global lines, target
    lines = []
    target = None
    if os.path.exists("levels.json"):
        with open("levels.json", 'r') as f:
            all_levels = json.load(f)
            level_data = all_levels.get(str(level_number), {})
            lines = level_data.get("lines", [])
            target_data = level_data.get("target")
            target = tuple(map(int, target_data)) if target_data is not None else None
        print(f"Level {level_number} loaded!")
    else:
        print("No levels file found, starting fresh.")


def save_level():
    data = {
        "lines": lines,
        "target": list(target) if target else None
    }

    if os.path.exists("levels.json"):
        with open("levels.json", 'r') as f:
            all_levels = json.load(f)
    else:
        all_levels = {}

    all_levels[str(level)] = data
    with open("levels.json", 'w') as f:
        json.dump(all_levels, f, indent=4)
    print(f"Level {level} saved!")


def draw_text(text, x, y):
    surface = font.render(text, True, dark_blue)
    screen.blit(surface, (x, y))


def draw_trash_button():
    pygame.draw.rect(screen, turquoise, TRASH_RECT)
    draw_text("Trash", TRASH_RECT.x + 4, TRASH_RECT.y + 6)


running = True
load_level(level)

while running:
    screen.fill(pastel_blue)
    pygame.draw.rect(screen, blue, (0, 0, WIDTH, HEIGHT), 10)
    draw_text(f"Pen Type: {current_pen}", 30, 20)
    draw_text("Press 1-5 to switch pen | S to save | Arrow keys to switch levels", 30, 50)
    draw_text("Press T to place target", 30, 80)
    draw_text(f"Level: {level}", 30, 110)
    draw_trash_button()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                current_pen = pen_types[0]
            elif event.key == pygame.K_2:
                current_pen = pen_types[1]
            elif event.key == pygame.K_3:
                current_pen = pen_types[2]
            elif event.key == pygame.K_4:
                current_pen = pen_types[3]
            elif event.key == pygame.K_5:
                current_pen = pen_types[4]
            elif event.key == pygame.K_s:
                save_level()
            elif event.key == pygame.K_t:
                placing_target = True
            elif event.key == pygame.K_RIGHT:
                level += 1
                load_level(level)
            elif event.key == pygame.K_LEFT:
                if level > 1:
                    level -= 1
                    load_level(level)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if TRASH_RECT.collidepoint(event.pos):
                    lines.clear()
                    target = None
                    print(f"Cleared lines for level {level}")
                elif placing_target:
                    target = event.pos
                    placing_target = False
                else:
                    drawing = True
                    start_pos = event.pos

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing:
                end_pos = event.pos
                lines.append({
                    "start": start_pos,
                    "end": end_pos,
                    "type": current_pen
                })
                drawing = False

    for line in lines:
        color = {
            'normal': (0, 0, 0),
            'slippery': (0, 255, 255),
            'magnetic': (255, 0, 0),
            'slime': (0, 255, 0),
            'bounce': (255, 0, 255)
        }[line['type']]
        pygame.draw.line(screen, color,
                         tuple(map(int, line['start'])),
                         tuple(map(int, line['end'])),
                         10)

    if target:
        pygame.draw.circle(screen, (255, 0, 0), target, 15)
        pygame.draw.circle(screen, pastel_blue, target, 10)

    if drawing and start_pos:
        pygame.draw.line(screen, (200, 200, 200), start_pos, pygame.mouse.get_pos(), 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
