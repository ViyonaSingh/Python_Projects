import pygame
from pygame.locals import *
from shapes import Rectangle, Circle, Triangle

# Initialising
pygame.init()

# Fenstergröße & Zellen
WIDTH, HEIGHT = 700, 700
CELL_WIDTH = WIDTH / 10
GRID_COLOR = (230, 230, 230)
WHITE = (255, 255, 255)
LIGHTBLUE = (5, 213, 250)
PURPLE = (205, 110, 255)
BLUE = (50, 50, 255)
BLACK = (0, 0, 0)
PURPLE_BAR_HEIGHT = 100

# Farben zum Durchwechseln
AVAILABLE_COLORS = [BLUE, PURPLE, BLACK, LIGHTBLUE]

# Fenster und Schriftarten
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Word by Viyona')
font_small = pygame.font.SysFont('freesansbold.ttf', 30)
font_medium = pygame.font.SysFont('freesansbold.ttf', 50)
font_large = pygame.font.SysFont('freesansbold.ttf', 70)

# Zustand
shapes = []
current_color_index = 0
selected_shape = None
dragging = False
offset_x = offset_y = 0


def draw_ui():
    window.fill(WHITE)

    # Rasterlinien
    for i in range(1, int(HEIGHT / (CELL_WIDTH / 2))):
        y = i * (CELL_WIDTH / 2)
        pygame.draw.line(window, GRID_COLOR, (0, y), (WIDTH, y))
    for i in range(1, int(WIDTH / (CELL_WIDTH / 2))):
        x = i * (CELL_WIDTH / 2)
        pygame.draw.line(window, GRID_COLOR, (x, CELL_WIDTH), (x, HEIGHT))

    # Horizontale Linien oben
    pygame.draw.line(window, LIGHTBLUE, (0, CELL_WIDTH), (WIDTH, CELL_WIDTH))
    pygame.draw.line(window, LIGHTBLUE, (0, 0), (WIDTH, 0))
    for i in range(1, 10):
        pygame.draw.line(window, LIGHTBLUE, (i * CELL_WIDTH, 0), (i * CELL_WIDTH, CELL_WIDTH))

    # Steuerungsleiste unten
    pygame.draw.rect(window, PURPLE, pygame.Rect(0, HEIGHT - PURPLE_BAR_HEIGHT, WIDTH, PURPLE_BAR_HEIGHT))

    print_button('Rect', BLACK, 10, HEIGHT - 90, font_small, bg_color=LIGHTBLUE)
    print_button('Circle', BLACK, 120, HEIGHT - 90, font_small, bg_color=LIGHTBLUE)
    print_button('Triangle', BLACK, 230, HEIGHT - 90, font_small, bg_color=LIGHTBLUE)

    print_button('+', BLACK, 340, HEIGHT - 95, font_small, bg_color=(200, 255, 200), width=50, height=50)
    print_button('-', BLACK, 400, HEIGHT - 95, font_small, bg_color=(255, 200, 200), width=50, height=50)
    print_button('Color', BLACK, 460, HEIGHT - 90, font_small, bg_color=(255, 255, 180), width=100)


def print_button(text, text_color, x, y, font, bg_color=(255, 255, 255), width=100, height=40, radius=12):
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(window, bg_color, button_rect, border_radius=radius)
    pygame.draw.rect(window, BLACK, button_rect, 2, border_radius=radius)
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=button_rect.center)
    window.blit(text_surf, text_rect)


def draw_shapes():
    for shape in shapes:
        if isinstance(shape, Rectangle):
            pygame.draw.rect(window, shape.color, pygame.Rect(shape.x, shape.y, shape.width, shape.height))
        elif isinstance(shape, Circle):
            pygame.draw.circle(window, shape.color, (int(shape.x), int(shape.y)), int(shape.r))
        elif isinstance(shape, Triangle):
            pygame.draw.polygon(window, shape.color, [
                (shape.x1, shape.y1),
                (shape.x2, shape.y2),
                (shape.x3, shape.y3)
            ])


def cycle_color(shape):
    global current_color_index
    current_color_index = (current_color_index + 1) % len(AVAILABLE_COLORS)
    shape.color = AVAILABLE_COLORS[current_color_index]


def create_shape(form):
    if form == "rect":
        shape = Rectangle()
    elif form == "circle":
        shape = Circle()
    elif form == "triangle":
        shape = Triangle()
    else:
        return

    shape.color = BLUE
    shapes.append(shape)


def get_shape_at(x, y):
    for shape in reversed(shapes):
        if shape.covers(x, y):
            return shape
    return None


# Haupt-Loop
running = True
while running:
    draw_ui()
    draw_shapes()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        elif event.type == MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()

            if HEIGHT - PURPLE_BAR_HEIGHT <= y <= HEIGHT:
                if 10 < x < 110:  # Rechteck-Button
                    create_shape("rect")
                elif 120 < x < 220:  # Kreis-Button
                    create_shape("circle")
                elif 230 < x < 330:  # Dreieck-Button
                    create_shape("triangle")

                # Überprüfen, ob untere Steuerungsleiste
                elif y >= HEIGHT - PURPLE_BAR_HEIGHT:
                    if 340 < x < 390 and selected_shape:  # Resize + Button
                        selected_shape.resize(1.1)
                    elif 400 < x < 460 and selected_shape:  # Resize - Button
                        selected_shape.resize(0.9)
                    elif 460 < x < 560 and selected_shape:  # Color Button
                        cycle_color(selected_shape)

            else:
                # Falls in Form klicken
                selected = get_shape_at(x, y)
                if selected:
                    selected_shape = selected
                    dragging = True
                    if isinstance(selected, Triangle):
                        cx = (selected.x1 + selected.x2 + selected.x3) / 3
                        cy = (selected.y1 + selected.y2 + selected.y3) / 3
                    else:
                        cx, cy = selected.x, selected.y
                    offset_x = x - cx
                    offset_y = y - cy

        elif event.type == MOUSEBUTTONUP:
            dragging = False

        elif event.type == MOUSEMOTION and dragging and selected_shape:
            x, y = pygame.mouse.get_pos()
            if isinstance(selected_shape, Triangle):
                cx = (selected_shape.x1 + selected_shape.x2 + selected_shape.x3) / 3
                cy = (selected_shape.y1 + selected_shape.y2 + selected_shape.y3) / 3
                dx = x - offset_x - cx
                dy = y - offset_y - cy
                selected_shape.x1 += dx
                selected_shape.y1 += dy
                selected_shape.x2 += dx
                selected_shape.y2 += dy
                selected_shape.x3 += dx
                selected_shape.y3 += dy
            else:
                selected_shape.x = x - offset_x
                selected_shape.y = y - offset_y

        elif event.type == KEYDOWN and selected_shape:
            if event.key == K_UP:
                selected_shape.move("UP")
            elif event.key == K_DOWN:
                selected_shape.move("DOWN")
            elif event.key == K_LEFT:
                selected_shape.move("LEFT")
            elif event.key == K_RIGHT:
                selected_shape.move("RIGHT")

pygame.quit()
