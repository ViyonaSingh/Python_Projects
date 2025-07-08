import pygame
import numpy as np
import csv
import os

# Config
GRID_SIZE = 20
PIXEL_SIZE = 20  # for visible scaling
SCREEN_SIZE = GRID_SIZE * PIXEL_SIZE
BG_COLOR = (255, 255, 255)
DRAW_COLOR = (0, 0, 0)
DATA_FILE = "2_drawings_dataset.csv"

# Initialize
pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Draw and Label")
clock = pygame.time.Clock()

# Drawing grid
grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)


def draw_grid():
    screen.fill(BG_COLOR)
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if grid[y, x] == 1:
                rect = pygame.Rect(x * PIXEL_SIZE, y * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE)
                pygame.draw.rect(screen, DRAW_COLOR, rect)
    pygame.display.flip()


def save_drawing(label):
    flat_pixels = grid.flatten()
    row = list(flat_pixels) + [label]
    file_exists = os.path.exists(DATA_FILE)
    with open(DATA_FILE, mode="a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow([f"pixel_{i}" for i in range(GRID_SIZE * GRID_SIZE)] + ["label"])
        writer.writerow(row)
    print(f"Saved drawing as '{label}'")


def reset_grid():
    global grid
    grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)


# Main loop
running = True
drawing = False
while running:
    draw_grid()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif pygame.mouse.get_pressed()[0]:  # Draw with left mouse button
            x, y = pygame.mouse.get_pos()
            grid_y = y // PIXEL_SIZE
            grid_x = x // PIXEL_SIZE
            if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                grid[grid_y, grid_x] = 1

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                label = input("Label for this drawing: ")
                save_drawing(label)
                reset_grid()
            elif event.key == pygame.K_BACKSPACE:
                reset_grid()
                print("Cleared grid")

    pass

pygame.quit()
