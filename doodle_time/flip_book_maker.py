import pygame
import json
import os

pygame.init()
screen = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("Flip A Clip 🎨")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)

# Easter Pastel Colors + More Colors
PASTEL_PINK = (255, 182, 193)
PASTEL_YELLOW = (255, 255, 186)
PASTEL_BLUE = (173, 216, 230)
PASTEL_GREEN = (144, 238, 144)
PASTEL_PURPLE = (230, 230, 250)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ERASER = WHITE
LIGHT_ORANGE = (255, 204, 153)
DARK_ORANGE = (255, 140, 0)
LIGHT_BLUE = (173, 206, 250)
TURQUOISE = (64, 224, 208)
LIGHT_GREEN = (144, 238, 144)
PINK = (255, 105, 180)
VIOLET = (238, 130, 238)
TAN = (210, 180, 140)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREY = (100, 100, 100)

# State
current_color = BLACK
pen_size = 10
drawing = False
canvas_rect = pygame.Rect(60, 50, 700, 600)  # Slightly smaller canvas

# Frame data
lines = []
frame = 1
all_frames = {}
playing = False
play_fps = 5
play_timer = 0

# Show previous strokes flag
show_previous_strokes = False


def load_all_frames():
    global all_frames
    if os.path.exists("all_frames.json"):
        with open("all_frames.json", "r") as f:
            try:
                raw_data = json.load(f)
                all_frames = {
                    int(k): [(tuple(stroke_pos), tuple(stroke_color), stroke_size) for stroke_pos, stroke_color, stroke_size in v]
                    for k, v in raw_data.items()
                }
            except Exception as e:
                print("Error loading:", e)
                all_frames = {}


def save_all_frames():
    all_frames[frame] = lines
    with open("all_frames.json", "w") as f:
        json.dump({str(k): v for k, v in all_frames.items()}, f)


def load_frame(n):
    global lines
    lines = all_frames.get(n, [])


color_buttons = []  # List of (rect, color) pairs


def draw_palette():
    global color_buttons
    color_buttons = []

    colors = [
        (BLACK, ""), (LIGHT_BLUE, ""), (PASTEL_PINK, ""),
        (PASTEL_GREEN, ""), (PASTEL_PURPLE, ""), (LIGHT_ORANGE, ""),
        (DARK_ORANGE, ""), (TURQUOISE, ""), (LIGHT_GREEN, ""),
        (PINK, ""), (VIOLET, ""), (TAN, ""), (BLUE, ""), (RED, ""), (ERASER, "")
    ]

    x, y = 850, 100
    cols = 3
    for idx, (pen_color, name) in enumerate(colors):
        row = idx // cols
        col = idx % cols
        color_rect = pygame.Rect(x + col * 40, y + row * 40, 30, 30)
        pygame.draw.rect(screen, pen_color, color_rect, border_radius=5)
        color_buttons.append((color_rect, pen_color))  # Save rect and color


def draw_ui():
    # Easter background and decorations
    screen.fill(PASTEL_YELLOW)
    pygame.draw.rect(screen, PASTEL_BLUE, (830, 0, 170, 700))  # Right panel
    pygame.draw.rect(screen, WHITE, canvas_rect)  # Drawing area
    pygame.draw.rect(screen, WHITE, canvas_rect, 30)

    # Info at the top
    draw_text(f"Frame: {frame}", 850, 20)
    draw_text(f"FPS: {play_fps}", 850, 50)

    # Play button
    pygame.draw.rect(screen, PASTEL_PINK, (850, 620, 120, 40), border_radius=10)
    label = "Play" if not playing else "Pause"
    play_text = font.render(f"{label} ", True, (0, 0, 0))
    screen.blit(play_text, (860, 630))

    # Pen Size Control
    draw_text("Pen Size:", 850, 550)
    pygame.draw.rect(screen, PASTEL_GREEN, (850, 580, 30, 30), border_radius=5)
    pygame.draw.rect(screen, PASTEL_GREEN, (890, 580, 30, 30), border_radius=5)
    draw_text("-", 860, 585)
    draw_text("+", 900, 585)
    draw_text(str(pen_size), 935, 585)

    # Draw the color palette grid
    draw_palette()


def draw_text(text, x, y):
    screen.blit(font.render(text, True, (0, 0, 0)), (x, y))


def draw_previous_frame_strokes():
    if show_previous_strokes and frame > 1:
        # Draw strokes from previous frames
        for f in range(frame):
            for pen_pos, pen_color, p_size in all_frames.get(f, []):
                pygame.draw.circle(screen, GREY, pen_pos, p_size)


load_all_frames()
load_frame(frame)

running = True
while running:
    dt = clock.tick(60)

    # Draw the UI and Easter bunny
    draw_ui()

    # Draw previous frame strokes if toggled
    draw_previous_frame_strokes()

    # Draw the strokes for the current frame
    for pos, color, size in lines:
        pygame.draw.circle(screen, color, pos, size)

    # Animation playback
    if playing:
        play_timer += dt
        if play_timer > 1000 // play_fps:
            play_timer = 0
            frame += 1
            if frame not in all_frames:
                frame = min(all_frames.keys()) if all_frames else 1
            load_frame(frame)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                save_all_frames()

            # change frame
            elif event.key == pygame.K_RIGHT:
                if not playing:
                    frame += 1
                    load_frame(frame)
            elif event.key == pygame.K_LEFT:
                if not playing and frame > 1:
                    frame -= 1
                    load_frame(frame)
            # change fps
            elif event.key == pygame.K_PLUS:
                play_fps += 1
            elif event.key == pygame.K_MINUS:
                play_fps = max(1, play_fps - 1)
            # toggle the previous strokes visibility
            elif event.key == pygame.K_a:
                show_previous_strokes = not show_previous_strokes

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            # Check palette color buttons
            for rect, color in color_buttons:
                if rect.collidepoint(mx, my):
                    current_color = color
                    break

            # Play button
            if 850 <= mx <= 970 and 620 <= my <= 660:
                playing = not playing
                play_timer = 0
                if playing:
                    frame = min(all_frames.keys()) if all_frames else 1
                    load_frame(frame)

            # Pen size
            elif 850 <= mx <= 880 and 580 <= my <= 610:
                pen_size = max(2, pen_size - 1)
            elif 890 <= mx <= 920 and 580 <= my <= 610:
                pen_size = min(30, pen_size + 1)

            # 🖌️ Start drawing
            elif canvas_rect.collidepoint(mx, my):
                drawing = True
                lines.append((event.pos, current_color, pen_size))

        elif event.type == pygame.MOUSEMOTION and drawing:
            if canvas_rect.collidepoint(pygame.mouse.get_pos()):
                lines.append((pygame.mouse.get_pos(), current_color, pen_size))

        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False

    pygame.display.flip()

pygame.quit()
