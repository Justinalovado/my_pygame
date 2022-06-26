from random import randint
from sys import exit
from tkinter import font
import pygame
from Entity import Enemy, Player

# initialization
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1024,768))

background = pygame.image.load("img/background1.png").convert_alpha()
gameover_cover = pygame.image.load("img/gameover_hollow_cover.png").convert_alpha()
gradient_background = pygame.image.load("img/red_green_gradient.png").convert_alpha()

pygame.display.set_caption("Da game")
player = Player()
enemies = []
game_state = "gameon"
revive_gauge = 0
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
    screen.fill((88,88,88))
    global player
    player = Player()
    global enemies
    enemies = []
    global game_state
    game_state = "gameset"
    for i in range(randint(3,10)):
        enemies.append(Enemy())
    global revive_gauge
    revive_gauge = 0
    global std_font
    std_font = pygame.font.Font("font\yayusa3d.ttf", 64)

# function to draw every element on screen
def show_elements(screen):
    screen.blit(background, (0,0))
    for enemy in enemies:
        enemy.show(screen)
    player.show(screen)
    # bullets
    for bullet in player.getBullets():
      bullet.show(screen)

initialise_game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            elif event.key == pygame.K_SPACE and game_state!="gameon":
                game_state = "gameon"
            else:
                pass
    # collect data for updates
    keys_pressed = pygame.key.get_pressed()
    # game on
    if game_state == "gameon":
        
        # simulate all elements' behaviour
        update_elements(keys_pressed)

        # render all elements
        show_elements(screen)

        if player.is_dead():
            game_state = "gameover"

    # game set
    elif game_state == "gameset":
        game_state = "idle"
        # initialise_game()
        text = std_font.render("Press SPACE to start", True, 'white', None)
        screen.blit(text, (200,375))
    # game over
    elif game_state == "gameover":
        screen.blit(gradient_background, (0, revive_gauge))
        screen.blit(gameover_cover, (0, 0))
        if keys_pressed[pygame.K_r]:
            revive_gauge -= 20
        elif revive_gauge<0:
            revive_gauge += 10
        if revive_gauge<-768:
            initialise_game()
        # game_state = "idle"
    else:
        pass
        
    pygame.display.update()
    clock.tick(60)



        