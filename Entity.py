
from random import randint
from turtle import left, screensize
from pkg_resources import ensure_directory
import pygame


# ATTACKSTATE NEEDS TO BE ADDED
SECOND = 60
BULLETSPEED = 4
ATTACKSTATE = 0.5 * SECOND
HOSTILITY_LIST = [
    ['player', 'enemy'],
]

class Player:
    def __init__(self) -> None:
        self.x = 0
        self.y = 0
        self.health = 30
        self.attack_point = 10
        self.speed = 3
        self.img = pygame.image.load("img/man.png").convert_alpha()
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.hitbox = self.img.get_rect()
        self.is_invincible = False
        self.invinc_countdown = 0
        # self.bullets = []
        self.bulletVelocity = (1, 1)
        self.name = "player"
        self.is_reloaded = True
        self.reload_tick = 0


    def update(self, keys, enemies, projectiles):
        self.move(keys)
        self.is_taking_melee(enemies)
        if self.invinc_countdown > 0:
            self.invinc_countdown -= 1
        else:
            self.is_invincible = False
        # if self.health <= 0:
        #     self.dead = True
        if keys[pygame.K_k]:
            self.attack(projectiles)
        # updating bullets
        # for bullet in self.bullets:
        #     bullet.update()
        # self.bullets = [b for b in self.bullets if not b.is_outbound()]

    def attack(self, projectiles):
        if self.is_reloaded:
            projectiles.append(Bullet(
                self.x,
                self.y, 
                self.attack_point,
                self.bulletVelocity[0], 
                self.bulletVelocity[1],
                self.name
            ))
            self.is_reloaded = False
            self.reload_tick = 0.5 * SECOND
        else:
            if self.reload_tick > 0:
                self.reload_tick -= 1
            else:
                self.reload_tick = 0
                self.is_reloaded = True
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
        if velocity != (0, 0):
            self.bulletVelocity = velocity
        # if keys[pygame.K_k]:
        #     self.bullets.append(
        #         Bullet(self.x, self.y, self.attack_point,
        #                self.bulletVelocity[0], self.bulletVelocity[1]))
        self.x, self.y = self.x + velocity[0], self.y + velocity[1]
        pygame.Rect.move_ip(self.hitbox, velocity[0], velocity[1])
        if self.is_outbound():
            self.x, self.y = self.x - velocity[0], self.y - velocity[1]
            pygame.Rect.move_ip(self.hitbox, -velocity[0], -velocity[1])

    def is_outbound(self):
        screen_right = 1024 - self.width
        screen_bottom = 768 - self.width
        return True if (self.x < 0 or self.x > screen_right or self.y < 0
                        or self.y > screen_bottom) else False

    def is_taking_melee(self, enemies):
        for enemy in enemies:
            if pygame.Rect.colliderect(self.hitbox, enemy.hitbox):
                self.take_dmg(enemy.attack_point)

    def take_dmg(self, dmg):
        if self.is_invincible == False:
            self.health -= dmg
            print(f"Player took {dmg} dmg, current health is {self.health}")
            self.is_invincible = True
            self.invinc_countdown = 60

    def is_dead(self):
        # return True if self.health <= 0 else False
        return self.health <= 0
    def show(self, screen, show_hitbox=True):
        screen.blit(self.img, (self.x, self.y))
        if show_hitbox:
            pygame.draw.rect(screen, "lightgreen", self.hitbox, width=1)

    def getBullets(self):
        return self.bullets


class Enemy:
    def __init__(self, x=None, y=None) -> None:
        self.img = pygame.image.load("img/enemy.png").convert_alpha()
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.x = x if x != None else randint(0, 1024 - self.width)
        self.y = y if y != None else randint(0, 768 - self.width)
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.health = 100
        self.velocity = (randint(1, 3), randint(1, 3))
        self.attack_point = 10
        self.name = "enemy"

    def update(self, bullets=[]):
        self.move()
        # self.is_taking_range(bullets)
        
    def move(self):
        self.x, self.y = self.x - self.velocity[0], self.y - self.velocity[1]
        screen_right = 1024 - self.width
        screen_bottom = 768 - self.width
        if self.x < 0 or self.x > screen_right:
            self.velocity = (-self.velocity[0], self.velocity[1])
        if self.y < 0 or self.y > screen_bottom:
            self.velocity = (self.velocity[0], -self.velocity[1])
        self.x, self.y = self.x - self.velocity[0], self.y - self.velocity[1]
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def is_outbound(self):
        screen_right = 1024 - self.width
        screen_bottom = 768 - self.width
        return True if (self.x < 0 or self.x > screen_right or self.y < 0
                        or self.y > screen_bottom) else False

    # def is_taking_range(self, bullets):
    #     for bullet in bullets:
    #         if pygame.Rect.colliderect(self.hitbox, bullet.hitbox):
    #             self.take_dmg(bullet.dmg)

    def take_dmg(self, dmg):
        self.health -= dmg
        print(f"{self.name} took {dmg} dmg, current health is {self.health}")

    def show(self, screen, show_hitbox=True):
        screen.blit(self.img, (self.x, self.y))
        if show_hitbox:
            pygame.draw.rect(screen, "lightgreen", self.hitbox, width=1)

    def is_dead(self):
        # return True if self.health <= 0 else False
        return self.health <= 0

class Bullet:
    def __init__(self, x, y, dmg, vX, vY, source) -> None:
        self.x = x
        self.y = y
        self.dmg = dmg
        self.velocity = (vX, vY)
        self.speed = BULLETSPEED
        self.img = pygame.image.load("img/bullet.png").convert_alpha()
        self.img = pygame.transform.scale(self.img, (10, 10))
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.source = source
        self.pierce = 0
        self.dead = False
        

    def update(self, entities):
        self.x += self.velocity[0] * self.speed
        self.y += self.velocity[1] * self.speed
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.check_hit(entities)
    def is_outbound(self):
        screen_right = 1024
        screen_bottom = 768
        return True if (self.x < 0 or self.x > screen_right or self.y < 0
                        or self.y > screen_bottom) else False

    def show(self, screen, show_hitbox=True):
        screen.blit(self.img, (self.x, self.y))
        if show_hitbox:
            pygame.draw.rect(screen, "lightgreen", self.hitbox, width=1)
    
    def is_dead(self):
        return self.dead

    def check_hit(self, entities):
        for entity in entities:
            if pygame.Rect.colliderect(self.hitbox, entity.hitbox):
                relation = [self.source, entity.name]
                if relation in HOSTILITY_LIST or relation[::-1] in HOSTILITY_LIST:
                    entity.take_dmg(self.dmg)
                    if self.pierce > 0:
                        self.pierce -= 1
                    else:
                        self.dead = True
        