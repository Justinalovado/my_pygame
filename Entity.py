from importlib.resources import is_resource
from random import randint
import this
import pygame
class Player:
    def __init__(self) -> None:
        self.x = 0
        self.y = 0
        self.health = 100
        self.attack_point = 10
        self.speed = 3
        self.img = pygame.image.load("img/man.png").convert_alpha()
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.hitbox = self.img.get_rect()
        self.is_invincible = False
        self.invinc_countdown = 0
    def update(self, keys, enemies):
        self.move(keys)
        self.is_taking_melee(enemies)
        if self.invinc_countdown>0:
            self.invinc_countdown -= 1
        else:
            self.is_invincible = False
    def move(self, keys):
        velocity = (0, 0)
        if keys[pygame.K_d]:
            velocity = (self.speed, velocity[1])
        if keys[pygame.K_a]:
            velocity = (-self.speed, velocity[1])
        if keys[pygame.K_s]:
            velocity = (velocity[0], self.speed)
        if keys[pygame.K_w]:
            velocity = (velocity[0], -self.speed)
        self.x, self.y = self.x + velocity[0], self.y + velocity[1]
        pygame.Rect.move_ip(self.hitbox, velocity[0], velocity[1])
        if self.is_outbound():
            self.x, self.y = self.x - velocity[0], self.y - velocity[1]
            pygame.Rect.move_ip(self.hitbox, -velocity[0], -velocity[1])
            
    def is_outbound(self):
        screen_right = 1024-self.width
        screen_bottom = 768-self.width
        return True if (self.x<0 or self.x>screen_right or 
                        self.y<0 or self.y>screen_bottom) else False
    def is_taking_melee(self, enemies):
        for enemy in enemies:
            if pygame.Rect.colliderect(self.hitbox, enemy.hitbox):
                self.take_dmg(enemy.attack_point)
    def take_dmg(self, dmg):
        if self.is_invincible == False:
            self.health -= dmg
            print(f"Player took {dmg} dmg, current health is {self.health}")
            self.is_invincible = True
            self.invinc_countdown = 120

class Enemy:
    def __init__(self, x=None, y=None) -> None:
        self.img = pygame.image.load("img/enemy.png").convert_alpha()
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.x = x if x!=None else randint(0, 1024-self.width)
        self.y = y if y!=None else randint(0, 768-self.width)
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.health = 100
        self.velocity = (randint(0, 5), randint(0, 5))
        self.attack_point = 10
        
    def update(self):
        self.move()
    def move(self):
        self.x, self.y = self.x - self.velocity[0], self.y - self.velocity[1]
        if self.is_outbound():
            self.velocity = (-self.velocity[0], -self.velocity[1])
            self.x, self.y = self.x - self.velocity[0], self.y - self.velocity[1]
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
    def is_outbound(self):
        screen_right = 1024-self.width
        screen_bottom = 768-self.width
        return True if (self.x<0 or self.x>screen_right or 
                        self.y<0 or self.y>screen_bottom) else False