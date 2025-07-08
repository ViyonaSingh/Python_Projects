import pygame
import random

pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Infinity Hopper")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
SKY = (135, 206, 235)
GREEN = (50, 205, 50)
RED = (255, 60, 60)
BLACK = (20, 20, 20)

# Player setup
player = pygame.Rect(100, HEIGHT - 150, 40, 40)
vel_y = 0
gravity = 1
jump_strength = 18
on_ground = False

# Platform list
platforms = []
spikes = []
world_shift = 0
platform_gap = 200
last_platform_x = 0

# Font
font = pygame.font.SysFont("None", 32)
big_font = pygame.font.SysFont("None", 48)

# Score
distance_travelled = 0
game_over = False


def create_platform(x):
    height_variation = random.randint(50, 150)
    p_height = HEIGHT - height_variation
    width = random.randint(100, 150)
    platform = pygame.Rect(x, p_height, width, 20)
    platforms.append(platform)

    # Randomly place spikes
    if random.random() < 0.3:
        spike = pygame.Rect(x + random.randint(10, width - 30), p_height - 20, 20, 20)
        spikes.append(spike)


# Generate initial platforms
for i in range(6):
    create_platform(last_platform_x)
    last_platform_x += platform_gap


def reset_game():
    global platforms, spikes, last_platform_x, world_shift, distance_travelled, game_over
    player.x = 100
    player.y = HEIGHT - 150
    platforms = []
    spikes = []
    world_shift = 0
    distance_travelled = 0
    last_platform_x = 0
    game_over = False
    for iii in range(6):
        create_platform(last_platform_x)
        last_platform_x += platform_gap


# Game loop
running = True
while running:
    screen.fill(SKY)
    clock.tick(60)

    if game_over:
        text = big_font.render("Game Over! Press R to Restart", True, RED)
        screen.blit(text, (WIDTH // 2 - 200, HEIGHT // 2))
        pygame.display.flip()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            reset_game()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        continue

    # Input handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    dx = 0
    if keys[pygame.K_LEFT]:
        dx = -6
    if keys[pygame.K_RIGHT]:
        dx = 6

    if keys[pygame.K_UP] and on_ground:
        vel_y = -jump_strength

    # Gravity
    vel_y += gravity
    if vel_y > 10:
        vel_y = 10
    player.y += vel_y

    # Move player and scroll world
    player.x += dx
    if player.x > WIDTH // 2:
        scroll = player.x - WIDTH // 2
        player.x = WIDTH // 2
        world_shift -= scroll
        distance_travelled += scroll

        for p in platforms:
            p.x -= scroll
        for s in spikes:
            s.x -= scroll
        last_platform_x -= scroll

    # Generate new platforms
    while last_platform_x < WIDTH + 400:
        create_platform(last_platform_x)
        last_platform_x += platform_gap

    # Platform collision
    on_ground = False
    for p in platforms:
        if player.colliderect(p) and vel_y >= 0:
            if player.bottom <= p.top + 15:
                player.bottom = p.top
                vel_y = 0
                on_ground = True

    # Spike collision
    for s in spikes:
        if player.colliderect(s):
            game_over = True

    # Fall off the screen
    if player.y > HEIGHT:
        game_over = True

    # Draw platforms
    for p in platforms:
        pygame.draw.rect(screen, GREEN, p)

    # Draw spikes
    for s in spikes:
        pygame.draw.polygon(screen, RED, [
            (s.x, s.y + s.height),
            (s.x + s.width // 2, s.y),
            (s.x + s.width, s.y + s.height),
        ])

    # Draw player
    pygame.draw.rect(screen, BLACK, player)

    # Score
    score = font.render(f"Distance: {distance_travelled // 10}", True, BLACK)
    screen.blit(score, (20, 20))

    pygame.display.flip()
