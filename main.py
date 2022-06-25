from random import randint
from sys import exit
from numpy import gradient
import pygame
from Entity import Enemy, Player

# initialization
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1024,768))

background = pygame.image.load("img/background1.png")
gameover_screen = pygame.image.load("img/gameover.png")
gameover_cover = pygame.image.load("img/gameover_hollow_cover.png").convert_alpha()
gradient_background = pygame.image.load("img/red_green_gradient.png")

pygame.display.set_caption("Da game")
player = Player()
enemies = []
game_state = "gameon"
gradient_height = 0
    # randomly create enemies
for i in range(randint(3,10)):
    enemies.append(Enemy())

# function for simulating all elements
def update_elements(keys_pressed):
  for enemy in enemies:
      enemy.update(player.getBullets())
      if enemy.is_dead():
        enemies.remove(enemy)
  player.update(keys_pressed, enemies)
    
def initialise_game():
    global player
    player = Player()
    global enemies
    enemies = []
    global game_state
    game_state = "gameon"
    for i in range(randint(3,10)):
        enemies.append(Enemy())
    global gradient_height
    gradient_height = 0
    

# function to draw every element on screen
def show_elements(screen):
    screen.blit(background, (0,0))
    for enemy in enemies:
        enemy.show(screen)
    player.show(screen)
    # bullets
    for bullet in player.getBullets():
      bullet.show(screen)

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
    # collect data for updates
    keys_pressed = pygame.key.get_pressed()
    if game_state == "gameon":
        
        # simulate all elements' behaviour
        update_elements(keys_pressed)

        # render all elements
        show_elements(screen)

        if player.is_dead():
            game_state = "gameover"
    elif game_state == "gameover":
        if keys_pressed[pygame.K_r]:
            gradient_height -= 20
        elif gradient_height<0:
            gradient_height += 10
        if gradient_height<-768:
            initialise_game()
            
        # screen.blit(gameover_screen, (0,0))
        screen.blit(gradient_background, (0, gradient_height))
        screen.blit(gameover_cover, (0, 0))
        # game_state = "idle"
    else:
        pass
        
    pygame.display.update()
    clock.tick(60)



        