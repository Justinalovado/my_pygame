import this
import pygame
class player:
    def __init__(self) -> None:
        self.x = 0
        self.y = 0
        self.health = 100
        self.attackPoint = 10
        self.speed = 3
        self.img = pygame.image.load("img/man.png").convert_alpha()
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.hitbox = self.img.get_rect() 
        self.velocity = (0,0)
    def update(self, keys):
        self.move(keys)
        

    def move(self, keys):
        velocity = (0, 0)
        if keys[pygame.K_d]:
            velocity = (self.speed, velocity[1])
            self.velocity = (self.speed, velocity[1])
        if keys[pygame.K_a]:
            velocity = (-self.speed, velocity[1])
            self.velocity = (-self.speed, velocity[1])
        if keys[pygame.K_s]:
            velocity = (velocity[0], self.speed)
            self.velocity = (velocity[0], self.speed)
        if keys[pygame.K_w]:
            velocity = (velocity[0], -self.speed)
            self.velocity = ((velocity[0], -self.speed))
            

        # updates x,y positions
        self.x, self.y = self.x + velocity[0], self.y + velocity[1]
        # updates hitbox
        pygame.Rect.move_ip(self.hitbox, velocity[0], velocity[1])

        if self.is_outbound():
            self.x, self.y = self.x - velocity[0], self.y - velocity[1]
            pygame.Rect.move_ip(self.hitbox, -velocity[0], -velocity[1])
            
    def is_outbound(self):
        screen_right = 1024-self.width
        screen_bottom = 768-self.width
        return True if (self.x<0 or self.x>screen_right or 
                        self.y<0 or self.y>screen_bottom) else False

    def attack(self, keys):
        if keys[pygame.K_k]:
            
            pass
        
            
            



            