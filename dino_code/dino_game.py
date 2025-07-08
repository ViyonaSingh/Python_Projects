import pygame
import random
import time
from pygame import QUIT

# Farben, Größen
breite = 800
hoehe = 800
schwarz = (0, 0, 0)
weiss = (255, 255, 255)
gelb = (255, 243, 128)
blau = (100, 198, 198)
# Initialize
pygame.init()
pygame.display.set_caption('Dino internet game from Viyona')
pygame.display.init()
pygame.font.init()
# Schriften
duenn = pygame.font.Font('freesansbold.ttf', 25)
duenn_dick = pygame.font.SysFont('bahnenschrift.ttf', 50)
dick_duenn = pygame.font.SysFont('bahnenschrift.ttf', 75)
dick = pygame.font.SysFont('bahnenschrift.ttf', 100)
# Kakteen
cactus = pygame.image.load('dino_game_images/cactus.png')
two_cactus = (pygame.image.load('dino_game_images/cacti.png'))
cactus = pygame.transform.scale(cactus, (70, 75))
two_cactus = pygame.transform.scale(two_cactus, (70, 75))
cacti = [cactus, two_cactus]
# Fenster einstellen
fenster = pygame.display.set_mode((breite, hoehe))
# Dinos
green_dino = (pygame.image.load('dino_game_images/dino.png'))
green_dino = pygame.transform.scale(green_dino, (75, 80))
fire_dino = (pygame.image.load('dino_game_images/fire_dino.png'))
fire_dino = pygame.transform.scale(fire_dino, (75, 80))
hurt_dino = (pygame.image.load('dino_game_images/hurted_dino.png'))
hurt_dino = pygame.transform.scale(hurt_dino, (75, 80))
# Feuer
fire_ball = (pygame.image.load('dino_game_images/fire_ball.png'))
fire_ball = pygame.transform.scale(fire_ball, (25, 18))
# burned cactus
burned_cactus = (pygame.image.load('dino_game_images/burned_cactus.png'))
burned_cactus = pygame.transform.scale(burned_cactus, (50, 30))


# Paint a scene of the screen
def paint_screen(seconds_of_clock, cactus_type, cactus_x, dino_y, dino_type, fire_ball_running, fire_x, fire_y):
    # paint surface
    fenster.fill(weiss)
    # draw desert
    pygame.draw.rect(fenster, gelb, pygame.Rect(0, 675, 800, 125))
    # paint_clock
    write_clock_seconds = duenn.render(str(seconds_of_clock), True, schwarz)
    show_clock = duenn.render('TIME:', True, schwarz)
    fenster.blit(show_clock, (10, 10))
    fenster.blit(write_clock_seconds, (100, 10))
    # paint cacti
    if cactus_type != burned_cactus:
        fenster.blit(cactus_type, (cactus_x, 600))
    else:
        fenster.blit(cactus_type, (cactus_x, 645))
    # paint dino
    fenster.blit(dino_type, (75, dino_y))
    # paint FIREBALL
    if fire_ball_running:
        fenster.blit(fire_ball, (fire_x, fire_y))
    pygame.display.flip()


# Overlapping two rectangular objects
def touch(r1, r2):
    print(' came to touch with :', r1, r2)
    if r1[0] is None or r2[0] is None or r1[1] is None:
        return False
    # Case 1
    if between(r1[0], r2[0], r1[0] + r1[2]) and between(r1[1], r2[1], r1[1] + r1[3]):
        return True
    # Case 2
    if between(r1[0], r2[0], r1[0] + r1[2]) and between(r1[1], r2[1] + r2[3], r1[1] + r1[3]):
        return True
    # Case 3
    if between(r1[0], r2[0], r1[0] + r1[2]) and between(r2[1], r1[1], r2[1] + r2[3]):
        return True
    return False


def between(a, b, c):
    if a <= b <= c:
        return True
    else:
        return False


# write record
def record_file(seconds, spaces):
    score = str(round(spaces * 0.5 + seconds))
    record = open("record_file", "r+")
    if record.readlines()[-1] < score:
        print("bigger")
        record.write('\n' + score)
        return True
    else:
        print('smaller')
        record.close()
        return False


# Dino Y States
class States:
    AT_BOTTOM = 1
    JUMPING = 2
    COMING_DOWN = 3


# Variables
jumps = 0
m = 15
fire_x = None
fire_y = None
fire_ball_running = False
dino_type = green_dino
highest_y = 400
state = States.AT_BOTTOM
max_y = 600 - 75
jump_sequence = []
clock_seconds = 0
dino_time = pygame.time.Clock()
cactus_x = 800
next_cactus = random.choice(cacti)
dino_y = 595
delay = 0.02
start_time = time.time()
# While - Loops
while True:
    # update clock
    time.sleep(delay)
    # update cactus location
    if cactus_x < -75:
        cactus_x = 800
        next_cactus = random.choice(cacti)
    cactus_x -= 8
    # update dino location
    if state == States.JUMPING:
        dino_y -= 5
    if state == States.COMING_DOWN:
        dino_y += 5
    if dino_y <= max_y:
        state = States.COMING_DOWN
    if dino_y == 595:
        state = States.AT_BOTTOM
        max_y = 525
    # update dino type
    if int(time.time() - start_time) % 60 <= 10:
        dino_type = fire_dino
    else:
        dino_type = green_dino
    # update fire_x
    if fire_ball_running:
        fire_x += 8
    if fire_ball_running and fire_x >= 800:
        fire_ball_running = False
    # touching check dino and cactus
    dino_touching = touch([75 + m, dino_y + m, 75 - m, 75 - m], [cactus_x + m, 605 + m, 75 - m, 75 - m])
    dino_touching = dino_touching or touch([cactus_x + m, 605 + m, 75 - m, 75 - m], [75 + m, dino_y + m, 75 - m, 75 - m])
    if dino_touching and next_cactus != burned_cactus:
        dino_type = hurt_dino
        new_record = record_file(time.time() - start_time, jumps)
        fenster.fill(blau)
        if new_record:
            write_record = dick_duenn.render(str(str(round(time.time() - start_time + 0.5 * jumps))) + '   New Record', True, gelb)
            fenster.blit(write_record, (250, 250))
            pygame.display.flip()
            time.sleep(3)
            break
        else:
            write_record = duenn.render('Well Done! You have got ' + str(round(time.time() - start_time + 0.5 * jumps)) + ' points.', True, gelb)
            fenster.blit(write_record, (50, 50))
            pygame.display.flip()
            time.sleep(3)
            break
    # touching check fire and cactus
    if fire_ball_running:
        fire_touching = touch([fire_x, fire_y, 25, 18], [cactus_x, 605, 75, 75])
        if fire_touching:
            next_cactus = burned_cactus
    paint_screen(int(time.time() - start_time), next_cactus, cactus_x, dino_y, dino_type, fire_ball_running, fire_x,
                 fire_y)
    # TYPING CASES
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                jumps += 1
                if max_y > highest_y and state == States.JUMPING:
                    max_y -= 40
                if state == States.AT_BOTTOM:
                    state = States.JUMPING
            # FIRE!!!!!
            elif event.key == pygame.K_f:
                if dino_type == fire_dino:
                    fire_x = 150
                    fire_ball_running = True
                    fire_y = dino_y + 15
                else:
                    pass
            else:
                pass
# todo:
# score
# records file
# game over state
# viyona_code < dino_game < images, code
# new game!!! -> ???
