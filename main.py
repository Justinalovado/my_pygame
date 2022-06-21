from random import randint
from sys import exit
import pygame
from Entity import Enemy, Player


pygame.init()
clock = pygame.time.Clock()
background = pygame.image.load("img/background1.png")
screen = pygame.display.set_mode((1024,768))
pygame.display.set_caption("Da game")
player = Player()
enemies = []
for i in range(randint(3,10)):
    enemies.append(Enemy())
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
    screen.blit(background, (0,0))
    for enemy in enemies:
        enemy.update()
        screen.blit(enemy.img, (enemy.x, enemy.y))
    player.update(keys_pressed, enemies)
    pygame.draw.rect(screen, 'green', player.hitbox)
    screen.blit(player.img, (player.x, player.y))
    pygame.display.update()
    clock.tick(60)

        