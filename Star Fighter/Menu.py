import pygame, sys, time
from pygame.locals import *

pygame.init()

DISPLAY = pygame.display.set_mode((600, 450))
pygame.display.set_caption("Star Fighter")

skins = [pygame.image.load("skin 1.png"),
         pygame.image.load("skin 2.png"),
         pygame.image.load("skin 3.png"),
         pygame.image.load("skin 4.png"),
         pygame.image.load("skin 5.png")
        ]

skin = 0

font = pygame.font.Font("freesansbold.ttf", 15)
skins_instructions_image = font.render("Arrowkeys to cycle through skins or press 1-5", True, (200, 200, 200), (0, 0, 0))
play_instructions_image = font.render("Press return to play", True, (200, 200, 200), (0, 0, 0))

scores_file = open("scores.txt", "r")
scores = scores_file.read().split(",")
scores_file.close()

highest = 1
for i in range(1, len(scores)):
    if int(scores[i]) > int(scores[highest]):
        highest = i
total = 0
for i in range(1, len(scores)):
    total += int(scores[i])
mean = total / len(scores)
highestimage = font.render("Highscore: " + str(scores[highest]), True, (200, 200, 200), (0, 0, 0))
meanimage = font.render("Mean: " + str(mean), True, (200, 200, 200), (0, 0, 0))

while True:
    DISPLAY.fill((0, 0, 0))
    DISPLAY.blit(skins_instructions_image, (300 - (skins_instructions_image.get_width() * 0.5), 0))
    DISPLAY.blit(skins[skin], (284, 40))
    DISPLAY.blit(highestimage, (10, 100))
    DISPLAY.blit(meanimage, (10, 115))
    DISPLAY.blit(play_instructions_image, (300 - (play_instructions_image.get_width() * 0.5), 400))
    

    pygame.event.pump()
    if pygame.key.get_pressed()[K_LEFT]:
        if skin == 0:
            skin = 4
        else:
            skin -= 1
        while pygame.key.get_pressed()[K_LEFT]:
            pygame.event.pump()
    if pygame.key.get_pressed()[K_RIGHT]:
        if skin == 4:
            skin = 0
        else:
            skin += 1
        while pygame.key.get_pressed()[K_RIGHT]:
            pygame.event.pump()
    if pygame.key.get_pressed()[K_1]:
        skin = 0
    if pygame.key.get_pressed()[K_2]:
        skin = 1
    if pygame.key.get_pressed()[K_3]:
        skin = 2
    if pygame.key.get_pressed()[K_4]:
        skin = 3
    if pygame.key.get_pressed()[K_5]:
        skin = 4

    if pygame.key.get_pressed()[K_RETURN]:
        pygame.image.save(skins[skin], "ur_ship.png")
        exec(open("StarFighter.py", "r").read())

    if pygame.key.get_pressed()[K_LALT] and pygame.key.get_pressed()[K_F4]:
        pygame.quit()
        sys.exit()

    pygame.display.update()

pygame.quit()
sys.exit()
