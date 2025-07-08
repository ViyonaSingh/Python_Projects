import pygame
from pygame import QUIT
import random
import time
from nava import play, stop_all
import math

# Farben, Größen
cell_width = 60
width = 620
height = 750
black = (0, 0, 0)
turkis = (0, 200, 200)
light_blue = (100, 120, 185)
white = (255, 255, 255)
light_brown = (249, 210, 166)
brown = (187, 109, 62)
dark_brown = (123, 56, 15)
red = (255, 69, 0)
dark_red = (139, 0, 0)
indigo = (255, 220, 255)
pink = (255, 105, 180)
# Initialize
pygame.init()
pygame.display.set_caption('Muff Journey from Viyona')
pygame.display.init()
pygame.font.init()
# Schriften
duenn = pygame.font.Font('freesansbold.ttf', 25)
duenn_dick = pygame.font.SysFont('bahnenschrift.ttf', 50)
dick_duenn = pygame.font.SysFont('bahnenschrift.ttf', 75)
dick = pygame.font.SysFont('bahnenschrift.ttf', 100)
# make window
window = pygame.display.set_mode((width, height))
# music
game_over = 'music/game-over-39-199830.mp3'
death_sound = 'music/videogame-death-sound-43894.mp3'
epic_game_over = 'music/game-over-man-136233.mp3'
on_the_road = 'music/on-the-road-to-the-eighties_59sec-177566.mp3'
techno = 'music/8bit-music-for-game-68698.mp3'
action = 'music/the-nft-gaming-action-drum-n-bass-207012 Kopie.mp3'
neon = 'music/neon-gaming-128925.mp3'
fight = 'music/pixel-fight-8-bit-arcade-music-background-music-for-video-36-second-208771.mp3'
applause = 'music/applause-2-31567.mp3'


class Environment:
    def __init__(self):
        self.cake_list = []
        self.move_speed = 0.5
        self.before_jump = 650
        self.rect_y = 730
        self.start_time = time.time()
        self.no_error = 'pot_code'

    # writing record in a file
    def record_file(self, file_name, game_points):
        self.no_error = 'pot_ty_code'
        record = open(file_name, "r+")
        if int(record.readlines()[-1]) < int(game_points):
            # print("bigger")
            record.write('\n' + str(game_points))
            return True
        else:
            # print('smaller')
            record.close()
            return False

    # Overlapping two rectangular objects
    def touch(self, r1, r2):
        self.no_error = 'pot_ty_code'
        return pygame.Rect.colliderect(r1, r2)

    # three object one is between
    def between(self, t, u, v):
        self.no_error = 'pot_ty_code'
        if t < u < v:
            return True
        else:
            return False

    # two objects, one is on the other one
    def side_touch(self, r1, r2):
        if self.between(r2[1], r1[1] + r1[3], r2[1] + r2[3] / 4):
            if self.between(r2[0], r1[0] + 20, (r2[0] + r2[2])) or self.between(r2[0], (r1[0] + r1[2] - 20),
                                                                                (r2[0] + r2[2])):
                return True
        else:
            return False

    # posing cakes in the sky (:
    def make_cakes(self):
        for cake in range(0, 1000):
            c.cake_y = 610 - cake * 140
            c.cake_x = random.randint(0, 540)
            self.cake_list.append([c.cake_x, c.cake_y, c.width, c.height])

    # print the cakes using cake_list
    def refresh_cakes(self):
        for cake in self.cake_list:
            window.blit(c.cake, (cake[0], cake[1]))

    # move screen
    def move_screen(self, direction, speed):
        self.move_speed = speed
        if direction == 'DOWN':
            ch.chocolate_y += self.move_speed
            for cakes_y in e.cake_list:
                cakes_y[1] += self.move_speed
            self.before_jump += self.move_speed
            self.rect_y += self.move_speed
            m.y += self.move_speed
        elif direction == 'UP':
            ch.chocolate_y -= self.move_speed
            for cakes_y in e.cake_list:
                cakes_y[1] -= self.move_speed
            self.before_jump -= self.move_speed
            self.rect_y -= self.move_speed
            m.y -= self.move_speed
        pygame.display.flip()

    # paint_clock in the right upper corner
    def clock(self):
        write_clock_seconds = duenn.render(str(round(time.time() - self.start_time)), True, turkis)
        show_clock = duenn.render('TIME:', True, turkis)
        window.blit(show_clock, (450, 10))
        window.blit(write_clock_seconds, (540, 10))


class Muffin:
    def __init__(self):
        self.width = 100
        self.height = 80
        self.speed = 5
        self.y = 650
        self.x = width / 2 - self.width / 2
        self.muff = pygame.image.load('muff.png')
        self.muff = pygame.transform.scale(self.muff, (self.width, self.height))
        self.muff_shock = pygame.image.load('shock_muff.png')
        self.muff_shock = pygame.transform.scale(self.muff_shock, (self.width, self.height))
        self.step_x = 0
        self.step_y = 0
        self.gun_round = 1

    # changing the positions if left or right pressed
    def move(self, jumping_state, right, left):
        if self.y <= 510 or self.y >= 620 and ch.chocolate_y <= 750:
            self.speed = 30
        else:
            self.speed = 5
        if game == 'right':
            self.speed = 3
        if jumping_state == 2:
            self.y -= 0.1 * self.speed
        elif right:
            self.x += 0.1 * self.speed
        elif left:
            self.x -= 0.1 * self.speed
        if jumping_state == 3:
            self.y += 0.1 * self.speed
            window.blit(self.muff_shock, (self.x, self.y))
        if jumping_state != 3:
            window.blit(self.muff, (self.x, self.y))

    # you fly to the opposite direction through the gun force
    def water_gun_move(self):
        window.fill(indigo)
        e.clock()
        window.blit(shooting_number_blit, (100, 10))
        pygame.draw.rect(window, pink, pygame.Rect(0, e.rect_y, 720, 65))
        self.x += self.step_x
        self.y -= self.step_y
        window.blit(self.muff, (self.x, self.y))
        if m.gun_round == 50:
            self.step_x = 0
            self.step_y = 0


class Cake:
    def __init__(self):
        self.cake = pygame.image.load('cake.png')
        self.cake_x = None
        self.cake_y = None
        self.height = 25
        self.width = 120
        self.cake = pygame.transform.scale(self.cake, (self.width, self.height))


class Chocolate:
    def __init__(self):
        self.chocolate = pygame.image.load('chocolate.png')
        self.chocolate = pygame.transform.scale(self.chocolate, (620, 750))
        self.chocolate_y = 760

    # raising the chocolate
    def rise_up(self):
        if m.y + 800 <= self.chocolate_y:
            self.chocolate_y -= 0.2
        else:
            self.chocolate_y -= 0.1
        window.blit(self.chocolate, (0, self.chocolate_y))


class Potato:
    def __init__(self):
        self.aalu = pygame.image.load('aalu.png')
        self.aalu = pygame.transform.scale(self.aalu, (65, 80))
        self.mad = pygame.image.load('mad_aalu.png')
        self.mad = pygame.transform.scale(self.mad, (80, 80))
        self.vampling = pygame.image.load('vamp_aalu.png')
        self.vampling = pygame.transform.scale(self.vampling, (80, 80))
        self.knife = pygame.image.load('knife.png')
        self.knife = pygame.transform.scale(self.knife, (60, 60))
        self.potato_y = 650
        self.potato_x = 0
        self.knife_pos = [self.potato_x, self.potato_y]
        self.side = None
        self.speed_p = 0.2
        self.target_height = 40
        self.shoot_direction = None
        self.potato_to_blit = self.aalu
        self.shooting = False

    # moving aalu the monster randomly
    def potato_move(self):
        if shooting_number >= 10:
            self.potato_to_blit = self.mad
        if shooting_number >= 30:
            self.potato_to_blit = self.vampling
        window.fill(indigo)
        window.blit(shooting_number_blit, (100, 10))
        e.clock()
        pygame.draw.rect(window, pink, pygame.Rect(0, e.rect_y, 720, 65))
        window.blit(m.muff, (m.x, m.y))
        window.blit(w.water_gun_to_blit, w.water_gun_rect)
        window.blit(b.bullet, (b.bullet_x, b.bullet_y))
        window.blit(p.knife, p.knife_pos)
        if self.potato_y >= 650:
            self.side = random.choice(['right', 'left'])
            self.target_height = random.randint(300, 620)
            self.shoot_direction = [random.randint(-101, 101) / 100, random.randint(0, 101) / 100]
            self.knife_pos = [self.potato_x, self.potato_y]
            self.potato_shoot()
        if self.potato_y > self.target_height:
            self.potato_y -= self.speed_p
            if self.side == 'right':
                self.potato_x += self.speed_p
            elif self.side == 'left':
                self.potato_x -= self.speed_p
        elif self.potato_y < self.target_height:
            self.potato_y += self.speed_p
            self.target_height = 750
            if self.side == 'right':
                self.potato_x += self.speed_p
            elif self.side == 'left':
                self.potato_x -= self.speed_p
        if self.shooting:
            self.potato_shoot()
        window.blit(self.potato_to_blit, (self.potato_x, self.potato_y))

    # shooting the bloody knife
    def potato_shoot(self):
        self.shooting = True
        window.fill(indigo)
        e.clock()
        window.blit(shooting_number_blit, (100, 10))
        pygame.draw.rect(window, pink, pygame.Rect(0, e.rect_y, 720, 65))
        window.blit(m.muff, (m.x, m.y))
        window.blit(w.water_gun_to_blit, w.water_gun_rect)
        self.knife_pos[0] += self.shoot_direction[0]
        self.knife_pos[1] -= self.shoot_direction[1]
        window.blit(self.knife, self.knife_pos)
        if not -60 < self.knife_pos[0] < 620 or not -60 < self.knife_pos[1] < 750:
            self.shooting = False
        if b.going:
            b.shoot()


class Water_gun:
    def __init__(self, muffin):
        self.width = 60
        self.height = 30
        self.turn_angle = None
        self.water_gun = pygame.image.load('water_gun.png')
        self.water_gun_to_blit = None
        self.water_gun = pygame.transform.scale(self.water_gun, (self.width, self.height))
        self.w_pos = [None, None]
        self.water_gun_rect = [100, 100]
        self.m = muffin

    # turning water gun
    def water_gun_turn(self, mouse_x, mouse_y):
        window.fill(indigo)
        e.clock()
        window.blit(shooting_number_blit, (100, 10))
        pygame.draw.rect(window, pink, pygame.Rect(0, e.rect_y, 720, 65))
        self.w_pos = [self.m.x + self.m.width - 20 + 10, self.m.y + self.m.height / 2 + 10]
        mouse = [mouse_x, mouse_y]
        water_pos = [self.m.x + self.m.width - 20 + 70, self.m.y + self.m.height / 2 + 12]
        muff_pos = [self.m.x + self.m.width / 2, self.m.y + self.m.height / 2]
        ang = math.degrees(math.atan2(mouse[1] - muff_pos[1], mouse[0] - muff_pos[0]) -
                           math.atan2(water_pos[1] - muff_pos[1], water_pos[0] - muff_pos[0]))
        self.turn_angle = -ang + 360 if ang < 0 else -ang
        self.water_gun_to_blit = pygame.transform.rotate(self.water_gun, self.turn_angle)
        self.water_gun_rect = self.water_gun.get_rect(center=self.w_pos)

    # updating  the position / state of the water_gun
    def update_pos(self):
        window.fill(indigo)
        e.clock()
        window.blit(shooting_number_blit, (100, 10))
        pygame.draw.rect(window, pink, pygame.Rect(0, e.rect_y, 720, 65))
        window.blit(self.m.muff, (self.m.x, self.m.y))
        window.blit(self.water_gun_to_blit, self.water_gun_rect)
        window.blit(p.knife, p.knife_pos)


class Bullet:
    def __init__(self, muffin, water_gun):
        self.width = 20
        self.height = 12
        self.bullet_x = m.x + m.width / 2
        self.bullet_y = m.y + m.height / 2
        self.bullet = pygame.image.load('bullet_egg.png')
        self.bullet = pygame.transform.scale(self.bullet, (self.width, self.height))
        self.x_step = None
        self.y_step = None
        self.going = False
        self.m = muffin
        self.w = water_gun

    # shooting the egg
    def shoot(self):
        window.fill(indigo)
        e.clock()
        window.blit(shooting_number_blit, (100, 10))
        pygame.draw.rect(window, pink, pygame.Rect(0, e.rect_y, 720, 65))
        window.blit(m.muff, (m.x, m.y))
        window.blit(self.w.water_gun_to_blit, self.w.water_gun_rect)
        window.blit(p.knife, p.knife_pos)
        self.bullet_x -= self.x_step
        self.bullet_y += self.y_step
        window.blit(self.bullet, (self.bullet_x, self.bullet_y))
        if not -22 < self.bullet_x < 620 or not -15 < self.bullet_y < 750:
            self.x_step = 0
            self.y_step = 0
            self.going = False


# Muff Y States
class States:
    AT_CAKE = 1
    JUMPING = 2
    COMING_DOWN = 3


# giving variables to the classes
e = Environment()
m = Muffin()
c = Cake()
ch = Chocolate()
p = Potato()
w = Water_gun(m)
b = Bullet(m, w)
# global variables which are used during the games
window.fill(indigo)
state = States.AT_CAKE
staying_plate = 0
shooting_number = 0
tried = False
first = True
shooting_number_blit = duenn.render('Shots: ' + str(shooting_number), True, turkis)
game_over_page = pygame.image.load('game_over_page.png')
game_over_page = pygame.transform.scale(game_over_page, (620, 750))
start_page = pygame.image.load('start_page.png')
start_page = pygame.transform.scale(start_page, (620, 750))
record_page = pygame.image.load('record_page.png')
record_page = pygame.transform.scale(record_page, (620, 750))
setting = pygame.image.load('setting.png')
setting = pygame.transform.scale(setting, (100, 100))
game = None
click_x = None
click_y = None
window.blit(start_page, (0, 0))
window.blit(setting, (510, 630))
pygame.display.flip()
player_ready = False
# asking which game the user wants to play
while True:
    if player_ready:
        break
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if 510 < x < 610 and 630 < y < 730:
                window.fill(indigo)
                left_side = duenn.render('If you want to play Muff Climb press arrow left', True, turkis)
                window.blit(left_side, (35, 50))
                right_side = duenn.render('If you want to play Muff Fight press arrow right', True, turkis)
                window.blit(right_side, (35, 100))
                pygame.display.flip()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player_ready = True
                game = 'right'
            if event.key == pygame.K_LEFT:
                player_ready = True
                game = 'left'

if game == 'left':
    e.make_cakes()
    song = play(random.choice([on_the_road, techno]), async_mode=True, loop=True)
    while True:
        # raising chocolate and setting clock
        ch.rise_up()
        e.clock()
        # changing states
        if e.side_touch([m.x, m.y, m.width, m.height], (0, e.rect_y, 720, 65)):
            state = States.AT_CAKE
        elif state == 3:
            for info in e.cake_list:
                if e.side_touch([m.x, m.y, m.width, m.height], info):
                    state = States.AT_CAKE
                    staying_plate = e.cake_list.index(info) + 1
        elif m.y < e.before_jump - 250:
            state = States.COMING_DOWN
        # staying in the screen
        if m.x < 0:
            m.x += 2
        if m.x > 620 - 100:
            m.x -= 2
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                ch.rise_up()
                e.clock()
                if event.key == pygame.K_SPACE:
                    window.fill(indigo)
                    m.move(False, False, False)
                    pygame.draw.rect(window, pink, pygame.Rect(0, e.rect_y, 720, 65))
                    e.refresh_cakes()
                    ch.rise_up()
                    e.clock()
                if event.key == pygame.K_UP and state == States.AT_CAKE:
                    state = States.JUMPING
                    e.before_jump = m.y
        # letting muff move
        if state != 1:
            window.fill(indigo)
            m.move(state, False, False)
            pygame.draw.rect(window, pink, pygame.Rect(0, e.rect_y, 720, 65))
            e.refresh_cakes()
            ch.rise_up()
            e.clock()
        # moving smoothly left and right
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            window.fill(indigo)
            m.move(False, True, False)
            pygame.draw.rect(window, pink, pygame.Rect(0, e.rect_y, 720, 65))
            e.refresh_cakes()
            ch.rise_up()
            e.clock()
            # checking if you still have floor to stand on after moving right
            if not state == 2 and not state == 3:
                for info in e.cake_list:
                    if e.side_touch([m.x, m.y, m.width, m.height], (0, e.rect_y, 720, 65)) and e.side_touch(
                            [m.x, m.y, m.width, m.height], e.cake_list[0]):
                        state = States.AT_CAKE
                        break
                    else:
                        state = States.COMING_DOWN
        if keys[pygame.K_LEFT]:
            window.fill(indigo)
            m.move(False, False, True)
            pygame.draw.rect(window, pink, pygame.Rect(0, e.rect_y, 720, 65))
            e.refresh_cakes()
            ch.rise_up()
            e.clock()
            # checking if you still have floor to stand on after moving left
            if not state == 2 and not state == 3:
                for info in e.cake_list:
                    if e.side_touch([m.x, m.y, m.width, m.height], (0, e.rect_y, 720, 65)) and e.side_touch(
                            [m.x, m.y, m.width, m.height], e.cake_list[0]):
                        state = States.AT_CAKE
                        break
                    else:
                        state = States.COMING_DOWN
        # moving screen down
        if m.y <= 510:
            e.move_screen('DOWN', abs(m.y - 510) / 1000)
            window.fill(indigo)
            window.blit(m.muff, (m.x, m.y))
            e.refresh_cakes()
            ch.rise_up()
            e.clock()
            pygame.draw.rect(window, pink, pygame.Rect(0, e.rect_y, 720, 65))
            window.blit(ch.chocolate, (0, ch.chocolate_y))
        # moving screen up
        if m.y >= 620:
            e.move_screen('UP', abs(m.y - 620) / 100)
            window.fill(indigo)
            window.blit(m.muff, (m.x, m.y))
            e.refresh_cakes()
            ch.rise_up()
            e.clock()
            pygame.draw.rect(window, pink, pygame.Rect(0, e.rect_y, 720, 65))
            window.blit(ch.chocolate, (0, ch.chocolate_y))
        # GAME OVER!!!
        if m.y + m.height > ch.chocolate_y + 100:
            stop_all()
            play(death_sound, async_mode=False)
            window.fill(indigo)
            window.blit(game_over_page, (0, 0))
            points = duenn.render(
                'Points:' + str(math.floor((staying_plate / (round(time.time() - e.start_time)) * 100))), True, turkis)
            window.blit(points, (170, 290))
            pygame.display.flip()
            if e.record_file('records_muff_climb',
                             str(math.floor((staying_plate / (round(time.time() - e.start_time)) * 100)))):
                window.fill(indigo)
                window.blit(record_page, (0, 0))
                play(applause, async_mode=False)
                pygame.display.flip()
            break
        pygame.display.flip()

if game == 'right':
    w.water_gun_turn(0, 0)
    w.update_pos()
    song = play(random.choice([fight, action, neon]), async_mode=True, loop=True)
    while True:
        # setting clock
        pygame.draw.rect(window, indigo, pygame.Rect(450, 10, 200, 50))
        e.clock()
        # changing states
        if m.y >= 650:
            state = States.AT_CAKE
        else:
            state = States.COMING_DOWN
        # staying in the screen
        if m.x < 0:
            m.x = 0
        if m.x > 620 - 100:
            m.x = 520
        if m.y < 0:
            m.y = 0
        if m.y + 80 > 750:
            m.y = 630
        # staying in the screen (potato)
        if p.potato_x < 0:
            p.potato_x = 0
        if p.potato_x > 620 - 100:
            p.potato_x = 520
        if p.potato_y < 0:
            p.potato_y = 0
        if p.potato_y + 80 > 750:
            p.potato_y = 630
        # coming down
        if state == 3:
            window.fill(indigo)
            e.clock()
            shooting_number_blit = duenn.render('Shots: ' + str(shooting_number), True, turkis)
            window.blit(shooting_number_blit, (100, 10))
            pygame.draw.rect(window, pink, pygame.Rect(0, e.rect_y, 720, 65))
            m.move(state, False, False)
            turn_x, turn_y = pygame.mouse.get_pos()
            w.water_gun_turn(turn_x, turn_y)
            w.update_pos()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            # moving muff with the water gun method :)
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_x, click_y = pygame.mouse.get_pos()
                b.going = True
                tried = False
                b.bullet_x = w.water_gun_rect[0]
                b.bullet_y = w.water_gun_rect[1]
                b.x_step = (w.water_gun_rect[0] - click_x) / 300
                b.y_step = (click_y - w.water_gun_rect[1]) / 300
                b.shoot()
                # shooting egg
                for m.gun_round in range(1, 20):
                    m.step_x = (m.x + m.width / 2 - click_x) / 30
                    m.step_y = (click_y - m.y) / 30
                    m.water_gun_move()
                    w.update_pos()
                    m.gun_round += 1
            # turning water_gun
            if event.type == pygame.MOUSEMOTION:
                turn_x, turn_y = pygame.mouse.get_pos()
                w.water_gun_turn(turn_x, turn_y)
                w.update_pos()
        if b.going:
            b.shoot()
        p.potato_move()
        # updating points
        if b.going and not tried:
            if e.touch(pygame.Rect(b.bullet_x + 3, b.bullet_y + 3, b.width - 3, b.height - 3),
                       pygame.Rect(p.potato_x + 10, p.potato_y + 10, 55, 70)):
                shooting_number += 1
                tried = True
        # GAME OVER!!!
        if e.touch(pygame.Rect(m.x + 10, m.y + 10, m.width - 10, m.height - 10),
                   pygame.Rect(p.potato_x + 10, p.potato_y + 10, 55, 70)) \
                or e.touch(pygame.Rect(m.x + 10, m.y + 10, m.width - 10, m.height - 10),
                           pygame.Rect(p.knife_pos[0] + 10, p.knife_pos[1] + 10, 50, 50)):
            stop_all()
            play(game_over, async_mode=False)
            window.fill(indigo)
            window.blit(game_over_page, (0, 0))
            points = duenn.render(
                'Points:' + str(math.floor((shooting_number / (round(time.time() - e.start_time)) * 100))), True,
                turkis)
            window.blit(points, (170, 290))
            pygame.display.flip()
            if e.record_file('records_muff_fight',
                             str(math.floor((shooting_number / (round(time.time() - e.start_time)) * 100)))):
                window.fill(indigo)
                window.blit(record_page, (0, 0))
                play(applause, async_mode=False)
                pygame.display.flip()
            break
        pygame.display.flip()

# staying in the screen till user clicks the red cross (:
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

# Instructions:
# Muff CLimb is a game inspired from doodle sack and the raising lava inspired from super mario
# you have to climb higher and higher with the keys
# Muff Fight is a fully self-made game with the super_villain called Aalu
# have to shoot aalu with the water_gun which you can control with the mouse

# Facts:
# This is an about-two-month-project with my brother
# I am writing this to make my code longer (:
# Today is the 20. August
# We are in America one week till today (:
# I think Khushi you are reading this (:
# just to
# get
# 650 lines
