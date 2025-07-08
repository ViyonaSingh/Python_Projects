import pygame
import random
import sys

# Setup
pygame.init()
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Build the DNA Strand")
clock = pygame.time.Clock()
font = pygame.font.SysFont("None", 48)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BASE_COLORS = {'A': (255, 100, 100), 'T': (100, 205, 100), 'C': (100, 100, 255), 'G': (205, 205, 100)}

# Game variables
bases = ['A', 'T', 'C', 'G']
complements = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
falling_bases = []
spawn_timer = 0
score = 0
lives = 3

# DNA strand target
template_strand = random.choices(bases, k=5)
target_strand = [complements[base] for base in template_strand]
current_index = 0

# Player
player = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 60, 100, 20)
player_speed = 10


# Helper functions
def draw_text(text, x, y, color=WHITE, size=36):
    label = pygame.font.SysFont("None", size).render(text, True, color)
    screen.blit(label, (x, y))


def spawn_base():
    base = random.choice(bases)
    x = random.randint(0, WIDTH - 30)
    return {'rect': pygame.Rect(x, 0, 30, 30), 'base': base}


# Main loop
while True:
    screen.fill(BLACK)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Move player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player.x += player_speed
    player.x = max(0, min(WIDTH - player.width, player.x))

    # Spawn bases
    spawn_timer += 1
    if spawn_timer > 30:
        falling_bases.append(spawn_base())
        spawn_timer = 0

    # Update bases
    for base in falling_bases[:]:
        base['rect'].y += 5
        pygame.draw.rect(screen, BASE_COLORS[base['base']], base['rect'])
        draw_text(base['base'], base['rect'].x + 5, base['rect'].y)

        if base['rect'].colliderect(player):
            expected = target_strand[current_index]
            if base['base'] == expected:
                score += 1
                current_index += 1
                if current_index >= len(target_strand):
                    draw_text("You built the full DNA strand!", 50, HEIGHT // 2, (0, 255, 0), 42)
                    pygame.display.flip()
                    pygame.time.delay(3000)
                    pygame.quit()
                    sys.exit()
            else:
                lives -= 1
                if lives <= 0:
                    draw_text("Out of lives! Game Over!", 100, HEIGHT // 2, (255, 0, 0), 42)
                    pygame.display.flip()
                    pygame.time.delay(3000)
                    pygame.quit()
                    sys.exit()
            falling_bases.remove(base)
        elif base['rect'].y > HEIGHT:
            falling_bases.remove(base)

    # Draw player
    pygame.draw.rect(screen, (200, 200, 200), player)

    # UI
    draw_text(f"Template: {''.join(template_strand)}", 20, 20)
    draw_text(f"Build:     {''.join(target_strand)}", 20, 60)
    draw_text(f"Progress:  {''.join(target_strand[:current_index])}", 20, 100)
    draw_text(f"Lives: {lives}", WIDTH - 160, 20)
    draw_text(f"Score: {score}", WIDTH - 160, 60)

    pygame.display.flip()
    clock.tick(60)
