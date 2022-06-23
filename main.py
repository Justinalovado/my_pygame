from random import randint
from sys import exit
import pygame
from Entity import Enemy, Player


pygame.init()
clock = pygame.time.Clock()
background = pygame.image.load("img/background1.png")
gameover_screen = pygame.image.load("img/gameover.png")
screen = pygame.display.set_mode((1024,768))
pygame.display.set_caption("Da game")
player = Player()
enemies = []
game_state = "gameon"
# randomly create enemies
for i in range(randint(3,10)):
    enemies.append(Enemy())

# function for simulating all elements
def update_elements(keys_pressed):
    for enemy in enemies:
        enemy.update()
    player.update(keys_pressed, enemies)
    


# function to draw every element on screen
def show_elements(screen):
    screen.blit(background, (0,0))
    for enemy in enemies:
        enemy.show(screen)
    player.show(screen)

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
    if game_state == "gameon":
        # collect data for updates
        keys_pressed = pygame.key.get_pressed()

        # simulate all elements' behaviour
        update_elements(keys_pressed)

        # render all elements
        show_elements(screen)

        if player.is_dead():
            game_state = "gameover"
    elif game_state == "gameover":
        print("dead")
        screen.blit(gameover_screen, (0,0))
        game_state = "idle"
    else:
        pass
        
    pygame.display.update()
    clock.tick(60)



        