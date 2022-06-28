import pygame
# file containing utility classes
# does not need to be implemented
class Corrdinate:
    def __init__(self, topLeftX, topLeftY, width, height) -> None:
        self.topLeftX = topLeftX
        self.topLeftY = topLeftY
        self.x = topLeftX + width / 2 # default 'x' as center x
        self.y = topLeftY + height / 2 # default 'y' as center y
        

class Hitbox:
    def __init__(self,topLeftX, topLeftY, width, heigh) -> None:
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
    
class Cooldown:
    def __init__(self) -> None:
        self.invinvible = 0
        self.reload = 0