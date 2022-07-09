from random import randint
import pygame



class Weapon:
    def __init__(self) -> None:
        self.color = (0, 0, 255)

class Remote_controlled_bullet:
    def __init__(self, x=None, y=None) -> None:
        self.img = pygame.image.load("img/item/remote.png").convert_alpha()
        self.img = pygame.transform.scale(self.img, (33, 33))
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.x = x if x != None else randint(0, 1024 - self.width)
        self.y = y if y != None else randint(0, 768 - self.height)
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)


    def update(self, player, screen, items):
        self.show(screen)
        if self.is_picked_up(player):
            items.remove(self)

    
    def is_picked_up(self, player):
        if pygame.Rect.colliderect(player.hitbox, self.hitbox):
            player.remote_bullet_item = True
            return True
    
    def show(self, screen, show_hitbox=True):
        screen.blit(self.img, (self.x, self.y))
        if show_hitbox:
            pygame.draw.rect(screen, "lightgreen", self.hitbox, width=1)

ITEM_LIST = [Remote_controlled_bullet]  
        