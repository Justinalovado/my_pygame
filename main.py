from sys import exit
import pygame
from Entity import player

flag = 1
pygame.init()
clock = pygame.time.Clock()
# background, screen
background = pygame.image.load("img/background1.png")
screen = pygame.display.set_mode((1024,768))

# title
pygame.display.set_caption("Da game")

# player
player = player()

# attack
bullet = pygame.image.load("img/bullet.png")
bullet = pygame.transform.scale(bullet, (10, 10))
bullets = []

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            elif event.key == pygame.K_k:
                bullet_x_pos = player.x + player.width / 2
                bullet_y_pos = player.y + player.height / 2
                bullets.append([bullet_x_pos, bullet_y_pos])
            else:
                pass

    keys_pressed = pygame.key.get_pressed()
    if (1 in keys_pressed):
        player.move(keys_pressed)
    screen.blit(background, (0,0))
    pygame.draw.rect(screen, 'green', player.hitbox)
    screen.blit(player.img, (player.x, player.y))
    
    bullets = [[b[0] + player.velocity[0]*4 , b[1] + player.velocity[1]*4] for b in bullets]

    bullets = [[b[0], b[1]] for b in bullets if (b[1] > 0 and b[1] <= 768) and (b[0] > 0 and b[0] <= 1024)]
    for b_x, b_y in bullets:
        screen.blit(bullet, (b_x, b_y))
    if flag:
        print(type(player.hitbox))
        flag = 0
    pygame.display.update()
    clock.tick(60)

        