import pygame
class player:
    def __init__(self) -> None:
        self.x = 0
        self.y = 0
        self.health = 100
        self.attackPoint = 10
        self.speed = 3
        self.img = pygame.image.load("img/man.png").convert_alpha()
        self.rect = self.img.get_rect()
    def move(self, input):
        if input[pygame.K_d]:
            self.x += self.speed
        if input[pygame.K_a]:
            self.x -= self.speed
        if input[pygame.K_s]:
            self.y += self.speed
        if input[pygame.K_w]:
            self.y -= self.speed
    
            