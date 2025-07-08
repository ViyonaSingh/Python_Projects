import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()

# Ball properties
x, y = 300, 50
radius = 20
velocity_y = 0
gravity = 0.5
bounce_strength = -12

while True:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Gravity and bounce
    velocity_y += gravity
    y += velocity_y
    if y + radius > 400:
        y = 400 - radius
        velocity_y = bounce_strength

    pygame.draw.circle(screen, (255, 0, 0), (int(x), int(y)), radius)
    pygame.display.flip()
    clock.tick(60)
