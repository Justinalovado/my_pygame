from glob import escape
from platform import python_branch
from sys import exit
import pygame
import os
from Entity import player


pygame.init()
clock = pygame.time.Clock()
background = pygame.image.load("img/background1.png")
screen = pygame.display.set_mode((1024,768))
pygame.display.set_caption("Da game")
player = player()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            else:
                pass
    keys_pressed = pygame.key.get_pressed()
    if (1 in keys_pressed):
        player.move(keys_pressed)
    screen.blit(background, (0,0))
    screen.blit(player.img, (player.x, player.y))
    pygame.display.update()
    clock.tick(60)

        