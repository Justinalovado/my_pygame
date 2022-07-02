from random import randint
import pygame


class Weapon:
    def __init__(self) -> None:
        self.color = (0, 0, 255)

class Init_items:
    def __init__(self) -> None:
        self.list = [Remote_controlled_bullet()]

class Remote_controlled_bullet:
    def __init__(self, x=None, y=None) -> None:
        self.img = pygame.image.load("img/item/remote.png").convert_alpha()
        self.img = pygame.transform.scale(self.img, (13, 13))
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        
        self.x = x if x != None else randint(0, 1024 - self.width)
        self.y = y if y != None else randint(0, 768 - self.height)
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)


    def update(self, player):
        self.is_picked(player)
    
    def is_picked(self, player):
        if pygame.Rect.colliderect(player.hitbox, self.hitbox):
            pass
        
  
        
        