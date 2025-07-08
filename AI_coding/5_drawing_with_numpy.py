import pygame
import numpy as np
import os

pygame.init()

# Settings
GRID_SIZE = 20
PIXEL_SIZE = 20
SCREEN_SIZE = GRID_SIZE * PIXEL_SIZE
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Draw (press S to save, C to clear)")

# Load or create dataset
if os.path.exists("5_drawings.npy"):
    dataset = list(np.load("5_drawings.npy", allow_pickle=True))
else:
    dataset = []

drawing = np.zeros((GRID_SIZE, GRID_SIZE), dtype=np.uint8)

running = True
while running:
    screen.fill((255, 255, 255))

    # Draw grid lines
    for x in range(0, SCREEN_SIZE, PIXEL_SIZE):
        pygame.draw.line(screen, (200, 200, 200), (x, 0), (x, SCREEN_SIZE))
    for y in range(0, SCREEN_SIZE, PIXEL_SIZE):
        pygame.draw.line(screen, (200, 200, 200), (0, y), (SCREEN_SIZE, y))

    # Draw filled pixels
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if drawing[y][x]:
                rect = pygame.Rect(x * PIXEL_SIZE, y * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE)
                pygame.draw.rect(screen, (0, 0, 0), rect)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Draw with left mouse button
        if pygame.mouse.get_pressed()[0]:
            mx, my = pygame.mouse.get_pos()
            gx, gy = mx // PIXEL_SIZE, my // PIXEL_SIZE
            if 0 <= gx < GRID_SIZE and 0 <= gy < GRID_SIZE:
                drawing[gy][gx] = 1

        # Erase with right mouse button
        if pygame.mouse.get_pressed()[2]:
            mx, my = pygame.mouse.get_pos()
            gx, gy = mx // PIXEL_SIZE, my // PIXEL_SIZE
            if 0 <= gx < GRID_SIZE and 0 <= gy < GRID_SIZE:
                drawing[gy][gx] = 0

        # Keyboard events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                dataset.append(drawing.copy())
                np.save("5_drawings.npy", np.array(dataset))
                print(f"Saved drawing #{len(dataset)}")
                drawing = np.zeros((GRID_SIZE, GRID_SIZE), dtype=np.uint8)

            if event.key == pygame.K_c:
                drawing = np.zeros((GRID_SIZE, GRID_SIZE), dtype=np.uint8)

    pygame.display.flip()

pygame.quit()
