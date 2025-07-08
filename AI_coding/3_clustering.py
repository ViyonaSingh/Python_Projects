import pygame
import numpy as np
from sklearn.cluster import KMeans

# Settings
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
CLUSTERS = 4
PALETTE_HEIGHT = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Draw & Cluster Colors")
clock = pygame.time.Clock()

# Drawing canvas
canvas = pygame.Surface((WIDTH, HEIGHT - PALETTE_HEIGHT))
canvas.fill((255, 255, 255))  # Start with white background

# Initial brush
brush_color = (0, 0, 0)
brush_size = 8

# Color map for number keys
colors = {
    pygame.K_1: (0, 0, 0),  # Black
    pygame.K_2: (255, 0, 0),  # Red
    pygame.K_3: (0, 255, 0),  # Green
    pygame.K_4: (0, 0, 255),  # Blue
    pygame.K_5: (255, 255, 0),  # Yellow
    pygame.K_6: (255, 165, 0),  # Orange
    pygame.K_7: (255, 192, 203),  # Pink
    pygame.K_8: (128, 0, 128),  # Purple
    pygame.K_9: (255, 255, 255),  # White (eraser)
}


def downsample_surface(surface):
    small = pygame.transform.smoothscale(surface, (GRID_SIZE, GRID_SIZE))
    pixel_array = pygame.surfarray.array3d(small)
    flat_pixels = pixel_array.reshape(-1, 3)
    # Filter out almost-white pixels
    filtered = flat_pixels[~np.all(flat_pixels > 240, axis=1)]
    return filtered


def cluster_colors(pixels, n_clusters=CLUSTERS):
    if len(pixels) < n_clusters:
        return [(200, 200, 200)] * n_clusters
    model = KMeans(n_clusters=n_clusters, n_init='auto')
    model.fit(pixels)
    return model.cluster_centers_.astype(int)


def show_palette(colors):
    block_width = WIDTH // len(colors)
    for i, color in enumerate(colors):
        pygame.draw.rect(screen, color, (i * block_width, HEIGHT - PALETTE_HEIGHT, block_width, PALETTE_HEIGHT))


def draw_ui():
    font = pygame.font.SysFont("None", 24)
    text = font.render("This is the utilized palette", True,
                       (0, 0, 0))
    screen.blit(text, (10, HEIGHT - PALETTE_HEIGHT + 10))


running = True
while running:
    screen.blit(canvas, (0, 0))  # Show current canvas

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    for key in colors:
        if keys[key]:
            brush_color = colors[key]

    mouse = pygame.mouse.get_pressed()
    if mouse[0]:  # Left-click
        mx, my = pygame.mouse.get_pos()
        if my < HEIGHT - PALETTE_HEIGHT:
            pygame.draw.circle(canvas, brush_color, (mx, my), brush_size)

    if keys[pygame.K_SPACE]:
        pixels = downsample_surface(canvas)
        palette = cluster_colors(pixels)
        show_palette(palette)

    draw_ui()
    # Draw current brush color in corner
    pygame.draw.rect(screen, brush_color, (WIDTH - 40, HEIGHT - PALETTE_HEIGHT + 10, 30, 30))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
