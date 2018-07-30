import pygame, sys, time, math, random
from pygame.locals import *

pygame.init()

DISPLAY = pygame.display.set_mode((600, 450), 0, 0)
pygame.display.set_caption("Star Fighter")


ur_ship_image = pygame.image.load("ur_ship.png")
ur_ship_x = 300
ur_ship_y = 240
ur_ship_x_speed = 0
ur_ship_y_speed = 0
ur_ship_shields = 4
ur_ship_direction = 0

points = 0

alive = True

shots = [] #[0]x [1]y [2]direction
shot_image = pygame.image.load("shot.png")
shot_cooldown = 0
shot_energy = 100

enemy_ships = [[100, 100, 0, 0], [200, 500, 0, 0], [0, 400, 0, 0]] #[0]:x  [1]:y  [2]:x_speed [3]:y_speed
enemy_ship_image = pygame.image.load("enemy.png")
explode_images = []
for i in range(0, 6):
    explode_images.append(pygame.image.load("explode-" + str(i + 1) + ".png"))

explosions = [] #[0]x [1]y [2]frame

alive = True

def sin(n):
    return(math.sin(math.radians(n)))

def cos(n):
    return(math.cos(math.radians(n)))

def asin(n):
    return(math.degrees(math.asin(n)))

def display_background():
    DISPLAY.fill((0, 0, 0))

def display_ship():
    ship_image_rotated = pygame.transform.rotate(ur_ship_image, -ur_ship_direction) #create rotated image
    DISPLAY.blit(ship_image_rotated, (ur_ship_x - (ship_image_rotated.get_width() * 0.5), ur_ship_y - (ship_image_rotated.get_height() * 0.5)))

def do_movement():
    global ur_ship_x, ur_ship_y, ur_ship_x_speed, ur_ship_y_speed, ur_ship_direction, shot_cooldown, shot_energy, enemy_ships

    ur_ship_x_speed *= 0.9
    ur_ship_y_speed *= 0.9

    ur_ship_x += ur_ship_x_speed
    ur_ship_y += ur_ship_y_speed

    pygame.event.pump()
    key_pressed = pygame.key.get_pressed()

    if key_pressed[K_UP] or key_pressed[K_w]:
        ur_ship_x_speed += sin(ur_ship_direction) * 1.5
        ur_ship_y_speed -= cos(ur_ship_direction) * 1.5
        if key_pressed[K_RCTRL] and shot_energy > 0:
            ur_ship_x_speed += sin(ur_ship_direction)
            ur_ship_y_speed -= cos(ur_ship_direction)
            shot_energy -= 1

    if key_pressed[K_LEFT] or key_pressed[K_a]:
        ur_ship_direction -= 8

    if key_pressed[K_RIGHT] or key_pressed[K_d]:
        ur_ship_direction += 8

    if key_pressed[K_SPACE] and shot_cooldown > 10 and shot_energy > 19:
        shots.append([ur_ship_x, ur_ship_y, ur_ship_direction])
        shot_cooldown = 0
        shot_energy -= 25
    shot_cooldown += 1
    if shot_energy < 100:
        shot_energy += 1

    for i in range(0, len(enemy_ships)):
        x_distance = ur_ship_x - enemy_ships[i][0]
        y_distance = ur_ship_y - enemy_ships[i][1]
        distance = math.sqrt((x_distance ** 2) + (y_distance ** 2))

        if distance < 30:
            ship_dies()

    if ur_ship_x > 600:
        ur_ship_x = 0
    if ur_ship_x < 0:
        ur_ship_x = 600
    if ur_ship_y > 450:
        ur_ship_y = 0
    if ur_ship_y < 0:
        ur_ship_y = 450

def do_quit_sensing():
    pygame.event.pump()
    key_pressed = pygame.key.get_pressed()

    if key_pressed[K_F4] and key_pressed[K_LALT]:
        pygame.quit()
        sys.exit()

def display_shots():
    global points
    i = 0
    while i < len(shots):
        shots[i][0] += sin(shots[i][2]) * 18
        shots[i][1] -= cos(shots[i][2]) * 18

        rotated_image = pygame.transform.rotate(shot_image, -shots[i][2])

        x_display = shots[i][0] - (rotated_image.get_width() * 0.5)
        y_display = shots[i][1] - (rotated_image.get_height() * 0.5)

        DISPLAY.blit(rotated_image, (x_display, y_display))

        for a in range(0, len(enemy_ships)):
            if shots[i][0] > enemy_ships[a][0] - 16 and shots[i][0] < enemy_ships[a][0] + 16 and shots[i][1] > enemy_ships[a][1] - 16 and shots[i][1] < enemy_ships[a][1] + 16:
                explosions.append([enemy_ships[a][0], enemy_ships[a][1], 1])
                shots.pop(i)
                enemy_ships.pop(a)
                points += 1
                break
        try:
            if shots[i][0] > 600 or shots[i][0] < 0 or shots[i][1] > 450 or shots[i][1] < 0:
                shots.pop(i)
        except IndexError:
            pass
        
        i += 1

def display_bars():
    global shot_cooldown, shot_energy, ur_ship_shields, points

    pygame.draw.line(DISPLAY, (0, 100, 200), (5, 450), (5, 450 - shot_energy), 10)
    for i in range(0, ur_ship_shields):
        pygame.draw.line(DISPLAY, (200, 200, 0), (20, 450 - (i * 25)), (20, 430 - (i * 25)), 10)

    font = pygame.font.Font("freesansbold.ttf", 20)
    score_image = font.render("Score: " + str(points), True, (0, 200, 0), (0, 0, 0))
    DISPLAY.blit(score_image, (0, 0))

def display_enemy_ships():
    global enemy_ships, ur_ship_x, ur_ship_y, alive

    i = 0
    while i < len(enemy_ships):

        enemy_ships[i][0] += (enemy_ships[i][2] * 0.3)
        enemy_ships[i][1] += (enemy_ships[i][3] * 0.3)

        enemy_ships[i][2] *= 0.9
        enemy_ships[i][3] *= 0.9

        if alive:
            xdistance = enemy_ships[i][0] - ur_ship_x
            ydistance = enemy_ships[i][1] - ur_ship_y
            distance = math.sqrt((xdistance ** 2) + (ydistance ** 2))
            direction = asin(xdistance / distance)
            if ydistance > 0:
                direction = 180 - direction

            enemy_ships[i][2] -= sin(direction)
            enemy_ships[i][3] += cos(direction)

            enemy_ship_image_rotated = pygame.transform.rotate(enemy_ship_image, 180 - direction)

        display_x = enemy_ships[i][0] - (enemy_ship_image_rotated.get_width() * 0.5)
        display_y = enemy_ships[i][1] - (enemy_ship_image_rotated.get_height() * 0.5)

        DISPLAY.blit(enemy_ship_image_rotated, (display_x, display_y))

        i += 1

def display_explosions():
    for i in range(0, len(explosions)):
        DISPLAY.blit(explode_images[explosions[i][2]], (explosions[i][0] - 32, explosions[i][1] - 32))
        explosions[i][2] += 1
        if explosions[i][2] == 6:
            explosions.pop(i)
            break

def do_spawn():
    global enemy_ships, points

    if len(enemy_ships) < (0.1 * points) + 3:
        rand = random.randint(1, 10)
        if rand == 1:
            enemy_ships.append([0, random.randint(0, 450), 0, 0, 90])
        elif rand == 2:
            enemy_ships.append([600, random.randint(0, 450), 0, 0, 270])
        elif rand == 3:
            enemy_ships.append([random.randint(0, 600), 0, 0, 0, 180])
        elif rand == 4:
            enemy_ships.append([random.randint(0, 600), 0, 0, 0, 450])

def display_score():
    global points

    font = pygame.font.Font("freesansbold.ttf", 50)
    score_image = font.render("Score: " + str(points), True, (0, 200, 0), (0, 0, 0))
    DISPLAY.blit(score_image, (300 - (score_image.get_width() * 0.5), 200))

def ship_dies():
    global points
    explosions.append([ur_ship_x, ur_ship_y, 1])
    for i in range(0, 49):
        display_background()
        display_shots()
        display_enemy_ships()
        display_explosions()
        display_score()
        pygame.display.update()

        pygame.event.pump()
        do_quit_sensing()
        do_spawn()

        time.sleep(0.03)

    scores_file = open("scores.txt", "r")
    scores = scores_file.read().split(",")
    scores_file.close()

    scores.append(str(points))

    scores_string = scores.pop(0)
    for i in range(0, len(scores)):
        scores_string = scores_string + ","
        scores_string = scores_string + str(scores[i])

    scores_file = open("scores.txt", "w")
    scores_file.write(scores_string)
    scores_file.close()

    pygame.quit()
    sys.exit()

    #I need to find a way to get it to exit execution of this file at this point...

while True:
    display_background()
    display_ship()
    display_shots()
    display_bars()
    display_enemy_ships()
    display_explosions()
    pygame.display.update()

    pygame.event.pump()
    do_movement()
    do_quit_sensing()
    do_spawn()

    time.sleep(0.03)
