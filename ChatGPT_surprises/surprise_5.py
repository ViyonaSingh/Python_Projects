import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ERASER_SIZE = 20

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drawing App")
clock = pygame.time.Clock()

# Set up the drawing surface
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)

# Drawing variables
drawing = False
last_pos = None
current_color = BLACK
brush_size = 5

# Main loop
running = True
while running:
    screen.fill(WHITE)  # Fill the screen with white

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click to start drawing
                drawing = True
                last_pos = event.pos
            elif event.button == 3:  # Right click to use the eraser
                drawing = True
                current_color = WHITE
                last_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False
        elif event.type == pygame.MOUSEMOTION:
            if drawing:
                if current_color == WHITE:  # If using eraser, erase instead of draw
                    pygame.draw.circle(canvas, WHITE, event.pos, ERASER_SIZE)
                else:
                    pygame.draw.line(canvas, current_color, last_pos, event.pos, brush_size)
                last_pos = event.pos

    # Update the display with the canvas
    screen.blit(canvas, (0, 0))

    # Color selection buttons
    pygame.draw.rect(screen, RED, (10, 10, 50, 50))
    pygame.draw.rect(screen, GREEN, (70, 10, 50, 50))
    pygame.draw.rect(screen, BLUE, (130, 10, 50, 50))
    pygame.draw.rect(screen, YELLOW, (190, 10, 50, 50))

    # Switch colors on button press
    mouse_pos = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0]:
        if 10 <= mouse_pos[0] <= 60 and 10 <= mouse_pos[1] <= 60:
            current_color = RED
        elif 70 <= mouse_pos[0] <= 120 and 10 <= mouse_pos[1] <= 60:
            current_color = GREEN
        elif 130 <= mouse_pos[0] <= 180 and 10 <= mouse_pos[1] <= 60:
            current_color = BLUE
        elif 190 <= mouse_pos[0] <= 240 and 10 <= mouse_pos[1] <= 60:
            current_color = YELLOW

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
